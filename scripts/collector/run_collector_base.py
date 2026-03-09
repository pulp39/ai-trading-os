from __future__ import annotations

from src.collector import BaseCollector


def main() -> None:
    collector = BaseCollector("base_collector")

    event_id = collector.record_startup_event(
        metadata={
            "entry_point": "scripts/collector/run_collector_base.py",
            "purpose": "foundation_validation",
        }
    )

    print("Collector foundation initialized successfully.")
    print(f"collector_name: {collector.collector_name}")
    print(f"trace_event_id: {event_id}")


if __name__ == "__main__":
    main()
