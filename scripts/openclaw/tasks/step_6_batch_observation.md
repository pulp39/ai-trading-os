---
task_id: step-6-batch-observation
version: 1.0
role: collector
step: 6
command: |
  bash -lc 'run batch observations'
expected_output:
  - Observation Result
  - Snapshot Result
  - Trace Result
stop_conditions:
  - any_symbol_failure
writes_state: true
requires_approval: false
parent_document: docs/anchors/technical/OPENCLAW_FLIGHT_CHECKLIST.md
---

# STEP 6 — Batch Observation

## Purpose
Validate collector across symbols.

## Notes
- Each symbol independent
- Diagnostic use only
