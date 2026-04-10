# OPERATIONAL_PROTOCOL_ANCHOR

## Role
Operational Layer（実運用手順の中核）

## Purpose
ATOSの開場中運用を再現可能な手順として定義する

---

## Source of Truth
- P-20260331-004（ATOS Operational Protocol v1）
- P-20260410-002（AiiD Redefinition & Role Reorganization）
- P-20260331-001（Preview Formalization）
- P-20260331-002（Execution Gate）
- P-20260331-003（Phase 9B）

---


---

## 2026-04-10 Role Reorganization Note（P-20260410-002）

本プロトコルにおける役職参照は以下の新配置に従う。

| 役職 | 担当 |
|------|------|
| Proposer | ChatGPT |
| Librarian | Claude Cowork |
| Collector | OpenClaw |
| Executer | Codex |

プロトコル手順自体は変更なし。役職名が参照される箇所は上記配置で解釈する。

---

## ATOS Operational Protocol v1

### Execution Sequence
1. Preflight  
   詳細な手順と成功条件は `docs/anchors/technical/RUNTIME_ENVIRONMENT_ANCHOR.md` を参照する。
2. Go / No-Go 判定
3. Command Classification Declaration
4. Market Observation
5. Observation Freshness Check
    stale と判定された場合は、その時点で NO_GO とし、Preview / Execution へ進まない。
6. Preview / Readiness Check
7. Execution Gate Confirmation
8. Bounded WRITE Execution（必要時のみ）
9. Report

---

## Core Principles

### Freshness Principle
Preview は常に最新 observation を前提とする  
stale observation では readiness 判定を行わない

---

### Execution Boundary Principle
Execution は必ず gate を通過した後にのみ発生する

---

### Command Classification Principle
すべてのコマンドは実行前に
- observation-only
- bounded WRITE
に分類される

---

### Minimal Execution Principle
WRITE は必要最小限に限定する

---

### Kill Switch Principle
Execution Gate または上位判断により即時停止可能

---

## Execution Mode Declaration

本番系の誤接続を防ぐため、broker に関与する可能性のあるコマンドは、
実行前に必ず mode を明示しなければならない。

### Required Pre-Execution Declaration

以下を実行前に明示する：

- command_class
- broker_mode
- broker_touch
- external_order_allowed
- kabu_port
- password_source
- dry_run

例：

- command_class = observation-only / bounded WRITE
- broker_mode = production / test / internal_simulation
- broker_touch = true / false
- external_order_allowed = true / false
- kabu_port = 18080 / 18081 / none
- password_source = KABU_API_PASSWORD / KABU_API_TEST_PASSWORD / none
- dry_run = true / false

### Interpretation Rules

- `production` は本番 broker 接続を意味する
- `test` は検証用 broker 接続を意味する
- `internal_simulation` は broker 非接続の内部シミュレーションを意味する

### Operational Rule

特に以下の条件を満たすコマンドは、宣言なしに実行してはならない：

- PowerShell bridge を経由する
- KabuStation API に到達する
- port / password の選択を伴う
- execution 相当の bounded WRITE を含む可能性がある

### Founder Visibility Principle

Founder は各コマンドについて、少なくとも以下を実行前に把握できる状態であるべきである：

- そのコマンドが broker に触るか
- test / production のどちらに向いているか
- 外部注文送信が許可されているか

mode ambiguity は NO_GO とする。

---

## Preview Layer Alignment

### Readiness States
- READY
- NOT_READY
- REPRICE_REQUIRED
- DATA_INVALID

---

## Trace Event Alignment

実装上のイベント名：
execution_readiness_evaluated

仕様との差分は将来Proposalで統一する

---

---

## Operational Notes（Non-Normative）

### First Live Market Execution Note（Phase 7.x）

This note provides guidance for the first live-market execution cycle.
It does not modify the Operational Protocol itself.

#### Context
- Preflight, Runtime, and Bridge diagnostics completed successfully
- Closed-market bounded WRITE test succeeded
- Collector path confirmed to produce downstream writes

#### Important Clarification

The collector command:
python scripts/collector/collect_board_once.py <symbol>

must be treated as:

- command type: bounded WRITE
- not observation-only
- not pair-bounded
- may trigger downstream writes (indicator_observation, registrar-related steps)

#### First Live Execution Plan

At market open:

1. classify next command before execution
2. confirm explicit GO for bounded WRITE
3. execute collector for a single symbol (e.g. 7203)
4. verify freshness of observation
5. proceed to preview/readiness only if freshness passes
6. do not introduce additional WRITE beyond the collector path unless reclassified

#### Stop Conditions

Immediately stop if:

- command classification is ambiguous
- WRITE scope expands beyond expected collector behavior
- freshness cannot be confirmed
- execution path deviates from expected collector path

### Phase 9B Execution Constraint

During Phase 9B testing:

- API recovery (token/register/board) must be completed before any execution-like step
- simulated_order must remain:
  - dry-run only
  - test port (18081) only
  - bounded WRITE only

No real order is allowed in Phase 9B.

---

### Known Execution Boundary

collector-based observation paths may trigger downstream writes.

simulated_order path is preferred for bounded execution validation.

---

### Real Order Activation Ladder (Phase 9B-3)

Execution path must be opened strictly in the following order:

1. internal_simulation (no broker)
2. dry_run (env validation only)
3. token_acquisition (broker connectivity only)
4. submission boundary (sendorder)

Skipping steps is prohibited.

Each step must be validated independently before proceeding.

---

## Notes

このアンカーは「どう動くか」の唯一の参照点である