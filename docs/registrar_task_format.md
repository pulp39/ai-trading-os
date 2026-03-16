# Registrar Task Format

Version: 1.0
Date: 2026-03-14
Status: active
Purpose: Canonical format specification for Registrar task payloads in
AI Trading OS

---

## 1. Purpose

This document defines the canonical format for Registrar task payloads
in AI Trading OS.

A Registrar task is the structured instruction unit passed from the
Registrar (or Founder direct path) to the executing participant
(Assistant Registrar).

This document must be interpreted consistently with:

- `docs/anchors/governance/EXECUTION_MODEL_ANCHOR.md`
- `docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md`

---

## 2. Minimum Required Fields

A valid Registrar task payload must contain the following minimum fields.

### 2.1 Task Identity

- `task_id` — unique identifier for this task
- `issuing_role` — role issuing the instruction (e.g., Registrar, Founder)
- `target_executor` — intended executing participant (e.g., openclaw_aux)

### 2.2 Scope

- `allowed_files` — explicit list of files permitted to be modified
- `prohibited_files` — files that must not be touched
- `allowed_branch_prefix` — sandbox branch prefix required for execution
- `intended_outcome` — plain-language description of the expected result

### 2.3 Preconditions

- `repository_check` — confirm correct repository is active
- `branch_check` — confirm execution is on an allowed branch
- `scope_check` — confirm task scope matches instruction
- `staged_file_verification` — explicit staged file check before commit

### 2.4 Execution Steps

Steps must be defined in order:

1. create / edit / verify target files
2. verify staged files
3. commit
4. push
5. trace_event handling (record or draft)

### 2.5 Stop Conditions

The task must define explicit stop conditions, including at minimum:

- precondition failure
- scope drift detected
- unauthorized file inclusion
- branch rule violation

### 2.6 Result Report

The executing participant must produce a result report containing:

- success / stopped / failed status
- short explanation of outcome
- resulting branch and commit summary where applicable
- trace_event result or draft status

---

## 3. Task Validity Rule

A Registrar task is considered institutionally valid only when:

- all minimum required fields are present
- the allowed branch prefix is consistent with sandbox branch policy
- the intended outcome is clearly stated
- stop conditions are explicitly defined

A task missing required fields must not be executed.

The executing participant must return the task for clarification rather
than proceed on assumptions.

---

## 4. Relation to Execution Model

This document defines the input specification for Registrar tasks.

The execution rules governing how tasks are carried out — including
precondition checks, scope limits, retry rules, commit validity, and
stop-on-failure behavior — are defined in:

`docs/anchors/governance/EXECUTION_MODEL_ANCHOR.md`

Task format and execution rules are related but separate concerns:

- this document answers: what must a valid task contain?
- EXECUTION_MODEL_ANCHOR.md answers: how must execution proceed?

---

## 5. Versioning

This format specification may be updated through institutional procedure.

Changes to the task format that affect existing execution pipelines must
be coordinated with updates to:

- `docs/anchors/governance/EXECUTION_MODEL_ANCHOR.md`
- `CLAUDE.md` (if Registrar execution protocol references this format)
- any runner implementation depending on this format

---

## 6. Final Rule

All Registrar task payloads must conform to this format before execution
is initiated.

The canonical Registrar task format reference is:

`docs/registrar_task_format.md`
```

---

## 変更サマリー
```
EXECUTION_MODEL_ANCHOR.md:
  Section 14  : 内容削除 → docs/registrar_task_format.md への参照に置き換え
  Section 19  : OpenClaw詳細削除 → OPENCLAW anchor への参照に簡略化
  Section 20  : docs/registrar_task_format.md への参照を追加
  Version     : 1.0 → 1.1

docs/registrar_task_format.md (新規):
  Section 1   : Purpose
  Section 2   : Minimum Required Fields (旧 Section 14 の内容)
  Section 3   : Task Validity Rule
  Section 4   : Relation to Execution Model (境界の明示)
  Section 5   : Versioning
  Section 6   : Final Rule