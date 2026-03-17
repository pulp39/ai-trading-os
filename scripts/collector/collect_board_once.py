#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
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


def register_symbol_via_powershell(symbol: str) -> None:
    password = os.environ["KABU_API_PASSWORD"]

    ps_script = f"""
$ErrorActionPreference = "Stop"
$env:KABU_API_PASSWORD = {json.dumps(password)}

$tokenBody = @{{ APIPassword = $env:KABU_API_PASSWORD }} | ConvertTo-Json
$token = (Invoke-RestMethod -Method Post -Uri "http://localhost:{KABU_PORT}/kabusapi/token" -ContentType "application/json" -Body $tokenBody).Token

$regBody = @{{
    Symbols = @(
        @{{ Symbol = "{symbol}"; Exchange = {EXCHANGE} }}
    )
}} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Method Put -Uri "http://localhost:{KABU_PORT}/kabusapi/register" -Headers @{{ "X-API-KEY" = $token }} -ContentType "application/json" -Body $regBody | Out-Null
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

    password = os.environ["KABU_API_PASSWORD"]

    ps_script = f"""
$ErrorActionPreference = "Stop"
$env:KABU_API_PASSWORD = {json.dumps(password)}

$tokenBody = @{{ APIPassword = $env:KABU_API_PASSWORD }} | ConvertTo-Json
$token = (Invoke-RestMethod -Method Post -Uri "http://localhost:{KABU_PORT}/kabusapi/token" -ContentType "application/json" -Body $tokenBody).Token

Invoke-RestMethod -Method Get -Uri "http://localhost:{KABU_PORT}/kabusapi/board/{symbol}@{EXCHANGE}" -Headers @{{ "X-API-KEY" = $token }} |
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


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: python collect_board_once.py <symbol>")
        sys.exit(1)

    symbol = sys.argv[1]

    print("Registering symbol via Windows PowerShell...")
    register_symbol_via_powershell(symbol)

    print("Fetching board via Windows PowerShell...")
    board_path = save_board_via_powershell(symbol)

    with open(board_path, "r", encoding="utf-8-sig") as f:
        board = json.load(f)

    insert_board_snapshot(board)

    print("Converting to observation...")
    obs_path = run_convert(board_path)

    print("Creating registrar task...")
    task_path = run_register(obs_path)

    print("Executing registrar runner...")
    run_registrar(task_path)

    print("Done.")


if __name__ == "__main__":
    main()