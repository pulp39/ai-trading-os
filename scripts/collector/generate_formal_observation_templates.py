#!/usr/bin/env python3
"""
generate_formal_observation_templates.py

Purpose:
- Generate one or more formal observation JSON template files
- Use explicit session dates to avoid ambiguity
- Produce institutionally consistent filenames and observation IDs

Usage examples:
    python scripts/collector/generate_formal_observation_templates.py ^
      --instrument "ES1! (S&P 500 E-mini Futures, front month)" ^
      --reference-instrument "NQ1! (Nasdaq-100 E-mini Futures, front month)" ^
      --dates 2026-03-10 2026-03-11 2026-03-12 2026-03-13 2026-03-16

    python scripts/collector/generate_formal_observation_templates.py ^
      --instrument "ES1! (S&P 500 E-mini Futures, front month)" ^
      --reference-instrument "NQ1! (Nasdaq-100 E-mini Futures, front month)" ^
      --dates 2026-03-10 2026-03-11 ^
      --output-dir data/observations/es1
"""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path


COLLECTOR_ID = "collector_base_collector_v1"
COLLECTOR_DESIGNATION = "base_collector_v1"
ACTIVATION_TRACE_EVENT_ID = 35
ASSET_CLASS = "equity index futures"
TIMEFRAME = "daily"
SESSION_DATE_CONVENTION = "exchange_defined_completed_trading_session_date"
PROPOSAL_BASIS = "P-20260310-008"
DEFAULT_SIGNAL_QUALITY_TIER = "partial"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate formal observation JSON template files."
    )
    parser.add_argument(
        "--instrument",
        required=True,
        help='Authorized instrument, e.g. "ES1! (S&P 500 E-mini Futures, front month)"',
    )
    parser.add_argument(
        "--reference-instrument",
        required=True,
        help='Reference instrument, e.g. "NQ1! (Nasdaq-100 E-mini Futures, front month)"',
    )
    parser.add_argument(
        "--dates",
        nargs="+",
        required=True,
        help="Explicit session dates in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--output-dir",
        default="data/observations",
        help="Directory to write JSON files into. Default: data/observations",
    )
    parser.add_argument(
        "--default-tier",
        default=DEFAULT_SIGNAL_QUALITY_TIER,
        choices=["complete", "partial", "minimal", "unreliable"],
        help="Default signal quality tier. Default: partial",
    )
    return parser.parse_args()


def validate_dates(dates: list[str]) -> list[str]:
    validated: list[str] = []
    for value in dates:
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError as exc:
            raise SystemExit(f"Invalid date format: {value}. Use YYYY-MM-DD.") from exc
        validated.append(value)
    return validated


def build_template(
    session_date: str,
    sequence: int,
    instrument: str,
    reference_instrument: str,
    signal_quality_tier: str,
) -> dict:
    observation_id = (
        f"OBS-{COLLECTOR_ID}-{session_date.replace('-', '')}-{sequence:03d}"
    )

    collection_timestamp_utc = f"{session_date}T22:15:00Z"

    template = {
        "observation_status": "formal",
        "collector_id": COLLECTOR_ID,
        "observation_id": observation_id,
        "authorized_asset_class": ASSET_CLASS,
        "authorized_timeframe": TIMEFRAME,
        "authorized_instrument": instrument,
        "session_date": session_date,
        "session_date_convention": SESSION_DATE_CONVENTION,
        "collection_timestamp_utc": collection_timestamp_utc,
        "observation_payload": {
            "price_context": {
                "close": 0,
                "return_1d": 0,
                "distance_from_short_mean": 0,
                "distance_from_baseline_mean": 0,
            },
            "volume_context": {
                "session_volume": 0,
                "short_window_volume_mean": 0,
                "baseline_window_volume_mean": 0,
                "volume_ratio_short_to_baseline": 0,
            },
            "volatility_regime": {
                "realized_vol_short": 0,
                "realized_vol_baseline": 0,
                "realized_vol_ratio_short_to_baseline": 0,
                "implied_vol_front": None,
                "implied_minus_realized": None,
            },
            "macro_event_proximity": {
                "days_to_next_scheduled_macro_event": 0,
                "days_from_last_scheduled_macro_event": 0,
                "macro_event_flag": None,
            },
            "correlation_state": {
                "reference_instrument": reference_instrument,
                "rolling_correlation_short": 0,
                "rolling_correlation_baseline": 0,
                "correlation_regime_change_flag": None,
            },
        },
        "quality_classification": {
            "signal_quality_tier": signal_quality_tier,
            "dimensional_completeness_flags": {
                "price_context": True,
                "volume_context": True,
                "volatility_regime": True,
                "macro_event_proximity": True,
                "correlation_state": True,
            },
            "reliability_notes": [
                "Replace with session-specific reliability notes."
            ],
        },
        "cadence_status": {
            "declared_cadence": "once_per_completed_trading_session",
            "cadence_deviation": False,
            "cadence_deviation_note": None,
        },
        "traceability": {
            "proposal_basis": PROPOSAL_BASIS,
            "collector_designation": COLLECTOR_DESIGNATION,
            "collector_role_status": "active",
            "activation_trace_event_id": ACTIVATION_TRACE_EVENT_ID,
        },
    }

    return template


def make_filename(session_date: str, instrument: str) -> str:
    symbol = instrument.split(" ")[0].replace("!", "").replace("/", "_").lower()
    return f"{session_date}_{symbol}.json"


def main() -> int:
    args = parse_args()
    dates = validate_dates(args.dates)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    written_files: list[Path] = []

    for idx, session_date in enumerate(dates, start=1):
        payload = build_template(
            session_date=session_date,
            sequence=1,
            instrument=args.instrument,
            reference_instrument=args.reference_instrument,
            signal_quality_tier=args.default_tier,
        )

        out_path = output_dir / make_filename(session_date, args.instrument)

        if out_path.exists():
            raise SystemExit(
                f"Refusing to overwrite existing file: {out_path}\n"
                "Rename it or move it before re-running."
            )

        with out_path.open("w", encoding="utf-8", newline="\n") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        written_files.append(out_path)

    print("Generated formal observation templates:")
    for path in written_files:
        print(f"  - {path}")

    print("\nNext step:")
    print("  Fill in the numeric fields and reliability notes, then run ingest_formal_observation.py on each file.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())