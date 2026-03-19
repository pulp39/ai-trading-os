#!/usr/bin/env python3
"""
scripts/openclaw/run_simulated_order.py
Bounded simulated_order execution path (P-20260319-016)
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

import psycopg

BASE_DIR = Path(__file__).resolve().parents[2]
TASK_ARTIFACT = BASE_DIR / "registrar_queue" / "simulated_order_task.json"


def load_task_artifact() -> dict:
    if not TASK_ARTIFACT.exists():
        raise FileNotFoundError(f"Approved task artifact not found: {TASK_ARTIFACT}")
    with TASK_ARTIFACT.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_aab(aab: dict, task: dict) -> None:
    scope = aab.get("execution_scope", {})
    constraints = aab.get("constraints", {})

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


def record_execution(aab: dict, order_params: dict) -> None:
    metadata = {
        "event_type": "execution_recorded",
        "execution_subtype": "simulated_order",
        "aab_id": aab.get("aab_id", ""),
        "target_agent_id": "openclaw",
        "status": "simulated",
        "order_params": order_params,
        "dry_run": True,
        "external_order_sent": False,
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
    }

    print(f"[simulated_order] dry_run order_params: {json.dumps(order_params, indent=2, ensure_ascii=False)}")

    record_execution(aab, order_params)
    print("[simulated_order] execution_recorded (subtype=simulated_order)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python run_simulated_order.py <aab_path>")
        sys.exit(1)
    main(sys.argv[1])