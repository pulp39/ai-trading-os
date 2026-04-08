---
task_id: step-4-symbol-registration
version: 1.0
role: collector
step: 4
command: |
  bash -lc '...register_symbol_once_8306_tmp.py'
expected_output:
  - Registration Result
  - Registration Response
stop_conditions:
  - registration_failure
writes_state: true
requires_approval: false
parent_document: docs/anchors/technical/OPENCLAW_FLIGHT_CHECKLIST.md
---

# STEP 4 — Symbol Registration

## Purpose
Recover symbol state after restart.

## Notes
- UNKNOWN state must be resolved once
- No retry allowed
