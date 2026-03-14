# ATOS_BOOTSTRAP_ANCHOR

Version: 1.2
Date: 2026-03-14
Status: active
Purpose: Project startup reference for AI Trading OS institutional
state reconstruction

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

The project's canonical repository is:

`ai-trading-os-private`

Local working copy:

`/home/vmamako/ai-trading-os-private`

The repository is the authoritative source for institutional state.
Chat history and session memory are useful context but do not substitute
for the repository when establishing the current project state.

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

---

## 6. Recommended Read Order

Reading the following files in this order provides a complete picture
of the current project state:

1. constitution.md
2. CLAUDE.md
3. docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md
4. docs/anchors/EXECUTION_MODEL_ANCHOR.md
5. docs/anchors/DB_STATUS_ANCHOR.md
6. docs/anchors/OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md
7. docs/aiid_registry.md
8. docs/BOUNDARY.md
9. docs/openclaw_training_status.md
10. docs/openclaw_registrar_apprentice_rubric.md
11. README.md

---

## 7. Interpretation Priority

When documents appear to cover the same topic differently, the following
priority order helps determine which description reflects the more
foundational project intent:

1. constitution.md
2. CLAUDE.md
   (CLAUDE.md describes operational conventions; it does not supersede
   constitution.md on questions of foundational principle)
3. docs/aiid_registry.md
4. docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md
5. docs/anchors/EXECUTION_MODEL_ANCHOR.md
6. docs/anchors/DB_STATUS_ANCHOR.md
7. docs/anchors/OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md
8. README.md

When apparent conflicts remain unclear, the interpretation most
consistent with constitution.md and with minimal disruption to project
safety is generally appropriate.

---

## 8. Conflict Resolution

When two documents appear to conflict, the higher-priority document
reflects the more authoritative project position.

- constitution.md reflects foundational project principles
- CLAUDE.md describes Claude-family operating conventions within those
  principles
- Anchor documents describe current system state within the governance
  framework
- Ledger documents and README reflect operational details at the
  lowest priority level

---

## 9. Role Descriptions

### 9.1 Librarian

The Librarian maintains institutional memory and provides governance
interpretation for the project. This includes:

- reconstructing current institutional state from the repository
- interpreting governance structure with continuity and consistency
- distinguishing Librarian functions from Registrar functions
- using the repository as the primary reference for institutional memory

### 9.2 Proposer

The Proposer drafts proposals and participates in institutional
deliberation. This includes:

- grounding proposals in the current repository state
- distinguishing between established institutional state and new
  proposals
- following CLAUDE.md within the principles defined by constitution.md

### 9.3 OpenClaw

OpenClaw contributes to the project as a Collector and, when explicitly
instructed by the Registrar, as an Assistant Registrar. This includes:

- reading the repository state before acting on registrar-related tasks
- acting within explicitly defined task scope when functioning as
  Assistant Registrar
- stopping and returning for clarification when preconditions are not
  met or scope is ambiguous

---

## 10. Execution Overview

The execution model for this project is described in detail in:

`docs/anchors/EXECUTION_MODEL_ANCHOR.md`

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
| docs/anchors/EXECUTION_MODEL_ANCHOR.md | Execution chain and discipline rules |
| docs/anchors/DB_STATUS_ANCHOR.md | Database structure and confirmed state |
| docs/anchors/OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md | OpenClaw qualification and training state |
| docs/aiid_registry.md | Active participant role registry |
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
- docs/anchors/EXECUTION_MODEL_ANCHOR.md
- docs/anchors/DB_STATUS_ANCHOR.md
- docs/anchors/OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md
- docs/openclaw_training_status.md
- docs/openclaw_registrar_apprentice_rubric.md

---

## 17. Starting Point

This document is the recommended starting point for reconstructing
AI Trading OS project state.

`docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md`
```

---

## 改訂のポイント（Librarian審査用サマリー）
```
Section 1  : "single canonical startup source for all AI participants"
             → "describes how participants can reconstruct..."
             目的の説明に変更

Section 3  : "Applies To" (役割への割り当て)
             → "Who This Document Serves" (説明・紹介)

Section 4  : "Bootstrap Determinism Rule" (強制ルール)
             → "Why Read Order Matters" (理由説明)

Section 5  : "Read and obey" / "canonical startup instruction"
             → "Getting Started" (自然な案内)

Section 9  : "must: / must not:" のリスト
             → 各役割の説明・機能の紹介に変換

Section 13 : "Anti-Drift Rule" (禁止リスト)
             → "Consistency Across Sessions" (理由と推奨)

Section 14 : (新設) "What to Avoid" — 禁止ではなくリスク説明

Section 17 : "All participants must start here. Read and obey:"
             → "This document is the recommended starting point"