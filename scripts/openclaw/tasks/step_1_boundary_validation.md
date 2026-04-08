---
task_id: step-1-boundary-validation
version: 1.0
role: collector
step: 1
command: |
  bash -lc 'cd /mnt/c/ai-trading-os-private && export PATH="$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0" && source ./.env.local && source scripts/registrar/.venv/bin/activate && powershell.exe -NoProfile -Command "..."'
expected_output:
  - WSL Env
  - PowerShell Used Values
  - Match Result
  - Boundary Integrity
stop_conditions:
  - mismatch
  - parser_failure
writes_state: false
requires_approval: false
parent_document: docs/anchors/technical/OPENCLAW_FLIGHT_CHECKLIST.md
---

# STEP 1 — Boundary Validation

## Purpose
Ensure env parity between WSL and PowerShell.

## Notes
- Exact one-command execution
- STOP on mismatch
