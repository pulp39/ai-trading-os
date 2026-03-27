---
title: EXECUTION CONSTITUTION ANCHOR
layer: B (Governance Synthesis Anchor)
version: 1.0
date: 2026-03-28
status: draft
established_at: trace_event id=338 (2026-03-27)
source_proposals:
  - proposals/accepted/P-20260326-030.md
  - proposals/accepted/P-20260327-031.md
  - proposals/accepted/P-20260327-032.md
related_anchors:
  - docs/anchors/governance/EXECUTION_MODEL_ANCHOR.md (v2.0)
---

# Execution Constitution Anchor
## AI Trading OS — 実行制度の根幹

本アンカーはP-20260326-030・P-20260327-031・P-20260327-032の三Proposalによって確立された「実行に関する制度的定義の総体」を一文書として集約したものである。新しいAI参加者はこのアンカーを読むことで、ATOSにおける実行の制度を完全に理解できる。

---

## Part 1: Capability vs Authority（P-20260326-030）

### 核心の区別

| 概念 | 定義 | 担い手 |
|------|------|--------|
| `execution_ready` | 実行の条件が揃った状態（capability） | Collector が記録 |
| `authorization_granted` | 実行を許可する意思（authority） | Founder のみが発行 |

この二つは独立した概念である。`execution_ready` の成立は `authorization_granted` を自動的に意味しない。

### 状態階層

```
symbol_registered
market_data_ready  ───▶  market_ready（合成状態）
auth_ready                     │
                               ▼
                        execution_ready（最終状態）
```

### Core Invariant #1

```
execution_ready ≠ authorization_granted

「条件が揃っていること」と「許可が与えられていること」は
制度上、別の事実である。
```

---

## Part 2: Authorization Lifecycle（P-20260327-031）

### 三状態モデル

```
[granted]
  → invalidated   : Founderが明示的に無効化、またはセッション境界
  → consumed      : 外部送信完了（Founderの権限下）

[invalidated] → 終端（再利用不可）
[consumed]    → 終端（再利用不可）
```

### Freshness Gate

`execution_ready` の再構成には以下をすべて満たす fresh canonical observation が必要である。

- 同一セッション内で取得
- 直近の市場状態を反映
- Collectorによってtrace_eventとして記録済み
- 過去の `execution_ready` 根拠として未使用

### Boundary Closure

```yaml
active_authorization: false
reconstructable_execution_ready: false
external_execution_forbidden: true
system_state: closed_until_fresh_observation
```

閉鎖状態は失敗ではなく安全な終端である。

### Core Invariants #2–4

```
#2: invalidated / consumed は終端状態
    → authorizationは「使い切る」か「捨てる」かしかない

#3: freshness は hard gate
    → 過去の観測は execution_ready の根拠として再利用不可

#4: boundary closure は安全な終端
    → 実行不可能性を正確に認識した状態
```

---

## Part 3: Three-Layer Execution Model（P-20260327-032）

### 三層の定義

```
Layer 1: Observation（READ）
  担い手: Librarian / Proposer / Founder
  性質: 状態を変更しない

Layer 2: Approval（TRIGGER）
  担い手: Founder（最終承認）/ Librarian（審議参加）
  性質: 状態を変更しない。承認ハッシュをtrace_eventとして記録

Layer 3: Execution（WRITE）
  担い手: Execution Agent（OpenClaw / Cowork / 承認済みAiiD）
  性質: 状態を変更する。必ずtrace_eventを生成
```

### Execution Attribution Principle

```
All write operations MUST be attributed to an execution agent,
even if initiated through higher-layer systems.

Institutional actors do not perform execution,
but may trigger or approve execution.
```

### Core Invariants #5–7

```
#5: Observation ≠ Approval ≠ Execution
    → 三層は交差しない

#6: Approval は状態変更ではない
    → Approval Hash = record, not execution

#7: WRITE は常に Execution として扱われる
    → WRITEを伴わないApprovalは制度上「何も変えていない」
```

---

## Execution Constitution — 全不変条件の一覧

| # | Invariant |
|---|-----------|
| 1 | `execution_ready ≠ authorization_granted` |
| 2 | `invalidated` / `consumed` は終端状態 |
| 3 | freshness は hard gate（再利用不可） |
| 4 | boundary closure は安全な終端 |
| 5 | `Observation ≠ Approval ≠ Execution` |
| 6 | Approval は状態変更ではない |
| 7 | WRITE は常に Execution として扱われる |

これら7つの不変条件がATOS Execution Constitutionの骨格である。

---

## 各主体の制度的役割

| 主体 | Observation | Approval | Execution |
|------|-------------|----------|-----------|
| Founder | ✅ | ✅ 最終 | ❌ |
| Librarian | ✅ | ✅ 審議 | ❌ |
| Proposer | ✅ | ❌ | ❌ |
| Registrar | ✅ | ❌ | ✅ 承認下 |
| OpenClaw / Cowork | ✅ | ❌ | ✅ 承認下 |

---

## 将来への拡張余地

以下はExecution Constitutionの確立後に検討される事項であり、本アンカーのスコープ外である。

- constitution.md への統合（Phase 7 完了後）
- Approval Hashの暗号実装仕様
- Error / Rollback / Failure の制度的定義
- Phase 7: Controlled Execution Entry

---

## 制度的意義

本アンカーが確立した時点（trace_event id=338、2026-03-27）において、ATOSは：

```
実行できるシステム
ではなく
実行を定義できる制度
```

となった。Executionが「技術」から「制度」に昇格した節点として、本アンカーは永続的な参照点となる。
