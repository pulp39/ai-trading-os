anchor_id: EXECUTION_SAFETY_ANCHOR
title: Execution Safety and Consumption Model
type: governance
status: active
version: 1.1
date: 2026-04-10
---

# EXECUTION SAFETY ANCHOR

## Purpose

Define the execution safety model of ATOS, including consumption and duplicate prevention.

This anchor ensures that execution is:
- non-repeatable
- traceable
- bounded
- safe for future real_order integration

---

## Core Principle

1 READY context = 1 execution

A READY context is a consumable resource.
It can be used exactly once.

---

## READY Context

Each READY state generates a unique identifier:

ready_context_id = rctx-YYYYMMDD-NNNN

This ID is attached to all execution-related events.

---

## Context States

- active: execution allowed
- consumed: execution already performed
- invalidated: context is unsafe
- expired: TTL exceeded

---

## State Transitions

active → consumed      (execution_performed)
active → invalidated   (execution_failed / kill switch / invalid data)
active → expired       (TTL exceeded)

No reverse transition is allowed.

---

## Duplicate Execution Prevention

Execution Gate must enforce:

if state != active:
    NO_GO

and record:

event_type: execution_blocked
reason:
- duplicate:consumed
- duplicate:invalidated
- duplicate:expired

---

## Trace Requirements

The following events must exist:

- execution_readiness_evaluated
- execution_performed
- execution_consumed
- execution_blocked

---

## Consumption Principle

Execution consumes the context.

After consumption:
- no retry
- no reuse
- no replay

---

## Non-Reversibility

Once a context is:
- consumed
- invalidated
- expired

it can never return to active.

---

## Operational Meaning

Execution permission is not persistent.

A new execution always requires:
Observation → Preview → READY

---

## Phase Status

This model is fully implemented and validated in Phase 9B.

It is a prerequisite for:
Phase 9B-3 (real_order connection)

---

## Executer (Codex) — Scope Note（P-20260410-002）

Codex is newly established as Executer role (2026-04-10).

Execution safety constraints defined in this anchor apply to ALL execution agents,
including Codex:

- 1 READY context = 1 execution (non-repeatable)
- All WRITE operations must produce a corresponding trace_event
- Execution Gate must enforce state validation before any WRITE
- No state mutation / No external order / No partial execution on failure

**Codex-specific boundary:**
Detailed execution boundaries for Codex are to be established via a separate
Codex onboarding Proposal. Until that Proposal is accepted:
- Codex operates under P-20260409-001 (Phase 10 Failure Discipline) principles
- Codex does NOT execute real_order operations
- All Codex execution requires explicit Librarian or Founder authorization

---

## Phase Status（更新）

| Phase | 状態 |
|-------|------|
| Phase 9B | ✅ 完全実装・検証済み |
| Phase 10 | 🔄 Failure Discipline テスト進行中（P-20260409-001） |

This model is a prerequisite for:
- Phase 9B-3 (real_order connection)
- Codex Executer onboarding
