# AI_TRADING_OS_MASTER_ANCHOR
Version: 2.2
Date: 2026-03-15
Status: active
Purpose: Institutional state overview for AI Trading OS

---

## 1. About This Document

This document provides a high-level overview of the current
institutional state of AI Trading OS. It covers:

- the active governance structure
- the current participant roles
- the canonical repository
- a summary of the execution layer
- a summary of the database layer
- a summary of OpenClaw's current status

For detailed rules on execution, database structure, or OpenClaw
training, see the specialized anchor documents listed in Section 15.

This document is intended to be read alongside:

- `constitution.md`
- `docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md`

---

## 2. Canonical Repository

The canonical repository for this project is: `ai-trading-os-private`
Local working copy: `/home/vmamako/ai-trading-os-private`

The repository is the authoritative source for institutional state.
Chat history and session memory provide useful context but do not
substitute for the repository when establishing current project state.

---

## 3. Getting Started

Reconstructing project state for a new session works best by starting
from:

```
docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md
```

That document describes the recommended read order and explains how
the documents in this project relate to each other.

Reading this master anchor alone, without completing the bootstrap read
order, may give an incomplete picture of the current state.

---

## 4. Governance Approach

AI Trading OS operates under a structured institutional governance
model. Institutional continuity depends on:

- constitutional principles (defined in `constitution.md`)
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

Following P-20260315-001, documents are organized as follows:

| Layer | Documents |
|---|---|
| Layer 0 — All AiiD (common) | `docs/ai_participant_onboarding.md` |
| Layer 1 — Bootstrap | `docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md` |
| Layer 2 — Master Overview | `docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md` |
| Layer 3 — Governance Anchors | `docs/anchors/governance/EXECUTION_MODEL_ANCHOR.md` |
| Layer 4 — Technical Anchors | `docs/anchors/technical/DB_STATUS_ANCHOR.md`, `docs/anchors/technical/OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md` |
| Layer 5 — Working Ledgers | `docs/aiid_registry.md`, `docs/BOUNDARY.md`, `docs/openclaw_training_status.md`, `docs/openclaw_registrar_apprentice_rubric.md` |
| Constitution | `constitution.md` + `docs/amendments/` |

All AiiD read Layers 0–2. Role-specific layers are referenced as
needed.

**Bootstrap read order remains unchanged.** This restructuring affects
document organization, not the conceptual reconstruction sequence.

---

## 8. Role Descriptions

**Librarian**
Focuses on institutional interpretation and continuity. Distinguishes
Librarian functions from Registrar functions. Uses the repository as
the primary reference for institutional memory.

**Proposer**
Works under restored institutional context. Grounds proposals in the
current repository state rather than session memory alone.

**OpenClaw**
Performs bounded execution tasks when explicitly instructed by the
Registrar. Does not initiate execution autonomously or act outside
defined task scope.

These descriptions help maintain consistent role behavior across
sessions and participants.

---

## 9. Execution Layer Summary

The execution layer is described in detail in:

```
docs/anchors/governance/EXECUTION_MODEL_ANCHOR.md
```

In summary, execution flows through role-based paths:

- Founder Direct Path: Founder → Registrar → Assistant Registrar
- Institutional Path: Collector → Proposer → Librarian → Registrar → Assistant Registrar
- Common Path: Librarian → Registrar → Assistant Registrar

Good execution practice involves bounded scope, explicit instruction,
precondition checking, and traceable recording.

---

## 10. Database Layer Summary

The database layer is described in detail in:

```
docs/anchors/technical/DB_STATUS_ANCHOR.md
```

In summary:
- Operational database: trading DB
- host: 192.168.250.11
- Market data: `public.board_snapshots`
- Collector status: `ops.collector_status`
- Institutional event log: `research.trace_event`
- Proposal persistence: `research.proposal`

---

## 11. OpenClaw Status Summary

OpenClaw's training and qualification state is described in detail in:

```
docs/anchors/technical/OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md
```

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

- implementing P-20260315-001 documentation simplification
- enabling OpenClaw as a practical Assistant Registrar execution node
- verifying claude_registrar database privileges before runner
  implementation
- maintaining clear role boundaries as the project grows

---

## 13. What This Document Does Not Cover

This anchor provides a high-level overview. The following topics are
covered in specialized documents:

- detailed DB schema → `docs/anchors/technical/DB_STATUS_ANCHOR.md`
- detailed execution rules → `docs/anchors/governance/EXECUTION_MODEL_ANCHOR.md`
- OpenClaw validation history → `docs/anchors/technical/OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md`
- full ledger content → working ledger documents

---

## 14. Stability Note

This master anchor is intended to remain stable and readable even as
lower-level documents evolve. When lower-level documents are updated,
this anchor should be checked for consistency.

This document reflects current state rather than constitutional
principles. Where they differ, `constitution.md` and
`ATOS_BOOTSTRAP_ANCHOR.md` reflect the higher-priority view.

---

## 15. Reference Map

| What you need | Where to find it |
|---|---|
| Project startup and read order | `docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md` |
| General AI onboarding | `docs/ai_participant_onboarding.md` |
| Execution rules | `docs/anchors/governance/EXECUTION_MODEL_ANCHOR.md` |
| Database state | `docs/anchors/technical/DB_STATUS_ANCHOR.md` |
| OpenClaw qualification | `docs/anchors/technical/OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md` |
| Participant registry | `docs/aiid_registry.md` |
| Role boundary definition | `docs/BOUNDARY.md` |
| OpenClaw training ledger | `docs/openclaw_training_status.md` |
| Evaluation rubric | `docs/openclaw_registrar_apprentice_rubric.md` |
| Enacted amendments | `docs/amendments/` |

---

## 16. Version History

| Version | Date | Change |
|---|---|---|
| 2.0 | 2026-03-12 | Initial anchor structure |
| 2.1 | 2026-03-14 | Tone revision (imperative → explanatory) |
| 2.2 | 2026-03-15 | P-20260315-001: new path structure, Layer 0 added, reference map updated |