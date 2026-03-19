import argparse
import json
import os
from datetime import datetime, timezone

import psycopg


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


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Formalize an approved draft into a trading_proposal event."
    )
    parser.add_argument("--draft-event-id", type=int, required=True)
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--source-hypothesis-event-id", type=int, required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument(
        "--content",
        default=None,
        help="Optional custom content message.",
    )
    args = parser.parse_args()

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

    with psycopg.connect(
        host=pg_host,
        port=pg_port,
        dbname=pg_database,
        user=pg_user,
        password=pg_password,
    ) as conn:
        tp_id = generate_tp_id(conn)

        content = args.content or (
            f"Formal trading proposal {tp_id} created from proposal draft {args.draft_event_id}"
        )

        metadata = {
            "tp_id": tp_id,
            "title": args.title,
            "status": "formalized",
            "symbol": args.symbol,
            "summary": args.summary,
            "aab_bundle_id": None,
            "source_hypothesis_event_id": args.source_hypothesis_event_id,
            "source_proposal_draft_event_id": args.draft_event_id,
        }

        sql = """
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
                sql,
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
        f"draft_event_id={args.draft_event_id} tp_id={tp_id}"
    )


if __name__ == "__main__":
    main()