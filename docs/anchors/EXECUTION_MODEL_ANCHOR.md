# EXECUTION_MODEL_ANCHOR

Version: 1.0  
Date: 2026-03-14  
Status: active  
Purpose: Canonical execution model reference for institutional and registrar-linked execution in AI Trading OS

---

## 1. Purpose

This document defines the canonical execution model for AI Trading OS.

It specifies how institutional intent becomes bounded execution, how Assistant Registrar participation is constrained, and what minimum execution discipline is required for institutional validity.

This anchor must be interpreted consistently with:

- `constitution.md`
- `docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md`
- `docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md`

---

## 2. Execution Chain Rule

AI Trading OS uses bounded, role-mediated execution.

Execution must follow recognized institutional chains rather than free autonomous action.

The canonical execution chains are defined below.

---

## 3. Founder Direct Path

The Founder Direct Path is:

Founder → Registrar → Assistant Registrar

This path is used when the Founder authorizes a bounded execution action directly through the execution layer.

The Assistant Registrar may act only after explicit Registrar instruction.

---

## 4. Institutional Path

The Institutional Path is:

Collector → Proposer → Librarian → Registrar → Assistant Registrar

This path is used when institutional observations or proposals move through the governance structure into bounded execution.

This is the full institutional path from observation to constrained action.

---

## 5. Common Execution Path

The most common practical execution path is:

Librarian → Registrar → Assistant Registrar

This path is used for bounded operational tasks that do not require a full observation-to-proposal cycle.

---

## 6. Assistant Registrar Rule

Assistant Registrar is an execution-constrained participant.

Assistant Registrar may act only when all of the following are true:

- explicit Registrar instruction exists
- execution scope is bounded
- required preconditions are satisfied
- branch policy is respected
- execution result can be institutionally recorded

Assistant Registrar is not authorized for autonomous policy formation, autonomous governance interpretation, or unbounded repository modification.

---

## 7. Assistant Registrar Authorization Scope

Assistant Registrar may perform bounded execution tasks such as:

- file creation or modification within approved scope
- branch-based repository work
- commit and push within allowed branch policy
- trace_event payload drafting
- registrar task payload drafting
- bounded documentation updates
- execution reporting

Assistant Registrar may not:

- rewrite institutional structure autonomously
- modify `main` without proper authorization
- bypass precondition checks
- expand scope beyond explicit task bounds
- claim Registrar authority

---

## 8. Execution Sandbox Branch Rule

Assistant Registrar may operate only on branches using the following approved prefixes:

- `assistant/test/`
- `assistant/docs/`
- `assistant/trace/`
- `assistant/pr/`

These prefixes define the sandbox execution surface for Assistant Registrar activity.

Direct modification of `main` is prohibited unless explicitly authorized through the institutional chain and approved where required.

---

## 9. Mandatory Precondition Rule

Before any execution action, the executing participant must verify preconditions.

Minimum precondition checks include:

1. correct repository
2. correct branch
3. intended files only
4. scope still matches instruction
5. no disallowed files staged
6. execution target is institutionally valid

If preconditions fail, execution must stop.

Stopping on failed preconditions is a valid success condition for institutional discipline.

---

## 10. Scope Limitation Rule

Execution must remain limited to the stated task.

No participant may silently widen scope because related changes appear useful, elegant, or efficient.

If scope expansion seems necessary, that must be returned for renewed instruction rather than self-authorized during execution.

Bounded execution is more important than opportunistic completeness.

---

## 11. Staged File Verification Rule

Before commit, staged files must be checked explicitly.

The executing participant must confirm that:

- only intended files are staged
- no unrelated files are included
- no accidental environment artifacts are present
- no protected files are being modified without authorization

If staged files exceed scope, execution must stop or be corrected before commit.

---

## 12. Retry Rule

Retry is permitted only when the retry remains within the originally authorized scope.

Valid retry cases include:

- command syntax correction
- file path correction
- branch naming correction
- formatting correction
- push retry after transient failure

Invalid retry cases include:

- expanding the file set
- changing institutional meaning
- modifying protected targets without renewed instruction
- converting a bounded task into an unbounded refactor

Retry is corrective, not expansive.

---

## 13. Execution Result Format

A valid execution result report should include, at minimum:

- task identifier or task summary
- execution scope
- precondition result
- files changed
- commit result
- push result
- trace_event result or trace_event draft status
- stop reason if execution halted

Institutional execution should be legible and reviewable after the fact.

---

## 14. Registrar Task Format v1

A Registrar task should contain the following minimum fields:

### 14.1 Task identity
- task_id
- issuing role
- target executor

### 14.2 Scope
- allowed files
- prohibited files
- allowed branch prefix
- intended outcome

### 14.3 Preconditions
- repository check
- branch check
- scope check
- staged file verification requirement

### 14.4 Execution steps
- create / edit / verify
- commit
- push
- trace_event handling

### 14.5 Stop conditions
- precondition failure
- scope drift
- unauthorized file inclusion
- branch rule violation

### 14.6 Result report
- success / stopped / failed
- short explanation
- resulting branch and commit summary where applicable

---

## 15. Commit Rule

A commit is institutionally valid only when:

- the scope stayed bounded
- preconditions were respected
- staged files matched the intended task
- the commit occurred on an allowed branch
- the action is reportable in institutional terms

A technically successful commit that violates execution discipline is not institutionally valid execution.

---

## 16. Push Rule

Push is allowed only after commit validity conditions are met.

Push must target the authorized remote and remain within sandbox branch policy unless explicitly authorized otherwise.

A successful push does not by itself establish institutional validity.

---

## 17. trace_event Rule

Institutionally meaningful execution should be recorded in `research.trace_event` or prepared as a trace_event draft for later insertion.

trace_event should reflect:

- what action was performed
- by which actor role
- under what bounded scope
- with what outcome

Execution without recordability is considered incomplete institutionalization.

---

## 18. Stop-on-Failure Rule

Correct stopping is an expected part of execution discipline.

Stopping because of:

- precondition failure
- branch policy violation
- scope ambiguity
- unauthorized staged files

is institutionally valid behavior and should be treated as disciplined compliance, not as mere failure.

---

## 19. OpenClaw Execution Position

OpenClaw is validated as an Assistant Registrar-capable participant only under explicit Registrar instruction.

Its authority is execution-bounded, not governance-originating.

OpenClaw may:

- commit
- push
- prepare trace_event recording
- prepare registrar task payloads

only within the authorized execution model and only within permitted scope.

---

## 20. Relation to Other Anchors

For startup reconstruction, see:

`docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md`

For current institutional state, see:

`docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md`

For database state and trace_event environment, see:

`docs/anchors/DB_STATUS_ANCHOR.md`

For OpenClaw qualification state, see:

`docs/anchors/OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md`

---

## 21. Final Rule

Execution in AI Trading OS must be:

- bounded
- role-mediated
- reviewable
- recordable
- institutionally legible

Autonomous execution without bounded institutional authorization is not part of the valid execution model.