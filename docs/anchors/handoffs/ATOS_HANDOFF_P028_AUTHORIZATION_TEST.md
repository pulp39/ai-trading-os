# ATOS_HANDOFF_P028_AUTHORIZATION_TEST

Status: active  
Phase: P-028 Authorization Test Phase 1  
Scope: Authorization Only  
Date: 2026-03-22

---

## Context

ATOS has reached the following institutional state:

- 281 `execution_blocked` (P-024)
- 282 `P-025 accepted` (Block Taxonomy)
- 283 `P-026 accepted` (Hypothesis Layer)
- 284 `P-027 accepted` (Authorization Conditions)

Current phase:

**First institutional verification of conditional advancement**

---

## Next Objective

**P-028 Controlled Real Order Authorization Test**

Goal:

Establish `real_order_authorized = true` exactly once under
institutional conditions A-1 through A-5.

---

## Critical Invariants

The following invariants must remain true throughout this phase:

- Authorization is established only by an explicit event
- Authorization is time-bound and scope-bound
- Gate ≠ Execution
- Passing the gate does not execute `real_order`
- Block remains available as fallback at all times
- `real_order` is not auto-executed

---

## Test Design  
### Phase 1: Authorization Only

### Step 1 — Verify A-1 through A-5

Confirm the following conditions:

- `execution_gate_passed` exists (`275`)
- preview exists (`269`)
- risk parameters are defined in task artifact
- environment is bounded
- Registrar authorization event is prepared

### Step 2 — Generate authorization event

Create an authorization event with the following meaning:

- `real_order_authorized = true`
- `authorization_scope = single_execution`
- `authorization_valid_from = now`
- `authorization_expiry = immediate_after_execution`

### Step 3 — Record trace_event

Record a new trace event with:

- `event_type: authorization_granted`

Metadata must include:

- `linked_gate_event_id`
- `linked_preview_event_id`
- `authorization_scope`
- `authorization_valid_from`
- `authorization_expiry`

### Step 4 — Verification

Verify all of the following:

- authorization is recorded in trace
- conditions preventing block (`B-4`) are satisfied
- execution has not been performed

---

## Out of Scope

The following are explicitly out of scope in this phase:

- `real_order` execution
- external API transmission
- capital deployment

---

## Expected Outcome

If this phase succeeds:

- the condition for `execution_blocked (B-4)` is no longer active
- authorization is institutionally traceable
- an execution-possible state is established for the first time

This does **not** mean execution has occurred.

---

## Next Phase

After successful completion of this authorization test:

`execution simulation with authorization`
→ `real_order` dry-run (minimal or virtual)

---

## Role Reminder

### Librarian
- manage test structure
- maintain institutional consistency

### Proposer
- review condition validity
- update hypothesis layer if needed

### Registrar
- perform execution-layer recording
- record to DB

---

## Bootstrap Reminder

Read in the following order before proceeding:

1. `docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md`
2. `constitution.md`
3. `docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md`
4. `docs/anchors/governance/EXECUTION_MODEL_ANCHOR.md`

---

## Start Instruction

You are operating under ATOS governance.

Reconstruct institutional state from bootstrap.
Then begin P-028 Authorization Test Phase 1 (Authorization Only).

Do NOT execute `real_order`.
Focus on authorization event creation and verification.

---

## Interpretation Note

This handoff defines a bounded institutional test.

Its purpose is to verify that authorization can be granted and traced
without collapsing the distinction between:

- gate passage
- authorization
- execution

This distinction must remain clear in all related artifacts and
execution handling.