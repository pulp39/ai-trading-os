# EXECUTION_MODEL_ANCHOR
Version: 1.3
Date: 2026-03-16
Status: active
Purpose: Execution model reference for AI Trading OS

---

## 1. About This Document

This document describes the execution model for AI Trading OS.
It explains how institutional intent becomes bounded action, how the
Assistant Registrar role participates in execution, and what execution
discipline looks like in this project.

This document is intended to be read alongside:

- `constitution.md`
- `docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md`
- `docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md`

---

## 2. How Execution Works in This Project

AI Trading OS uses role-mediated, bounded execution rather than
autonomous action. Execution flows through recognized paths involving
Founder, Registrar, and Assistant Registrar roles. The paths are
described below.

---

## 3. Founder Direct Path

```
Founder → Registrar → Assistant Registrar
```

Used when the Founder authorizes a bounded action directly through
the execution layer. The Assistant Registrar acts after explicit
Registrar instruction.

---

## 4. Institutional Path

```
Collector → Proposer → Librarian → Registrar → Assistant Registrar
```

Used when observations or proposals move through the full governance
structure into bounded execution.

---

## 5. Common Execution Path

```
Librarian → Registrar → Assistant Registrar
```

The most common practical path for bounded operational tasks that do
not require a full observation-to-proposal cycle.

---

## 6. Assistant Registrar Role

The Assistant Registrar performs bounded execution tasks under explicit
Registrar instruction. Execution is appropriate when:

- explicit Registrar instruction exists
- execution scope is clearly defined
- preconditions have been verified
- branch policy is respected
- the result can be recorded institutionally

The Assistant Registrar role is execution-focused rather than
governance-originating. It does not autonomously form policy or
interpret governance documents.

---

## 7. What the Assistant Registrar Can Do

When acting under explicit Registrar instruction, the Assistant
Registrar may perform tasks such as:

- file creation or modification within approved scope
- branch-based repository work
- commit and push within allowed branch policy
- trace_event payload drafting
- registrar task payload drafting
- bounded documentation updates
- execution reporting

The role is not designed for:

- autonomous rewriting of institutional structure
- modifying main without proper authorization
- bypassing precondition checks
- expanding scope beyond explicit task bounds
- acting with Registrar-level authority

---

## 8. Sandbox Branch Policy

By default, Assistant Registrar activity takes place on sandbox
branches with the following prefixes:

- `assistant/test/`
- `assistant/docs/`
- `assistant/trace/`
- `assistant/pr/`

Direct modification of main follows an explicit authorization path
involving Registrar instruction and, where appropriate, Founder
approval.

---

## 9. Precondition Checks

Before taking any execution action, verifying the following helps
ensure the action is within scope and safe:

- correct repository is active
- correct branch is checked out
- only intended files are in scope
- scope still matches the instruction
- no disallowed files are staged
- execution target is institutionally valid

If preconditions are not met, stopping and returning for clarification
is the appropriate response — and is considered good execution
discipline, not a failure.

---

## 9.1 AiiD Activity Authorization Check

Before executing any instruction involving an AiiD participant,
the activity authorization state of the AiiD may be verified.

The authorization mechanism is defined in:

```
founder_records/proposals/FR-20260316-001.md
```

Current implementation: Stub Phase

```
activity_authorization(aiid) → returns 1
```

During the stub phase, all institutionally recognized AiiD
participants are considered authorized. This check serves as a
placeholder for future authorization logic and does not affect
current execution behavior.

When the stub phase ends, this check becomes an active gate
in the execution flow.

---

## 10. Scope

Execution stays within the stated task scope. If related changes
appear useful or efficient but were not part of the original
instruction, the appropriate path is to raise them for renewed
instruction rather than including them autonomously.

Bounded execution is a design principle of this project, not a
limitation.

---

## 11. Staged File Verification

Before committing, checking staged files explicitly helps avoid
unintended changes:

- only intended files are staged
- no unrelated files are included
- no environment artifacts are staged
- no protected files are included without authorization

If staged files exceed scope, correcting before commit is the right
approach.

---

## 12. Retry

Retry is appropriate when the retry stays within the originally
authorized scope.

Appropriate retry cases:
- command syntax correction
- file path correction
- branch naming correction
- formatting correction
- push retry after transient failure

Retry is not appropriate for:
- expanding the file set
- changing institutional meaning
- modifying protected targets without renewed instruction
- converting a bounded task into an unbounded refactor

---

## 13. Execution Result Format

A useful execution result report includes:

- task identifier or summary
- execution scope
- precondition result
- files changed
- commit result
- push result
- trace_event result or draft status
- stop reason if execution halted

Clear reporting makes execution reviewable and supports institutional
traceability.

---

## 14. Registrar Task Format

The format for Registrar task payloads is described in:

```
docs/registrar_task_format.md
```

That document specifies the minimum fields and structure for a valid
task payload.

---

## 15. Commit Validity

A commit reflects good execution discipline when:

- scope stayed bounded
- preconditions were respected
- staged files matched the intended task
- the commit occurred on an allowed branch
- the action is describable in institutional terms

A technically successful commit that bypasses execution discipline
does not represent valid institutional execution.

---

## 16. Push

Push follows commit validity. It targets the authorized remote and
respects sandbox branch policy unless explicitly authorized otherwise.

A successful push is part of execution, not the sole measure of
institutional validity.

---

## 17. trace_event Recording

Institutionally meaningful execution is recorded in
`research.trace_event` or prepared as a trace_event draft.

A trace_event captures:
- what action was performed
- by which role
- within what scope
- with what outcome

Recording supports the project's goal of making execution reviewable
and reconstructible.

---

## 18. Stopping as Good Practice

Stopping execution because of a failed precondition, branch policy
concern, scope ambiguity, or unexpected staged files is expected and
appropriate behavior. It is treated as disciplined compliance with the
execution model, not as failure.

---

## 19. OpenClaw Execution Role

OpenClaw participates as an Assistant Registrar when explicitly
instructed by the Registrar.

Its role is limited to bounded execution within system scope and does
not extend to external execution authority.

### 19.1 Execution Capability vs Authority

Execution in AI Trading OS is separated into:

- execution capability (system-side readiness)
- execution authority (external transmission control)

OpenClaw possesses execution capability but does not possess execution
authority.

### 19.2 Execution Readiness

OpenClaw can:

- validate execution conditions
- perform dry-run procedures
- prepare registrar tasks
- reach a READY_FOR_EXECUTION state

Execution readiness represents a fully prepared state within the
institutional system, but it does not constitute execution itself.

### 19.3 Execution Boundary

Execution is defined as:

> the initiation of external transmission

This includes:

- API order submission
- any outbound action affecting external systems

OpenClaw does not cross this boundary.

### 19.4 Human Execution Layer

External execution is performed through a human-controlled layer:

```text
Observation → Proposal → Gate → Authorization
→ Assistant Registrar (OpenClaw: execution preparation)
        ↓
Human Execution Layer (Founder: execution authority)
        ↓
External Systems (APIs / Markets)

Only the Human Execution Layer holds execution authority.

19.5 Authorization Lifecycle

Before execution:

authorization_granted (permission exists)

At execution moment:

authorization_consumed (irreversible)

Characteristics of authorization_consumed:

triggered at external transmission
independent of outcome (success/failure/unknown)
non-reversible
19.6 Safety Lock

After execution:

post_submit_safety_lock is applied

This prevents:

duplicate submission
unintended retries
re-consumption of authorization
19.7 Scope Limitation

OpenClaw must not:

initiate external execution
bypass execution authority boundaries
simulate external execution as completed
perform actions that imply capital deployment

Its role remains strictly within execution preparation.

For institutional boundary definitions, see:

docs/BOUNDARY.md

---

## 20. Related Documents

| Document | What it covers |
|---|---|
| `docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md` | Project startup and read order |
| `docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md` | Current institutional state |
| `docs/anchors/technical/DB_STATUS_ANCHOR.md` | Database state and trace_event environment |
| `docs/anchors/technical/OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md` | OpenClaw qualification |
| `docs/registrar_task_format.md` | Registrar task payload format |
| `founder_records/proposals/FR-20260316-001.md` | AiiD Activity Authorization Bit definition |

---

## 21. Summary

Execution in AI Trading OS is:

- bounded by explicit instruction
- role-mediated through recognized paths
- reviewable through execution reporting
- recordable via trace_event
- institutionally legible

This design enables AI participants to collaborate safely within a
shared governance framework.

---

## 22. Execution Governance Summary

Execution in AI Trading OS is defined by the following principles:

- Execution capability ≠ execution authority
- Execution authority is human-controlled
- Execution occurs at external transmission
- Authorization is consumed at execution moment
- Post-execution state is locked (safety lock)

This model ensures:

- clear separation of responsibility
- prevention of unintended capital deployment
- traceable and reviewable execution flow

Execution is not defined by script completion, but by
institutional boundary crossing.
