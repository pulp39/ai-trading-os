#!/usr/bin/env python3
"""
ingest_formal_observation.py

Purpose:
- Read a formal observation JSON file
- Validate minimum institutional requirements
- Insert the record into trace_event
- Print the resulting trace_event_id

Usage:
    python scripts/collector/ingest_formal_observation.py path\to\observation.json

Optional environment variables:
    PGHOST
    PGPORT
    PGDATABASE
    PGUSER
    PGPASSWORD

Notes:
- This script is intentionally minimal and conservative.
- It only accepts formal observations.
- It is designed for the active Collector:
    collector_base_collector_v1
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

try:
    import psycopg2
    from psycopg2.extras import Json
except ImportError as exc:
    raise SystemExit(
        "psycopg2 is not installed. Install it first with:\n"
        "pip install psycopg2-binary"
    ) from exc


EXPECTED_COLLECTOR_ID = "collector_base_collector_v1"
EXPECTED_ASSET_CLASS = "equity index futures"
EXPECTED_TIMEFRAME = "daily"
EXPECTED_ACTIVATION_TRACE_EVENT_ID = 35
EXPECTED_EVENT_TYPE = "market_observation_recorded"


@dataclass
class ValidationResult:
    errors: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def get_nested(data: dict[str, Any], path: Iterable[str]) -> Any:
    current: Any = data
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def require_field(data: dict[str, Any], path: list[str], errors: list[str]) -> Any:
    value = get_nested(data, path)
    if value is None:
        errors.append(f"Missing required field: {'.'.join(path)}")
    return value


def validate_observation(data: dict[str, Any]) -> ValidationResult:
    errors: list[str] = []

    # Top-level required fields
    require_field(data, ["observation_status"], errors)
    require_field(data, ["collector_id"], errors)
    require_field(data, ["observation_id"], errors)
    require_field(data, ["authorized_asset_class"], errors)
    require_field(data, ["authorized_timeframe"], errors)
    require_field(data, ["authorized_instrument"], errors)
    require_field(data, ["session_date"], errors)
    require_field(data, ["session_date_convention"], errors)
    require_field(data, ["collection_timestamp_utc"], errors)
    require_field(data, ["observation_payload"], errors)
    require_field(data, ["quality_classification"], errors)
    require_field(data, ["cadence_status"], errors)
    require_field(data, ["traceability"], errors)

    # Fixed institutional constraints
    if data.get("observation_status") != "formal":
        errors.append("observation_status must be 'formal'")

    if data.get("collector_id") != EXPECTED_COLLECTOR_ID:
        errors.append(
            f"collector_id must be '{EXPECTED_COLLECTOR_ID}', "
            f"got '{data.get('collector_id')}'"
        )

    if data.get("authorized_asset_class") != EXPECTED_ASSET_CLASS:
        errors.append(
            f"authorized_asset_class must be '{EXPECTED_ASSET_CLASS}', "
            f"got '{data.get('authorized_asset_class')}'"
        )

    if data.get("authorized_timeframe") != EXPECTED_TIMEFRAME:
        errors.append(
            f"authorized_timeframe must be '{EXPECTED_TIMEFRAME}', "
            f"got '{data.get('authorized_timeframe')}'"
        )

    # Payload dimensions required by institutional schema
    payload = data.get("observation_payload", {})
    if not isinstance(payload, dict):
        errors.append("observation_payload must be an object")
    else:
        for dim in (
            "price_context",
            "volume_context",
            "volatility_regime",
            "macro_event_proximity",
            "correlation_state",
        ):
            if dim not in payload:
                errors.append(f"Missing required observation_payload dimension: {dim}")

    # Quality classification checks
    qc = data.get("quality_classification", {})
    if not isinstance(qc, dict):
        errors.append("quality_classification must be an object")
    else:
        if qc.get("signal_quality_tier") not in {"complete", "partial", "minimal", "unreliable"}:
            errors.append(
                "quality_classification.signal_quality_tier must be one of: "
                "complete, partial, minimal, unreliable"
            )

        dcf = qc.get("dimensional_completeness_flags")
        if not isinstance(dcf, dict):
            errors.append("quality_classification.dimensional_completeness_flags must be an object")

        rn = qc.get("reliability_notes")
        if not isinstance(rn, list):
            errors.append("quality_classification.reliability_notes must be an array")

    # Traceability checks
    traceability = data.get("traceability", {})
    if not isinstance(traceability, dict):
        errors.append("traceability must be an object")
    else:
        if traceability.get("collector_role_status") != "active":
            errors.append("traceability.collector_role_status must be 'active'")

        if traceability.get("activation_trace_event_id") != EXPECTED_ACTIVATION_TRACE_EVENT_ID:
            errors.append(
                "traceability.activation_trace_event_id must be "
                f"{EXPECTED_ACTIVATION_TRACE_EVENT_ID}"
            )

    # Cadence checks
    cadence = data.get("cadence_status", {})
    if not isinstance(cadence, dict):
        errors.append("cadence_status must be an object")
    else:
        if "declared_cadence" not in cadence:
            errors.append("Missing required field: cadence_status.declared_cadence")
        if "cadence_deviation" not in cadence:
            errors.append("Missing required field: cadence_status.cadence_deviation")

    # Timestamp parseability
    ts = data.get("collection_timestamp_utc")
    if ts is not None:
        try:
            datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except ValueError:
            errors.append("collection_timestamp_utc must be valid ISO-8601 UTC timestamp")

    return ValidationResult(errors=errors)


def build_content(data: dict[str, Any]) -> str:
    instrument = data["authorized_instrument"]
    session_date = data["session_date"]
    tier = data["quality_classification"]["signal_quality_tier"]
    return (
        "Formal observation record submitted by "
        f"{data['collector_id']} for the completed daily trading session "
        f"of {instrument} on {session_date}. "
        "Record conforms to the institutional observation schema and is "
        f"submitted for admissibility assessment under P-20260310-007. "
        f"Signal quality tier: {tier}."
    )


def get_db_connection():
    required_env = ["PGHOST", "PGPORT", "PGDATABASE", "PGUSER", "PGPASSWORD"]
    missing = [key for key in required_env if not os.getenv(key)]
    if missing:
        raise SystemExit(
            "Missing required database environment variables: "
            + ", ".join(missing)
        )

    return psycopg2.connect(
        host=os.environ["PGHOST"],
        port=os.environ["PGPORT"],
        dbname=os.environ["PGDATABASE"],
        user=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
    )


def insert_trace_event(data: dict[str, Any]) -> int:
    ts = datetime.fromisoformat(data["collection_timestamp_utc"].replace("Z", "+00:00"))
    content = build_content(data)

    sql = """
        INSERT INTO trace_event (
            ts,
            agent_id,
            actor_type,
            event_type,
            content,
            metadata
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
    """

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql,
                (
                    ts,
                    data["collector_id"],
                    "ai",
                    EXPECTED_EVENT_TYPE,
                    content,
                    Json(data),
                ),
            )
            trace_event_id = cur.fetchone()[0]
        conn.commit()

    return trace_event_id


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "Usage:\n"
            "  python scripts/collector/ingest_formal_observation.py "
            "path\\to\\observation.json",
            file=sys.stderr,
        )
        return 2

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 2

    try:
        with input_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON: {exc}", file=sys.stderr)
        return 2

    result = validate_observation(data)
    if not result.ok:
        print("Validation failed:", file=sys.stderr)
        for err in result.errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    try:
        trace_event_id = insert_trace_event(data)
    except Exception as exc:
        print(f"Database insert failed: {exc}", file=sys.stderr)
        return 1

    print("Formal observation ingested successfully.")
    print(f"trace_event_id: {trace_event_id}")
    print(f"observation_id: {data['observation_id']}")
    print(
        "signal_quality_tier: "
        f"{data['quality_classification']['signal_quality_tier']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())