#!/usr/bin/env python3
import subprocess
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from collector_run_writer import write_collector_run

SKIP_MARKET_HOURS_CHECK = True

SYMBOLS = ["7203", "8306", "6758"]
TOKYO = ZoneInfo("Asia/Tokyo")


def is_market_open() -> bool:
    now = datetime.now(TOKYO)
    weekday = now.weekday()
    if weekday >= 5:
        return False

    minutes = now.hour * 60 + now.minute
    morning_open = 9 * 60
    morning_close = 11 * 60 + 30
    afternoon_open = 12 * 60 + 30
    afternoon_close = 15 * 60 + 30

    return (
        morning_open <= minutes < morning_close
        or afternoon_open <= minutes < afternoon_close
    )


def main() -> int:
    if (not SKIP_MARKET_HOURS_CHECK) and (not is_market_open()):
        print("Market is closed. Skipping collection.")
        return 0

    started_at = datetime.now(TOKYO).isoformat(timespec="seconds")

    success_symbols: list[str] = []
    failed_symbols: list[str] = []

    for symbol in SYMBOLS:
        print(f"=== collecting {symbol} ===")
        result = subprocess.run(
            [sys.executable, "scripts/collector/collect_board_once.py", symbol]
        )
        if result.returncode == 0:
            print(f"OK: {symbol}")
            success_symbols.append(symbol)
        else:
            print(f"FAILED: {symbol}")
            failed_symbols.append(symbol)

    completed_at = datetime.now(TOKYO).isoformat(timespec="seconds")
    snapshot_count = len(success_symbols)

    if snapshot_count == len(SYMBOLS):
        status = "success"
    elif snapshot_count == 0:
        status = "failure"
    else:
        status = "partial_failure"

    write_collector_run(
        symbols=SYMBOLS,
        snapshot_count=snapshot_count,
        status=status,
        started_at=started_at,
        completed_at=completed_at,
        failed_symbols=failed_symbols,
        aab_bundle_id=None,
    )

    return 0 if status == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())