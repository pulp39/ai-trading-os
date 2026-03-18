#!/usr/bin/env python3
import os

import psycopg

from proposal_writer import write_proposal_drafted

PROPOSED_BY = "Proposer"
PROPOSAL_TYPE = "trading_hypothesis"


def _get_trace_db_dsn() -> str:
    host = os.environ["OPENCLAW_TRACE_DB_HOST"]
    port = os.environ.get("OPENCLAW_TRACE_DB_PORT", "5432")
    dbname = os.environ["OPENCLAW_TRACE_DB_NAME"]
    user = os.environ["OPENCLAW_TRACE_DB_USER"]
    password = os.environ["OPENCLAW_TRACE_DB_PASSWORD"]
    sslmode = os.environ.get("OPENCLAW_TRACE_DB_SSLMODE", "prefer")

    return (
        f"host={host} port={port} dbname={dbname} "
        f"user={user} password={password} sslmode={sslmode}"
    )


def fetch_recent_hypotheses(limit: int = 100) -> list[dict]:
    sql = """
        SELECT
            id,
            ts,
            metadata->>'symbol' AS symbol,
            metadata->>'hypothesis' AS hypothesis,
            metadata->>'confidence' AS confidence
        FROM research.trace_event
        WHERE event_type = 'hypothesis_proposed'
        ORDER BY ts DESC, id DESC
        LIMIT %s
    """

    with psycopg.connect(_get_trace_db_dsn()) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (limit,))
            rows = cur.fetchall()

    result = []
    for row in rows:
        result.append(
            {
                "id": row[0],
                "ts": row[1],
                "symbol": row[2],
                "hypothesis": row[3],
                "confidence": row[4],
            }
        )
    return result


def build_title(symbol: str) -> str:
    return f"Hypothesis: {symbol} VWAP Signal"


def main() -> int:
    hypotheses = fetch_recent_hypotheses(limit=100)
    if not hypotheses:
        print("No hypothesis_proposed events found.")
        return 0

    created_ids: list[int] = []

    for event in hypotheses:
        event_id = write_proposal_drafted(
            proposal_type=PROPOSAL_TYPE,
            source_hypothesis_event_id=event["id"],
            symbol=event["symbol"],
            title=build_title(event["symbol"]),
            summary=event["hypothesis"],
            confidence=event["confidence"] or "low",
            proposed_by=PROPOSED_BY,
            triggered_at=event["ts"].isoformat(),
            status="draft",
            aab_bundle_id=None,
        )
        if event_id is not None:
            created_ids.append(event_id)

    print(
        "proposal trigger evaluation complete: "
        f"proposal_created={len(created_ids)}"
    )
    if created_ids:
        print(f"proposal event ids: {created_ids}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
    