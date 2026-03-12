# Librarian–Proposer Interaction Model

Purpose:
Define the institutional interaction between the Librarian and Proposer roles
within AI Trading OS.

This document establishes how observations become proposals,
how decisions are made, and how institutional changes are executed.

---

# 1. Roles

## Proposer

Responsibilities:

- Generate proposals based on observations
- Analyze system behavior and research results
- Suggest institutional improvements
- Produce proposal documents

The Proposer does NOT execute system changes.

---

## Librarian

Responsibilities:

- Evaluate proposals
- Maintain institutional integrity
- Approve or reject proposals
- Authorize Registrar execution tasks

The Librarian acts as the **decision authority** for operational changes.

---

## Registrar

Responsibilities:

- Execute authorized institutional changes
- Record trace events
- Apply repository changes
- Move tasks to processed queue

The Registrar is the **execution authority**.

---

# 2. Institutional Flow

The institutional workflow is defined as:

Observation
↓
Proposer creates Proposal
↓
Librarian reviews Proposal
↓
Decision

IF accepted
↓
Registrar task generated
↓
Registrar execution
↓
trace_event + Git commit

IF rejected
↓
trace_event recording rejection

---

# 3. Proposal Lifecycle

A proposal progresses through the following states:

draft  
proposed  
accepted  
rejected  
executed

The Registrar executes institutional changes only after a proposal
reaches the **accepted** state.

---

# 4. Execution Principle

Separation of responsibilities:

Proposer → ideas and analysis  
Librarian → decisions  
Registrar → execution and recording

This separation prevents uncontrolled system modification.

---

# 5. Traceability

All institutional decisions must be traceable through:

- proposal documents
- trace_event records
- git commits
- registrar tasks

This ensures full historical accountability.

---

# End of Document