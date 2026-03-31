#!/usr/bin/env python3
"""
scripts/openclaw/run_order_preview.py
Bounded order_preview path (P-20260320-017 / P-20260321-019)

Behavior:
- reads approved order_preview task artifact
- validates AAB scope and dry-run constraints
- binds preview to a single latest board_snapshots row
- uses current_price as estimated_price (observation extension only)
- records order_preview_recorded into research.trace_event

P-019 override behavior:
- off-hours test override is allowed only under strict bounded conditions
- market_closed / snapshot_stale may be overridden for test-only readiness
- override usage is always recorded explicitly

Non-goals:
- no external order execution
- no capital mutation
- no simulated_order behavior changes
- no slippage logic
"""

import json
import os
import sys
from datetime import datetime, time, timedelta
from pathlib import Path

import psycopg

from scripts.collector.readiness_writer import write_execution_readiness_evaluated

BASE_DIR = Path(__file__).resolve().parents[2]
TASK_ARTIFACT = BASE_DIR / "registrar_queue" / "order_preview_task.json"


def load_task_artifact() -> dict:
    if not TASK_ARTIFACT.exists():
        raise FileNotFoundError(f"Approved task artifact not found: {TASK_ARTIFACT}")
    with TASK_ARTIFACT.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Required environment variable is missing: {name}")
    return value


def get_trace_db_conn():
    return psycopg.connect(
        host=get_required_env("OPENCLAW_TRACE_DB_HOST"),
        port=get_required_env("OPENCLAW_TRACE_DB_PORT"),
        dbname=get_required_env("OPENCLAW_TRACE_DB_NAME"),
        user=get_required_env("OPENCLAW_TRACE_DB_USER"),
        password=get_required_env("OPENCLAW_TRACE_DB_PASSWORD"),
    )


def is_regular_tse_market_hours(now_local: datetime) -> bool:
    if now_local.weekday() >= 5:
        return False

    current = now_local.time()
    morning_open = time(9, 0)
    morning_close = time(11, 30)
    afternoon_open = time(12, 30)
    afternoon_close = time(15, 30)

    in_morning = morning_open <= current <= morning_close
    in_afternoon = afternoon_open <= current <= afternoon_close
    return in_morning or in_afternoon


def validate_aab(aab: dict, task: dict) -> None:
    scope = aab.get("execution_scope", {})
    constraints = aab.get("constraints", {})

    if scope.get("action_type") != "order_preview":
        raise ValueError("execution_scope.action_type must be order_preview")

    symbol = scope.get("symbol")
    if symbol not in task["allowed_symbols"]:
        raise ValueError(f"Symbol {symbol} not in allowed_symbols")

    order_type = scope.get("order_type", "market")
    if order_type not in task["allowed_order_types"]:
        raise ValueError(f"order_type {order_type} not allowed")

    side = scope.get("side")
    if side not in task["allowed_sides"]:
        raise ValueError(f"side {side} not allowed")

    quantity = scope.get("quantity", 0)
    if not isinstance(quantity, int) or quantity <= 0:
        raise ValueError(f"quantity must be a positive integer, got {quantity}")
    if quantity > task["max_quantity"]:
        raise ValueError(f"quantity {quantity} exceeds max {task['max_quantity']}")

    if not constraints.get("dry_run", False):
        raise ValueError("dry_run must be true for order_preview")

    if constraints.get("external_order_allowed", True):
        raise ValueError("external_order_allowed must be false")

    if not constraints.get("preview_only", False):
        raise ValueError("preview_only must be true for order_preview")


def fetch_latest_snapshot(conn, symbol: str) -> dict:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, captured_at, symbol, exchange, current_price
            FROM public.board_snapshots
            WHERE symbol = %s
            ORDER BY captured_at DESC, id DESC
            LIMIT 1
            """,
            (symbol,),
        )
        row = cur.fetchone()

    if not row:
        raise ValueError(f"No board_snapshots row found for symbol {symbol}")

    snapshot_id, captured_at, row_symbol, exchange, current_price = row
    return {
        "snapshot_id": snapshot_id,
        "captured_at": captured_at,
        "symbol": row_symbol,
        "exchange": exchange,
        "current_price": float(current_price) if current_price is not None else None,
    }


def is_override_allowed(aab: dict, task: dict) -> bool:
    constraints = aab.get("constraints", {})

    return (
        constraints.get("dry_run") is True
        and constraints.get("preview_only") is True
        and constraints.get("external_order_allowed") is False
        and constraints.get("state_change_allowed") is False
        and constraints.get("test_override_allowed") is True
        and task.get("off_hours_test_override") is True
    )


def evaluate_readiness(aab: dict, snapshot: dict, task: dict) -> tuple[str, list[str], list[str], bool, bool]:
    now_local = datetime.now().astimezone()
    failed_checks: list[str] = []
    overridden_checks: list[str] = []

    override_allowed = is_override_allowed(aab, task)

    if snapshot["current_price"] is None:
        failed_checks.append("price_unavailable")

    freshness_limit_ms = int(task.get("freshness_max_ms", 5000))
    snapshot_age_ms = int((now_local - snapshot["captured_at"]).total_seconds() * 1000)

    market_open = is_regular_tse_market_hours(now_local)
    market_closed = not market_open
    snapshot_stale = snapshot_age_ms > freshness_limit_ms

    if market_closed:
        if override_allowed:
            overridden_checks.append("market_closed")
        else:
            failed_checks.append("market_closed")

    if snapshot_stale:
        if override_allowed:
            overridden_checks.append("snapshot_stale")
        else:
            failed_checks.append("snapshot_stale")

    readiness = "ready" if len(failed_checks) == 0 else "stale"

    return readiness, failed_checks, overridden_checks, market_open, override_allowed


def derive_readiness_reason(readiness: str, failed_checks: list[str], overridden_checks: list[str]) -> str:
    if failed_checks:
        return ",".join(failed_checks)
    if overridden_checks:
        return "overridden:" + ",".join(overridden_checks)
    return readiness


def record_execution_readiness_evaluated(
    snapshot: dict,
    readiness: str,
    failed_checks: list[str],
    overridden_checks: list[str],
    task: dict,
) -> int:
    now_local = datetime.now().astimezone()
    freshness_seconds = round((now_local - snapshot["captured_at"]).total_seconds(), 3)
    return write_execution_readiness_evaluated(
        symbol=snapshot["symbol"],
        exchange=snapshot["exchange"],
        readiness_state=readiness,
        reason=derive_readiness_reason(readiness, failed_checks, overridden_checks),
        freshness_seconds=freshness_seconds,
        metadata={
            "hard_limit_result": "PASS" if not failed_checks else "FAIL",
            "soft_limit_result": "NOT_EVALUATED",
            "failed_checks": failed_checks,
            "overridden_checks": overridden_checks,
            "freshness_limit_ms": int(task.get("freshness_max_ms", 5000)),
            "source_snapshot_id": snapshot["snapshot_id"],
            "captured_at": snapshot["captured_at"].isoformat(),
            "evaluated_at": now_local.isoformat(),
        },
    )


def record_order_preview(
    conn,
    aab: dict,
    snapshot: dict,
    readiness: str,
    failed_checks: list[str],
    overridden_checks: list[str],
    market_open: bool,
    override_allowed: bool,
    task: dict,
) -> dict:
    scope = aab.get("execution_scope", {})
    now_local = datetime.now().astimezone()
    valid_until = now_local + timedelta(seconds=int(task.get("preview_validity_seconds", 30)))
    freshness_ms = int((now_local - snapshot["captured_at"]).total_seconds() * 1000)

    metadata = {
        "event_type": "order_preview_recorded",
        "preview_subtype": "current_price_binding",
        "aab_id": aab.get("aab_id", aab.get("trust_token", "")),
        "proposal_id": aab.get("proposal_id", ""),
        "symbol": scope.get("symbol"),
        "exchange": snapshot.get("exchange"),
        "order_type": scope.get("order_type", "market"),
        "side": scope.get("side"),
        "quantity": scope.get("quantity"),
        "estimated_price": snapshot.get("current_price"),
        "price_source": "public.board_snapshots.current_price",
        "source_snapshot_id": snapshot.get("snapshot_id"),
        "captured_at": snapshot.get("captured_at").isoformat(),
        "preview_generated_at": now_local.isoformat(),
        "valid_until": valid_until.isoformat(),
        "readiness": readiness,
        "market_state": "open" if market_open else "closed",
        "freshness_ms": freshness_ms,
        "reproducible": True,
        "failed_checks": failed_checks,
        "overridden_checks": overridden_checks,
        "test_mode": override_allowed,
        "off_hours_test_applied": override_allowed,
        "stale_snapshot_test_override": "snapshot_stale" in overridden_checks,
        "dry_run": True,
        "external_order_sent": False,
        "recorded_by": "OpenClaw/Recorder",
        "recorded_at": now_local.isoformat(),
    }

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO research.trace_event
              (ts, agent_id, actor_type, event_type, symbol, exchange, content)
            VALUES (NOW(), 'openclaw', 'ai', %s, %s, %s, %s)
            RETURNING id
            """,
            (
                "order_preview_recorded",
                scope.get("symbol"),
                snapshot.get("exchange"),
                json.dumps(metadata, ensure_ascii=False),
            ),
        )
        trace_event_id = cur.fetchone()[0]

    metadata["trace_event_id"] = trace_event_id
    return metadata


def main(aab_path: str) -> None:
    task = load_task_artifact()

    with open(aab_path, "r", encoding="utf-8") as f:
        aab = json.load(f)

    validate_aab(aab, task)

    conn = get_trace_db_conn()
    with conn:
        snapshot = fetch_latest_snapshot(conn, aab["execution_scope"]["symbol"])
        readiness, failed_checks, overridden_checks, market_open, override_allowed = evaluate_readiness(
            aab, snapshot, task
        )
        readiness_trace_event_id = record_execution_readiness_evaluated(
            snapshot,
            readiness,
            failed_checks,
            overridden_checks,
            task,
        )
        preview = record_order_preview(
            conn,
            aab,
            snapshot,
            readiness,
            failed_checks,
            overridden_checks,
            market_open,
            override_allowed,
            task,
        )

    conn.close()
    preview["execution_readiness_evaluated_trace_event_id"] = readiness_trace_event_id

    print(
        "[order_preview] preview_recorded: "
        f"{json.dumps(preview, indent=2, ensure_ascii=False)}"
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python run_order_preview.py <aab_path>")
        sys.exit(1)
    main(sys.argv[1])