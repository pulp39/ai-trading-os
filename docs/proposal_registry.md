# Proposal Registry

This document tracks all proposals created within AI Trading OS.

The registry provides a simple index linking proposal identifiers to their status and purpose.

Proposal identifiers follow the rule defined in:

docs/proposal_semantics.md

Format:

P-YYYYMMDD-NNN

Example:

P-20260310-001

---

## Registry

| proposal_id | status | date | title | notes |
|-------------|--------|------|-------|------|
| P-20260310-001 | accepted | 2026-03-10 | Initial institutional proposal pipeline test | first formal proposal |

---

## Status Types

Possible proposal statuses:

- draft
- under_review
- accepted
- rejected
- archived

---

## Purpose

The registry serves several institutional purposes:

- track research evolution
- link proposals to trace_event records
- provide quick access to proposal history
- support AI proposers in referencing prior work

---

## Maintenance

The registry is updated when:

- a new proposal is introduced
- a proposal changes status
- a proposal is archived

Updates are typically performed by the Librarian role.
