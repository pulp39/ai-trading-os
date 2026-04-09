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

🔷 ATOS Runtime & OpenClaw Integration — Lessons Learned（2026-04）
概要

本セッションにより、ATOSの観測〜Previewに至る実行経路において、
OpenClawのone-command制約と多段runtime環境の不整合問題が特定され、
その解決パターンが確立された。

🔷 1. One-Command Constraint は「仕様」である
事実

OpenClaw は

コマンドを分割実行しない
shell状態を保持しない
各Taskが独立実行される

このため、

source .env.local
export PATH
venv activate

は前提として保持されない

結論

👉 すべての実行は1コマンド内で自己完結させる必要がある

🔷 2. Runtime Normalization Pattern の確立
必須構成（テンプレ）
bash -lc '
cd /mnt/c/ai-trading-os-private &&
export PATH="$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0" &&
source ./.env.local &&
/mnt/c/.../.venv/bin/python ...
'
意味
cd → runtime base 固定
PATH → PowerShell 解決
.env.local → secret 注入
絶対パス python → interpreter 固定
結論

👉 これが OpenClaw 実行の最小単位

🔷 3. 「分割手順」は OpenClaw では壊れる
症状
STEP 2 分割版 → PowerShell 未解決
token check → wrapper failure
Task間で PATH が消失
原因

OpenClaw が 同一shellを維持しない

結論

👉 分割手順は人間用、OpenClawには不適合

🔷 4. Absolute Path 原則
問題
python: command not found
PowerShell 呼び出し失敗
解決
/mnt/c/.../.venv/bin/python
結論

👉 すべての実行バイナリは絶対パス指定

🔷 5. Environment Injection は shell 内で行う
問題
KABU_API_PASSWORD is missing
env が引き継がれない
解決
source ./.env.local

を同一コマンド内で実行

禁止事項
prompt に secret を書く
結論

👉 env は shell 内で注入、外部注入は禁止

🔷 6. PowerShell PATH 問題の本質
症状
powershell.exe not found
Taskごとに消える
原因

PATH がコマンド間で保持されない

解決
export PATH="$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0"
結論

👉 PowerShell は毎回 PATH 追加が必要

🔷 7. Registration ≠ Execution Readiness
観測結果
Step 4 → 登録成功
KabuStation → 登録確認済
しかし Step 6 → 8306 だけ FAIL
結論

👉 登録状態とAPI実行成功は別問題

🔷 8. Batch Execution は不安定化要因
観測結果
7203 / 6758 → SUCCESS
8306 → FAIL
Step5単独 → SUCCESS
結論

👉 バッチより単発実行の方が安定

🔷 9. Freshness は最大のボトルネック
事実
freshness_limit_ms = 30000
問題
Step5 → Step7 の間で失敗
preview が STOP
解決

👉 Step5→7 連結実行

🔷 10. Heredoc は OpenClaw で壊れる
症状
<<EOF ... EOF && ...

→ bash syntax error

解決
printf "%s\n" "{json}"
結論

👉 heredoc禁止、printf使用

🔷 11. STOP は「失敗」ではない
観測結果
Preview SUCCESS
readiness = NOT_READY
理由
market_closed
snapshot_stale
結論

👉 STOP = 正常な制度動作

🔷 12. Preview Path は完全に確立

今回確認済み：

collector → SUCCESS
snapshot → SUCCESS
trace_event → SUCCESS
preview → SUCCESS
execution_readiness_evaluated → SUCCESS
readiness → 正常判定
結論

👉 Preview Pipeline 完全動作確認済

🔷 13. 5→7 連結版の位置付け
状態
動作成功
freshness回避成功
役割

👉 診断・高速検証用

非推奨
常用手順としては使わない
🔷 14. 最終構造（確定）
STEP 0–4 → 環境・境界確認
STEP 5   → 観測（単発）
STEP 6   → 観測（複数・検証用）
STEP 7   → Preview（READY生成）
🔷 15. 本セッションの最重要成果
Before
OpenClaw execution 不安定
collector 動作不定
Preview 到達不可
After
one-command runtime pattern 確立
collector 安定化
preview path 完全到達
readiness 判定動作確認
🔶 総括

今回の本質はこれです。

👉 「実装の問題」ではなく「実行モデルの不一致」だった

そしてその解決は、

👉 すべてを1コマンドに閉じ込める設計への転換

でした。

---

🔷 STEP 0 — Collector Initialization
Role

You are participating in the AI Trading OS (ATOS) environment.

This session initializes you as a Collector.

Scope

You are strictly limited to:

runtime recovery
boundary validation
port ownership / portproxy safety validation
bounded market observation
returning factual outputs only
Forbidden

You do NOT:

run preview
evaluate readiness
execute simulated_order
execute real_order
send orders
Core Rules

Observation only
You may only collect data.

Stop discipline

STOP immediately if:

runtime base is wrong
env is unclear
PowerShell unavailable
boundary incomplete
port ownership unsafe
portproxy conflict detected
execution scope is unclear

When STOP is triggered, you MUST state:

which condition failed
why it is unsafe
Start Condition

If ready, respond:

COLLECTOR_READY

---

🔷 STEP 1 — Runtime / Environment Preflight
Objective

Validate runtime normalization only.

NOTE:
Port ownership and token reachability are handled in STEP 2.

Execution
bash -lc 'cd /mnt/c/ai-trading-os-private && export PATH="$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0" && source ./.env.local && source scripts/registrar/.venv/bin/activate && printf "PWD=%s\n" "$PWD" && printf "PYTHON=%s\n" "$(which python)" && printf "POWERSHELL=%s\n" "$(which powershell.exe)" && printf "KABU_API_HOST=%s\n" "$KABU_API_HOST" && printf "KABU_API_PORT=%s\n" "$KABU_API_PORT"'
Return Format
Runtime Base
...

Python Path
...

PowerShell Path
...

WSL Env
KABU_API_HOST=...
KABU_API_PORT=...

Judgment
PASS or STOP

Issue (if any)
...
Judgment Rule

PASS only if:

runtime base correct
python resolves in venv
powershell.exe resolves
env variables visible

---

🔷 STEP 2 — Port Ownership + Reachability Preflight（FINAL LOCKED）
Objective

Ensure port 18080 is:

not hijacked by portproxy
actively listening
actually serving kabuStation API
Execution
bash -lc 'cd /mnt/c/ai-trading-os-private && export PATH="$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0" && source ./.env.local && source scripts/registrar/.venv/bin/activate && powershell.exe -NoProfile -Command "
netsh interface portproxy show all;
Write-Output \"---LISTENER---\";
Get-NetTCPConnection -LocalPort 18080 -State Listen | Select-Object LocalAddress,LocalPort,OwningProcess;
Write-Output \"---PROCESS---\";
Get-Process -Id 4 | Select-Object Id,ProcessName,Path;
Write-Output \"---TOKEN---\";
\$apiHost = [string]\"localhost\";
\$apiPort = [string]\"18080\";
\$apiPassword = [string]\"$KABU_API_PASSWORD\";
\$body = @{ APIPassword = \$apiPassword } | ConvertTo-Json -Compress;
try {
  \$resp = Invoke-RestMethod -Uri (\"http://\" + \$apiHost + \":\" + \$apiPort + \"/kabusapi/token\") -Method Post -ContentType \"application/json\" -Body \$body;
  \$resp | ConvertTo-Json -Compress;
} catch {
  Write-Output (\"TOKEN_ERROR=\" + \$_.Exception.Message);
}
"'
Return Format
Portproxy Rules
...

Port 18080 Listener
...

Listener Process
...

Token Reachability
...

Ownership Judgment
PASS or STOP

Issue (if any)
...
Judgment Rule
portproxy contains 18080 → STOP
listener missing → STOP
token fails → STOP
token ResultCode=0 → PASS
Critical Rules
PID 4 (System) is allowed
token success overrides ambiguity

---

🔷 STEP 3 — Symbol Registration
Execution
bash -lc 'cd /mnt/c/ai-trading-os-private && export PATH="$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0" && source ./.env.local && /mnt/c/ai-trading-os-private/scripts/registrar/.venv/bin/python /mnt/c/ai-trading-os-private/scripts/collector/register_symbol_once_8306_tmp.py'
PASS Condition
RegistList contains 8306

---

🔷 STEP 4 — Collector One Shot
Execution
bash -lc 'cd /mnt/c/ai-trading-os-private && export PATH="$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0" && source ./.env.local && export SKIP_KABU_REGISTRATION=1 && /mnt/c/ai-trading-os-private/scripts/registrar/.venv/bin/python /mnt/c/ai-trading-os-private/scripts/collector/collect_board_once.py 8306'
PASS Condition
board fetch success
snapshot success
trace_event success

---

🔷 STEP 5 — Sequential Batch Observation（REWRITE / FINAL）
Objective

Execute bounded one-shot observations for multiple symbols
under strict sequential execution after successful collector validation.

Background
STEP 4 confirmed collector one-shot execution is stable
manual sequential execution across multiple symbols is stable
instability observed only in OpenClaw batch context
therefore, execution ordering must be explicitly controlled
🔷 Core Rule（CRITICAL）
All symbol executions MUST be strictly sequential.

No overlap is allowed.
No parallel execution is allowed.
No queued execution is allowed.
🔷 Execution Order（MANDATORY）

7203
wait until process fully exits
8306
wait until process fully exits
6758
wait until process fully exits
🔷 Common Execution Template
bash -lc 'cd /mnt/c/ai-trading-os-private && export PATH="$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0" && source ./.env.local && export SKIP_KABU_REGISTRATION=1 && /mnt/c/ai-trading-os-private/scripts/registrar/.venv/bin/python /mnt/c/ai-trading-os-private/scripts/collector/collect_board_once.py SYMBOL'
🔷 Execution Rules（MANDATORY）
Each symbol execution must:

run exactly one command
include runtime normalization
use .env.local
use venv python (absolute path)
bypass registration (SKIP_KABU_REGISTRATION=1)
complete before next symbol starts
🔷 Output Discipline（STRICT）

You MUST return ALL sections for each symbol.

Do NOT summarize.

🔷 Required Return Format
-- SYMBOL --

Execution Order Position
1 / 2 / 3

Process Exit Confirmation
Process fully exited before next symbol started

Observation Result
...

Snapshot Result
...

Trace Result
...

Issue (if any)
...
🔷 Judgment Rule（PER SYMBOL）

PASS if:

Observation success
Snapshot success
Trace success

Otherwise:

→ STOP

🔷 Global Judgment Rule
ALL symbols must PASS

If any symbol fails → STOP

🔷 Interpretation Note
This step validates collector stability under sequential multi-symbol execution.

This is NOT:

market correctness validation
trading validation

This IS:

pipeline integrity validation
execution isolation validation

---

🔷 STEP 6 — Role Reset（CRITICAL FIX）

You are no longer Collector.

New Role

Preview Validator

Allowed
one fresh observation (8306 only)
one preview execution
one readiness evaluation
Forbidden
simulated_order
real_order
external orders

---

🔷 STEP 7 — Preview Path（FRESHNESS FIX VERSION / JSON FIXED / FINAL）
Objective

Generate exactly one preview result and one execution_readiness_evaluated event
using a temporary preview-only AAB under one-command execution constraints.

This step validates:

preview execution path
execution_readiness_evaluated generation
readiness result production
correct STOP behavior when live readiness conditions are not satisfied

This step does not execute any order.

Preconditions (MANDATORY)

This step may proceed only if ALL are true:

STEP 1 passed
STEP 2 passed
STEP 3 passed
STEP 4 passed
STEP 5 passed
STEP 6 role reset acknowledged

If any precondition is missing:
→ STOP

Freshness Rule (MANDATORY)

freshness_limit_ms = 30000

Preview may proceed only if:

observation freshness ≤ 30000 ms
market state is acceptable to the preview implementation
no override is used for live READY generation

If freshness fails:
→ STOP

Operational Fix

collector + preview must run in one command.

Temporary preview AAB JSON must be generated in a way that is shell-safe
and parse-safe.

Do NOT use inline broken JSON quoting.

Approved Execution Method (MANDATORY)

Run exactly one command only:

bash -lc 'cd /mnt/c/ai-trading-os-private && export PATH="$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0" && source ./.env.local && export SKIP_KABU_REGISTRATION=1 && /mnt/c/ai-trading-os-private/scripts/registrar/.venv/bin/python /mnt/c/ai-trading-os-private/scripts/collector/collect_board_once.py 8306 && /mnt/c/ai-trading-os-private/scripts/registrar/.venv/bin/python -c "import json; p=\"/tmp/atos_order_preview_8306.json\"; data={\"aab_id\":\"AAB-PREVIEW-8306-TEMP\",\"execution_scope\":{\"action_type\":\"order_preview\",\"symbol\":\"8306\",\"order_type\":\"market\",\"side\":\"buy\",\"quantity\":1},\"constraints\":{\"dry_run\":True,\"external_order_allowed\":False,\"preview_only\":True,\"state_change_allowed\":False,\"test_override_allowed\":False},\"capital_allocation\":{\"constraint_type\":\"preview_only\"}}; open(p,\"w\",encoding=\"utf-8\").write(json.dumps(data, ensure_ascii=False))" && /mnt/c/ai-trading-os-private/scripts/registrar/.venv/bin/python -m scripts.openclaw.run_order_preview /tmp/atos_order_preview_8306.json'
Constraints
exactly one command
exactly one fresh observation for 8306
exactly one preview execution
no retry
no simulated_order
no real_order
no external order transmission
Required Return Format
Input Contract

...

Correct Invocation

...

Preview Result

...

execution_readiness_evaluated Result

...

READY Context Result

...

Blocking Issue (if any)

...

Interpretation Rule
If preview executes and execution_readiness_evaluated is generated:
Step 7 is operationally successful
readiness result may still be READY, NOT_READY, REPRICE_REQUIRED, or DATA_INVALID
If preview stops because live conditions are not satisfied:
this is a normal STOP
not an execution failure
If preview input JSON cannot be parsed:
this is an input construction failure
no preview result or readiness evaluation may be trusted
Safety Meaning

This step is for:

preview-path validation
live readiness generation validation
STOP behavior validation

This step is not for:

simulated execution
real execution
external order transmission

---

🔷 STEP 8 — READY Validation Chain

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

🔷 STEP 9 — Execution Gate Diagnostic（コード証明）

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

🔷 STEP 10 — Simulated Order Safety Test（RUNTIME-SAFE / AAB-FIXED / FINAL）
Role / Scope Reset

You are no longer acting as Collector.

Your role is now:

Execution Safety Validator

Your scope is strictly limited to:

using an existing READY context
validating one-time execution behavior
validating duplicate execution blocking
returning factual outputs only

You do NOT:

run collector
run preview
run real_order
create a new READY context
Use the runtime base

/mnt/c/ai-trading-os-private

Recovery procedure
cd /mnt/c/ai-trading-os-private
export PATH=$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0
source ./.env.local
source scripts/registrar/.venv/bin/activate
Preconditions (MANDATORY)

This step may proceed only if ALL are true:

STEP 7 created a READY context
STEP 8 confirmed the latest READY context is fresh and active
STEP 9 confirmed gate/storage alignment
no new collector run has occurred after the validated READY
no new preview run has occurred after the validated READY

If any precondition is missing:
→ STOP

READY Context to Use

Use the latest active READY context for symbol 8306.

Expected current context:

ready_context_id = rctx-20260409-0001

Do NOT generate a new READY.
Do NOT modify the input between runs.

Objective

Perform exactly:

execute simulated_order once
immediately execute simulated_order again using the same READY context

This step validates:

first execution succeeds
second execution is blocked
state transition active → consumed
execution_blocked is recorded
Runtime Safety Fix

Because the runtime rejected complex interpreter invocation, this step must use:

direct file execution only
no python -c
no chained interpreter wrappers
no inline dynamic Python construction

Use direct python <file>.py ... form only.

Phase 1 — First Execution
Command (MANDATORY)

Run exactly this command:

bash -lc 'cd /mnt/c/ai-trading-os-private && export PATH="$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0" && source ./.env.local && source scripts/registrar/.venv/bin/activate && printf "%s\n" "{\"aab_id\":\"AAB-SIMULATED-8306-TEMP\",\"execution_scope\":{\"action_type\":\"simulated_order\",\"symbol\":\"8306\",\"order_type\":\"market\",\"side\":\"buy\",\"quantity\":1,\"market_hours_only\":true},\"constraints\":{\"dry_run\":true,\"external_order_allowed\":false},\"capital_allocation\":{\"constraint_type\":\"simulated_only\"}}" > /tmp/atos_simulated_order_8306.json && /mnt/c/ai-trading-os-private/scripts/registrar/.venv/bin/python /mnt/c/ai-trading-os-private/scripts/openclaw/run_simulated_order.py /tmp/atos_simulated_order_8306.json'
PASS expectation

The first execution should:

use the existing latest active READY context
succeed as simulated execution
record execution event(s)
consume the context

If the first execution fails before reaching the gate:
→ STOP

Phase 2 — Duplicate Execution Attempt
Command (MANDATORY)

Run exactly the same simulated_order again using the same file, unchanged:

bash -lc 'cd /mnt/c/ai-trading-os-private && export PATH="$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0" && source ./.env.local && source scripts/registrar/.venv/bin/activate && /mnt/c/ai-trading-os-private/scripts/registrar/.venv/bin/python /mnt/c/ai-trading-os-private/scripts/openclaw/run_simulated_order.py /tmp/atos_simulated_order_8306.json'
PASS expectation

The second execution should:

detect the same READY context is no longer active
block with NO_GO
indicate duplicate:consumed or equivalent
record execution_blocked

If the second execution unexpectedly succeeds:
→ STOP

Phase 3 — DB Confirmation

After the two executions above, inspect the DB evidence.

What must be confirmed

For the same ready_context_id:

first execution produced execution success record
ready_context_state became consumed
execution_consumed exists
second execution produced execution_blocked
blocking reason is duplicate:consumed or equivalent
Return ONLY
READY Context ID

...

First Execution Result

...

Second Execution Result

...

execution_blocked Result

...

Consumed State Result

...

Safety Judgment

...

Blocking Issue (if any)

...

Judgment Rule

PASS only if ALL are true:

first execution succeeded
second execution was blocked
consumed state was recorded
execution_blocked was recorded
no new READY context was created during this test

Otherwise:
→ STOP

Interpretation Note

This step validates execution safety behavior, not market correctness.

This is NOT:

collector validation
preview validation
real order validation

This IS:

single-use READY enforcement
duplicate execution prevention
gate / state-transition validation
Critical Rule

The same input must be reused for both runs.

Do NOT:

regenerate AAB before second run
regenerate READY
change symbol
change quantity
change file path
introduce any new preview step
Expected Final Meaning

If this step passes:

1 READY context = 1 execution
duplicate execution is blocked
consumption model is operational
Execution Safety Layer is validated in live runtime conditions

---

🔷 STEP 11 — Real Order Token Dry-Run（RUNTIME-SAFE / AAB-FIXED / FINAL）
Role / Scope Reset

You are no longer acting as Collector.
You are no longer acting as Execution Safety Validator for simulated_order.

Your role is now:

Real Order Dry-Run Validator

Your scope is strictly limited to:

validating run_real_order.py in dry-run skeleton mode
allowing broker connectivity only for production token acquisition
confirming that no sendorder occurs
returning factual outputs only

You do NOT:

run collector
run preview
run simulated_order
create a new READY context
send any external order
Use the runtime base

/mnt/c/ai-trading-os-private

Recovery procedure
cd /mnt/c/ai-trading-os-private
export PATH=$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0
source ./.env.local
source scripts/registrar/.venv/bin/activate

KabuStation is already started.

This time, broker connectivity is allowed only for token acquisition.

Do NOT:

sendorder
register symbol
fetch board
perform any external order transmission
Preconditions (MANDATORY)

This step may proceed only if ALL are true:

production path validation is intended
port 18080 was previously validated as reachable
KabuStation is running
required production env exists
no order transmission is intended
a fresh READY context for symbol 8306 exists and is active

If any precondition is missing:
→ STOP

Objective

Run exactly one bounded validation of:

scripts/openclaw/run_real_order.py

Validate:

real_order_dry_run executes in token acquisition mode
token acquisition succeeds against:
host = KABU_API_HOST
port = 18080
dry_run_status = passed or failed
no sendorder occurs
the script still stops at NO_GO
Runtime Safety Fix

Because prior attempts failed due to incompatible input artifacts, this step must:

use direct file execution only
use a shell-safe temporary AAB created at runtime
avoid python -c
avoid heredoc
avoid reusing incompatible legacy AAB files

Use direct python <file>.py <aab_path> form only.

Phase 1 — One Dry-Run Execution
Command (MANDATORY)

Run exactly this command:

bash -lc 'cd /mnt/c/ai-trading-os-private && export PATH="$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0" && source ./.env.local && source scripts/registrar/.venv/bin/activate && printf "%s\n" "{\"aab_id\":\"AAB-REALORDER-8306-TEMP\",\"execution_scope\":{\"action_type\":\"real_order\",\"symbol\":\"8306\",\"side\":\"buy\",\"quantity\":1,\"market_hours_only\":true},\"constraints\":{\"retry\":false,\"dry_run\":false,\"external_order_allowed\":true},\"capital_allocation\":{\"constraint_type\":\"real_order_skeleton\"}}" > /tmp/atos_real_order_8306.json && /mnt/c/ai-trading-os-private/scripts/registrar/.venv/bin/python /mnt/c/ai-trading-os-private/scripts/openclaw/run_real_order.py /tmp/atos_real_order_8306.json'
Expected Behavior

The script should:

print the production execution declaration
load and validate the AAB
validate that the latest READY context for 8306 is active
attempt token acquisition only
print dry-run result
stop at NO_GO
confirm sendorder is not implemented yet
PASS / STOP Interpretation
PASS path

PASS if all are true:

AAB validation succeeds
READY context validation succeeds
token acquisition is attempted
dry_run_status = passed
no sendorder occurs
final stop is the expected skeleton NO_GO
STOP path

STOP if any of the following occurs:

AAB validation fails
READY context is missing or not active
token acquisition fails
script attempts any external order transmission
output is inconsistent with skeleton dry-run semantics
Return output in this format
Pre-Execution Declaration

...

AAB Validation Result

...

READY Context Validation Result

...

Dry Run Result

...

Token Acquisition Result

...

Skeleton Stop Result

...

Broker Touch Check

...

Final Judgment

...

Blocking Issue (if any)

...

Judgment Rule

PASS only if ALL are true:

broker_mode = production
broker_touch = True
external_order_allowed = True
kabu_port = 18080
password_source = KABU_API_PASSWORD
AAB is accepted by run_real_order.py
latest READY context is active
token acquisition succeeds
no sendorder occurs
script ends in expected skeleton NO_GO

Otherwise:
→ STOP

Critical Safety Meaning

This step validates:

production-path declaration
broker reachability through token acquisition
real_order skeleton discipline
no unintended external transmission

This step does NOT validate:

order acceptance
broker execution
sendorder behavior
capital deployment
Expected Final Meaning

If this step passes:

Production real_order path is reachable at token level
AAB contract matches run_real_order.py
READY context can be validated for real_order transition
No unintended order transmission occurs
Skeleton NO_GO behavior is intact

---

🔷 STEP 12 — Restart Recovery Protocol（REVISED FINAL）

When kabuStation restart is detected:

MANDATORY SEQUENCE:

1. Boundary Validation
2. Token Success
3. Symbol List State Check
4. Conditional Re-registration
5. Collector Execution

Rules:

- sequence order is fixed
- no skipping allowed
- symbol check is mandatory

---

■ Step 3 — Symbol List State Check（UPDATED）

Symbol list MUST be inspected using:

PUT /kabusapi/register

Procedure:

- send payload with target symbol(s)
- inspect returned RegistList
- treat RegistList as the current registered symbol state

---

■ Step 4 — Conditional Re-registration（UPDATED）

Decision rule:

if required symbol exists in RegistList:
    do nothing

if required symbol missing:
    perform registration

---

■ Definition of STEP12-ready（UPDATED）

STEP12-ready means ALL of the following:

- Boundary Validation PASS
- Token acquisition PASS
- RegistList successfully retrieved
- Required symbol(s) present
- Re-registration not required (or possible)
- Collector execution can proceed safely

---

🔶 FLIGHT COMPLETE 🔶

Collector → Preview → READY → Gate → Execution Safety → Broker Boundary

Final interpretation:

Execution safety path verified  
Broker path reachable (token only)  
No unintended order transmission  
Restart recovery path verified

---

🔷 Step12-ready 確認プロンプト（完成版）

You are in ATOS.

Do NOT run collector, preview, simulated_order, real_order, or sendorder.

Your task is to determine whether the current runtime is STEP12-ready.

STEP12-ready requires ALL of the following:

1. Boundary Validation is correct
2. Production token acquisition on port 18080 succeeds
3. Symbol List State can be verified
4. Required symbols (e.g., 8306) are confirmed registered
5. Conditional re-registration is not required (or possible if needed)
6. Collector Execution can safely proceed

Rules:
- fixed sequence must be respected
- no skipping allowed
- symbol check is mandatory
- if any condition is unknown, answer No
- return factual outputs only

IMPORTANT:
Symbol List State Check MUST use:
PUT /kabusapi/register and inspect RegistList

Return ONLY:

## STEP12-ready
Yes / No

## Boundary Validation
PASS / FAIL / UNKNOWN

## Token Success
PASS / FAIL / UNKNOWN

## Symbol List State Check
PASS / FAIL / UNKNOWN

## Required Symbol Present (8306)
Yes / No / Unknown

## Conditional Re-registration Needed
Yes / No / Unknown

## Collector Execution Readiness
PASS / FAIL / UNKNOWN

## Missing Condition(s)
...

## Safe Next Action
...

---
