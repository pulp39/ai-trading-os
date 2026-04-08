---
task_id: step-7-preview-path
version: 1.0
role: collector
step: 7
command: |
  bash -lc 'execute preview'
expected_output:
  - Preview Result
  - execution_readiness_evaluated Result
  - READY Context Result
stop_conditions:
  - NOT_READY
writes_state: true
requires_approval: false
parent_document: docs/anchors/technical/OPENCLAW_FLIGHT_CHECKLIST.md
---

# STEP 7 — Preview Path

## Purpose
Validate preview pipeline and readiness evaluation.

## Notes
- Preview only
- STOP on NOT_READY is valid
