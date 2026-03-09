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
        event_type="collector_boundary_definition",
        content=(
            "Defined the collector boundary in repository documentation so "
            "that collectors remain limited to observation and recording, "
            "while interpretation, hypothesis generation, and recommendation "
            "are reserved for future proposal-producing roles."
        ),
        metadata={
            "phase": "collector_refinement_closure",
            "scope": "documentation",
            "purpose": "role_boundary_definition",
            "entry_point": "docs/roles/collector.md",
            "commit": "e6251cb",
        },
    )


if __name__ == "__main__":
    main()