# AI TRADING OS — MASTER ANCHOR
Version: 2026-03-12
Purpose: Provide a stable cross-thread anchor for institutional state, architecture, and operational procedures of the AI Trading OS.

---

# 1. Project Overview

AI Trading OS is an institutional architecture for AI-assisted trading research and automated execution.

The system is designed to ensure:

- Safe execution separation
- Reproducible research
- Institutional knowledge accumulation
- Prevention of AI overfitting
- Long-term system evolution

Key principle:

> AI proposes.  
> Execution authority is structurally constrained.

---

# 2. System Architecture

## Host Environment

Mother Machine:  
Roon Server PC (Always On)

Purpose:

- Hyper-V host
- VM orchestration
- data persistence
- institutional memory gateway

---

## Virtual Machine Structure

### VM-A — Research Environment

Purpose:

- AI reasoning
- research generation
- institutional discussion
- proposal drafting

Responsibilities:

- Proposal authoring
- research hypothesis formation
- institutional deliberation

VM-A must never place trading orders.

---

### VM-B — Database Memory Node

Purpose:

- Institutional memory
- trace_event logging
- persistent research storage

Technology:

- PostgreSQL
- schema: `research`

Core table:

`research.trace_event`

All institutional and research events must be logged here.

---

### Trading VM

Purpose:

- Order execution only

Rules:

- Only this VM can place orders.
- AI cannot execute trades directly.
- Risk Manager controls execution authority.

---

# 3. Institutional Governance Model

## Founder

Human authority responsible for:

- constitutional decisions
- system direction
- final institutional authority

Founder decisions are recorded as Founder Records (FR).

---

## Librarian

Role:

Institutional custodian.

Responsibilities:

- maintain institutional consistency
- evaluate proposals
- authorize Registrar actions
- preserve historical trace

Agent:

`gpt54_librarian`

---

## Proposer

Role:

Generate institutional proposals and system evolution ideas.

Agent:

`Claude`

Responsibilities:

- create proposals
- propose institutional improvements
- propose collector hypotheses

---

## Registrar

Role:

Execute authorized institutional changes.

Agent:

`Claude`

Responsibilities:

- apply repository updates
- register trace_events
- maintain Founder record files
- execute JSON-based institutional tasks

Registrar operates only under **Librarian authorization**.

---

## Collector

Role:

Collect observations and research signals.

Example:

`collector_base_collector_v1`

Collectors may include future AI agents such as OpenClaw.

Collectors do not modify institutional state.

---

# 4. Institutional Record Types

## Proposal (P)

Institutional change proposal.

Location:

`founder_records/proposals/`

Status lifecycle:

`draft → proposed → accepted → rejected`

---

## Founder Record (FR)

Founder decision records.

Location:

`founder_records/`

---

## trace_event

Institutional event log stored in PostgreSQL.

Table:

`research.trace_event`

Columns include:

`id, ts, agent_id, actor_type, event_type, content, metadata`

This table represents the **institutional memory layer** of AI Trading OS.

---

# 5. Institutional State Summary

## Accepted Proposals

- P-20260310-001 — accepted
- P-20260310-002 — accepted
- P-20260310-003 — accepted
- P-20260310-004 — accepted
- P-20260310-005 — accepted
- P-20260310-006 — accepted
- P-20260310-007 — accepted
- P-20260310-008 — accepted
- P-20260310-009 — accepted
- P-20260310-010 — accepted
- P-20260310-011 — accepted
- P-20260311-001 — accepted

## Founder Records

- FR-20260310-001 — approval record registered
- FR-20260310-002 — retroactive proposal record registered under `founder_records/proposals/`

## Collector State

- `collector_base_collector_v1` active
- ES1! daily observation formally active

## OpenClaw State

- Stage 0 review in progress
- design document submission pending

---

# 6. Registrar Operational Architecture (2026-03-12)

Registrar capability has been fully operationalized.

This represents the first working institutional execution layer.

## Registrar Database Identity

Dedicated database role:

`claude_registrar`

Permissions:

- CONNECT on `trading`
- USAGE on `research` schema
- INSERT, SELECT on `research.trace_event`
- USAGE, SELECT on `research.trace_event_id_seq`

Security principle:

Registrar has **minimal write authority**.

## Registrar Local Credentials

Stored locally:

`.env.registrar`

Example structure:

```env
PGHOST=192.168.250.11
PGPORT=5432
PGDATABASE=trading
PGUSER=claude_registrar
PGPASSWORD=******

This file is gitignored.

Registrar Execution Host

Registrar operations are executed on:

VMA

Standard environment:

C:\ai-trading-os

Registrar Milestone trace_event IDs

institutional Registrar operationalization: 48

registrar execution pipeline milestone: 49

registrar safety controls milestone: 50

Interpretation:

48 records the institutional introduction of operational Registrar capability under Librarian authorization.

49 records the establishment of the Registrar execution pipeline.

50 records the addition of Registrar safety controls including idempotency behavior, processed task segregation, and dry-run mode.

7. Registrar Automation Pipeline

Registrar actions are executed through JSON tasks.

Task Queue

registrar_queue/

Example:

REG-20260311-001.json

Processed Queue

registrar_queue/processed/

Completed tasks are moved here automatically.

Registrar Scripts

Primary scripts:

scripts/registrar/register_trace_events.py

scripts/registrar/apply_registrar_task.py

Capabilities:

update proposal status

create institutional files

insert trace_event records

update trace_event references

git commit

git push

move tasks to processed queue

8. Registrar Safety Features

Registrar includes multiple safety mechanisms.

Idempotent Execution

If an action was already completed, Registrar reuses existing state where possible.

Example:

existing trace_event found → reuse id

existing file found → skip or preserve

target status already present → do not fail

Dry-Run Mode

Registrar task preview:

--dry-run

Example:

python scripts/registrar/apply_registrar_task.py --task registrar_queue\REG-XXXX.json --dry-run

Dry-run:

performs validation

simulates execution

performs no database writes

performs no file writes

performs no git commits

does not move the task to processed/

Processed Task Isolation

Completed tasks move automatically to:

registrar_queue/processed/

This prevents accidental double execution in normal operation.

9. Registrar Standard Execution Procedure

Standard VMA execution workflow:

cd C:\ai-trading-os

git pull
git status

python scripts/registrar/apply_registrar_task.py --task registrar_queue\REG-XXXX.json --dry-run

python scripts/registrar/apply_registrar_task.py --task registrar_queue\REG-XXXX.json

git log --oneline -1
git status

This is now the standard Registrar operating sequence.

10. Current Institutional Interpretation

AI Trading OS is no longer only in institutional design mode.

It has entered early institutional execution mode with an operational Registrar pipeline.

Current institutional structure:

Founder
  └─ Librarian (canonical authority)
       └─ Proposer (Claude)
       └─ Registrar (Claude)
  └─ Collector (collector_base_collector_v1)

This is the first point at which institutional proposal, approval, registration, database logging, and repository synchronization are all connected in a working loop.

11. Immediate Next Objectives

Create Registrar task template:

registrar_queue/template/REG_TEMPLATE.json

Execute one fresh lightweight Registrar task end-to-end on VMA.

Document and stabilize the standard Registrar operating procedure in anchor and/or operational docs.

Resume higher-level institutional progression after Registrar baseline stabilization.

Possible next topic:

OpenClaw Collector evaluation

12. Next Thread Entry Anchor

Next thread must begin with:

ANCHOR
https://raw.githubusercontent.com/pulp39/ai-trading-os/main/docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md

This ensures continuity of institutional state.

---

# 2026-03-12 Constitutional Milestone Update

## CRC Deliberation 01 — Execution Authority Gap

Outcome  
Constitutional Amendment enacted.

Related Proposal  
P-20260312-002

Founder Enactment  
FR-20260312-003

Result  
Articles A–D added to constitution.

Meaning  
Execution Authority boundary established.

---

## CRC Deliberation 02 — AI Identity (Exploratory Phase)

Outcome  
Constitutional Amendment enacted.

Related Proposal  
P-20260312-003  
"AI Identity and Institutional Continuity"

Founder Enactment  
FR-20260312-004

Constitution Update  
Articles E–G added.

Core Principles introduced

Institutional Subject  
Institutional Continuity Principle  
Role Succession Principle

Meaning  
AI institutional identity formally defined.

---

## Constitution Structure (Current)

AI Trading OS Constitution

Article 1–10  
Fundamental Governance Principles

Article A–D  
Execution Authority

Article E–G  
AI Identity and Institutional Continuity

---

## Institutional Record Chain (P-20260312-003)

Proposal  
proposals/accepted/P-20260312-003.md

CRC Recommendation  
trace_event 65

Founder Enactment  
FR-20260312-004  
trace_event 68

Constitution Update  
trace_event 69

Founder Historical Record  
FR-20260312-005  
trace_event 70

Proposal Archive Registration  
commit 6b7f31f  
trace_event 71

Status  
COMPLETE

---

## CRC Status

CRC Deliberation 02  
Status: CLOSED

Next Deliberation Candidates

Deliberation 03  
Registrar delegation constitutional formalization

Deliberation 04  
Collector governance framework

Deliberation 05  
Institutional health metrics

---

## Note

Anchor documents themselves are not yet formally defined in the constitutional system.

The institutional status, lifecycle, and governance of anchor documents should be discussed in a future CRC session.