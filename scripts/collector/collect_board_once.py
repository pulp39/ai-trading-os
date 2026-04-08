#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from indicator_writer import write_indicator_observation
from snapshot_writer import insert_board_snapshot

KABU_PORT = 18080
EXCHANGE = 1

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "collector_input"

CONVERT_SCRIPT = BASE_DIR / "scripts" / "collector" / "convert_board_to_observation.py"
REGISTER_SCRIPT = BASE_DIR / "scripts" / "registrar" / "register_observation_file.py"
RUNNER_SCRIPT = BASE_DIR / "scripts" / "registrar" / "registrar_db_runner.py"


def run_powershell(ps_script: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", ps_script],
        capture_output=True,
        text=True,
        encoding="cp932",
        errors="replace",
    )


def get_kabu_host() -> str:
    host = (os.environ.get("KABU_API_HOST") or "localhost").strip()
    if not host:
        raise RuntimeError("KABU_API_HOST is empty")
    return host


def get_kabu_password() -> str:
    password = os.environ.get("KABU_API_PASSWORD")
    if not password:
        raise RuntimeError("KABU_API_PASSWORD is missing or empty")
    return password


def should_skip_registration() -> bool:
    return os.environ.get("SKIP_KABU_REGISTRATION", "").strip() == "1"


def register_symbol_via_powershell(symbol: str) -> None:
    host = get_kabu_host()
    password = get_kabu_password()

    ps_script = f"""
$ErrorActionPreference = "Stop"

$apiHost = [string]{json.dumps(host)}
$apiPort = [string]"{KABU_PORT}"
$apiPassword = [string]{json.dumps(password)}

$tokenBody = @{{ APIPassword = $apiPassword }} | ConvertTo-Json -Compress
$tokenUri = "http://" + $apiHost + ":" + $apiPort + "/kabusapi/token"
$tokenResp = Invoke-RestMethod -Method Post -Uri $tokenUri -Body $tokenBody -ContentType "application/json"
$token = $tokenResp.Token

$registerBodyObj = @{{
    Symbols = @(
        @{{
            Symbol = "{symbol}"
            Exchange = {EXCHANGE}
        }}
    )
}}
$registerBody = $registerBodyObj | ConvertTo-Json -Compress -Depth 5
$registerUri = "http://" + $apiHost + ":" + $apiPort + "/kabusapi/register"
$headers = @{{ "X-API-KEY" = $token }}

$registerResp = Invoke-RestMethod -Method Put -Uri $registerUri -Headers $headers -Body $registerBody -ContentType "application/json"
$registerResp | ConvertTo-Json -Compress
"""

    result = run_powershell(ps_script)
    if result.returncode != 0:
        raise RuntimeError(
            "PowerShell symbol registration failed\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )


def save_board_via_powershell(symbol: str) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    board_path = DATA_DIR / f"board_{symbol}_{KABU_PORT}.json"
    board_path_windows = subprocess.check_output(
        ["wslpath", "-w", str(board_path)],
        text=True,
    ).strip()

    host = get_kabu_host()
    password = get_kabu_password()

    ps_script = f"""
$ErrorActionPreference = "Stop"

$apiHost = [string]{json.dumps(host)}
$apiPort = [string]"{KABU_PORT}"
$apiPassword = [string]{json.dumps(password)}

$tokenBody = @{{ APIPassword = $apiPassword }} | ConvertTo-Json -Compress
$tokenUri = "http://" + $apiHost + ":" + $apiPort + "/kabusapi/token"
$tokenResp = Invoke-RestMethod -Method Post -Uri $tokenUri -Body $tokenBody -ContentType "application/json"
$token = $tokenResp.Token

$boardUri = "http://" + $apiHost + ":" + $apiPort + "/kabusapi/board/{symbol}@{EXCHANGE}"
$headers = @{{ "X-API-KEY" = $token }}

Invoke-RestMethod -Method Get -Uri $boardUri -Headers $headers |
    ConvertTo-Json -Depth 10 |
    Set-Content -Encoding UTF8 "{board_path_windows}"
"""

    result = run_powershell(ps_script)
    if result.returncode != 0:
        raise RuntimeError(
            "PowerShell board fetch failed\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )

    if not board_path.exists():
        raise FileNotFoundError(f"Board file was not created: {board_path}")

    return board_path


def run_convert(board_path: Path) -> Path:
    result = subprocess.run(
        [sys.executable, str(CONVERT_SCRIPT), str(board_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return Path(result.stdout.strip())


def run_register(obs_path: Path) -> Path:
    result = subprocess.run(
        [sys.executable, str(REGISTER_SCRIPT), str(obs_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return Path(result.stdout.strip())


def run_registrar(task_path: Path) -> None:
    subprocess.run(
        [sys.executable, str(RUNNER_SCRIPT), "--task", str(task_path)],
        check=True,
    )


def _coerce_captured_at(value) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value)
    raise TypeError(f"Unsupported captured_at type: {type(value)}")


def main() -> None:
    if len(sys.argv) != 2:
        print(f"usage: {sys.executable} collect_board_once.py <symbol>")
        sys.exit(1)

    symbol = sys.argv[1]

    if should_skip_registration():
        print("Skipping symbol registration because SKIP_KABU_REGISTRATION=1")
    else:
        print("Registering symbol via Windows PowerShell...")
        register_symbol_via_powershell(symbol)

    print("Fetching board via Windows PowerShell...")
    board_path = save_board_via_powershell(symbol)

    with open(board_path, "r", encoding="utf-8-sig") as f:
        board = json.load(f)

    print("Writing board snapshot...")
    snapshot_result = insert_board_snapshot(board)

    snapshot_id = snapshot_result["snapshot_id"]
    captured_at = _coerce_captured_at(snapshot_result["captured_at"])

    print("Writing indicator observation...")
    indicator_event_id = write_indicator_observation(
        symbol=str(symbol),
        captured_at=captured_at,
        current_price=board.get("CurrentPrice"),
        vwap=board.get("VWAP"),
        source_snapshot_id=snapshot_id,
        aab_bundle_id=None,
    )

    print(
        f"indicator_observation written: "
        f"symbol={symbol}, snapshot_id={snapshot_id}, event_id={indicator_event_id}"
    )

    print("Converting to observation...")
    obs_path = run_convert(board_path)

    print("Creating registrar task...")
    task_path = run_register(obs_path)

    print("Executing registrar runner...")
    run_registrar(task_path)

    print("Done.")


if __name__ == "__main__":
    main()