---
AiiD Registry
Layer: B (Institutional State Snapshot)
Maintained by: Registrar
Last updated: 2026-03-13
Authority: P-20260313-002 (AiiD Specification)
---

# AiiD Registry

## Active AiiD Records

| aiid | display_name | role | model | appointed_by | appointment_date | status |
|---|---|---|---|---|---|---|
| claude_proposer | Claude Proposer | Proposer | Claude | Founder | 2026-03-10 | active |
| claude_registrar | Claude Registrar | Registrar | Claude | Founder | 2026-03-11 | active |

## Assembly Member Seats

| aiid | display_name | role | model | appointed_by | appointment_date | status |
|---|---|---|---|---|---|---|
| gpt_librarian | GPT Librarian | Assembly Member | GPT | Founder | 2026-03-13 | active |
| claude_proposer | Claude Proposer | Assembly Member | Claude | Founder | 2026-03-13 | active |

## Observation Layer

| aiid | display_name | role | model | deployment | appointed_by | appointment_date | status |
|---|---|---|---|---|---|---|---|
| collector_core | Collector Core | Collector | OpenClaw | VM-A | Founder | 2026-03-13 | active |



## Auxiliary AiiD

| aiid | display_name | role | model | deployment | appointed_by | appointment_date | status |
|---|---|---|---|---|---|---|---|
| openclaw_aux | OpenClaw Auxiliary | Auxiliary AiiD | OpenClaw | VM-A | Founder | 2026-03-13 | active |



## Notes

Existing agent_id values (claude_proposer, claude_registrar) are recognized
as valid AiiD identifiers per P-20260313-002 section 4.4.

Registry entries are Institutional State Snapshots (Layer B).
Authoritative records are trace_events (Layer A).

Updates to this registry require a Registrar task following Librarian review.

Institutional role vs. runtime process:
  AiiD Registry records institutional roles, not runtime processes.
  A single runtime agent (e.g., OpenClaw) may occupy multiple institutional
  roles (collector_core for Layer D, openclaw_aux for Layer C).
  These roles are governed separately.
