#!/usr/bin/env python3
import json
import os
from typing import Optional

import psycopg

EVENT_TYPE = "hypothesis_proposed"
AGENT_ID = "proposer"
ACTOR_TYPE = "ai"


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


def hypothesis_exists(
    *,
    symbol: str,
    indicator_id: str,
    trigger_type: str,
    basis_event_ids: list[int],
) -> bool:
    sql = """
        SELECT 1
        FROM research.trace_event
        WHERE event_type = 'hypothesis_proposed'
          AND metadata->>'symbol' = %s
          AND metadata->>'indicator_id' = %s
          AND metadata->>'trigger_type' = %s
          AND metadata->'basis_event_ids' = %s::jsonb
        LIMIT 1
    """

    with psycopg.connect(_get_trace_db_dsn()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql,
                (
                    str(symbol),
                    indicator_id,
                    trigger_type,
                    json.dumps(basis_event_ids),
                ),
            )
            row = cur.fetchone()

    return row is not None


def write_hypothesis_proposed(
    *,
    proposed_by: str,
    trigger_type: str,
    trigger_condition: str,
    symbol: str,
    indicator_id: str,
    hypothesis: str,
    confidence: str,
    basis_event_ids: list[int],
    aab_bundle_id=None,
) -> Optional[int]:
    if hypothesis_exists(
        symbol=symbol,
        indicator_id=indicator_id,
        trigger_type=trigger_type,
        basis_event_ids=basis_event_ids,
    ):
        return None

    metadata = {
        "event_type": EVENT_TYPE,
        "proposed_by": proposed_by,
        "trigger_type": trigger_type,
        "trigger_condition": trigger_condition,
        "symbol": str(symbol),
        "indicator_id": indicator_id,
        "hypothesis": hypothesis,
        "confidence": confidence,
        "basis_event_ids": basis_event_ids,
        "aab_bundle_id": aab_bundle_id,
    }

    content = (
        f"Hypothesis proposed for symbol={symbol} via {trigger_type}: "
        f"{hypothesis}"
    )

    sql = """
        INSERT INTO research.trace_event (
            agent_id,
            actor_type,
            event_type,
            content,
            metadata
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s::jsonb
        )
        RETURNING id
    """

    with psycopg.connect(_get_trace_db_dsn()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql,
                (
                    AGENT_ID,
                    ACTOR_TYPE,
                    EVENT_TYPE,
                    content,
                    json.dumps(metadata, ensure_ascii=False),
                ),
            )
            event_id = cur.fetchone()[0]
        conn.commit()

    return event_id