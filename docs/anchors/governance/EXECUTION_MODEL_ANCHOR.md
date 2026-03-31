---
title: EXECUTION MODEL ANCHOR
layer: B (Institutional State Snapshot)
version: 2.0
date: 2026-03-28
supersedes: EXECUTION_MODEL_ANCHOR v1.3 (2026-03-16)
status: draft
related_proposals:
  - proposals/accepted/P-20260326-030.md
  - proposals/accepted/P-20260327-031.md
  - proposals/accepted/P-20260327-032.md
---

# Execution Model Anchor
## AI Trading OS — Institutional Execution Framework

---

## 1. Three-Layer Execution Model

P-20260327-032 により、ATOSの実行モデルは以下の三層として制度的に定義された。

### Layer 1: Observation Layer（観測層）

```
操作種別 : READ
担い手   : Librarian / Proposer / Founder
対象     : Git（local / private / public）、DB（research.trace_event 等）
```

状態を読み取る層。システムの状態を変更しない。観測権は実行権を含意しない。

### Layer 2: Approval Layer（承認層）

```
操作種別 : TRIGGER（承認ハッシュ / トークンの発行）
担い手   : Founder（最終承認権者）/ Librarian（審議参加）
対象     : 特定の実行行為の制度的承認
```

承認を制度的に記録・伝達する層。Approval LayerはGit / DBへの直接書き込みを行わない。承認ハッシュは `authorization_granted` 相当のtrace_eventとして記録される（状態変更ではなく記録）。Approval Layer における trace_event 記録は、Execution Layer の WRITE とは区別される制度記録であり、Git / DB の operational state mutation を意味しない。

### Layer 3: Execution Layer（実行層）

```
操作種別 : WRITE（状態変更）
担い手   : Execution Agent（OpenClaw / Cowork / その他承認済みAiiD）
対象     : Git（commit / push / merge）、DB（INSERT / UPDATE / DELETE）
```

実際の状態変更を行う層。すべてのWRITE操作はtrace_eventを必ず生成し、Execution Agentに帰属する。

---

## 2. 明示的原則

```
- Observation does not imply execution
- Approval does not imply execution
- Approval does not modify system state
- All WRITE operations are execution
- All WRITE operations MUST be attributed to an execution agent
- All WRITE operations MUST produce a corresponding trace_event
```

---

## 3. Execution Attribution Principle

すべてのWRITE操作は制度的にExecution Agentに帰属する。立法府（Librarian / Proposer / Founder）の指示・承認によって起動された操作であっても、制度上の実行主体はExecution Agentである。

```
All write operations MUST be attributed to an execution agent,
even if initiated through higher-layer systems.

Institutional actors do not perform execution,
but may trigger or approve execution.
```

### trace_event フィールド（WRITE操作）

```yaml
execution_actor   : <agent_id>
approved_by       : Founder
approval_hash     : <hash>
proposal_origin   : <proposal_id>
operation_type    : WRITE
target            : <git|db>
```

---

## 4. Authorization Lifecycle（P-20260327-031 参照）

authorizationは以下の三状態を持つ。

| 状態 | 意味 |
|------|------|
| `granted` | Founderが発行し、有効な状態 |
| `invalidated` | 明示的に無効化された終端状態 |
| `consumed` | 外部送信完了後の終端状態 |

`invalidated` と `consumed` はいずれも終端状態であり再利用不可。新たな実行サイクルには新たな `authorization_granted` が必要となる。

---

## 5. Authorization Pathways（v1.3 継承・更新）

三つの承認経路は引き続き有効であり、Three-Layer Modelの文脈で再定義される。

| 経路 | フロー | 説明 |
|------|--------|------|
| **Founder Direct** | Founder → Registrar → Assistant Registrar | Founder承認済みの直接指示 |
| **Institutional** | Collector → Proposer → Librarian → Registrar → Assistant Registrar | 制度的審議を経た完全フロー |
| **Common** | Librarian → Registrar → Assistant Registrar | 通常運用タスク |

いずれの経路においても、Approval LayerはFounderが担い、Execution LayerはRegistrar / OpenClaw等が担う。

---

## 6. 各主体のアクセス権

| 主体 | Observation（READ） | Approval（TRIGGER） | Execution（WRITE） |
|------|---------------------|---------------------|---------------------|
| **Founder** | ✅ | ✅（最終承認権者） | ❌（原則として実行主体ではない。必要時は別途明示的に定義された経路による） |
| **Librarian** | ✅ | ✅（審議参加） | ❌ |
| **Proposer** | ✅ | ❌（起草・提案のみ） | ❌ |
| **Registrar** | ✅ | ❌ | ✅（承認下） |
| **OpenClaw / Cowork** | ✅ | ❌ | ✅（承認下） |

---

## 7. Safety Mechanisms（v1.3 継承）

- サンドボックスブランチポリシーはAssistant Registrarの作業を規定する
- 事前条件の検証が必須（未達成時は即停止）
- ステージング内容の明示的確認（スコープ外ファイルの混入防止）
- post-execution safety lockにより重複送信を防止
- 停止は「失敗」ではなく「規律ある準拠」として扱われる

### 7.2 Bounded trace_event recording instruction discipline

Recording a `trace_event` to the database is a WRITE operation.

Therefore, instructions such as:
- "record a trace_event"
and
- "do not execute anything"

must not be combined without clarification.

If only a single trace-event write is intended, the instruction should explicitly authorize:
- exactly one bounded WRITE
- no other execution action

This reduces avoidable execution ambiguity for OpenClaw and other execution agents.

---

## 8. 変更履歴

| Version | Date | 変更内容 |
|---------|------|----------|
| v1.0–v1.3 | 〜2026-03-16 | 初期定義・段階的更新 |
| **v2.0** | **2026-03-28** | **Three-Layer Model / Execution Attribution / Authorization Lifecycle を統合** |

本アンカーはP-020–P-032の制度定義を運用レベルに統合したものである。
