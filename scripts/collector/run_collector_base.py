from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.collector.base import BaseCollector


def main() -> None:
    collector = BaseCollector(collector_name="base_collector")

    collector.record_validation_event(
        event_type="documentation_alignment",
        content=(
            "Established trace_event semantic rules and aligned repository "
            "documentation with institutional event recording guidelines."
        ),
        metadata={
            "phase": "collector_refinement",
            "scope": "documentation",
            "purpose": "institutional_alignment",
            "entry_point": "scripts/collector/run_collector_base.py",
        },
    )


if __name__ == "__main__":
    main()