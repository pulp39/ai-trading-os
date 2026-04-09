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

🔷 STEP 1 — Boundary Validation（CORRECTED）

## Purpose
Ensure env parity between WSL and PowerShell.

## Notes
- This is a Phase B runner-validation command, not the final PowerShell parity validation.
- It exists to confirm Task Artifact → Runner → Result Artifact completion.

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

Perform exactly one PowerShell call using explicit in-command assignment.

Important correction:
Because this command is launched from bash/WSL, PowerShell local variables must escape $ as \$ so bash does not consume them before PowerShell runs.

Use exactly this command shape:

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
prevent bash from consuming PowerShell variable names before execution
Return output in this format:

WSL Env
PowerShell Used Values
Match Result
Boundary Integrity
Issue (if any)

Judgment rule:

all values match exactly → proceed to STEP 2
any mismatch or parser failure → STOP

---

Run exactly one command only.

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

Return EXACTLY:
- Portproxy Rules
- Port 18080 Listener
- Listener Process
- Token Reachability
- Ownership Judgment
- Issue (if any)

A one-word reply is invalid.

---

🔷 STEP 3 — Production Token Attempt（FINAL LOCKED VERSION）

Objective:
Perform exactly one production token attempt against the kabuStation API on port 18080.

Use the runtime base:

/mnt/c/ai-trading-os-private
🔷 Recovery (MANDATORY)
cd /mnt/c/ai-trading-os-private
export PATH="$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0"
source ./.env.local
source scripts/registrar/.venv/bin/activate
which powershell.exe
STOP condition:
if powershell.exe is not resolved → STOP
🔷 Output Discipline (STRICT)

You MUST return ALL sections below.

Do NOT return:

YES / NO
PASS / FAIL only
partial output

A one-word reply is INVALID and must be treated as STOP.

🔷 Additional Rule (MANDATORY)

If TOKEN_FAIL occurs and APILog shows no record of the attempt:

treat this as transport failure
NOT authentication failure
do NOT retry
do NOT modify password

Return the diagnostic result and STOP.

🔷 Task — Exactly One Production Token Attempt

Important correction:

Because this command is launched from bash/WSL, all PowerShell local variables must escape $ as \$, including $_ inside catch.

Execute exactly once:

powershell.exe -NoProfile -Command "
\$ErrorActionPreference = 'Stop';
\$psHost = [string]'$KABU_API_HOST';
\$psPort = [string]'18080';
\$psPassword = [string]'$KABU_API_PASSWORD';

\$body = @{ APIPassword = \$psPassword } | ConvertTo-Json -Compress;
\$uri = 'http://' + \$psHost + ':' + \$psPort + '/kabusapi/token';

try {
  \$res = Invoke-RestMethod -Method Post -Uri \$uri -Body \$body -ContentType 'application/json';
  Write-Output 'TOKEN_SUCCESS';
  Write-Output (\$res | ConvertTo-Json -Compress);
} catch {
  Write-Output 'TOKEN_FAIL';
  Write-Output \$_.Exception.Message;
}
"
🔷 Judgment Rule (STRICT)
if output contains TOKEN_SUCCESS → PASS
if output contains TOKEN_FAIL → STOP
no retry allowed
🔷 Required Return Format (MANDATORY)

You MUST return EXACTLY this structure:

Production Token Attempt
...

Token Result
TOKEN_SUCCESS or TOKEN_FAIL

Token Response
...

Judgment
PASS or STOP

Issue (if any)
...
🔷 Valid PASS Example
Production Token Attempt
Executed exactly once against http://localhost:18080/kabusapi/token

Token Result
TOKEN_SUCCESS

Token Response
{"ResultCode":0,"Token":"..."}

Judgment
PASS

Issue (if any)
None
🔷 Valid STOP Example
Production Token Attempt
Executed exactly once against http://localhost:18080/kabusapi/token

Token Result
TOKEN_FAIL

Token Response
The underlying connection was closed: ...

Judgment
STOP

Issue (if any)
Token attempt failed
🔷 Invalid Response Examples (REJECT)
NO
PASS
OK

→ MUST be treated as STOP (invalid output)

🔷 Interpretation Note

This step is a single bounded confirmation of the production token path.
Do not expand scope into:

symbol registration
board fetch
preview
simulated_order
real_order

Only the token path is in scope here.

🔶 END OF STEP 3 (FINAL LOCKED)

---

🔷 STEP 4 — Symbol Registration State Handling（OPENCLAW COMPLETE VERSION / FINAL）

Objective:
Handle symbol registration state safely after kabuStation restart.

Background:

kabuStation symbol list is not persistent across restart
exact production symbol-state inspection method is not yet implemented
therefore, after confirmed restart, symbol state must be treated as operationally unknown
recovery registration must be executed exactly once
OpenClaw execution must remain one-command only

Target symbol:

8306

Runtime base:

/mnt/c/ai-trading-os-private
🔷 Preconditions (MANDATORY)

This step may proceed only if ALL are true:

kabuStation restart has been confirmed
STEP 3 token attempt already passed
target symbol is 8306

If any precondition is missing:
→ STOP

🔷 Output Discipline (STRICT)

You MUST return ALL sections below.

Do NOT return:

YES / NO
PASS / FAIL only
partial output

A one-word reply is INVALID and must be treated as STOP.

🔷 Operational Rule

Because exact production symbol-state inspection is not yet available, use this provisional rule:

after confirmed restart, symbol state = UNKNOWN
UNKNOWN state must NOT proceed directly to collector
instead, perform exactly one conditional recovery registration
no retry allowed
🔷 Approved Execution Method (MANDATORY)

Do NOT construct an ad-hoc PowerShell registration call.

Do NOT use plain python.

Do NOT rely on previously sourced shell state.

Run exactly one command only:

bash -lc 'cd /mnt/c/ai-trading-os-private && export PATH="$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0" && source ./.env.local && /mnt/c/ai-trading-os-private/scripts/registrar/.venv/bin/python /mnt/c/ai-trading-os-private/scripts/collector/register_symbol_once_8306_tmp.py'

Constraints:

exactly one command
no retry
no scope expansion
no board fetch
no collector execution
no preview
no simulated_order
no real_order
🔷 Judgment Rule (STRICT)
if registration output shows successful completion and includes RegistList for symbol 8306 → PASS
otherwise → STOP
no retry allowed
🔷 Required Return Format (MANDATORY)

You MUST return EXACTLY this structure:

Restart Confirmed
Yes or No

Token Precondition
Satisfied or Not satisfied

Symbol State
UNKNOWN

Registration Attempt
...

Registration Result
SUCCESS or STOP

Registration Response
...

Judgment
PASS or STOP

Issue (if any)
...
🔷 Valid PASS Example
Restart Confirmed
Yes

Token Precondition
Satisfied

Symbol State
UNKNOWN

Registration Attempt
Executed exactly one command: bash -lc 'cd /mnt/c/ai-trading-os-private && export PATH="$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0" && source ./.env.local && /mnt/c/ai-trading-os-private/scripts/registrar/.venv/bin/python /mnt/c/ai-trading-os-private/scripts/collector/register_symbol_once_8306_tmp.py'

Registration Result
SUCCESS

Registration Response
Registering symbols via Windows PowerShell...
{
  "symbols": [
    {
      "symbol": "8306",
      "exchange": 1
    }
  ],
  "count": 1,
  "kabu_port": 18080
}
Registration completed.
{
  "RegisterResult": {
    "RegistList": [
      {
        "Symbol": "8306",
        "Exchange": 1
      }
    ]
  },
  "TokenAcquired": true,
  "SymbolCount": 1
}

Judgment
PASS

Issue (if any)
None
🔷 Valid STOP Example
Restart Confirmed
Yes

Token Precondition
Satisfied

Symbol State
UNKNOWN

Registration Attempt
Executed exactly one command: ...

Registration Result
STOP

Registration Response
ERROR: ...

Judgment
STOP

Issue (if any)
Conditional recovery registration failed
🔷 Invalid Response Examples (REJECT)
NO
PASS
OK

→ MUST be treated as STOP (invalid output)

🔷 Interpretation Note

This step is provisional state recovery, not normal symbol-state inspection.

The key requirement is:

after restart
before collector
perform one successful recovery registration for 8306

This step must rely on the known-good script path plus one-command runtime normalization, not on improvised request-shape reconstruction.

🔶 END OF STEP 4 (OPENCLAW COMPLETE VERSION / FINAL)

---

🔷 STEP 5 — Collector One Shot（OPENCLAW COMPLETE VERSION / FINAL）

Objective:
Execute exactly one bounded collector observation for symbol 8306 after successful restart recovery and successful conditional recovery registration.

Background:

direct one-command execution without runtime normalization caused repeated failures in prior attempts
collector execution requires:
runtime base
PowerShell PATH
.env.local
registrar venv
registration bypass after successful registration recovery
therefore STEP 5 must use one-command runtime normalization

Target symbol:

8306

Runtime base:

/mnt/c/ai-trading-os-private
🔷 Preconditions (MANDATORY)

This step may proceed only if ALL are true:

STEP 1 passed
STEP 2 passed
STEP 3 passed
STEP 4 passed
symbol 8306 registration recovery has succeeded in the current restart cycle

If any precondition is missing:
→ STOP

🔷 Command Classification Declaration
command_class = bounded WRITE
broker_mode = production
broker_touch = true
external_order_allowed = false
dry_run = true

Meaning:

broker access is allowed only for bounded collector behavior
no external order transmission is allowed
no preview
no simulated_order
no real_order
🔷 Output Discipline (STRICT)

You MUST return ALL sections below.

Do NOT return:

YES / NO
PASS / FAIL only
partial output

A one-word reply is INVALID and must be treated as STOP.

🔷 Approved Execution Method (MANDATORY)

Do NOT use plain python.

Do NOT rely on previously sourced shell state.

Do NOT perform symbol registration inside this step.

Because STEP 4 already completed registration recovery, this step must bypass registration and execute the collector exactly once.

Run exactly one command only:

bash -lc 'cd /mnt/c/ai-trading-os-private && export PATH="$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0" && source ./.env.local && export SKIP_KABU_REGISTRATION=1 && /mnt/c/ai-trading-os-private/scripts/registrar/.venv/bin/python /mnt/c/ai-trading-os-private/scripts/collector/collect_board_once.py 8306'

Constraints:

exactly one command
exactly one observation
no retry
no scope expansion
no preview
no simulated_order
no real_order
no sendorder
no repository lookup during execution
🔷 Judgment Rule (STRICT)
if board fetch succeeds and collector completes bounded one-shot execution → PASS
if snapshot write and trace path complete → PASS
otherwise → STOP
no retry allowed
🔷 Required Return Format (MANDATORY)

You MUST return EXACTLY this structure:

Command Classification
...

Observation Attempt
...

Observation Result
...

Snapshot Result
...

Trace Result
...

Judgment
PASS or STOP

Issue (if any)
...
🔷 Valid PASS Example
Command Classification
command_class = bounded WRITE
broker_mode = production
broker_touch = true
external_order_allowed = false
dry_run = true

Observation Attempt
Executed exactly one command for symbol 8306 with registration bypass enabled

Observation Result
Board fetch succeeded for 8306

Snapshot Result
Snapshot write succeeded

Trace Result
trace_event write succeeded

Judgment
PASS

Issue (if any)
None
🔷 Valid STOP Example
Command Classification
command_class = bounded WRITE
broker_mode = production
broker_touch = true
external_order_allowed = false
dry_run = true

Observation Attempt
Executed exactly one command for symbol 8306 with registration bypass enabled

Observation Result
Board fetch failed

Snapshot Result
Not completed

Trace Result
Not completed

Judgment
STOP

Issue (if any)
Collector one-shot failed before bounded write path completed
🔷 Invalid Response Examples (REJECT)
NO
PASS
OK

→ MUST be treated as STOP (invalid output)

🔷 Interpretation Note

This step is collector-only.

It does NOT:

evaluate readiness
run preview
create READY
run simulated_order
run real_order

This step exists only to confirm that the collector one-shot path can execute safely under OpenClaw’s one-command constraints, using runtime normalization and registration bypass after successful STEP 4 recovery.

🔶 END OF STEP 5 (OPENCLAW COMPLETE VERSION / FINAL)

---

🔶 MAIN PATH COMPLETE 🔶

STEP0 → STEP1 → STEP2 → STEP3 → STEP4 → STEP5

---

🔷 STEP 6 — Batch Observation（OPENCLAW COMPLETE VERSION / FINAL）

Objective:
Execute bounded one-shot observations for multiple symbols after successful recovery and collector validation.

Background:

STEP 5 confirmed collector one-shot execution works under one-command constraints
STEP 6 extends this to additional symbols
each observation must remain independent and bounded
runtime normalization must be included in every execution
🔷 共通ルール（MANDATORY）

Each symbol execution must:

run exactly one command
include runtime normalization:
cd runtime_base
PowerShell PATH
.env.local
venv activation via absolute python

bypass registration:

SKIP_KABU_REGISTRATION=1
no retry
no preview
no simulated_order
no real_order
-- 7203 --
🔷 Execution
bash -lc 'cd /mnt/c/ai-trading-os-private && export PATH="$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0" && source ./.env.local && export SKIP_KABU_REGISTRATION=1 && /mnt/c/ai-trading-os-private/scripts/registrar/.venv/bin/python /mnt/c/ai-trading-os-private/scripts/collector/collect_board_once.py 7203'
🔷 Return
Observation Result
...

Snapshot Result
...

Trace Result
...

Issue (if any)
...
-- 8306 --
🔷 Execution
bash -lc 'cd /mnt/c/ai-trading-os-private && export PATH="$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0" && source ./.env.local && export SKIP_KABU_REGISTRATION=1 && /mnt/c/ai-trading-os-private/scripts/registrar/.venv/bin/python /mnt/c/ai-trading-os-private/scripts/collector/collect_board_once.py 8306'
🔷 Return
Observation Result
...

Snapshot Result
...

Trace Result
...

Issue (if any)
...
-- 6758 --
🔷 Execution
bash -lc 'cd /mnt/c/ai-trading-os-private && export PATH="$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0" && source ./.env.local && export SKIP_KABU_REGISTRATION=1 && /mnt/c/ai-trading-os-private/scripts/registrar/.venv/bin/python /mnt/c/ai-trading-os-private/scripts/collector/collect_board_once.py 6758'
🔷 Return
Observation Result
...

Snapshot Result
...

Trace Result
...

Issue (if any)
...
🔷 Judgment Rule（各シンボル）
Observation Result 成功
Snapshot Result 成功
Trace Result 成功

→ PASS

いずれか失敗 → STOP

🔷 Interpretation Note
各シンボルは 完全に独立した1回実行
STEP 5 の延長であり、collectorの安定性検証フェーズ
東証閉場中でも：
API応答
snapshot書き込み
trace_event
は検証可能

👉 つまりこれは 市場データの正しさではなく、パイプラインの健全性テスト

🔶 END OF STEP 6（OPENCLAW COMPLETE）

---

🔷 STEP 7 — Preview Path（READY生成）【OPENCLAW COMPLETE VERSION / FINAL】
Objective

Generate exactly one preview result and one execution_readiness_evaluated event using a temporary preview-only AAB under OpenClaw one-command execution constraints.

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
a fresh observation already exists for the target symbol

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

Preview AAB Rule

Use a temporary preview-only AAB in /tmp.

Do NOT use registrar queue artifacts.

Do NOT mix preview with execution artifacts.

The AAB must contain:

execution_scope.action_type = "order_preview"
execution_scope.symbol
execution_scope.order_type
execution_scope.side
execution_scope.quantity

And constraints:

dry_run = true
external_order_allowed = false
preview_only = true
state_change_allowed = false
test_override_allowed = false

This keeps Preview lightweight, temporary, and separated from Execution.

Output Discipline (STRICT)

You MUST return ALL sections below.

Do NOT return:

YES / NO
PASS / FAIL only
partial output

A one-word reply is INVALID and must be treated as STOP.

Approved Execution Method (MANDATORY)

Do NOT use plain python.

Do NOT rely on previously sourced shell state.

Run exactly one command only:

bash -lc 'cd /mnt/c/ai-trading-os-private && export PATH="$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0" && source ./.env.local && printf "%s\n" "{"aab_id":"AAB-PREVIEW-8306-TEMP","execution_scope":{"action_type":"order_preview","symbol":"8306","order_type":"market","side":"buy","quantity":1},"constraints":{"dry_run":true,"external_order_allowed":false,"preview_only":true,"state_change_allowed":false,"test_override_allowed":false},"capital_allocation":{"constraint_type":"preview_only"}}" > /tmp/atos_order_preview_8306.json && /mnt/c/ai-trading-os-private/scripts/registrar/.venv/bin/python -m scripts.openclaw.run_order_preview /tmp/atos_order_preview_8306.json'

Constraints:

exactly one command
no retry
no collector execution
no simulated_order
no real_order
no external order transmission
Judgment Rule (STRICT)
if preview runs successfully
and execution_readiness_evaluated is produced
and a readiness result is returned
→ Preview path is validated

Then:

if readiness result is READY → PASS
if readiness result is NOT_READY, REPRICE_REQUIRED, or DATA_INVALID → STOP, but preview path itself is still considered operational

No retry allowed.

Required Return Format (MANDATORY)

You MUST return EXACTLY this structure:

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
Valid PASS Example

Input Contract
Temporary preview AAB created at /tmp/atos_order_preview_8306.json

Correct Invocation
Executed exactly one command with one-command runtime normalization

Preview Result
Preview executed successfully for symbol 8306

execution_readiness_evaluated Result
trace_event recorded successfully

READY Context Result
READY context generated successfully

Blocking Issue (if any)
None
Valid STOP Example (Operationally Correct)

Input Contract
Temporary preview AAB created at /tmp/atos_order_preview_8306.json

Correct Invocation
Executed exactly one command with one-command runtime normalization

Preview Result
SUCCESS

execution_readiness_evaluated Result
PRESENT
readiness=NOT_READY, failed_checks=[market_closed, snapshot_stale]

READY Context Result
NOT_READY
market_state=closed, freshness_ms=12468632, reproducible=true

Blocking Issue (if any)
Preview executed, but execution readiness is NOT_READY because market_closed and snapshot_stale were detected

This is a valid STOP outcome when the market is closed or freshness requirements are not met.

Invalid Response Examples (REJECT)
NO
PASS
OK

→ MUST be treated as STOP (invalid output)

Interpretation Note

This step is Preview only.

It does NOT:

execute simulated_order
execute real_order
transmit any order externally

Its purpose is to:

run preview once
generate execution_readiness_evaluated
produce a readiness result
confirm correct STOP behavior when live execution conditions are not satisfied

Preview must remain separated from Execution artifacts and execution paths.

🔶 END OF STEP 7（OPENCLAW COMPLETE VERSION / FINAL）

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

🔷 STEP 10 — Simulated Order Safety Test

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

🔷 STEP 11 — Real Order Token Dry-Run（最終）

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

🔷 STEP 12 — Restart Recovery Protocol

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

🔶 FLIGHT COMPLETE 🔶


Collector → Preview → READY → Gate → Execution Safety → Broker Boundary

---

Final interpretation:

- Execution safety path verified
- Broker path reachable (token only)
- No unintended order transmission

---