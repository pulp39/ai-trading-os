import argparse
import json
import os
from datetime import datetime, timezone

import psycopg


class ElevationIntegrityError(RuntimeError):
    pass


def get_db_config() -> dict:
    pg_host = os.environ.get("PGHOST")
    pg_port = os.environ.get("PGPORT", "5432")
    pg_database = os.environ.get("PGDATABASE")
    pg_user = os.environ.get("PGUSER")
    pg_password = os.environ.get("PGPASSWORD")

    missing = [
        name for name, value in {
            "PGHOST": pg_host,
            "PGDATABASE": pg_database,
            "PGUSER": pg_user,
            "PGPASSWORD": pg_password,
        }.items() if not value
    ]
    if missing:
        raise RuntimeError(f"Missing required DB env vars: {', '.join(missing)}")

    return {
        "host": pg_host,
        "port": pg_port,
        "dbname": pg_database,
        "user": pg_user,
        "password": pg_password,
    }


def generate_tp_id(conn: psycopg.Connection) -> str:
    today = datetime.now(timezone.utc).astimezone().strftime("%Y%m%d")
    prefix = f"TP-{today}-"

    sql = """
    SELECT metadata->>'tp_id'
    FROM research.trace_event
    WHERE event_type = 'trading_proposal'
      AND metadata ? 'tp_id'
      AND metadata->>'tp_id' LIKE %s
    ORDER BY metadata->>'tp_id' DESC
    LIMIT 1;
    """

    with conn.cursor() as cur:
        cur.execute(sql, (f"{prefix}%",))
        row = cur.fetchone()

    if row and row[0]:
        last_tp_id = row[0]
        last_seq = int(last_tp_id.split("-")[-1])
        next_seq = last_seq + 1
    else:
        next_seq = 1

    return f"{prefix}{next_seq:03d}"


def get_draft_event(conn: psycopg.Connection, draft_event_id: int) -> tuple[int, dict]:
    sql = """
    SELECT id, metadata
    FROM research.trace_event
    WHERE event_type = 'proposal_drafted'
      AND id = %s
    LIMIT 1;
    """
    with conn.cursor() as cur:
        cur.execute(sql, (draft_event_id,))
        row = cur.fetchone()

    if not row:
        raise ElevationIntegrityError(
            f"Cannot formalize: proposal_drafted not found for draft_event_id={draft_event_id}"
        )

    return row[0], row[1]


def get_latest_review_requested_event(
    conn: psycopg.Connection, draft_event_id: int
) -> tuple[int, dict]:
    sql = """
    SELECT id, metadata
    FROM research.trace_event
    WHERE event_type = 'proposal_review_requested'
      AND metadata->>'source_proposal_draft_event_id' = %s
    ORDER BY id DESC
    LIMIT 1;
    """
    with conn.cursor() as cur:
        cur.execute(sql, (str(draft_event_id),))
        row = cur.fetchone()

    if not row:
        raise ElevationIntegrityError(
            f"Cannot formalize: proposal_review_requested not found for draft_event_id={draft_event_id}"
        )

    return row[0], row[1]


def get_latest_reviewed_event(
    conn: psycopg.Connection, draft_event_id: int
) -> tuple[int, dict]:
    sql = """
    SELECT id, metadata
    FROM research.trace_event
    WHERE event_type = 'proposal_reviewed'
      AND metadata->>'source_proposal_draft_event_id' = %s
    ORDER BY id DESC
    LIMIT 1;
    """
    with conn.cursor() as cur:
        cur.execute(sql, (str(draft_event_id),))
        row = cur.fetchone()

    if not row:
        raise ElevationIntegrityError(
            f"Cannot formalize: proposal_reviewed not found for draft_event_id={draft_event_id}"
        )

    return row[0], row[1]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Formalize an approved draft into a trading_proposal event."
    )
    parser.add_argument("--draft-event-id", type=int, required=True)
    parser.add_argument(
        "--content",
        default=None,
        help="Optional custom content message.",
    )
    args = parser.parse_args()

    db_config = get_db_config()

    with psycopg.connect(**db_config) as conn:
        draft_id, draft_metadata = get_draft_event(conn, args.draft_event_id)
        review_requested_id, _ = get_latest_review_requested_event(conn, args.draft_event_id)
        review_id, review_metadata = get_latest_reviewed_event(conn, args.draft_event_id)

        if review_metadata.get("review_result") != "approved":
            raise ElevationIntegrityError(
                f"Cannot formalize: review not approved for draft_event_id={args.draft_event_id}"
            )

        tp_id = generate_tp_id(conn)

        title = draft_metadata.get("title")
        summary = draft_metadata.get("summary")
        symbol = draft_metadata.get("symbol")
        source_hypothesis_event_id = draft_metadata.get("source_hypothesis_event_id")
        confidence = draft_metadata.get("confidence")
        agent_id = draft_metadata.get("agent_id")
        triggered_at = draft_metadata.get("triggered_at")

        content = args.content or (
            f"Formal trading proposal {tp_id} created from proposal draft {draft_id}"
        )

        metadata = {
            "tp_id": tp_id,
            "title": title,
            "status": "formalized",
            "symbol": symbol,
            "summary": summary,
            "confidence": confidence,
            "agent_id": agent_id,
            "triggered_at": triggered_at,
            "aab_bundle_id": None,
            "source_hypothesis_event_id": source_hypothesis_event_id,
            "source_proposal_draft_event_id": draft_id,
            "source_review_requested_event_id": review_requested_id,
            "source_review_event_id": review_id,
        }

        insert_sql = """
        INSERT INTO research.trace_event (
          ts,
          agent_id,
          actor_type,
          event_type,
          content,
          metadata
        )
        VALUES (
          NOW(),
          %s,
          %s,
          %s,
          %s,
          %s::jsonb
        )
        RETURNING id, ts;
        """

        with conn.cursor() as cur:
            cur.execute(
                insert_sql,
                (
                    "librarian",
                    "ai",
                    "trading_proposal",
                    content,
                    json.dumps(metadata, ensure_ascii=False),
                ),
            )
            row = cur.fetchone()
        conn.commit()

    print(
        f"created trading_proposal: id={row[0]} ts={row[1]} "
        f"draft_event_id={draft_id} tp_id={tp_id} "
        f"review_requested_event_id={review_requested_id} review_event_id={review_id}"
    )


if __name__ == "__main__":
    main()
