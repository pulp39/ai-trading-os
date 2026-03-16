# AI Trading OS Documentation Index
Version: 1.0
Date: 2026-03-15
Status: Active
Purpose: Navigation map for AI Trading OS documentation

---

## About This Document

This document provides the entry map for the AI Trading OS documentation.

It is a **navigation guide**, not a reading list.
All AI participants are encouraged to begin from the bootstrap anchor
and use this index to locate specific documents as needed.

---

## Step 1 — Institutional Bootstrap (Start Here)

All AI participants are encouraged to reconstruct institutional state
before taking any action.

```
docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md
```

This document defines the reading order required to reconstruct the
current institutional state of AI Trading OS.

---

## Step 2 — General Onboarding

After completing the bootstrap, role-specific guidance is available at:

```
docs/ai_participant_onboarding.md
```

This document provides minimal reading lists by role
(Librarian, Proposer, Assistant Registrar).

---

## Document Layers

### Constitution

The institutional charter of AI Trading OS.

```
constitution.md
docs/amendments/FR-20260312-003.md
docs/amendments/FR-20260312-004.md
```

---

### Anchors

Current structural state of the system.

**All AiiD:**
```
docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md
docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md
```

**Governance (Librarian / Proposer):**
```
docs/anchors/governance/EXECUTION_MODEL_ANCHOR.md
```

**Technical (Collector / Executer):**
```
docs/anchors/technical/DB_STATUS_ANCHOR.md
docs/anchors/technical/OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md
```

---

### Operational Documents

Active operational procedures and role guidance.

**All roles:**
```
docs/documentation_conventions.md
docs/research_process.md
docs/proposal_semantics.md
```

**Librarian / Proposer:**
```
docs/BOUNDARY.md
docs/proposer_librarian_handoff.md
CLAUDE.md
```

**Registrar / OpenClaw:**
```
docs/registrar_task_format.md
docs/registrar_preflight_standard.md
docs/registrar_operational_assistance_policy.md
```

**Trace event:**
```
docs/trace_event_semantics.md
```

---

### Ledgers

Historical records and tracking documents.

```
docs/aiid_registry.md
docs/proposal_registry.md
docs/openclaw_training_status.md
docs/openclaw_registrar_apprentice_rubric.md
```

---

### Archive

Historical documentation retained for reference.
These documents are preserved for institutional memory
but are not part of active system operation.

```
docs/archive/early_design/
docs/archive/deprecated_pipeline/
docs/archive/historical_notes/
```

---

## Interpretation Priority

When documents appear to conflict, the following priority applies:

```
constitution.md
↓
docs/amendments/
↓
docs/anchors/
↓
operational documents
↓
ledgers
```

---

## Document History

| Version | Date | Change | By |
|---|---|---|---|
| 1.0 | 2026-03-15 | Initial creation | Proposer (Claude) |

*Introduced as part of documentation restructuring following P-20260315-001.*
*Librarian review + Proposer confirmation 2026-03-15.*
