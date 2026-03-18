#!/usr/bin/env python3
import json
import os
from typing import Optional

import psycopg

EVENT_TYPE = "proposal_drafted"
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


def proposal_exists(source_hypothesis_event_id: int) -> bool:
    sql = """
        SELECT 1
        FROM research.trace_event
        WHERE event_type = 'proposal_drafted'
          AND metadata->>'source_hypothesis_event_id' = %s
        LIMIT 1
    """

    with psycopg.connect(_get_trace_db_dsn()) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (str(source_hypothesis_event_id),))
            row = cur.fetchone()

    return row is not None


def write_proposal_drafted(
    *,
    proposal_type: str,
    source_hypothesis_event_id: int,
    symbol: str,
    title: str,
    summary: str,
    confidence: str,
    proposed_by: str,
    triggered_at: str,
    status: str = "draft",
    aab_bundle_id=None,
) -> Optional[int]:
    if proposal_exists(source_hypothesis_event_id):
        return None

    metadata = {
        "event_type": EVENT_TYPE,
        "proposal_type": proposal_type,
        "source_hypothesis_event_id": source_hypothesis_event_id,
        "symbol": str(symbol),
        "title": title,
        "summary": summary,
        "confidence": confidence,
        "proposed_by": proposed_by,
        "agent_id": AGENT_ID,
        "status": status,
        "triggered_at": triggered_at,
        "aab_bundle_id": aab_bundle_id,
    }

    content = f"Draft proposal generated for symbol={symbol}: {title}"

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