#!/usr/bin/env python3

import json
import os
import subprocess
import sys
from pathlib import Path

import psycopg

EXECUTION_MODE = "production"
BROKER_TOUCH = True
EXTERNAL_ORDER_ALLOWED = True
KABU_PORT = 18080
PASSWORD_SOURCE = "KABU_API_PASSWORD"


def print_execution_declaration() -> None:
    print("[Execution Declaration]")
    print("command_class = bounded WRITE")
    print(f"broker_mode = {EXECUTION_MODE}")
    print(f"broker_touch = {BROKER_TOUCH}")
    print(f"external_order_allowed = {EXTERNAL_ORDER_ALLOWED}")
    print(f"kabu_port = {KABU_PORT}")
    print(f"password_source = {PASSWORD_SOURCE}")
    print("dry_run = False")


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


def run_powershell(ps_script: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", ps_script],
        capture_output=True,
        text=True,
        encoding="cp932",
        errors="replace",
    )


def load_aab(aab_path: str) -> dict:
    path = Path(aab_path)
    if not path.exists():
        raise FileNotFoundError(f"AAB file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_aab(aab: dict) -> None:
    required_top_level_keys = [
        "aab_id",
        "execution_scope",
        "constraints",
        "capital_allocation",
    ]
    for key in required_top_level_keys:
        if key not in aab:
            raise ValueError(f"Missing required AAB key: {key}")

    scope = aab["execution_scope"]
    constraints = aab["constraints"]
    capital_allocation = aab["capital_allocation"]

    required_scope_keys = [
        "symbol",
        "side",
        "quantity",
    ]
    for key in required_scope_keys:
        if key not in scope:
            raise ValueError(f"Missing required execution_scope key: {key}")

    symbol = scope["symbol"]
    side = scope["side"]
    quantity = scope["quantity"]

    if not isinstance(symbol, str) or not symbol.strip():
        raise ValueError(f"symbol must be a non-empty string, got {symbol!r}")

    if side not in {"buy", "sell"}:
        raise ValueError(f"side must be 'buy' or 'sell', got {side!r}")

    if not isinstance(quantity, int) or quantity <= 0:
        raise ValueError(f"quantity must be a positive integer, got {quantity!r}")

    if quantity != 1:
        raise ValueError(f"real_order currently requires quantity=1, got {quantity}")

    if constraints.get("retry", False):
        raise ValueError("retry must be false for real_order")

    if constraints.get("dry_run", False):
        raise ValueError("real_order main path must not be marked dry_run=true")

    if not capital_allocation:
        raise ValueError("capital_allocation must not be empty")


def validate_real_order_path_isolation(aab: dict) -> None:
    scope = aab["execution_scope"]
    constraints = aab["constraints"]

    if EXECUTION_MODE != "production":
        raise ValueError("run_real_order.py must operate in production mode only")

    if not BROKER_TOUCH:
        raise ValueError("run_real_order.py must have broker_touch=True")

    if not EXTERNAL_ORDER_ALLOWED:
        raise ValueError("run_real_order.py must have external_order_allowed=True")

    if KABU_PORT != 18080:
        raise ValueError("run_real_order.py must use KABU_PORT=18080")

    if PASSWORD_SOURCE != "KABU_API_PASSWORD":
        raise ValueError("run_real_order.py must use KABU_API_PASSWORD")

    if scope.get("market_hours_only") is False:
        raise ValueError("real_order must not disable market_hours_only")

    if constraints.get("external_order_allowed") is False:
        raise ValueError(
            "AAB constraints.external_order_allowed=false conflicts with real_order path"
        )


def fetch_ready_context_state(conn: psycopg.Connection, symbol: str) -> tuple[str, str]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT metadata->>'ready_context_id'
            FROM research.trace_event
            WHERE event_type = 'execution_readiness_evaluated'
              AND symbol = %s
              AND metadata->>'readiness_state' = 'READY'
              AND metadata ? 'ready_context_id'
            ORDER BY id DESC
            LIMIT 1
            """,
            (symbol,),
        )
        row = cur.fetchone()

        if not row or not row[0]:
            raise ValueError(f"No READY context found for symbol {symbol}")

        ready_context_id = row[0]

        cur.execute(
            """
            SELECT metadata->>'context_state'
            FROM research.trace_event
            WHERE event_type = 'ready_context_state'
              AND metadata->>'ready_context_id' = %s
            ORDER BY id DESC
            LIMIT 1
            """,
            (ready_context_id,),
        )
        state_row = cur.fetchone()

    context_state = state_row[0] if state_row and state_row[0] else "missing"
    return ready_context_id, context_state


def validate_ready_context_for_real_order(
    conn: psycopg.Connection, symbol: str
) -> tuple[str, str]:
    ready_context_id, context_state = fetch_ready_context_state(conn, symbol)

    if context_state != "active":
        raise ValueError(
            f"READY context {ready_context_id} is not active for real_order: {context_state}"
        )

    return ready_context_id, context_state


def acquire_kabu_token_dry_run() -> dict:
    """
    Production dry-run step:
    - verify PowerShell bridge is callable
    - verify KABU_API_HOST and KABU_API_PASSWORD are present
    - attempt token acquisition only

    This still does NOT:
    - send order
    - register symbol
    - fetch board
    """
    host = get_required_env("KABU_API_HOST")
    password = get_required_env("KABU_API_PASSWORD")

    ps_script = f"""
$ErrorActionPreference = "Stop"
$env:KABU_API_PASSWORD = {json.dumps(password)}

$tokenBody = @{{ APIPassword = $env:KABU_API_PASSWORD }} | ConvertTo-Json
$token = (Invoke-RestMethod -Method Post -Uri "http://{host}:{KABU_PORT}/kabusapi/token" -ContentType "application/json" -Body $tokenBody).Token

if (-not $token) {{
    throw "Token acquisition returned empty token"
}}

Write-Output $token
"""

    result = run_powershell(ps_script)

    if result.returncode != 0:
        return {
            "dry_run_status": "failed",
            "dry_run_type": "token_acquisition",
            "broker_mode": EXECUTION_MODE,
            "kabu_host": host,
            "kabu_port": KABU_PORT,
            "checks_passed": [
                "production_path_declared",
                "required_env_present",
            ],
            "checks_failed": [
                "token_acquisition",
            ],
            "stderr": result.stderr,
            "stdout": result.stdout,
        }

    token = result.stdout.strip()
    if not token:
        return {
            "dry_run_status": "failed",
            "dry_run_type": "token_acquisition",
            "broker_mode": EXECUTION_MODE,
            "kabu_host": host,
            "kabu_port": KABU_PORT,
            "checks_passed": [
                "production_path_declared",
                "required_env_present",
            ],
            "checks_failed": [
                "token_acquisition_empty",
            ],
            "stderr": result.stderr,
            "stdout": result.stdout,
        }

    return {
        "dry_run_status": "passed",
        "dry_run_type": "token_acquisition",
        "broker_mode": EXECUTION_MODE,
        "kabu_host": host,
        "kabu_port": KABU_PORT,
        "token_acquired": True,
        "checks_passed": [
            "production_path_declared",
            "required_env_present",
            "powershell_bridge_available",
            "token_acquisition",
        ],
        "checks_not_performed": [
            "sendorder",
            "broker_acceptance",
        ],
    }


def perform_real_order_dry_run(aab: dict, ready_context_id: str) -> dict:
    """
    Production dry-run:
    - AAB already validated
    - READY context already confirmed active
    - token acquisition is attempted
    - no external order transmission
    """
    scope = aab["execution_scope"]

    dry_run_result = acquire_kabu_token_dry_run()
    dry_run_result["symbol"] = scope["symbol"]
    dry_run_result["side"] = scope["side"]
    dry_run_result["quantity"] = scope["quantity"]
    dry_run_result["ready_context_id"] = ready_context_id

    return dry_run_result


def print_order_summary(aab: dict, ready_context_id: str, context_state: str) -> None:
    scope = aab["execution_scope"]

    summary = {
        "aab_id": aab["aab_id"],
        "symbol": scope["symbol"],
        "side": scope["side"],
        "quantity": scope["quantity"],
        "broker_mode": EXECUTION_MODE,
        "broker_touch": BROKER_TOUCH,
        "external_order_allowed": EXTERNAL_ORDER_ALLOWED,
        "kabu_port": KABU_PORT,
        "password_source": PASSWORD_SOURCE,
        "ready_context_id": ready_context_id,
        "context_state": context_state,
    }

    print("[Real Order Summary]")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def print_dry_run_result(dry_run_result: dict) -> None:
    print("[real_order_dry_run]")
    print(json.dumps(dry_run_result, ensure_ascii=False, indent=2))


def main(aab_path: str) -> None:
    print_execution_declaration()

    aab = load_aab(aab_path)
    validate_aab(aab)
    validate_real_order_path_isolation(aab)

    symbol = aab["execution_scope"]["symbol"]

    conn = get_trace_db_conn()
    try:
        ready_context_id, context_state = validate_ready_context_for_real_order(conn, symbol)
    finally:
        conn.close()

    dry_run_result = perform_real_order_dry_run(aab, ready_context_id)

    print("[AAB Loaded and Validated]")
    print_order_summary(aab, ready_context_id, context_state)
    print_dry_run_result(dry_run_result)

    if dry_run_result["dry_run_status"] != "passed":
        print("[NO_GO]")
        print("real_order_dry_run failed.")
        print("token acquisition did not succeed.")
        print("sendorder is not implemented.")
        sys.exit(1)

    print("[NO_GO]")
    print("run_real_order.py skeleton reached successfully.")
    print("READY context is active.")
    print("real_order_dry_run passed (token acquisition mode).")
    print("sendorder is not implemented yet.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python run_real_order.py <aab_path>")
        sys.exit(1)

    main(sys.argv[1])