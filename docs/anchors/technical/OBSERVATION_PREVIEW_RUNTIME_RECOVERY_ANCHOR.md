# OBSERVATION_PREVIEW_RUNTIME_RECOVERY_ANCHOR

Version: 1.0
Date: 2026-03-31
Status: active
Purpose: Recovery and pre-market readiness reference for Observation → Preview runtime under OpenClaw / WSL

---

> ⚠️ Status: deprecated  
> This content has been consolidated into `docs/anchors/technical/RUNTIME_ENVIRONMENT_ANCHOR.md`.  
> Refer to that anchor for current runtime, recovery, and troubleshooting guidance.

---

## 0. About This Document

This document provides a focused recovery guide for restoring the
Observation → Preview path before or during market-hours validation.

It is not a constitutional document.
It is not a broad execution document.
It is a technical-operational recovery anchor for repeated runtime issues
observed during Phase 7.5 validation.

This document should be used when:

- OpenClaw repeatedly fails before fresh board acquisition
- `.env.local` / `.venv` / PowerShell path issues are suspected
- KabuStation access succeeds manually but fails through OpenClaw
- market-open testing must be resumed quickly and safely

---

## 1. What This Anchor Covers

This anchor covers the bounded path:

Observation → Preview

It does **not** authorize:

- Approval
- Execution
- order transmission
- capital deployment

Its purpose is to restore and validate the technical path required to
obtain fresh observation data and reach bounded Preview readiness states.

---

## 2. Canonical Runtime Base

The canonical runtime base for this workflow is:

`/mnt/c/ai-trading-os-private`

Do **not** use:

`/home/vmamako/.openclaw/workspace`

for ATOS observation / preview runtime recovery in the current system.

If OpenClaw drifts toward `.openclaw/workspace`, correct it immediately
back to `/mnt/c/ai-trading-os-private`.

---

## 3. Canonical Environment Requirements

The following must be satisfied in the **same shell execution context**:

1. runtime base is `/mnt/c/ai-trading-os-private`
2. `.env.local` is sourced
3. `.venv` is activated
4. Windows PowerShell directory is added to `PATH`

If any of these are missing, repeated false debugging often occurs.

---

## 4. Repeated Failure Pattern Identified on 2026-03-31

The following failure loop was observed and should be treated as a known
recurrent risk:

### 4.1 Wrong runtime base drift
OpenClaw attempted to use:

`/home/vmamako/.openclaw/workspace`

instead of the canonical ATOS runtime base.

### 4.2 Environment not loaded in same shell
`.env.local` was not present in the same execution context as the Python
script, resulting in:

- `KABU_API_PASSWORD is missing or empty`

### 4.3 Virtual environment not activated
`.venv` was not activated in the same shell, resulting in:

- `ModuleNotFoundError: No module named 'psycopg'`

### 4.4 Windows PowerShell not resolvable from subprocess
Collector scripts internally called:

`powershell.exe`

but WSL `PATH` did not resolve it, resulting in:

- `FileNotFoundError: [Errno 2] No such file or directory: 'powershell.exe'`

### 4.5 Direct ad hoc token POST was less reliable than validated script path
Custom OpenClaw token POST attempts repeatedly returned `400`, while
the validated collector-script pathway succeeded.

**Conclusion:** prefer validated script paths over ad hoc direct token
construction unless script-level recovery is impossible.

---

## 5. Canonical Recovery Shell Pattern

Use the following shell preparation pattern when restoring the
Observation path:

```bash
cd /mnt/c/ai-trading-os-private && \
export PATH="/mnt/c/Windows/System32/WindowsPowerShell/v1.0:$PATH" && \
set -a && source ./.env.local && set +a && \
source ./.venv/bin/activate

This preparation pattern should be treated as the default recovery
baseline for OpenClaw / WSL observation work.

6. Canonical Recovery Order

Use the following order. Do not skip ahead.

Step 1 — restore environment context

Apply the canonical recovery shell pattern.

Step 2 — restore symbol registration

Run:

python3 scripts/collector/register_symbol_once.py

Success indicators:

TokenAcquired: true
registration result includes target symbol
SymbolCount is non-zero
Step 3 — restore board collection

Run:

python3 scripts/collector/collect_board_once.py 7203

Success indicators:

board fetch succeeds
board snapshot is written
indicator observation is written
registrar runner completes
Step 4 — apply freshness gate

Use newly collected timestamps:

CurrentPriceTime
BidTime
AskTime

Primary rule:

use CurrentPriceTime

Fallback:

use max(BidTime, AskTime) if needed and valid

If freshness > 60 seconds:

DATA_INVALID

Do not continue to later readiness checks.

Step 5 — apply hard limits

Hard limits currently include:

freshness > 60s → DATA_INVALID
slippage > 1.0% → NOT_READY
ask_qty < 100 → NOT_READY
Step 6 — apply temporary soft limits if explicitly provided

Example test-only soft limits used during Phase 7.5 validation:

reprice_threshold = 0.003
liquidity_threshold = 500

If soft limits are not explicitly provided, stop at:

HARD_LIMITS_PASS_SOFT_PENDING

7. Validated Phase 7.5 Result (2026-03-31)

The following bounded result was successfully achieved during market hours
for symbol 7203:

fresh observation acquired
freshness gate passed
hard limits passed
temporary soft-limit evaluation passed
readiness state reached READY
bounded trace_event write completed for:
event_type: execution_readiness_checked

This validated:

Observation → Preview → READY → STOP

The significance of this result is that the institution reached READY
without proceeding to execution.

8. Recovery Decision Table
Symptom	Most likely cause	Correct response
KABU_API_PASSWORD is missing or empty	.env.local not loaded in same shell	source .env.local in same shell context
ModuleNotFoundError: psycopg	.venv not activated	activate .venv in same shell context
No such file or directory: 'powershell.exe'	Windows PowerShell dir missing from PATH	add /mnt/c/Windows/System32/WindowsPowerShell/v1.0 to PATH
OpenClaw uses .openclaw/workspace	wrong runtime base drift	reset to /mnt/c/ai-trading-os-private
direct token POST returns 400 repeatedly	unstable ad hoc request path	switch back to validated collector script path
stale timestamps	market data not fresh	stop with DATA_INVALID
9. Operational Principle

When restoring Observation → Preview, prefer:

canonical runtime base
canonical environment loading
canonical script pathway

over:

ad hoc shell improvisation
custom direct token construction
alternate network routes

The shortest correct path is usually safer than the most “direct” path.

10. Relation to Other Anchors

This document should be read together with:

docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md
docs/anchors/governance/EXECUTION_MODEL_ANCHOR.md
docs/anchors/technical/WSL_ENVIRONMENT_ANCHOR.md

This anchor does not replace those documents.
It specializes them for pre-market and runtime recovery work.

11. Final Reminder

This anchor supports recovery of:

Observation → Preview

It does not authorize progression into:

Approval → Execution

If READY is reached, that is a validated institutional state —
not an instruction to execute.
