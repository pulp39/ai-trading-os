# ATOS Documentation Inventory Review
AI Trading OS

Status: Active Working Document
Maintained by: Librarian
Purpose: Repository document classification and structural review

---

## 1. Purpose

This document provides a structured inventory of repository documents
to evaluate alignment with the current ATOS anchor system
(introduced by P-20260315-001).

The goal is **classification**, not deletion.

Documents are categorized into four groups:

- **Canonical** — required to reconstruct institutional state
- **Operational** — used in daily system operation
- **Ledger** — historical or tracking records
- **Archive Candidate** — role unclear, superseded, or legacy

No document should be removed without explicit institutional review.

---

## 2. Classification Model

### Canonical

Documents required to reconstruct institutional state.
These form the core institutional layer and should remain stable.
Referenced in the bootstrap read order.

### Operational

Documents used in daily system operation.
Important but not required for system reconstruction.
Referenced by role as needed.

### Ledger

Historical or tracking documents.
Record system evolution but do not define governance.

### Archive Candidate

Documents that reflect legacy structures, superseded documentation,
or unclear responsibility. Relocated to `docs/archive/` rather than
deleted, to preserve institutional memory.

---

## 3. Canonical Documents

| Path | Status | Notes |
|---|---|---|
| `constitution.md` | Keep | Institutional charter (v1.4) |
| `docs/amendments/FR-20260312-003.md` | Keep | Constitutional amendment: execution authority |
| `docs/amendments/FR-20260312-004.md` | Keep | Constitutional amendment: AI identity |
| `docs/ai_participant_onboarding.md` | Keep | Layer 0 onboarding (v1.2 pending) |
| `docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md` | Keep | Bootstrap entry point |
| `docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md` | Keep | Institutional state map (v2.2) |
| `docs/anchors/governance/EXECUTION_MODEL_ANCHOR.md` | Keep | Governance execution model |
| `docs/anchors/technical/DB_STATUS_ANCHOR.md` | Keep | Technical system state |
| `docs/anchors/technical/OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md` | Keep | Registrar technical anchor |
| `docs/trace_event_semantics.md` | Keep | trace_event semantic definition |

---

## 4. Operational Documents

| Path | Status | Notes |
|---|---|---|
| `CLAUDE.md` | Keep | Proposer role guidance (Claude-family) |
| `docs/BOUNDARY.md` | Keep | Librarian/OpenClaw role boundary — constitution Article 5 implementation |
| `docs/documentation_conventions.md` | Keep | Documentation tone and style |
| `docs/proposal_semantics.md` | Keep | Proposal structure definition |
| `docs/registrar_task_format.md` | Keep | Registrar task payload format |
| `docs/registrar_preflight_standard.md` | Keep | Registrar execution safety checklist |
| `docs/registrar_operational_assistance_policy.md` | Keep (revision needed) | Delegation policy for openclaw_aux — incomplete sections require revision; tone adjustment recommended |
| `docs/research_process.md` | Keep | Research workflow specification — reference to institutional_model.md to be updated to MASTER_ANCHOR |
| `docs/proposer_librarian_handoff.md` | Keep | Current handoff standard (replaces librarian_proposer_interaction.md) |

**Future placement notes:**
- `docs/BOUNDARY.md` — candidate for `docs/governance/` when that layer matures
- `docs/proposer_librarian_handoff.md` — candidate for `docs/governance/` when that layer matures

---

## 5. Ledger Documents

| Path | Status | Notes |
|---|---|---|
| `docs/aiid_registry.md` | Keep | AI participant registry |
| `docs/openclaw_training_status.md` | Keep | OpenClaw training chronological record |
| `docs/openclaw_registrar_apprentice_rubric.md` | Keep | Training evaluation artifact |
| `docs/proposal_registry.md` | Keep | Proposal ledger |

---

## 6. Archive Candidates

| Path | Recommended Archive Path | Reason |
|---|---|---|
| `docs/claude_onboarding_prompt.md` | `docs/archive/historical_notes/` | Superseded by `docs/ai_participant_onboarding.md` |
| `docs/institutional_model.md` | `docs/archive/early_design/` | Conceptual explanation absorbed by constitution + MASTER_ANCHOR |
| `docs/proposal_execution_flow.md` | `docs/archive/deprecated_pipeline/` | Legacy institutional pipeline (pre-Registrar model) |
| `docs/librarian_proposer_interaction.md` | `docs/archive/early_design/` | Pre-constitution governance model; replaced by `proposer_librarian_handoff.md` |

---

## 7. Archive Structure

Recommended archive directory:

```
docs/archive/
  early_design/         ← initial institutional design documents
  deprecated_pipeline/  ← legacy execution pipeline documents
  historical_notes/     ← superseded operational notes
```

All archived documents should include a header:

```
---
archive_status: archived
archived_date: YYYY-MM-DD
archived_reason: [reason]
archived_by: Librarian review — Phase 3 documentation restructuring
---
```

---

## 8. Review Priority (Reference)

Documents reviewed in Phase 2 in the following order:

1. `docs/BOUNDARY.md` → Operational (reclassified from Ledger)
2. `docs/librarian_proposer_interaction.md` → Archive Candidate
3. `docs/proposer_librarian_handoff.md` → Operational
4. `docs/registrar_preflight_standard.md` → Operational
5. `docs/registrar_task_format.md` → Operational
6. `docs/registrar_operational_assistance_policy.md` → Operational (revision needed)
7. `docs/research_process.md` → Operational
8. `docs/institutional_model.md` → Archive Candidate
9. `docs/proposal_execution_flow.md` → Archive Candidate
10. `docs/openclaw_training_status.md` → Ledger
11. `docs/openclaw_registrar_apprentice_rubric.md` → Ledger

---

## 9. Next Steps

**Phase 3 — Archive Reclassification**

1. Add archive headers to the 4 Archive Candidate files
2. Create `docs/archive/` directory structure
3. Relocate Archive Candidates using `git mv`
4. Commit: `docs: archive legacy documents after anchor restructuring (Phase 3)`

**Phase 4 — Documentation Completion**

1. Update `docs/ai_participant_onboarding.md` v1.2 (bootstrap priority note)
2. Create `docs/DOCS_MASTER_INDEX.md`
3. Formalize as P-20260315-002

---

## 10. Document History

| Version | Date | Change | By |
|---|---|---|---|
| 1.0 | 2026-03-15 | Initial inventory — full repository scan (24 files) | Proposer (Claude) |
| 1.1 | 2026-03-15 | Phase 2 review results integrated; BOUNDARY reclassified to Operational; Archive plan added; future placement notes added | Librarian + Proposer |
