---
task_id: step-0-collector-initialization
version: 1.0
role: collector
step: 0
command: |
  respond COLLECTOR_READY
expected_output:
  - COLLECTOR_READY
stop_conditions:
  - role_violation
writes_state: false
requires_approval: false
parent_document: docs/anchors/technical/OPENCLAW_FLIGHT_CHECKLIST.md
---

# STEP 0 — Collector Initialization

## Purpose
Initialize OpenClaw as Collector.

## Notes
- No execution allowed
- Observation only
- STOP on any boundary ambiguity
