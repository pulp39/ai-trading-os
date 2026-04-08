---
task_id: step-3-production-token
version: 1.0
role: collector
step: 3
command: |
  powershell.exe -NoProfile -Command "token request"
expected_output:
  - Production Token Attempt
  - Token Result
  - Token Response
  - Judgment
stop_conditions:
  - TOKEN_FAIL
writes_state: false
requires_approval: false
parent_document: docs/anchors/technical/OPENCLAW_FLIGHT_CHECKLIST.md
---

# STEP 3 — Production Token Attempt

## Purpose
Validate token acquisition exactly once.

## Notes
- No retry allowed
- TOKEN_FAIL = STOP
