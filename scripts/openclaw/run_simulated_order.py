#!/usr/bin/env python3
"""
scripts/openclaw/run_simulated_order.py
Bounded simulated_order execution path (P-20260319-016)

Existing-file-only revision:
- allows off-hours dry-run tests when explicitly permitted by AAB
- uses test Kabu credentials for simulation
- keeps external order forbidden
"""

import json
import os
import sys
from datetime import datetime, time
from pathlib import Path

import psycopg

BASE_DIR = Path(__file__).resolve().parents[2]
TASK_ARTIFACT = BASE_DIR / "registrar_queue" / "simulated_order_task.json"


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


def get_test_kabu_config() -> dict:
    return {
        "host": get_required_env("KABU_API_HOST"),
        "port": int(get_required_env("KABU_API_TEST_PORT")),
        "password": get_required_env("KABU_API_TEST_PASSWORD"),
        "mode": "test",
    }


def is_regular_tse_market_hours(now_local: datetime) -> bool:
    """
    Regular TSE daytime session only.
    09:00-11:30 and 12:30-15:30 JST on weekdays.
    """
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


def validate_market_gate(aab: dict, task: dict) -> None:
    scope = aab.get("execution_scope", {})
    constraints = aab.get("constraints", {})
    test_controls = aab.get("test_controls", {})

    market_hours_only = scope.get("market_hours_only", True)
    dry_run = constraints.get("dry_run", False)
    allow_off_hours_test = test_controls.get("allow_off_hours_test", False)
    task_off_hours_allowed = task.get("off_hours_test_allowed", False)

    now_local = datetime.now().astimezone()

    if not market_hours_only:
        return

    if is_regular_tse_market_hours(now_local):
        return

    if dry_run and allow_off_hours_test and task_off_hours_allowed:
        return

    raise ValueError(
        "market_hours_only=true and request is outside regular TSE market hours, "
        "with no approved dry_run off-hours override"
    )


def validate_aab(aab: dict, task: dict) -> None:
    scope = aab.get("execution_scope", {})
    constraints = aab.get("constraints", {})
    capital_allocation = aab.get("capital_allocation", {})

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
        raise ValueError("dry_run must be true for simulated_order")

    if constraints.get("external_order_allowed", True):
        raise ValueError("external_order_allowed must be false")

    if capital_allocation.get("constraint_type") != "simulated_only":
        raise ValueError("capital_allocation.constraint_type must be simulated_only")

    validate_market_gate(aab, task)


def get_trace_db_conn():
    return psycopg.connect(
        host=get_required_env("OPENCLAW_TRACE_DB_HOST"),
        port=get_required_env("OPENCLAW_TRACE_DB_PORT"),
        dbname=get_required_env("OPENCLAW_TRACE_DB_NAME"),
        user=get_required_env("OPENCLAW_TRACE_DB_USER"),
        password=get_required_env("OPENCLAW_TRACE_DB_PASSWORD"),
    )


def record_execution(aab: dict, order_params: dict, kabu_mode: str, kabu_port: int) -> None:
    metadata = {
        "event_type": "execution_recorded",
        "execution_subtype": "simulated_order",
        "aab_id": aab.get("aab_id", ""),
        "target_agent_id": "openclaw",
        "status": "simulated",
        "order_params": order_params,
        "dry_run": True,
        "external_order_sent": False,
        "kabu_api_mode": kabu_mode,
        "kabu_api_port": kabu_port,
        "recorded_by": "OpenClaw/Recorder",
        "recorded_at": datetime.now().isoformat(),
    }

    conn = get_trace_db_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO research.trace_event
                  (ts, agent_id, actor_type, event_type, content)
                VALUES (NOW(), 'openclaw', 'ai', %s, %s)
                """,
                (
                    "execution_recorded",
                    json.dumps(metadata, ensure_ascii=False),
                ),
            )
    conn.close()


def main(aab_path: str) -> None:
    task = load_task_artifact()

    with open(aab_path, "r", encoding="utf-8") as f:
        aab = json.load(f)

    validate_aab(aab, task)

    # simulation must use test credentials/port only
    kabu_cfg = get_test_kabu_config()

    scope = aab.get("execution_scope", {})
    order_params = {
        "symbol": scope.get("symbol"),
        "order_type": scope.get("order_type", "market"),
        "side": scope.get("side"),
        "quantity": scope.get("quantity"),
        "estimated_price": None,
        "simulated_at": datetime.now().isoformat(),
        "dry_run": True,
        "external_order_sent": False,
        "kabu_api_mode": kabu_cfg["mode"],
        "kabu_api_port": kabu_cfg["port"],
    }

    print(
        f"[simulated_order] dry_run order_params: "
        f"{json.dumps(order_params, indent=2, ensure_ascii=False)}"
    )

    record_execution(aab, order_params, kabu_cfg["mode"], kabu_cfg["port"])
    print("[simulated_order] execution_recorded (subtype=simulated_order)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python run_simulated_order.py <aab_path>")
        sys.exit(1)
    main(sys.argv[1])