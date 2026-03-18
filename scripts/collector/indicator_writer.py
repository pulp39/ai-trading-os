import json
import os
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

import psycopg


TRACE_EVENT_TYPE = "indicator_observation"
INDICATOR_ID = "vwap_deviation"
INDICATOR_VERSION = "1.0"
ACTOR = "OpenClaw"


@dataclass
class VWAPDeviationResult:
    value: float
    interpretation: str


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


def _to_float(value) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, Decimal):
        return float(value)
    return float(value)


def compute_vwap_deviation(current_price, vwap) -> Optional[VWAPDeviationResult]:
    current_price_f = _to_float(current_price)
    vwap_f = _to_float(vwap)

    if current_price_f is None or vwap_f is None:
        return None
    if vwap_f == 0:
        return None

    value = (current_price_f - vwap_f) / vwap_f

    if value > 0:
        interpretation = "bullish"
    elif value < 0:
        interpretation = "bearish"
    else:
        interpretation = "neutral"

    return VWAPDeviationResult(value=value, interpretation=interpretation)


def write_indicator_observation(
    *,
    symbol: str,
    captured_at: datetime,
    current_price,
    vwap,
    source_snapshot_id: int,
    aab_bundle_id=None,
    actor: str = ACTOR,
) -> Optional[int]:
    result = compute_vwap_deviation(current_price=current_price, vwap=vwap)
    if result is None:
        return None

    metadata = {
        "event_type": TRACE_EVENT_TYPE,
        "actor": actor,
        "indicator_id": INDICATOR_ID,
        "indicator_version": INDICATOR_VERSION,
        "symbol": str(symbol),
        "captured_at": captured_at.isoformat(),
        "current_price": _to_float(current_price),
        "vwap": _to_float(vwap),
        "value": result.value,
        "interpretation": result.interpretation,
        "source_snapshot_id": source_snapshot_id,
        "aab_bundle_id": aab_bundle_id,
    }

    content = (
        f"Computed {INDICATOR_ID} for symbol={symbol} "
        f"from board snapshot {source_snapshot_id}: "
        f"value={result.value:.8f}, interpretation={result.interpretation}"
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
                    actor.lower(),
                    "ai",
                    TRACE_EVENT_TYPE,
                    content,
                    json.dumps(metadata, ensure_ascii=False),
                ),
            )
            event_id = cur.fetchone()[0]
        conn.commit()

    return event_id