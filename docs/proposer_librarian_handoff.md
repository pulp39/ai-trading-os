# Proposer-Librarian Handoff Standard

Purpose:
Define the minimum standard handoff between the Proposer and Librarian roles
so that accepted proposals can be converted into Registrar-executable work.

This document is intentionally operational and narrow.
It does not replace the broader institutional model.

---

# 1. Proposer Output

A Proposer submission should contain:

- proposal_id
- title
- status
- author
- objective
- rationale
- requested change
- affected files or records
- expected trace_event implications
- execution needs, if known

Minimum expectation:

The Proposer must clearly distinguish between:

- analysis
- recommendation
- requested institutional action

The Proposer does NOT perform execution.

---

# 2. Librarian Review Output

A Librarian review should produce one of the following outcomes:

- accepted
- rejected
- requires_revision
- deferred

A valid Librarian response should include:

- proposal_id
- decision
- reasoning
- execution authorization status
- registrar relevance
- any constraints on execution

If accepted, the response should be specific enough
for conversion into a Registrar task.

---

# 3. Registrar Handoff Requirements

When a proposal is accepted and execution is needed,
the Librarian-to-Registrar handoff must define:

- task_id
- authorization basis
- action list
- affected files
- trace_event requirements
- commit intent

The handoff should be concrete enough
to become a Registrar JSON task without reinterpretation.

---

# 4. Execution Boundary

Responsibility separation:

- Proposer creates and improves proposals
- Librarian evaluates and authorizes
- Registrar executes authorized actions

No role should silently absorb the role of another.

---

# 5. Traceability Rule

The full chain must remain auditable:

Proposal
-> Librarian review
-> Registrar task
-> trace_event
-> Git commit

This is the minimum traceability chain for institutional change.

---

# 6. Operational Goal

The purpose of this handoff standard is to reduce ambiguity
between proposal quality, decision quality, and execution quality.

A proposal should be easy to review.
A review should be easy to execute.
An execution should be easy to audit.

---

# End of Document