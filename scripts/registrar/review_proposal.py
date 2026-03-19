import argparse
import json
import os
import psycopg


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Record a proposal_reviewed event."
    )
    parser.add_argument("--draft-event-id", type=int, required=True)
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--source-hypothesis-event-id", type=int, required=True)
    parser.add_argument(
        "--review-result",
        choices=["approved", "rejected"],
        default="approved",
    )
    parser.add_argument(
        "--proposal-type",
        choices=["trading_proposal", "institution_proposal"],
        default="trading_proposal",
    )
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

    content = args.content or (
        f"Librarian reviewed proposal draft {args.draft_event_id}"
    )
    if args.review_result == "approved":
        content += f" and approved elevation to {args.proposal_type}"

    metadata = {
        "source_proposal_draft_event_id": args.draft_event_id,
        "source_hypothesis_event_id": args.source_hypothesis_event_id,
        "review_result": args.review_result,
        "proposal_type": args.proposal_type,
        "reviewed_by": "Librarian",
        "status": "reviewed",
        "symbol": args.symbol,
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

    with psycopg.connect(
        host=pg_host,
        port=pg_port,
        dbname=pg_database,
        user=pg_user,
        password=pg_password,
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql,
                (
                    "librarian",
                    "ai",
                    "proposal_reviewed",
                    content,
                    json.dumps(metadata, ensure_ascii=False),
                ),
            )
            row = cur.fetchone()
        conn.commit()

    print(
        f"created proposal_reviewed: id={row[0]} ts={row[1]} "
        f"draft_event_id={args.draft_event_id} result={args.review_result}"
    )


if __name__ == "__main__":
    main()
