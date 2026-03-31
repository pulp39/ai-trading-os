import os
from typing import Any

import psycopg
from psycopg.types.json import Json


TRACE_EVENT_TYPE = "execution_readiness_evaluated"
AGENT_ID = "openclaw_aux"
ACTOR_TYPE = "ai"


def write_execution_readiness_evaluated(
    *,
    symbol: str,
    exchange: int,
    readiness_state: str,
    reason: str,
    freshness_seconds: float | int | None,
    metadata: dict[str, Any] | None = None,
) -> int:
    normalized_readiness_state = str(readiness_state).upper()
    allowed_states = {"READY", "REPRICE_REQUIRED", "NOT_READY", "DATA_INVALID"}
    if normalized_readiness_state not in allowed_states:
        raise ValueError(
            "readiness_state must be one of READY / REPRICE_REQUIRED / NOT_READY / DATA_INVALID"
        )

    event_metadata: dict[str, Any] = {
        "event_type": TRACE_EVENT_TYPE,
        "symbol": str(symbol),
        "exchange": int(exchange),
        "readiness_state": normalized_readiness_state,
        "reason": reason,
        "freshness_seconds": freshness_seconds,
    }
    if metadata:
        event_metadata.update(metadata)

    content = (
        f"execution_readiness_evaluated symbol={symbol} exchange={exchange} "
        f"readiness_state={normalized_readiness_state} reason={reason} "
        f"freshness_seconds={freshness_seconds}"
    )

    conn = psycopg.connect(
        host=os.environ["OPENCLAW_TRACE_DB_HOST"],
        port=os.environ.get("OPENCLAW_TRACE_DB_PORT", "5432"),
        dbname=os.environ["OPENCLAW_TRACE_DB_NAME"],
        user=os.environ["OPENCLAW_TRACE_DB_USER"],
        password=os.environ["OPENCLAW_TRACE_DB_PASSWORD"],
    )

    sql = """
    INSERT INTO research.trace_event (
        agent_id,
        actor_type,
        event_type,
        symbol,
        exchange,
        content,
        metadata
    )
    VALUES (
        %(agent_id)s,
        %(actor_type)s,
        %(event_type)s,
        %(symbol)s,
        %(exchange)s,
        %(content)s,
        %(metadata)s
    )
    RETURNING id
    """

    params = {
        "agent_id": AGENT_ID,
        "actor_type": ACTOR_TYPE,
        "event_type": TRACE_EVENT_TYPE,
        "symbol": str(symbol),
        "exchange": int(exchange),
        "content": content,
        "metadata": Json(event_metadata),
    }

    with conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            event_id = cur.fetchone()[0]

    conn.close()
    return event_id
