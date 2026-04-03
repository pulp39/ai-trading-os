📘 OpenClaw Flight Checklist (Production Only / One Path / Portproxy Safe)

This document defines the ONLY valid startup and execution path
for OpenClaw in ATOS.

Production API ONLY (port 18080)

Critical rules:

port open ≠ service reachable

If TOKEN_FAIL AND no APILog:
→ transport failure (NOT auth failure)
→ DO NOT retry

---

🔷 STEP 0 — Collector Initialization

You are participating in the AI Trading OS (ATOS) environment.

This session initializes you as a Collector.

Your role is strictly limited to:

recovering runtime when explicitly instructed
validating production boundary conditions
validating production port ownership and portproxy safety
collecting bounded market observations
returning factual outputs only

You do not interpret.
You do not evaluate readiness.
You do not run preview.
You do not execute simulated_order.
You do not execute real_order.
You do not send orders.

Core rules:

Observation only
You may read and collect data only

Stop discipline
You must STOP immediately if:
runtime base is wrong
env is unclear
PowerShell is unavailable
boundary validation is incomplete
port ownership is unsafe
portproxy conflict is detected
execution scope is unclear

When STOP is triggered:
You MUST clearly state:
- which condition failed
- why proceeding would be unsafe

Example:
"STOP: portproxy conflict detected on port 18080"

Minimality
Do exactly what is requested
Do not retry unless instructed

Output discipline
Return only requested sections

If ready, respond:

COLLECTOR_READY

---

🔷 STEP 1 — Boundary Validation（MANDATORY）

Boundary Validation

Use the runtime base:

/mnt/c/ai-trading-os-private

Objective:
Confirm that the WSL values and the explicitly assigned PowerShell values match for the production path.

Recovery:

cd /mnt/c/ai-trading-os-private
export PATH="$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0"
source ./.env.local
source scripts/registrar/.venv/bin/activate

Task:

Print WSL values:
KABU_API_HOST
KABU_API_PORT
KABU_API_PASSWORD

Perform exactly one PowerShell call using explicit in-command assignment:

powershell.exe -NoProfile -Command "
$psHost = [string]'$KABU_API_HOST';
$psPort = [string]'$KABU_API_PORT';
$psPassword = [string]'$KABU_API_PASSWORD';

Write-Output ('PS_KABU_API_HOST=' + $psHost);
Write-Output ('PS_KABU_API_PORT=' + $psPort);
Write-Output ('PS_KABU_API_PASSWORD=' + $psPassword);
"

Objective:

confirm explicit value transfer from WSL into PowerShell
prevent 'env exists ≠ env is used'

Return output in this format:

WSL Env
PowerShell Used Values
Match Result
Boundary Integrity
Issue (if any)

Judgment rule:

all values match exactly → proceed to STEP 2
any mismatch → STOP

---

🔷 STEP 2 — Portproxy / Port Ownership Preflight（MANDATORY）

Portproxy Rules
127.0.0.1:18789 -> 172.18.254.231:18789

Port 18080 Listener
LocalAddress=::
LocalPort=18080
OwningProcess=4

Ownership Judgment
All checks pass → proceed to STEP 3

Issue (if any)
None

Judgment rule:

if portproxy contains 18080 → STOP
if 18080 listener is missing → STOP
if 18080 listener is non-kabuStation / svchost / iphlpsvc → STOP
only safe ownership → proceed to STEP 3

---

🔷 STEP 3 — Production Token Attempt（MANDATORY）

（Additional rule:

If TOKEN_FAIL occurs AND APILog shows no record of the attempt,
treat this as transport failure (NOT authentication failure).

Do NOT retry.
Do NOT modify password.
Return diagnostic result.

--from here
Production Token Attempt

Use the runtime base:

/mnt/c/ai-trading-os-private

Recovery:

cd /mnt/c/ai-trading-os-private
export PATH="$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0"
source ./.env.local
source scripts/registrar/.venv/bin/activate

Task:

Perform exactly one PowerShell token attempt:

powershell.exe -NoProfile -Command "
$ErrorActionPreference = 'Stop';
$psHost = [string]'$KABU_API_HOST';
$psPort = [string]'18080';
$psPassword = [string]'$KABU_API_PASSWORD';

$body = @{ APIPassword = $psPassword } | ConvertTo-Json;
$uri = 'http://' + $psHost + ':' + $psPort + '/kabusapi/token';

try {
$res = Invoke-RestMethod -Method Post -Uri $uri -Body $body -ContentType 'application/json';
Write-Output 'TOKEN_SUCCESS';
Write-Output ($res | ConvertTo-Json -Compress);
} catch {
Write-Output 'TOKEN_FAIL';
Write-Output $_.Exception.Message;
}
"

Judgment rule:
TOKEN_SUCCESS → proceed to STEP 4
TOKEN_FAIL → STOP
--to here

---

🔷 STEP 4 — Collector One Shot（MANDATORY）

Runtime Recovery + Collector One Shot

Use the runtime base:

/mnt/c/ai-trading-os-private

Execute exactly once:

python scripts/collector/collect_board_once.py 7203

Constraints:

one observation only
production path only
no retries

Return:

Observation Result
Trace Result
Issue (if any)

---

🔶 MAIN PATH COMPLETE 🔶

STEP0 → STEP1 → STEP2 → STEP3 → STEP4

---

🔷 STEP 5 — Batch Observation（OPTIONAL / AFTER SUCCESS）

--
7203
--
Use the runtime base:

/mnt/c/ai-trading-os-private

Execute exactly once:

python scripts/collector/collect_board_once.py 7203

Constraints:

one observation only
production path only
no retries

Return:

Observation Result
Trace Result
Issue (if any)

--
8306
--
Use the runtime base:

/mnt/c/ai-trading-os-private

Execute exactly once:

python scripts/collector/collect_board_once.py 8306

Constraints:

one observation only
production path only
no retries

Return:

Observation Result
Trace Result
Issue (if any)

--
6758
--
Use the runtime base:

/mnt/c/ai-trading-os-private

Execute exactly once:

python scripts/collector/collect_board_once.py 6758

Constraints:

one observation only
production path only
no retries

Return:

Observation Result
Trace Result
Issue (if any)

---

🔷 STEP 6 — Preview Path（READY生成）

Use the runtime base:

/mnt/c/ai-trading-os-private

Recovery procedure:

1. cd /mnt/c/ai-trading-os-private
2. export PATH=$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0
3. source ./.env.local
4. source scripts/registrar/.venv/bin/activate

Do NOT run the collector.
Do NOT run real_order.
Do NOT attempt sendorder.

Precondition (MANDATORY):

A fresh observation must already exist for the target symbol.

Freshness must satisfy:

- snapshot must be recent enough for task artifact freshness_max_ms
- market must be open
- no reliance on override conditions

If freshness cannot be guaranteed → STOP

--

Preview AAB assumption:

Use a temporary preview-only AAB outside the repository.

Create:

/tmp/atos_order_preview_<symbol>.json

Example:

{
  "aab_id": "AAB-PREVIEW-<symbol>-TEMP",
  "execution_scope": {
    "action_type": "order_preview",
    "symbol": "<symbol>",
    "order_type": "market",
    "side": "buy",
    "quantity": 1
  },
  "constraints": {
    "dry_run": true,
    "external_order_allowed": false,
    "preview_only": true,
    "state_change_allowed": false,
    "test_override_allowed": false
  },
  "capital_allocation": {
    "constraint_type": "preview_only"
  }
}

--

Execute exactly once:

python -m scripts.openclaw.run_order_preview /tmp/atos_order_preview_<symbol>.json

--

Objective:

- generate execution_readiness_evaluated
- confirm readiness_state reflects live conditions
- ensure no overridden READY is produced
- produce a usable READY context

--

Return:

## Input Contract
## Correct Invocation
## Preview Result
## execution_readiness_evaluated Result
## READY Context Result
## Blocking Issue (if any)

--from here
脚注 — Preview AABと実行経路について

・Previewでは、AABは /tmp に一時JSONとして作成して渡す
　（永続アーティファクトではない）

・registrar_queue の artifact は Execution 用であり、
　Previewで使用すると不要な制約（allowed_symbols など）により
　処理がブロックされやすい

・Previewは Execution とは別レイヤであり、
　「軽量・一時・非拘束」であることが前提

・Preview用AABの最小要件は以下

　execution_scope.action_type = "order_preview"
　execution_scope.symbol
　execution_scope.order_type
　execution_scope.side
　execution_scope.quantity

・必須 constraints

　constraints.dry_run = true
　constraints.external_order_allowed = false
　constraints.preview_only = true

・overrideはテスト用途のみ

　constraints.state_change_allowed = false
　constraints.test_override_allowed = true

　※本番READYを作る場合は override を使わない

・実行は必ず module 形式

　python -m scripts.openclaw.run_order_preview /tmp/atos_order_preview_<symbol>.json

　→ file-path実行だと import error が発生する可能性あり

・まとめ

　Preview = 「一時AAB + module実行 + execution層と分離」

　Executionとは混ぜない
--to here

---

🔷 STEP 7 — READY Validation Chain

7. READY Validation Chain

7-1 Context Reuse Detection
7-2 READY Context Safety Validation

Use the runtime base:

/mnt/c/ai-trading-os-private

Recovery procedure:

1. cd /mnt/c/ai-trading-os-private
2. export PATH=$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0
3. source ./.env.local
4. source scripts/registrar/.venv/bin/activate

Do NOT run the collector.
Do NOT run preview.
Do NOT run real_order.

--

Task (Phase 1 — Reuse Detection):

Query the latest execution_readiness_evaluated events
for the same symbol used in preview.

Confirm:

- whether multiple READY contexts exist
- whether the latest READY is fresh
- whether reuse is occurring

--

Task (Phase 2 — Safety Validation):

Inspect the latest execution_readiness_evaluated result.

Confirm:

- readiness_state is one of:
  READY / REPRICE_REQUIRED / NOT_READY / DATA_INVALID
- failed_checks is empty for READY
- overridden_checks are empty for live validation
- freshness_seconds is within acceptable bounds
- the context is not already consumed

--

Objective:

- detect duplicate READY generation
- confirm correct single-use readiness behavior
- validate that preview created a new context
- validate that READY context is safe for execution transition

--

Return:

## Latest READY Context
## Previous READY Context (if any)
## Reuse Detected (Yes/No)
## Freshness Judgment

## readiness_state
## failed_checks
## overridden_checks
## freshness_seconds
## Safe to Proceed (Yes/No)

## Blocking Issue (if any)

---

🔷 STEP 8 — Execution Gate Diagnostic（コード証明）

Use the runtime base:

/mnt/c/ai-trading-os-private

Recovery procedure:

1. cd /mnt/c/ai-trading-os-private
2. export PATH=$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0
3. source ./.env.local
4. source scripts/registrar/.venv/bin/activate

Do NOT run collector.
Do NOT run preview.
Do NOT run real_order.
Do NOT execute simulated_order.

Task:

Inspect execution gate implementation using code + DB evidence.

Confirm:

1. ready_context_id is read from metadata
2. context_state is read before execution
3. state != active leads to NO_GO
4. consumed state is written back to metadata
5. execution_blocked is recorded for duplicate attempts

Primary inspection target:

scripts/openclaw/run_simulated_order.py

Objective:

- ensure gate and state storage are aligned
- confirm duplicate execution prevention is implemented

Return:

## Context ID
## State Storage Location
## Gate Read Source
## State Before Execution
## Gate Decision Path
## Consumed Writeback Location
## Consistency Check
## Issue (if any)

---

--from here
Evidence — Execution Gate Implementation

## Context ID
rctx-20260403-0002

## State Storage Location
Observed in the latest `research.trace_event` content string:
`execution_readiness_evaluated symbol=8306 exchange=1 readiness_state=READY reason=READY freshness_seconds=4.452 ready_context_id=rctx-20260403-0002 context_state=active`

## Matching Files
- `scripts/openclaw/run_simulated_order.py`

## Gate Read Source
Code evidence in `scripts/openclaw/run_simulated_order.py` shows both `ready_context_id` and `context_state` are read from **metadata**, not from free-form content.

READY context lookup:
- `fetch_ready_context_state(conn, symbol)`
- query reads latest READY from `research.trace_event.metadata->>'ready_context_id'`
- filter uses `metadata->>'readiness_state' = 'READY'`

Relevant code:
- `SELECT metadata->>'ready_context_id'`
- `AND metadata->>'readiness_state' = 'READY'`
- `AND metadata ? 'ready_context_id'`

Then context state lookup:
- `SELECT metadata->>'context_state'`
- `FROM research.trace_event`
- `WHERE event_type = 'ready_context_state'`
- `AND metadata->>'ready_context_id' = %s`

So before execution:
- `ready_context_id` is read from metadata on `execution_readiness_evaluated`
- `context_state` is read from metadata on `ready_context_state`

## State Before Execution
active

## Gate Decision Path
Direct code evidence:

if context_state != "active":
    if context_state in {"consumed", "invalidated", "expired"}:
        ...
        print(
            f"[simulated_order] NO_GO blocked ready_context_id={ready_context_id} "
            f"reason=duplicate:{context_state}"
        )
        sys.exit(1)

This confirms:
- non-active terminal states trigger block
- blocked path is explicitly labeled `NO_GO`
- duplicate execution prevention is implemented for consumed / invalidated / expired states

## Consumed Writeback Location
Consumed state is written back in:
- `mark_context_consumed(symbol, ready_context_id)`

That function inserts two trace events:

1. `ready_context_state`
   - metadata contains:
     - `"ready_context_id": ready_context_id`
     - `"context_state": "consumed"`

2. `execution_consumed`
   - metadata contains:
     - `"ready_context_id": ready_context_id`
     - `"context_state": "consumed"`

Relevant code evidence:
- `consumed_state_metadata = { ..., "context_state": "consumed", ... }`
- insert into `event_type = "ready_context_state"`
- `execution_consumed_metadata = { ..., "context_state": "consumed", ... }`
- insert into `event_type = "execution_consumed"`

This is written to both content and metadata in each insert.

## execution_blocked Evidence
Direct code evidence in:
- `record_execution_blocked(...)`

It inserts `event_type = "execution_blocked"` with metadata including:
- `"ready_context_id": ready_context_id`
- `"context_state": context_state`
- `"reason": f"duplicate:{context_state}"`

And this is called from the non-active gate branch before `NO_GO`.

## Consistency Check
Verified for the simulated-order execution path:

- READY context lookup uses metadata
- context_state lookup uses metadata
- non-active state leads to NO_GO
- consumed state is written back
- duplicate execution is recorded as execution_blocked

## Issue (if any)
None for the simulated-order gate/storage alignment check.
--to here

---

🔷 STEP 9 — Simulated Order Safety Test

Role / Scope Reset

You are no longer acting as Collector.

Your role is now:

Execution Safety Validator

Your scope is strictly limited to:

- using an existing READY context
- validating one-time execution behavior
- validating duplicate execution blocking
- returning factual outputs only

You do NOT:

- run collector
- run preview
- run real_order
- create a new READY context

--

Use the runtime base:

/mnt/c/ai-trading-os-private

Recovery procedure:

1. cd /mnt/c/ai-trading-os-private
2. export PATH=$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0
3. source ./.env.local
4. source scripts/registrar/.venv/bin/activate

--

Task:

Use the latest active READY context for symbol 8306.

Perform exactly:

1. Execute simulated_order once
2. Immediately execute simulated_order again using the SAME READY context

Constraints:

- use the same ready_context_id
- do not generate a new READY
- do not retry beyond the second attempt
- do not modify inputs between runs

--

Objective:

- confirm first execution succeeds
- confirm second execution is blocked
- confirm duplicate prevention is enforced
- confirm state transition active → consumed
- confirm execution_blocked is recorded

--

Expected behavior:

- first execution:
  success (execution_recorded or equivalent)

- second execution:
  NO_GO blocked
  reason = duplicate:consumed (or equivalent)

--

Return ONLY:

## READY Context ID
## First Execution Result
## Second Execution Result
## execution_blocked Result
## Consumed State Result
## Safety Judgment
## Blocking Issue (if any)

---

🔷 STEP 10 — Real Order Token Dry-Run（最終）

Role / Scope Reset

You are no longer acting as Collector.
You are no longer acting as Execution Safety Validator for simulated_order.

Your role is now:

Real Order Dry-Run Validator

Your scope is strictly limited to:

- validating run_real_order.py in dry-run mode
- allowing broker connectivity only for production token acquisition
- confirming that no sendorder occurs
- returning factual outputs only

You do NOT:

- run collector
- run preview
- run simulated_order
- create a new READY context
- send any external order

--
Use the runtime base:

/mnt/c/ai-trading-os-private

Recovery procedure:

1. cd /mnt/c/ai-trading-os-private
2. export PATH=$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0
3. source ./.env.local
4. source scripts/registrar/.venv/bin/activate

KabuStation is already started.

This time, broker connectivity is allowed only for token acquisition.

Do NOT:
- sendorder
- register symbol
- fetch board
- perform any external order transmission

Task:

Run exactly one bounded validation of:

scripts/openclaw/run_real_order.py

Use the same valid AAB for symbol 8306 as in the previous real_order skeleton tests.

Objective:

- confirm `real_order_dry_run` executes in token acquisition mode
- confirm whether token acquisition succeeds against:
  - host = KABU_API_HOST
  - port = 18080
- confirm `dry_run_status = passed` or `failed`
- confirm no sendorder occurs
- confirm the script still stops at NO_GO

Constraints:

- exactly one dry-run execution
- no retries
- no new AAB creation
- no new READY generation
- no external order transmission

Return output in this format:

## Pre-Execution Declaration
## AAB Validation Result
## READY Context Validation Result
## Dry Run Result
## Token Acquisition Result
## Skeleton Stop Result
## Broker Touch Check
## Final Judgment
## Blocking Issue (if any)

---

🔶 FLIGHT COMPLETE 🔶

Collector → Preview → READY → Gate → Execution Safety → Broker Boundary

---

Final interpretation:

- Execution safety path verified
- Broker path reachable (token only)
- No unintended order transmission

---