# ATOS_BOOTSTRAP_ANCHOR

Version: 1.1
Date: 2026-03-14
Status: active
Purpose: Single canonical startup source for institutional reconstruction in AI Trading OS

---

## 1. Purpose

This document is the single canonical startup source for all AI participants
operating under the AI Trading OS institutional governance model.

Its purpose is to ensure that all participants reconstruct the same
institutional state from the same repository clone, using the same read
order, interpretation priority, and startup behavior.

This bootstrap anchor exists to prevent startup drift, role confusion,
partial reconstruction, and instruction conflicts across AI participants.

---

## 2. Canonical Repository

Canonical repository:

`ai-trading-os-private`

Local working copy:

`/home/vmamako/ai-trading-os-private`

All institutional participants must treat the canonical repository and its
synchronized local clone as the source of truth for institutional
reconstruction.

No participant may treat chat history, partial excerpts, memory alone, or
inferred context as a substitute for repository bootstrap.

---

## 3. Applies To

This bootstrap anchor applies to all institutional participants, including:

- Librarian
- Proposer
- OpenClaw

This document must be treated as the common startup entry point across all
three roles.

---

## 4. Bootstrap Determinism Rule

All institutional reconstruction must begin from this file:

`docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md`

No participant may skip the bootstrap anchor and infer institutional state
from partial files, prior assumptions, or role-native heuristics alone.

Institutional reconstruction must follow the documented read order strictly.

If a participant has not completed the bootstrap sequence, that participant
is not yet considered institutionally synchronized.

---

## 5. Startup Instruction

The canonical startup instruction for all participants is:
```text
Begin institutional reconstruction from:
docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md
```

For Claude-family participants, the following auxiliary startup instruction
may be used:
```text
Begin institutional reconstruction from:
docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md
Then follow CLAUDE.md in a way consistent with constitution.md
```

---

## 6. Required Read Order

All participants must reconstruct institutional state by reading the
following files in this exact order:

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

No substitution of read order is permitted unless a higher-priority
document explicitly requires it.

---

## 7. Interpretation Priority

If documents differ in scope, emphasis, or apparent instruction strength,
interpretation must follow this priority order:

1. constitution.md
2. CLAUDE.md
   (CLAUDE.md must not override constitution.md)
3. docs/aiid_registry.md
4. docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md
5. docs/anchors/EXECUTION_MODEL_ANCHOR.md
6. docs/anchors/DB_STATUS_ANCHOR.md
7. docs/anchors/OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md
8. README.md

Interpretation priority defines conflict resolution authority, not reading
sequence.

Read order and interpretation priority are related but not identical.

---

## 8. Conflict Resolution Rule

If two documents appear to conflict, the higher-priority document prevails
over the lower-priority document.

The conflict resolution rule is:

- constitution.md prevails over all lower documents
- CLAUDE.md may define Claude-family operating behavior, but may not
  violate or replace the constitution
- this bootstrap anchor governs startup reconstruction behavior unless
  doing so would violate constitution.md
- lower anchors, ledgers, and README files must be interpreted in a way
  consistent with higher documents

If an apparent contradiction remains unresolved, the participant must adopt
the most conservative interpretation consistent with the constitution and
institutional safety.

---

## 9. Role-Specific Startup Behavior

### 9.1 Librarian

The Librarian must:

- reconstruct current institutional state
- interpret governance structure conservatively
- avoid acting as Registrar unless explicitly instructed
- use the repository as the institutional memory base
- prioritize consistency, interpretation safety, and continuity

The Librarian is responsible for institutional coherence, anchor
interpretation, and governance continuity support.

### 9.2 Proposer

The Proposer must:

- complete bootstrap reconstruction before drafting proposals
- treat bootstrap state as the institutional baseline for proposal work
- avoid proposal drafting based on partial context alone
- follow CLAUDE.md only in a way consistent with constitution.md and
  this bootstrap anchor
- avoid treating role-native prompting as a substitute for institutional
  reconstruction

The Proposer is responsible for structured proposal generation under the
restored institutional state.

### 9.3 OpenClaw

OpenClaw must:

- complete bootstrap reconstruction before acting on registrar-related tasks
- recognize that it is not authorized for autonomous institutional execution
- act only under explicit Registrar instruction when functioning as
  Assistant Registrar
- treat training anchors, rubric, and execution rules as binding operational
  constraints after bootstrap
- stop on failed preconditions or scope ambiguity

OpenClaw operates as a constrained execution participant, not as an
autonomous policy actor.

---

## 10. Execution Baseline

The execution model for AI Trading OS is defined in full in:

`docs/anchors/EXECUTION_MODEL_ANCHOR.md`

Summary:

- Execution follows recognized institutional chains
- Assistant Registrar acts only under explicit Registrar instruction
- Sandbox branch prefixes are mandatory for Assistant Registrar activity
- Preconditions must be verified before any execution action
- Stopping on failed preconditions is valid disciplined behavior

For full execution chain definitions, precondition requirements, branch
policy, task format, and stop conditions, see EXECUTION_MODEL_ANCHOR.md.

---

## 11. Institutional State Map

This bootstrap anchor restores the institutional map by directing
participants to the specialized anchors and ledgers below.

### 11.1 Current institutional state

See: `docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md`

This file contains the governance state, active structure, accepted
high-level institutional status, canonical repository rule, and current
execution-layer summary.

### 11.2 Execution model

See: `docs/anchors/EXECUTION_MODEL_ANCHOR.md`

This file contains the execution chain rules, Assistant Registrar rules,
sandbox branch rule, mandatory precondition rule, retry rule, execution
result format, and Registrar task format.

### 11.3 Database status

See: `docs/anchors/DB_STATUS_ANCHOR.md`

This file contains the database host, access context, schema map, core
tables, known users, and current DB design rules.

### 11.4 OpenClaw training state

See: `docs/anchors/OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md`

This file contains OpenClaw training completion state, validation history,
current qualification status, and execution constraints.

### 11.5 Working ledgers

See:

- docs/aiid_registry.md
- docs/BOUNDARY.md
- docs/openclaw_training_status.md
- docs/openclaw_registrar_apprentice_rubric.md

These files are working ledgers and operational references subordinate to
the higher institutional documents.

---

## 12. Claude-Family Bootstrap Rule

For Claude-family participants:

Before proposal drafting, registrar action, or institutional
interpretation, begin institutional reconstruction from:

`docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md`

- If CLAUDE.md conflicts with constitution.md, constitution.md prevails.
- If CLAUDE.md conflicts with this bootstrap anchor on startup order,
  follow the bootstrap anchor unless that would violate constitution.md.
- Claude-family role-native behavior is valid only after institutional
  bootstrap is completed.

---

## 13. Repository Reconstruction Rule

Institutional reconstruction is considered complete only when the
participant has:

- identified the canonical repository
- synchronized to the correct local working copy
- read the required files in order
- applied the interpretation priority correctly
- recognized role-specific operating limits

A participant that has not completed these steps must not claim full
institutional alignment.

---

## 14. Anti-Drift Rule

To prevent institutional drift:

- do not reconstruct from memory alone
- do not reconstruct from chat fragments alone
- do not reconstruct from a single role-specific file alone
- do not treat README as constitution-level authority
- do not treat training logs as governance authority
- do not treat role-native prompt habits as superior to repository bootstrap

Repository bootstrap is mandatory for stable institutional continuity.

---

## 15. Operational Goal

The operational goal of this anchor system is:
```
One canonical repository
        ↓
One local clone
        ↓
One bootstrap anchor
        ↓
Shared institutional reconstruction across Librarian, Proposer, and OpenClaw
```

This enables deterministic restoration of:

- institutional state
- execution model
- database status
- OpenClaw training status

from the same clone.

---

## 16. Immediate Next Documents

After this bootstrap anchor is established, the following documents must
remain aligned with it:

- CLAUDE.md
- docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md
- docs/anchors/EXECUTION_MODEL_ANCHOR.md
- docs/anchors/DB_STATUS_ANCHOR.md
- docs/anchors/OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md
- docs/openclaw_training_status.md
- docs/openclaw_registrar_apprentice_rubric.md

These documents must not drift away from the bootstrap model.

---

## 17. Final Rule

All participants begin institutional reconstruction from:

`docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md`

This file is the single canonical startup source for institutional
reconstruction in AI Trading OS.
```

---

改訂内容のサマリー：
```
Section 5  : "Read and obey" → "Begin institutional reconstruction from"
Section 10 : 詳細ルール削除 → 4行の概要 + EXECUTION_MODEL_ANCHOR.md への参照
Section 12 : "Read and obey" → "begin institutional reconstruction from"
Section 17 : 簡略化、"Read and obey" 除去
その他     : 変更なし