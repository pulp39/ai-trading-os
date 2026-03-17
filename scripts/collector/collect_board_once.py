#!/usr/bin/env python3
import sys
import json
import urllib.request
import subprocess
from pathlib import Path

KABU_HOST = "172.18.240.1"
KABU_PORT = 18080
EXCHANGE = 1

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "collector_input"

CONVERT_SCRIPT = BASE_DIR / "scripts" / "collector" / "convert_board_to_observation.py"
REGISTER_SCRIPT = BASE_DIR / "scripts" / "registrar" / "register_observation_file.py"
RUNNER_SCRIPT = BASE_DIR / "scripts" / "registrar" / "registrar_db_runner.py"


def fetch_board(symbol: str) -> dict:
    url = f"http://{KABU_HOST}:{KABU_PORT}/kabusapi/board/{symbol}@{EXCHANGE}"
    with urllib.request.urlopen(url) as res:
        return json.loads(res.read().decode("utf-8"))


def save_board(symbol: str, board: dict) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / f"board_{symbol}_{KABU_PORT}.json"
    path.write_text(json.dumps(board, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def run_convert(board_path: Path) -> Path:
    result = subprocess.run(
        ["python", str(CONVERT_SCRIPT), str(board_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return Path(result.stdout.strip())


def run_register(obs_path: Path) -> Path:
    result = subprocess.run(
        ["python", str(REGISTER_SCRIPT), str(obs_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return Path(result.stdout.strip())


def run_registrar(task_path: Path) -> None:
    subprocess.run(
        ["python", str(RUNNER_SCRIPT), "--task", str(task_path)],
        check=True,
    )


def main():
    if len(sys.argv) != 2:
        print("usage: python collect_board_once.py <symbol>")
        sys.exit(1)

    symbol = sys.argv[1]

    print("Fetching board...")
    board = fetch_board(symbol)

    print("Saving board JSON...")
    board_path = save_board(symbol, board)

    print("Converting to observation...")
    obs_path = run_convert(board_path)

    print("Creating registrar task...")
    task_path = run_register(obs_path)

    print("Executing registrar runner...")
    run_registrar(task_path)

    print("Done.")


if __name__ == "__main__":
    main()