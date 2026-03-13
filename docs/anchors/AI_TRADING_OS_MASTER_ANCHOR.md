# AI TRADING OS — MASTER ANCHOR

Version: 2026-03-13
Layer: B (Institutional State Snapshot)
Purpose: Provide a stable cross-thread anchor for institutional state,
         architecture, and operational procedures of the AI Trading OS.
Canonical repository: ai-trading-os-private (private)

---

## 1. Project Overview

AI Trading OS is an institutional architecture for AI-assisted trading
research and automated execution. The system is designed to ensure:

- Safe execution separation
- Reproducible research
- Institutional knowledge accumulation
- Prevention of AI overfitting
- Long-term system evolution

Key principle: AI proposes. Execution authority is structurally constrained.

---

## 2. Repository Governance Model (Updated 2026-03-13)

### Dual Repository Model

As of 2026-03-13, AI Trading OS operates under a dual repository model
authorized by Founder.

```
Canonical operational repository:
  ai-trading-os-private  (private)
  -> All institutional operations, proposals, trace_events
  -> This document resides here

Legacy public repository:
  ai-trading-os  (public)
  -> Non-canonical public snapshot
  -> No longer the source of truth
```

Operational rule:
- origin  = legacy public (non-canonical)
- private = canonical operational
- All Registrar tasks execute against canonical (private) repository
- All institutional synchronization must use the private repository anchor

### Canonical Anchor Access

The canonical Master Anchor is located at:
```
Repository: pulp39/ai-trading-os-private
Path: docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md
Access: https://github.com/pulp39/ai-trading-os-private/blob/main/docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md
```

Note: Private repository requires authenticated GitHub access.
Raw content URL is not publicly accessible.

---

## 3. System Architecture

### Host Environment

```
Mother Machine: Roon Server PC (Always On)
Purpose:
  - Hyper-V host
  - VM orchestration
  - data persistence
  - institutional memory gateway
```

### Virtual Machine Structure

```
VM-A -- Research Environment
  Purpose: AI reasoning, research generation,
           institutional discussion, proposal drafting
  Responsibilities:
    - Proposal authoring
    - research hypothesis formation
    - institutional deliberation
    - Registrar execution (Claude Code)
    - Observation Layer (OpenClaw / collector_core)
  VM-A must never place trading orders.

VM-B -- Database Memory Node
  Purpose: Institutional memory, trace_event logging,
           persistent research storage
  Technology: PostgreSQL
  Schema: research
  Core table: research.trace_event
  All institutional and research events must be logged here.

Trading VM
  Purpose: Order execution only
  Rules:
    Only this VM can place orders.
    AI cannot execute trades directly.
    Risk Manager controls execution authority.
```

---

## 4. Institutional Governance Model

### Constitution

Version: 1.3 -- Enacted
Location: constitution.md

Article structure:
```
Article 1-10   Foundational Governance Principles
Article A-D    Execution Authority (CRC01)
Article E-G    AI Identity and Institutional Continuity (CRC02)
```

### Governance Flow

```
Founder
  +- Librarian / Speaker of the Assembly
       +- AI Assembly (deliberation)
            +- gpt_librarian   (Seat 1)
            +- claude_proposer (Seat 2)
       +- Proposer (Claude)
       +- Registrar (Claude / Claude Code on VM-A)
  +- Observation Layer
       +- collector_core (OpenClaw / VM-A)
```

### Role Summary

Founder
Human sovereign. Final authority on all institutional matters.
Founder decisions recorded as Founder Records (FR).

Librarian (gpt_librarian)
Institutional custodian. Speaker of the AI Assembly.
Evaluates proposals. Authorizes Registrar actions.
AiiD: gpt_librarian | Model: GPT | Status: active
Capability: GitHub repository read access (added 2026-03-13)

Proposer (claude_proposer)
Generates institutional proposals and system evolution ideas.
AI Assembly Member Seat 2.
AiiD: claude_proposer | Model: Claude | Status: active

Registrar (claude_registrar)
Executes authorized institutional changes via Claude Code on VM-A.
Operates only under Librarian authorization.
AiiD: claude_registrar | Model: Claude | Status: active

Collector (collector_core)
Observation Layer. Collects market signals. Does not modify
institutional state.
AiiD: collector_core | Occupant: OpenClaw | Deployment: VM-A
Phase: Phase A (kabuStation only) | Status: active

---

## 5. AI Assembly Framework (P-20260313-001)

Established: 2026-03-13 | trace_event: 80

### Session Types

```
Ordinary Session:
  Opened/closed by Founder via Librarian declaration.
  Closed state: idle.

Emergency Session:
  Convened by Librarian. Suspends Ordinary Session.
  Ends to idle (no automatic resumption).

Constitutional Review:
  Auto-elevated when constitutional amendment is on agenda.
```

Single-Agenda Rule: Only one agenda item may be under deliberation at a time.

### Current Assembly Seats

aiid            | role                    | model | trace_event
gpt_librarian   | Assembly Member Seat 1  | GPT   | 84
claude_proposer | Assembly Member Seat 2  | Claude| 85

---

## 6. AiiD Registry Summary (P-20260313-002)

Established: 2026-03-13 | trace_event: 81
Registry location: docs/aiid_registry.md (Layer B)

AiiD = institutional seat (not AI instance).
Defined per Constitution Article E, F.

### Active AiiD Records

aiid             | role                              | model     | status
claude_proposer  | Proposer / Assembly Member Seat 2 | Claude    | active
claude_registrar | Registrar                         | Claude    | active
gpt_librarian    | Assembly Member Seat 1            | GPT       | active
collector_core   | Collector / Primary Collector     | OpenClaw  | active

---

## 7. Observation Layer (P-20260313-003, P-20260313-004)

### Collector Core Seat (P-20260313-003)
Established: 2026-03-13 | trace_events: 86, 87

```
aiid:        collector_core
occupant:    OpenClaw
deployment:  VM-A
phase:       Phase A
status:      active
designation: Primary Collector (canonical_observation)
authority:   P-20260312-006
```

### OpenClaw Operational Integration (P-20260313-004)
Established: 2026-03-13 | trace_event: 88

Phase A data scope (kabuStation only):
  symbol, price, volume, previous_close, order_book, timestamp

Observation Report Format (provisional schema):
  observation_type: market
  source: kabuStation
  collector_id: collector_core
  phase: Phase A
  symbol: <ticker>
  timestamp: <ISO8601>
  data:
    price / volume / previous_close / change / order_book
  analysis:
    summary: <optional>
    hypothesis: <optional, non-binding, flagged>

Two-tier Recording Model:
  collector_core (OpenClaw)
        |
        v
  observation report
        |
        v
  Registrar
        |
        v
  trace_event (canonical_observation)

OpenClaw does not write directly to the trace_event system.

Phase A Constraints:
  Permitted: passive retrieval, observation report generation,
             optional non-binding hypothesis (flagged)
  Prohibited: order execution, repository modification,
              direct trace_event write, proposal enactment,
              data sources other than kabuStation

Future expansion (requires separate proposal):
  news feeds, sentiment, macro data, other external signals

---

## 8. Accepted Proposal Registry (Complete)

### 2026-03-10
P-20260310-001  Proposal Semantics Definition
P-20260310-002  trace_event Schema Definition
P-20260310-003  Institutional Role Formalization
P-20260310-004  Proposal Lifecycle Formalization
P-20260310-005  Research Process Framework
P-20260310-006  Proposer Onboarding
P-20260310-007  Registrar Role Establishment
P-20260310-008  Registrar Database Authorization
P-20260310-009  AI Collector Evaluation Framework
P-20260310-010  Founder Record Directory
P-20260310-011  OpenClaw Provisional Invitation

### 2026-03-11
P-20260311-001  Registrar Operational Authorization

### 2026-03-12
P-20260312-001  CRC Framework
P-20260312-002  Execution Authority Clarification (CRC01)      TE:65
P-20260312-003  AI Identity and Institutional Continuity (CRC02) TE:68,69
P-20260312-004  Delegated Institutional Seats (CRC03)
P-20260312-005  Anchor Governance Framework
P-20260312-006  Collector Governance Framework
P-20260312-007  CLAUDE.md Registrar Execution Protocol

### 2026-03-13
P-20260313-001  AI Assembly Establishment Framework             TE:80
P-20260313-002  AiiD Specification                              TE:81
P-20260313-003  Collector Core Seat Establishment               TE:86,87
P-20260313-004  OpenClaw Operational Integration                TE:88

---

## 9. CRC Deliberation History

CRC01  Execution Authority Gap          Articles A-D enacted  P-20260312-002  TE:65
CRC02  AI Identity (Exploratory)        Articles E-G enacted  P-20260312-003  TE:68,69
CRC03  Delegated Institutional Seats    Enacted               P-20260312-004
CRC04  Anchor Governance               Framework enacted      P-20260312-005
CRC05  Market Observation Governance   PENDING

---

## 10. Registrar Operational Architecture

### Execution Environment
```
Host: VM-A
Directory: C:\ai-trading-os
Agent: Claude Code
Authentication: billyinocean@gmail.com
```

### Registrar Identity
```
Database role: claude_registrar
Permissions: INSERT/SELECT on research.trace_event
Credentials: .env.registrar (gitignored, local only)
```

### Standard Execution Procedure (per CLAUDE.md Layer C)
```
1. git pull
2. git status (must be clean -- stop if not)
3. Review task JSON
4. dry-run: python scripts/registrar/apply_registrar_task.py --task <file> --dry-run
5. Present dry-run result to Founder
6. Await Founder confirmation (yes/no)
7. Live execution
8. git log --oneline -3
9. Confirm trace_event id
```

### Safety Features
- Idempotent execution (reuse existing state)
- Dry-run mode (no writes)
- Processed task isolation (registrar_queue/processed/)
- .env.registrar modification prohibited
- Unrelated commit prohibition

### Known Issue
apply_registrar_task.py: run_git() uses stdout.strip() -- leading
space in git status --porcelain may cause path parse issues when
using create_file + overwrite: true. Future fix candidate.

---

## 11. trace_event Key Milestones

id  | event_type                          | content
48  | registrar_operationalized           | Registrar capability established
49  | registrar_pipeline                  | Execution pipeline milestone
50  | registrar_safety_controls           | Idempotency, dry-run, processed isolation
51  | registrar_baseline_validation       | REG-20260312-001 end-to-end
52  | registrar_operational_learning      | REG-20260312-002
65  | crc_recommendation                  | CRC01 Execution Authority
68  | founder_enactment                   | CRC02 AI Identity FR-20260312-004
69  | constitution_update                 | Articles E-G enacted
80  | operational_governance_rule_enacted | P-20260313-001 AI Assembly
81  | operational_governance_rule_enacted | P-20260313-002 AiiD Specification
82  | aiid_appointed                      | gpt_librarian (Assembly Seat 1)
83  | aiid_appointed                      | claude_proposer (Assembly Seat 2)
84  | aiid_appointed                      | gpt_librarian confirmed
85  | aiid_appointed                      | claude_proposer confirmed
86  | aiid_appointed                      | collector_core (OpenClaw / VM-A)
87  | operational_governance_rule_enacted | P-20260313-003 enacted
88  | operational_governance_rule_enacted | P-20260313-004 enacted

---

## 12. Pending Items

CRC-05 Market Observation Governance     : PENDING (next session)
OpenClaw VM-A technical implementation   : PENDING (operational)
Observation frequency determination      : PENDING (Founder decision)
Apply_registrar_task.py bug fix proposal : PENDING (Founder judgment)

---

## 13. Documentation Layer Model

Layer A -- Institutional Records (Source of Truth)
  constitution.md
  proposals/*
  founder_records/*
  research.trace_event

Layer B -- Institutional State Snapshot
  docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md  (this document)
  docs/aiid_registry.md

Layer C -- AI Operational Context
  CLAUDE.md

---

## 14. Governance to Execution to Sensing Cycle

As of 2026-03-13, the full institutional cycle is established:

  [Market]
      |
      v
  [collector_core / OpenClaw]
      | observation report
      v
  [Registrar]
      | trace_event (canonical_observation)
      v
  [Proposer]
      | proposal
      v
  [AI Assembly deliberation]
      | Librarian APPROVED
      v
  [Registrar]
      | enacted
      v
  [Institutional record]

CRC-05 (Market Observation Governance) will define the formal
institutional interface between Market and Collector, completing
the pipeline specification.

---

## 15. Next Thread Entry

Next thread must begin with:

  ANCHOR
  https://github.com/pulp39/ai-trading-os-private/blob/main/docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md

Note: Authenticated GitHub access required (private repository).

Recommended reading order for new session:
1. constitution.md
2. docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md  (this document)
3. docs/aiid_registry.md
4. CLAUDE.md
5. docs/registrar_preflight_standard.md

---

Layer B document. Not authoritative. Derived from Layer A records.
Updated: 2026-03-13 by Registrar (REG-20260313-006)
Authority: Founder (Proposal A decision, 2026-03-13)
