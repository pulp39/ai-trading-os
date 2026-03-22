# P028_PHASE4_EXTERNAL_ORDER_ALLOWED_EVENT

Status: draft  
Date: 2026-03-22  
Phase: P-028 Phase 4

---

## Purpose

This document defines the institutional event design for:

```text
external_order_allowed = true

This state must be explicit, traceable, and independent from:

authorization_granted
execution_recorded
authorization_consumed

It is a distinct institutional permission layer.

1. Definition

external_order_allowed = true means:

An actual external order transmission is permitted for one bounded live
test under explicitly defined safety conditions.

It does not mean:

unrestricted live trading
repeated order permission
strategy deployment
autonomous execution rights
2. Why This Must Be Separate

The following states are distinct and must remain separate:

authorization_granted

The system is permitted to proceed toward execution under bounded
conditions.

execution_recorded (simulation)

The execution flow has been simulated.

execution_recorded (real_order_dry_run)

The real_order path has been dry-run validated.

external_order_allowed

The system is explicitly allowed to transmit an external order.

authorization_consumed

The one-time authorization has been spent by actual external
transmission.

These states must not collapse into one event.

3. Proposed Event Shape

Suggested trace_event structure:

event_type: external_order_allowed
actor_type: ai
agent_id: claude_registrar
Suggested content

A bounded minimal live real_order test was explicitly permitted under
Phase 4 conditions. External order transmission is allowed for a single
live test only, under minimum lot size, maximum loss bound, and explicit
abort conditions.

4. Required Metadata

The event metadata should include at minimum:

phase: P-028 Phase 4
linked_trace_event_phase1: 285
linked_trace_event_execution_simulation: 286
linked_trace_event_real_order_dry_run: 288
authorization_active: true
authorization_consumed: false
external_order_allowed: true
authorization_scope: single_execution
live_test_scope: single_minimal_order
minimum_lot_defined: true
maximum_loss_bound_defined: true
abort_condition_defined: true
bounded_environment_confirmed: true
autonomous_retry_allowed: false
capital_escalation_allowed: false
5. Preconditions

This event may be recorded only when all of the following are true:

authorization exists and remains active
authorization has not been consumed
execution simulation has been validated
real_order dry-run has been validated
minimum lot size is defined
maximum loss bound is defined
abort condition is defined
bounded environment is confirmed
explicit Founder-approved live test decision exists
6. Institutional Meaning

Once this event is recorded:

external_order_allowed = true

becomes institutionally valid.

However, this still does not itself transmit an order.

It only enables the next bounded step:

minimal live real_order execution
7. Separation Rule

The following sequence should remain explicit:

authorization_granted
→ execution_recorded (simulation)
→ execution_recorded (real_order_dry_run)
→ external_order_allowed
→ execution_recorded (live)
→ authorization_consumed

This order is institutionally safer than collapsing permission and
execution into one step.

8. Failure Handling

If any live-test boundary becomes unclear or invalid before order
transmission:

external_order_allowed should be treated as unusable
execution must stop
a new authorization review may be required

This prevents implicit carry-forward of risky permission states.

9. Draft Status

This document defines the proposed event model for explicit live-test
permission.

It should be reviewed before any Registrar task for live execution is
created.