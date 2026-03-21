#!/usr/bin/env python3
import os
from collections import defaultdict

import psycopg

from hypothesis_writer import write_hypothesis_proposed

THRESHOLD_ABS_VALUE = 0.005
CONSECUTIVE_COUNT = 3
INDICATOR_ID = "vwap_deviation"
PROPOSED_BY = "Proposer"


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


def fetch_recent_indicator_events(limit: int = 200) -> list[dict]:
    sql = """
        SELECT
            id,
            ts,
            metadata->>'symbol' AS symbol,
            metadata->>'indicator_id' AS indicator_id,
            (metadata->>'value')::double precision AS value,
            metadata->>'interpretation' AS interpretation
        FROM research.trace_event
        WHERE event_type = 'indicator_observation'
          AND metadata->>'indicator_id' = %s
        ORDER BY ts DESC, id DESC
        LIMIT %s
    """

    with psycopg.connect(_get_trace_db_dsn()) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (INDICATOR_ID, limit))
            rows = cur.fetchall()

    result = []
    for row in rows:
        result.append(
            {
                "id": row[0],
                "ts": row[1],
                "symbol": row[2],
                "indicator_id": row[3],
                "value": row[4],
                "interpretation": row[5],
            }
        )
    return result


def build_threshold_hypothesis(symbol: str, value: float) -> str:
    if value > 0:
        return f"{symbol} shows price strength above VWAP beyond threshold"
    return f"{symbol} shows price weakness below VWAP beyond threshold"


def build_consecutive_hypothesis(symbol: str, interpretation: str, count: int) -> str:
    if interpretation == "bullish":
        return f"{symbol} shows sustained buying pressure above VWAP across {count} consecutive observations"
    if interpretation == "bearish":
        return f"{symbol} shows sustained selling pressure below VWAP across {count} consecutive observations"
    return f"{symbol} shows sustained neutral behavior around VWAP across {count} consecutive observations"


def evaluate_threshold(events: list[dict]) -> list[int]:
    created_ids: list[int] = []

    for event in events:
        value = event["value"]
        if abs(value) < THRESHOLD_ABS_VALUE:
            continue

        if value > 0:
            trigger_condition = f"|value| >= {THRESHOLD_ABS_VALUE:.3f} and value > 0"
        else:
            trigger_condition = f"|value| >= {THRESHOLD_ABS_VALUE:.3f} and value < 0"

        event_id = write_hypothesis_proposed(
            proposed_by=PROPOSED_BY,
            trigger_type="threshold",
            trigger_condition=trigger_condition,
            symbol=event["symbol"],
            indicator_id=event["indicator_id"],
            hypothesis=build_threshold_hypothesis(event["symbol"], value),
            confidence="low",
            basis_event_ids=[event["id"]],
            aab_bundle_id=None,
        )
        if event_id is not None:
            created_ids.append(event_id)

    return created_ids


def evaluate_consecutive(events: list[dict]) -> list[int]:
    created_ids: list[int] = []
    grouped: dict[str, list[dict]] = defaultdict(list)

    for event in events:
        grouped[event["symbol"]].append(event)

    for symbol, symbol_events_desc in grouped.items():
        symbol_events = list(reversed(symbol_events_desc))

        streak: list[dict] = []
        last_interpretation = None

        for event in symbol_events:
            interpretation = event["interpretation"]

            if interpretation not in {"bullish", "bearish", "neutral"}:
                streak = []
                last_interpretation = None
                continue

            if interpretation == last_interpretation:
                streak.append(event)
            else:
                streak = [event]
                last_interpretation = interpretation

            if len(streak) >= CONSECUTIVE_COUNT:
                basis = streak[-CONSECUTIVE_COUNT:]
                basis_event_ids = [e["id"] for e in basis]

                event_id = write_hypothesis_proposed(
                    proposed_by=PROPOSED_BY,
                    trigger_type="consecutive",
                    trigger_condition=f"{CONSECUTIVE_COUNT} consecutive {interpretation}",
                    symbol=symbol,
                    indicator_id=INDICATOR_ID,
                    hypothesis=build_consecutive_hypothesis(
                        symbol, interpretation, CONSECUTIVE_COUNT
                    ),
                    confidence="low",
                    basis_event_ids=basis_event_ids,
                    aab_bundle_id=None,
                )
                if event_id is not None:
                    created_ids.append(event_id)

    return created_ids


def main() -> int:
    events = fetch_recent_indicator_events(limit=200)
    if not events:
        print("No indicator_observation events found.")
        return 0

    threshold_ids = evaluate_threshold(events)
    consecutive_ids = evaluate_consecutive(events)

    print(
        "hypothesis trigger evaluation complete: "
        f"threshold_created={len(threshold_ids)} "
        f"consecutive_created={len(consecutive_ids)}"
    )

    if threshold_ids:
        print(f"threshold event ids: {threshold_ids}")
    if consecutive_ids:
        print(f"consecutive event ids: {consecutive_ids}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())