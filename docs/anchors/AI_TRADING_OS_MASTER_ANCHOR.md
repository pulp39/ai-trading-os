# AI_TRADING_OS_MASTER_ANCHOR

Version: 2.1
Date: 2026-03-14
Status: active
Purpose: Institutional state overview for AI Trading OS

---

## 1. About This Document

This document provides a high-level overview of the current
institutional state of AI Trading OS.

It covers:

- the active governance structure
- the current participant roles
- the canonical repository
- a summary of the execution layer
- a summary of the database layer
- a summary of OpenClaw's current status

For detailed rules on execution, database structure, or OpenClaw
training, see the specialized anchor documents listed in Section 16.

This document is intended to be read alongside:

- `constitution.md`
- `docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md`

---

## 2. Canonical Repository

The canonical repository for this project is:

`ai-trading-os-private`

Local working copy:

`/home/vmamako/ai-trading-os-private`

The repository is the authoritative source for institutional state.
Chat history and session memory provide useful context but do not
substitute for the repository when establishing current project state.

---

## 3. Getting Started

Reconstructing project state for a new session works best by starting
from:

`docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md`

That document describes the recommended read order and explains how
the documents in this project relate to each other.

Reading this master anchor alone, without completing the bootstrap
read order, may give an incomplete picture of the current state.

---

## 4. Governance Approach

AI Trading OS operates under a structured institutional governance
model rather than an ad hoc workflow.

Institutional continuity in this project depends on:

- constitutional principles (defined in constitution.md)
- repository state as the shared source of truth
- anchor alignment across sessions
- role-bounded execution
- traceable change history

The project is designed to be persistent and reconstructible across
sessions and across different AI participants.

---

## 5. Active Participants

The currently recognized participants in AI Trading OS are:

| Role | Description |
|---|---|
| Founder | Human authority and final decision-maker |
| Librarian | Institutional memory and governance interpretation |
| Proposer | Proposal drafting and institutional deliberation |
| OpenClaw | Collector and Assistant Registrar (bounded execution) |

### 5.1 Founder

The human constitutional authority and final institutional
decision-maker for this project.

### 5.2 Librarian

Responsible for institutional coherence, governance interpretation,
and continuity across sessions.

### 5.3 Proposer

Responsible for structured proposal generation under the current
institutional state.

### 5.4 OpenClaw

A validated execution participant contributing as Collector and, under
explicit Registrar instruction, as Assistant Registrar within bounded
scope.

---

## 6. Institutional Model Overview

The institutional model can be summarized as:
```
Constitution
     ↓
Bootstrap Anchor
     ↓
Institutional Anchors
     ↓
Working Ledgers
     ↓
Bounded Execution
```

Project state is restored from the repository rather than recreated
from conversation context alone.

---

## 7. Document Layer Overview

| Layer | Documents |
|---|---|
| Layer 0 — Foundation | constitution.md, CLAUDE.md |
| Layer 1 — Bootstrap | docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md |
| Layer 2 — State Anchors | AI_TRADING_OS_MASTER_ANCHOR.md, EXECUTION_MODEL_ANCHOR.md, DB_STATUS_ANCHOR.md, OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md |
| Layer 3 — Working Ledgers | docs/aiid_registry.md, docs/BOUNDARY.md, docs/openclaw_training_status.md, docs/openclaw_registrar_apprentice_rubric.md |

---

## 8. Role Descriptions

### Librarian

Focuses on institutional interpretation and continuity. Distinguishes
Librarian functions from Registrar functions. Uses the repository as
the primary reference for institutional memory.

### Proposer

Works under restored institutional context. Grounds proposals in the
current repository state rather than session memory alone.

### OpenClaw

Performs bounded execution tasks when explicitly instructed by the
Registrar. Does not initiate execution autonomously or act outside
defined task scope.

These descriptions help maintain consistent role behavior across
sessions and participants.

---

## 9. Execution Layer Summary

The execution layer is described in detail in:

`docs/anchors/EXECUTION_MODEL_ANCHOR.md`

In summary, execution flows through role-based paths:
```
Founder Direct Path:
Founder → Registrar → Assistant Registrar

Institutional Path:
Collector → Proposer → Librarian → Registrar → Assistant Registrar

Common Path:
Librarian → Registrar → Assistant Registrar
```

Good execution practice in this project involves bounded scope,
explicit instruction, precondition checking, and traceable recording.

---

## 10. Database Layer Summary

The database layer is described in detail in:

`docs/anchors/DB_STATUS_ANCHOR.md`

In summary:

- Operational database: `trading`
- DB host: `192.168.250.11`
- Market data: `public.board_snapshots`
- Collector status: `ops.collector_status`
- Institutional event log: `research.trace_event`
- Proposal persistence: `research.proposal`

---

## 11. OpenClaw Status Summary

OpenClaw's training and qualification state is described in detail in:

`docs/anchors/OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md`

In summary:

- Phase 1 (workflow reconstruction): completed
- Phase 1.5 (task drafting): completed
- Assistant Registrar validation: completed
- Sandbox execution validation: completed

OpenClaw is currently recognized as Collector and Assistant Registrar.
Live database integration is planned but not yet active.

---

## 12. Current Project Direction

The project is currently focused on:

- stabilizing the anchor structure for consistent cross-session use
- enabling OpenClaw as a practical Assistant Registrar execution node
- verifying `claude_registrar` database privileges before runner
  implementation
- maintaining clear role boundaries as the project grows

---

## 13. What This Document Does Not Cover

This anchor provides a high-level overview. The following topics are
intentionally covered in specialized documents rather than here:

- detailed DB schema (see DB_STATUS_ANCHOR.md)
- detailed execution rules (see EXECUTION_MODEL_ANCHOR.md)
- OpenClaw validation history (see OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md)
- full ledger content (see working ledger documents)

Keeping this document focused helps it remain readable and useful as
a starting-point overview.

---

## 14. Stability Note

This master anchor is intended to remain stable and readable even as
lower-level documents evolve. When lower-level documents are updated,
this anchor should be checked for consistency.

This document reflects current state rather than constitutional
principles. Where they differ, constitution.md and
ATOS_BOOTSTRAP_ANCHOR.md reflect the higher-priority view.

---

## 15. Reference Map

| What you need | Where to find it |
|---|---|
| Project startup and read order | docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md |
| Execution rules | docs/anchors/EXECUTION_MODEL_ANCHOR.md |
| Database state | docs/anchors/DB_STATUS_ANCHOR.md |
| OpenClaw qualification | docs/anchors/OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md |
| Participant registry | docs/aiid_registry.md |
| Role boundary definition | docs/BOUNDARY.md |
| OpenClaw training ledger | docs/openclaw_training_status.md |
| Evaluation rubric | docs/openclaw_registrar_apprentice_rubric.md |

---

## 16. About This Version

This document provides a compact, current view of AI Trading OS
institutional state. It is intended to be updated when significant
governance or structural changes occur, and to remain aligned with the
bootstrap-centered reconstruction model described in
ATOS_BOOTSTRAP_ANCHOR.md.
```

---

## 改訂サマリー
```
Section 1  : "canonical authoritative" → "provides a high-level overview"
Section 3  : "must begin from / Read and obey" → "works best by starting from"
Section 4  : "not treated as loose conversational workflow" → 
             目的と設計を肯定的に説明
Section 8  : "This baseline prevents role drift" →
             "These descriptions help maintain consistent behavior"
Section 13 : "Intentionally Does Not Contain" → "What This Document Does Not Cover"
             禁止表現 → 設計意図の説明
Section 17 : "All participants must begin with bootstrap" →
             Section 16の参照マップに統合、Final Rule削除
全体      : must/must not → is/works best/helps ensure
```

---

**ATOS Anchor System 文体改訂 — 全anchor完了**
```
ATOS_BOOTSTRAP_ANCHOR.md              v1.0 → v1.2  ✓
AI_TRADING_OS_MASTER_ANCHOR.md        v2.0 → v2.1  ✓
EXECUTION_MODEL_ANCHOR.md             v1.1 → v1.2  ✓
DB_STATUS_ANCHOR.md                   v1.1 → v1.2  ✓
OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md v1.2 → v1.3  ✓
docs/registrar_task_format.md         v1.0 (変更なし、命令的表現なし)