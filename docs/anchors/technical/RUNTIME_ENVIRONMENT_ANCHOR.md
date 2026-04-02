# RUNTIME_ENVIRONMENT_ANCHOR

## Role
Runtime Layer（実行環境・復旧・トラブル統合）

---

## Purpose
WSL / PowerShell / env / venv の再現可能な実行環境を定義する

---

## Runtime Base
/mnt/c/ai-trading-os-private

---

## Standard Startup

```bash
cd /mnt/c/ai-trading-os-private
export PATH=$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0
source ./.env.local
source scripts/registrar/.venv/bin/activate
```

Note:
.env.local は WSL/bash runtime にのみ適用される。
PowerShell 実行時には自動的に使用されるとは限らない。

---

## Validation Checklist

* pwd
* which python
* which powershell.exe
* env 確認

---

## PowerShell Bridge

* powershell.exe が PATH で解決されること
* env 継承に依存しないこと（明示代入を前提とする）

---

## Common Failure

### 1. env 読み込みミス

誤: scripts/registrar/.env.local.wsl
正: ./.env.local

---

### 2. workspace drift

必ず runtime base を確認

---

### 3. venv 未有効化

python が system を向いていないか確認

---

## Recovery Procedure

1. runtime base に戻る
2. env 再source
3. venv 再activate
4. PowerShell確認

---

## Preflight Success Conditions

以下がすべて成立した場合、runtime preflight は成功とみなす：

- runtime base が `/mnt/c/ai-trading-os-private` である
- `python` が `scripts/registrar/.venv` 配下を指す
- `powershell.exe` が PATH で解決される
- `.env.local` 由来の必要環境変数が可視である

---

---

## WSL ↔ PowerShell Boundary Rules（Critical）

This section defines mandatory rules when invoking KabuStation API via PowerShell from WSL/Python context.

### Core Principle

Environment variables being visible in WSL/bash **does NOT guarantee** they are used in PowerShell request construction.

> env exists ≠ env is used

---

### Mandatory Rule — Explicit Assignment

When calling PowerShell (`powershell.exe`) for API access:

- DO NOT rely on environment variable inheritance
- ALWAYS assign required values explicitly inside PowerShell context

Example (conceptual):

$env:KABU_API_PASSWORD = "..."
$env:KABU_API_PORT = "18081"
Invoke-RestMethod ...


---

### Port ↔ Password Mapping (Strict)

The following mapping must be enforced:

- port 18081 → `KABU_API_TEST_PASSWORD`
- port 18080 → `KABU_API_PASSWORD`

Rules:

- No fallback from test → production
- No shared variable for both ports
- Variable name must match port context explicitly

---

### Execution Mode Resolution

ATOS における broker mode は、runtime 上で以下のように解決される：

- production
  - port: 18080
  - password source: `KABU_API_PASSWORD`

- test
  - port: 18081
  - password source: `KABU_API_TEST_PASSWORD`

- internal_simulation
  - port: none
  - password source: none
  - broker access: none

### Rule

`internal_simulation` は broker に接続しない。
したがって、KabuStation API token / register / board / sendorder への依存を持ってはならない。

### Safety Meaning

問題は「env が存在するか」ではなく、
「現在の command がどの mode として実行されるか」が
明示されているかどうかである。

port / password は単なる環境変数ではなく、
現在の execution mode の制度的表現として扱う。

---

### Known Failure Pattern (Critical)

If the following is observed:


{"APIPassword": null}


Then:

- The password value exists in WSL
- BUT is not reaching PowerShell request construction

Root cause is almost always:

- variable name mismatch, or
- missing explicit assignment in PowerShell context

DO NOT re-validate password value first.

---

### Diagnostic Priority Order

When token acquisition fails:

1. Verify variable presence inside PowerShell (not WSL)
2. Verify correct port (18080 vs 18081)
3. Verify request construction (content-type / body)
4. Only then consider password value mismatch

---

### Architectural Constraint

The execution path is:


WSL → Python → subprocess → powershell.exe → Invoke-RestMethod


Each boundary must be treated as isolated.

No implicit variable propagation should be assumed.

---

### Anti-Pattern (Prohibited)

The following approaches are prohibited:

- assuming `.env` presence implies correct runtime behavior
- relying on inherited env across subprocess boundaries
- mixing 18080 and 18081 contexts
- using a single password variable for both environments
- debugging via repeated retries without fixing mapping

---

### Institutional Insight

The primary failure mode in Phase 9B-1 was:

- not incorrect password
- not network failure
- but missing explicit PowerShell assignment

This rule is considered **critical for stable API interaction**.

---

### PowerShell Bridge Requirement (Critical)

KabuStation integration requires Windows PowerShell from WSL.

Required:
- powershell.exe must be available in PATH

Typical fix:
export PATH=$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0

Without this:
- symbol registration fails
- board fetch fails
- token acquisition fails

---

---

## 7. Incident Pattern — kabuStation 18080 Port Conflict（2026-04-03）

### Summary

A production API failure on port 18080 was caused not by kabuStation,
but by a Windows portproxy conflict.

The port appeared open, but requests never reached kabuStation.

---

### Symptom Pattern

- `Invoke-RestMethod`:
  - connection closed unexpectedly
- Python `requests`:
  - connection refused
- OpenClaw collector:
  - token / register path failure
- APILog:
  - no record of request attempts

---

### Key Diagnostic Findings

#### 1. Port appears open

Test-NetConnection localhost 18080
→ True

#### 2. Port owner is not kabuStation

Get-NetTCPConnection -LocalPort 18080 -State Listen

→ Owning process:
- `svchost.exe` (iphlpsvc)

#### 3. portproxy rule exists

netsh interface portproxy show all

Example:

0.0.0.0:18080 -> 127.0.0.1:18080

This is a self-referential proxy loop.

---

### Root Cause

Windows `iphlpsvc` (IP Helper Service) was holding port 18080
via a portproxy rule.

As a result:

- kabuStation could not bind to port 18080
- API requests never reached kabuStation
- APILog remained empty

---

### Resolution

Run in elevated PowerShell or cmd:

netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=18080

Then:

1. confirm removal

netsh interface portproxy show all

2. restart kabuStation

3. verify token:

ResultCode 0

---

### Preflight Check (MANDATORY for production API)

Before any 18080 usage, ALWAYS verify:

netsh interface portproxy show all

Get-NetTCPConnection -LocalPort 18080 -State Listen |
Select-Object LocalAddress,LocalPort,OwningProcess

Get-Process -Id <PID> |
Select-Object Id,ProcessName,Path

---

### Expected Healthy State

- port 18080 is owned by kabuStation
- no portproxy rule exists for 18080
- APILog records token request
- token returns `ResultCode 0`

---

### Invalid State Indicators

- portproxy entry exists for 18080
- port owner is `svchost.exe` / `iphlpsvc`
- API request not recorded in APILog
- token request fails without reaching API layer

---

### Institutional Interpretation

This is classified as:

- Layer: Runtime Layer
- Type: Transport Path Corruption
- Category: Silent Routing Failure

This failure occurs below the application layer and must be
excluded before diagnosing:

- API configuration
- authentication
- OpenClaw behavior

---

### Critical Lessons

port open ≠ service reachable

This pattern must be checked before any API-level debugging.

---

## Notes

本アンカーは以下を統合：

* WSL_ENVIRONMENT_ANCHOR
* OBSERVATION_PREVIEW_RUNTIME_RECOVERY_ANCHOR
* OPENCLAW_TROUBLESHOOTING_ANCHOR
