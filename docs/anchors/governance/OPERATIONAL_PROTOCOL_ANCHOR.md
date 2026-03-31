# OPERATIONAL_PROTOCOL_ANCHOR

## Role
Operational Layer（実運用手順の中核）

## Purpose
ATOSの開場中運用を再現可能な手順として定義する

---

## Source of Truth
- P-20260331-004（ATOS Operational Protocol v1）
- P-20260331-001（Preview Formalization）
- P-20260331-002（Execution Gate）
- P-20260331-003（Phase 9B）

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

## Notes

このアンカーは「どう動くか」の唯一の参照点である