---
task_id: step-5-collector-one-shot
version: 1.0
role: collector
step: 5
command: |
  bash -lc '...collect_board_once.py 8306'
expected_output:
  - Observation Result
  - Snapshot Result
  - Trace Result
stop_conditions:
  - board_fetch_failure
writes_state: true
requires_approval: false
parent_document: docs/anchors/technical/OPENCLAW_FLIGHT_CHECKLIST.md
---

# STEP 5 — Collector One Shot

## Purpose
Execute bounded observation.

## Notes
- Exactly one execution
- No preview or order allowed
