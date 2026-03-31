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

## Notes

このアンカーは「どう動くか」の唯一の参照点である