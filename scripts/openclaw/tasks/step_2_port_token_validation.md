---
task_id: step-2-port-token-validation
version: 1.0
role: collector
step: 2
command: |
  bash -lc 'cd /mnt/c/ai-trading-os-private && export PATH="$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0" && source ./.env.local && source scripts/registrar/.venv/bin/activate && powershell.exe -NoProfile -Command "netsh ... token check"'
expected_output:
  - Portproxy Rules
  - Listener
  - Token Reachability
stop_conditions:
  - transport_failure
  - ownership_conflict
writes_state: false
requires_approval: false
parent_document: docs/anchors/technical/OPENCLAW_FLIGHT_CHECKLIST.md
---

# STEP 2 — Port Ownership & Token Reachability

## Purpose
Validate production port 18080 ownership and token path.

## Notes
- TOKEN_FAIL without APILog = transport failure
- No retry allowed
