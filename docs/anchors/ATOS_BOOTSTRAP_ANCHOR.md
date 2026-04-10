# ATOS_BOOTSTRAP_ANCHOR

Version: 1.3
Date: 2026-04-10
Status: active
Purpose: Project startup reference for AI Trading OS institutional
state reconstruction

---
## Current Institutional State（最優先 — 2026-03-28更新）

このセクションが制度の現在状態として最優先で解釈される。

### 現在の制度フロー（六段構成）
Observation → Dialogue → Proposal → Preview → Approval → Execution

### 最新有効Proposal
- P-20260328-033: Dialogue Layer Formalization
- P-20260328-017: Order Preview and Price Binding Layer

### 現在のPhase
Phase 7 — Controlled Execution Entry（確立済み / 2026-03-28）

### 2026-03-30 Update — Observation Auto-Recovery (C Phase PoC)
- OpenClaw / WSL 環境からの Observation 自動復旧に成功（PoC）
- scripts/collector/collect_board_once.py を用いた Windows PowerShell bridge 経由での board取得が成立
- token取得 → symbol登録 → board取得 → snapshot → trace_event（market_observation）までの一連のパイプラインが自動実行で確認された
- Founder手動Observationは不要となり、既存collector経路が制度内の標準Observation手段として再確立された

Current interpretation:
Observation Layer is considered operational via Windows PowerShell bridge (WSL → PowerShell → localhost → KabuStation API).

### 2026-03-31 Operational Validation Update
The Observation → Preview cycle has now been validated during market hours for symbol 7203.

Confirmed:
- fresh observation acquisition succeeded
- hard limits check succeeded
- soft-limit test evaluation produced READY
- readiness evaluation was recorded in `research.trace_event`

Note:
Current implementation uses `execution_readiness_evaluated` as the trace_event name.
Earlier references to `execution_readiness_checked` reflect the proposal-stage naming.

Operational note:
For OpenClaw / WSL runtime recovery, use the technical runtime guidance in:
`docs/anchors/technical/RUNTIME_ENVIRONMENT_ANCHOR.md`

In practice, successful recovery required:
- runtime base `/mnt/c/ai-trading-os-private`
- sourcing `.env.local` in the same shell context
- activating `.venv` in the same shell context
- adding `/mnt/c/Windows/System32/WindowsPowerShell/v1.0` to PATH

### 2026-04-01 Execution Safety Update

- P-20260401-001: Execution Consumption and Duplicate Prevention Model
- Duplicate Execution Prevention 実装完了
- Phase 9B 完了

Current interpretation:

Execution Safety Layer is now active.
A READY context is consumable and cannot be reused.

### 2026-04-10 Role Reorganization & AiiD Redefinition

- P-20260410-002: AiiD Redefinition and Role Reorganization
- 役職再編（Proposer→ChatGPT / Librarian→Claude Cowork / Executer→Codex 新設）
- AiiD新定義: AI名 + Phase固定スレッド名 + 役職名 + Founder認証情報（非遡及）

Current interpretation:

Four active institutional roles are now defined.
Executer (Codex) is newly established for code implementation tasks.
AiiD is now Phase-scoped. Existing trace_event agent_id values are preserved (non-retroactive).

### 読み順（必須）
Bootstrap
EXECUTION_MODEL_ANCHOR
EXECUTION_SAFETY_ANCHOR
OPERATIONAL_PROTOCOL_ANCHOR
RUNTIME_ENVIRONMENT_ANCHOR
DB_STATUS_ANCHOR
HANDOFF_INDEX

---

## 1. About This Document

This document describes how participants in the AI Trading OS project
can reconstruct a consistent view of the project's current institutional
state from the repository.

Reading this document and the files listed in Section 6 provides a
shared starting point for Librarian, Proposer, and OpenClaw when
beginning a new session or joining an ongoing workflow.

---

## 2. Canonical Repository

The canonical repository for AI Trading OS is:

`https://github.com/pulp39/ai-trading-os-private`

This repository is the institutional source of truth.

The canonical local working repository for execution and editing is:

`C:\ai-trading-os-private`

This local repository is the primary working copy used for
implementation, execution, and document editing.

The public repository is:

`https://github.com/pulp39/ai-trading-os-public`

This repository exists for visibility and browsing access.
It is not the canonical source of institutional truth.

Summary:

- GitHub private repository = canonical source of truth
- `C:\ai-trading-os-private` = canonical local working repository
- GitHub public repository = browsing / reading repository

Chat history and session memory are useful context but do not substitute
for the canonical repository when establishing the current project state.

---

## 3. Who This Document Serves

This document is a reference for the three AI participants in AI Trading
OS:

- **Librarian** — institutional memory and governance interpretation
- **Proposer** — proposal drafting and institutional deliberation
- **OpenClaw** — collector and assistant registrar functions

Each participant has a distinct role. This document helps all three
start from the same shared understanding of project state.

---

## 4. Why Read Order Matters

The documents in this project build on each other. The constitution
defines the foundational principles. The anchors describe the current
state of specific systems. The ledgers record operational details.

Reading them in the order listed in Section 6 helps ensure that
higher-level principles are understood before more specific operational
documents are interpreted. Reading out of order risks misinterpreting
a specific rule without its broader institutional context.

---

## 5. Getting Started

To reconstruct project state for a new session, a participant can begin
by reading this file and then following the read order in Section 6.

For Claude-family participants, CLAUDE.md describes operational
conventions that work alongside constitution.md. Where the two appear
to differ, constitution.md reflects the foundational project principles.

## Bootstrap Position

ATOS_BOOTSTRAP_ANCHOR is not part of the five operational layers.
It serves as the Entry Point for anchor reconstruction.

Its role is:
- to define read order
- to provide a stable starting point
- to guide state reconstruction across sessions and AiiD participants

---

## 6. Recommended Read Order

Reading the following files in this order provides a complete picture
of the current project state.

This order reflects the layered anchor architecture:
Constitution → Execution Safety → Operational → Runtime → Data → Capability → Handoff

---

### 1. Core Constitution & Identity

1. constitution.md  
2. CLAUDE.md  
3. docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md  

---

### 2. Execution Model (Constitution Layer)

4. docs/anchors/governance/EXECUTION_MODEL_ANCHOR.md  

---

### 3. Execution Safety Layer（重要）

5. docs/anchors/governance/EXECUTION_SAFETY_ANCHOR.md  

This anchor defines:
- 1 READY context = 1 execution
- execution consumption model
- duplicate execution prevention

---

### 4. Operational Layer（中核）

6. docs/anchors/governance/OPERATIONAL_PROTOCOL_ANCHOR.md  

---

### 5. Runtime Layer（実行環境）

7. docs/anchors/technical/RUNTIME_ENVIRONMENT_ANCHOR.md  

---

### 6. Data Layer

8. docs/anchors/technical/DB_STATUS_ANCHOR.md  

---

### 7. Capability Layer

9. docs/anchors/technical/OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md  

---

### 8. Handoff Layer（最新の実運用知見）

10. docs/anchors/handoffs/HANDOFF_INDEX.md  
11. docs/anchors/handoffs/PHASE_9B_HANDOFF.md  
12. docs/anchors/handoffs/PHASE_9B_COMPLETION_HANDOFF.md  

This layer captures:
- Phase-based validation results
- latest operational discoveries
- knowledge not yet promoted to permanent anchors

---

### 9. Registry & Governance Context

13. docs/aiid_registry.md  
14. docs/BOUNDARY.md  

---

### 10. Operational Status

15. docs/openclaw_training_status.md  
16. docs/openclaw_registrar_apprentice_rubric.md  

---

### 11. Entry Documentation

17. README.md  

---

## Notes

- EXECUTION_SAFETY_ANCHOR defines execution constraints and must be read before any execution discussion
- OPERATIONAL_PROTOCOL_ANCHOR is the primary reference for "how to operate ATOS"
- RUNTIME_ENVIRONMENT_ANCHOR defines reproducible execution conditions
- Handoff layer captures the most recent validated behavior and should be referenced when working on active phases
- Legacy troubleshooting content is consolidated into runtime and incident pattern anchors

---

## 7. Interpretation Priority

1. constitution.md
2. CLAUDE.md
3. docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md
4. docs/anchors/governance/EXECUTION_MODEL_ANCHOR.md
5. docs/anchors/governance/EXECUTION_SAFETY_ANCHOR.md
6. docs/anchors/governance/OPERATIONAL_PROTOCOL_ANCHOR.md
7. docs/anchors/technical/RUNTIME_ENVIRONMENT_ANCHOR.md
8. docs/anchors/technical/DB_STATUS_ANCHOR.md
9. docs/anchors/technical/OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md
10. docs/anchors/handoffs/HANDOFF_INDEX.md
11. docs/aiid_registry.md
12. docs/BOUNDARY.md
13. docs/openclaw_training_status.md
14. docs/openclaw_registrar_apprentice_rubric.md
15. README.md

---

## 8. Conflict Resolution

When two documents appear to conflict, the higher-priority document
reflects the more authoritative project position.

- constitution.md reflects foundational project principles
- CLAUDE.md describes Claude-family operating conventions within those
  principles
- EXECUTION_MODEL_ANCHOR defines institutional execution structure
- OPERATIONAL_PROTOCOL_ANCHOR defines how ATOS is operated in practice
- RUNTIME_ENVIRONMENT_ANCHOR defines reproducible execution conditions
- DB and training anchors describe subsystem state
- Ledger documents and README reflect lower-priority operational detail

Legacy environment / troubleshooting anchors that have been consolidated
into RUNTIME_ENVIRONMENT_ANCHOR should be treated as deprecated.

---

## 9. Role Descriptions

### 9.1 Librarian（Claude Cowork）

The Librarian maintains institutional memory and provides governance
interpretation for the project. This includes:

- reconstructing current institutional state from the repository
- interpreting governance structure with continuity and consistency
- managing repository commits, anchor updates, and trace_event recording
- using the repository as the primary reference for institutional memory

Role assigned to: Claude Cowork（P-20260410-002, 2026-04-10）

### 9.2 Proposer（ChatGPT）

The Proposer drafts proposals and participates in institutional
deliberation. This includes:

- grounding proposals in the current repository state
- distinguishing between established institutional state and new
  proposals
- initiating institutional dialogue and proposal cycles

Role assigned to: ChatGPT（P-20260410-002, 2026-04-10）

### 9.3 Collector（OpenClaw）

OpenClaw contributes to the project as a Collector and, when explicitly
instructed, as an Assistant Registrar. This includes:

- reading the repository state before acting on registrar-related tasks
- acting within explicitly defined task scope when functioning as
  Assistant Registrar
- stopping and returning for clarification when preconditions are not
  met or scope is ambiguous

### 9.4 Executer（Codex）

Codex implements code-level tasks under institutional instruction.
This includes:

- executing code implementation tasks assigned via Proposal or Librarian
- operating within execution safety boundaries defined by P-20260409-001
- detailed execution boundaries to be established via separate Codex
  onboarding Proposal

---

## 10. Execution Overview

The execution model for this project is described in detail in:

`docs/anchors/governance/EXECUTION_MODEL_ANCHOR.md`

In summary, execution in AI Trading OS follows recognized role-based
paths rather than autonomous action. The Assistant Registrar role acts
on explicit instruction and within bounded scope. Sandbox branches
are used for Assistant Registrar activity by default.

---

## 11. Project State Map

This document provides orientation. The detailed state of each
subsystem is described in the following documents:

| Document | What it describes |
|---|---|
| docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md | Governance state and project structure |
| docs/anchors/governance/EXECUTION_MODEL_ANCHOR.md | Execution chain and discipline rules |
| docs/anchors/governance/OPERATIONAL_PROTOCOL_ANCHOR.md | Operational protocol and execution sequence |
| docs/anchors/technical/RUNTIME_ENVIRONMENT_ANCHOR.md | Runtime environment, recovery, and troubleshooting |
| docs/anchors/technical/DB_STATUS_ANCHOR.md | Database structure and confirmed state |
| docs/anchors/technical/OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md | OpenClaw qualification and training state |
| docs/aiid_registry.md | Active participant role registry (P-20260410-002 revised) |
| docs/BOUNDARY.md | Librarian / OpenClaw role boundary |
| docs/openclaw_training_status.md | OpenClaw training ledger |
| docs/openclaw_registrar_apprentice_rubric.md | OpenClaw evaluation rubric |

---

## 12. For Claude-Family Participants

CLAUDE.md describes conventions for Claude-family participants
operating in this project. It works alongside constitution.md rather
than replacing it.

Reconstructing project state from the repository before beginning
session work helps ensure consistency with other participants and with
the project's recorded institutional history.

---

## 13. Consistency Across Sessions

Project state is recorded in the repository. Chat history and session
memory provide useful context but may be incomplete or reflect
intermediate states.

When establishing the current project state — particularly for
governance decisions, proposal work, or registrar tasks — the
repository is the primary reference.

This applies equally to all participants: reconstructing from the
repository helps ensure consistent understanding across sessions and
across different AI participants.

---

## 14. What to Avoid

Reconstructing project state from a single document, from memory alone,
or from chat history alone risks an incomplete or outdated picture.
The read order in Section 6 is designed to provide a complete and
consistent view.

Treating any single document as the sole source — including this one —
without reading the others in context can lead to misinterpretation.

---

## 15. Project Goal

The goal of this anchor system is to make project state reconstructible
and consistent across sessions and participants:
```
One canonical repository
        ↓
One local clone
        ↓
One bootstrap document
        ↓
Shared project state for Librarian, Proposer, and OpenClaw
```

This enables any participant joining a new session to quickly arrive
at the same understanding of:

- current institutional structure
- execution model
- database state
- OpenClaw training and qualification status

---

## 16. Keeping Documents Aligned

The following documents describe subsystems that should remain
consistent with the principles in this document:

- CLAUDE.md
- docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md
- docs/anchors/governance/EXECUTION_MODEL_ANCHOR.md
- docs/anchors/technical/DB_STATUS_ANCHOR.md
- docs/anchors/technical/OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md
- docs/openclaw_training_status.md
- docs/openclaw_registrar_apprentice_rubric.md
- docs/anchors/governance/OPERATIONAL_PROTOCOL_ANCHOR.md
- docs/anchors/technical/RUNTIME_ENVIRONMENT_ANCHOR.md

---

## 17. Starting Point

This document is the recommended starting point for reconstructing
AI Trading OS project state.

`docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md`
