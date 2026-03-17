#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

from datetime import datetime, time
import zoneinfo

SKIP_MARKET_HOURS_CHECK = True

JST = zoneinfo.ZoneInfo("Asia/Tokyo")

def is_market_open() -> bool:
    now = datetime.now(JST).time()

    morning = time(9, 0) <= now <= time(11, 30)
    afternoon = time(12, 30) <= now <= time(15, 30)

    return morning or afternoon

SYMBOLS = ["7203", "8306", "6758"]

BASE_DIR = Path(__file__).resolve().parents[2]
COLLECT_SCRIPT = BASE_DIR / "scripts" / "collector" / "collect_board_once.py"


def main() -> int:
    if (not SKIP_MARKET_HOURS_CHECK) and (not is_market_open()):
        print("Market is closed. Skipping collection.")
        return

    python_exe = sys.executable
    overall_ok = True

    for symbol in SYMBOLS:
        print(f"=== collecting {symbol} ===")
        result = subprocess.run([python_exe, str(COLLECT_SCRIPT), symbol])

        if result.returncode != 0:
            print(f"FAILED: {symbol}")
            overall_ok = False
        else:
            print(f"OK: {symbol}")

    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())