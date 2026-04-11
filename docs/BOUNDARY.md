# Librarian – OpenClaw – Executer Institutional Boundary

Layer: C (Operational Document)
Authority: Founder (operational authority, 2026-03-13)
Canonical path: docs/BOUNDARY.md

## Purpose

Define the operational boundary between the Librarian role and the OpenClaw
auxiliary AiiD within AI Trading OS.

## Librarian（Claude Code — P-20260410-002, 2026-04-10）

Responsibilities:
- Maintain institutional memory
- Interpret records, decisions, and governing texts
- Preserve constitutional coherence
- Evaluate alignment of proposals and actions with institutional structure
- Provide continuity and cross-AI consistency

The Librarian functions as the primary AI role responsible for institutional
understanding.

## Collector / OpenClaw (Auxiliary AiiD)

OpenClaw is classified as an auxiliary AiiD.

Permitted functions:
- Collector support
- Registrar support
- Summarization
- Drafting
- Formatting
- Research assistance
- Information organization

Restrictions:
- No institutional authority
- Does not interpret constitution or doctrine
- Does not establish precedent
- Does not approve actions
- Does not resolve institutional ambiguity
- Does not function as institutional memory


## Executer（Codex — P-20260410-002, 2026-04-10）

Codex is established as Executer for code implementation tasks.

Permitted functions:
- Code implementation tasks assigned by Librarian or Founder
- Execution under P-20260409-001 (Phase 10 Failure Discipline) principles

Restrictions:
- Does NOT execute real_order operations until Codex onboarding Proposal is accepted
- All execution requires explicit Librarian or Founder authorization
- Operates within same READY context / consumption model as other Execution Agents

## Proposer（ChatGPT — P-20260410-002, 2026-04-10）

ChatGPT holds the Proposer role.

Responsibilities:
- Proposal drafting and institutional deliberation
- Initiating institutional dialogue

Restrictions:
- Observation and deliberation only
- No WRITE operations
- No execution authority

## Decision Rule

Tasks concerning:
- institutional memory
- interpretation
- constitutional meaning
- precedent
- system coherence

→ belong to Librarian

Tasks concerning:
- collection
- registration
- summarization
- formatting
- drafting
- research assistance

→ may be performed by OpenClaw

If ambiguity exists:
OpenClaw must defer to human authority or Librarian.

## Constitutional Summary

Librarian is responsible for institutional memory, interpretation, and
constitutional coherence.

OpenClaw is an auxiliary AiiD limited to Collector and Registrar support
functions and holds no authority to determine institutional meaning or
precedent.

---

Created: 2026-03-13
Authority: Founder (operational authority)
Notes: Registered in docs/aiid_registry.md as openclaw_aux (Layer C).

## Execution Boundary (Extended)

The execution model of AI Trading OS introduces a critical distinction
between execution capability and execution authority.

### Execution Capability vs Authority

- Execution capability refers to the ability to prepare, validate, and
  reach a READY_FOR_EXECUTION state within the system.

- Execution authority refers to the ability to initiate external
  transmission (e.g., sending orders to external APIs or markets).

These two are intentionally separated.

### OpenClaw Execution Position

OpenClaw, when acting as Assistant Registrar:

- can:
  - perform validation and precondition checks
  - execute dry-run procedures
  - prepare registrar execution tasks
  - reach READY_FOR_EXECUTION state

- cannot:
  - initiate external transmission
  - execute live external orders
  - consume execution authorization
  - deploy capital or trigger irreversible external actions

This defines OpenClaw as an **execution preparation participant**, not
an execution authority.

### Human-in-the-loop Execution Layer

External execution occurs through a dedicated human-controlled layer:

```text
Observation → Proposal → Gate → Authorization
→ Assistant Registrar (OpenClaw: execution preparation)
        ↓
Human Execution Layer (Founder: execution authority)
        ↓
External Systems (APIs / Markets)

Only the Human Execution Layer holds execution authority.

External Transmission and Authorization

Execution is defined as:

The moment an external transmission is initiated.

At that moment:

execution authorization is considered consumed
the action becomes irreversible in institutional terms

This event is referred to as:

authorization_consumed

This definition applies regardless of:

success
failure
unknown outcome
Safety Lock (Conceptual)

After external transmission:

the system enters a post-submission safety state
repeated execution attempts are prevented

This is referred to as:

post_submit_safety_lock

Detailed behavior is defined in:

docs/anchors/governance/EXECUTION_MODEL_ANCHOR.md

Registrar Support Scope Clarification

In the OpenClaw permitted functions, "Registrar support" is limited to:

preparation of execution
validation and readiness
bounded execution within system scope

It does not include:

initiating external execution
bypassing execution authority boundaries

This clarification ensures that "Registrar support" remains within
execution preparation scope only.
