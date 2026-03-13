---
AI TRADING OS — MASTER ANCHOR
Version: 2026-03-13-r3
Layer: B (Institutional State Snapshot)
Purpose: >
  Provide a stable cross-thread anchor for institutional state,
  architecture, and operational procedures of the AI Trading OS.
Canonical repository: ai-trading-os-private (private)
---

# AI TRADING OS — MASTER ANCHOR

Version: 2026-03-13-r3
Layer: B (Institutional State Snapshot)

## 1. Project Overview

AI Trading OS is an institutional architecture for AI-assisted trading
research and automated execution. The system is designed to ensure:

- Safe execution separation
- Reproducible research
- Institutional knowledge accumulation
- Prevention of AI overfitting
- Long-term system evolution

Key principle: AI proposes. Execution authority is structurally constrained.

## 2. Repository Governance Model (Updated 2026-03-13)

### Dual Repository Model

```
Canonical operational repository: ai-trading-os-private (private)
  -> All institutional operations, proposals, trace_events
  -> This document resides here

Legacy public repository: ai-trading-os (public)
  -> Non-canonical public snapshot
  -> No longer the source of truth
```

Operational rule:
```
origin  = legacy public (non-canonical)
private = canonical operational
```

All Registrar tasks execute against canonical (private) repository.

### Canonical Anchor Access

```
Repository: pulp39/ai-trading-os-private
Path:       docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md
Access:     https://github.com/pulp39/ai-trading-os-private/blob/main/docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md
```

Note: Private repository requires authenticated GitHub access.

## 3. System Architecture

### Host Environment

```
Mother Machine: Roon Server PC (Always On)
Purpose: Hyper-V host / VM orchestration / data persistence /
         institutional memory gateway
```

### Virtual Machine Structure

```
VM-A -- Research Environment
  Purpose: AI reasoning, research generation, institutional discussion,
           proposal drafting
  Responsibilities:
    - Proposal authoring / Research hypothesis formation
    - Institutional deliberation
    - Registrar execution (Claude Code)
    - Observation Layer (OpenClaw / collector_core)
  VM-A must never place trading orders.

VM-B -- Database Memory Node
  Purpose: Institutional memory, trace_event logging
  Technology: PostgreSQL | Schema: research
  Core table: research.trace_event

Trading VM
  Purpose: Order execution only
  Rules: Only this VM can place orders.
         AI cannot execute trades directly.
         Risk Manager controls execution authority.
```

## 4. Institutional Governance Model

```
Constitution Version: 1.3 -- Enacted
Location: constitution.md

Article structure:
  Article 1-10   Foundational Governance Principles
  Article A-D    Execution Authority (CRC01)
  Article E-G    AI Identity and Institutional Continuity (CRC02)
```

### Governance Flow

```
Founder
  +- Librarian / Speaker of the Assembly
  +- AI Assembly (deliberation)
  |    +- gpt_librarian (Seat 1)
  |    +- claude_proposer (Seat 2)
  +- Proposer (Claude)
  +- Registrar (Claude / Claude Code on VM-A)
  +- Observation Layer
       +- collector_core (OpenClaw / VM-A)
```

### Role Summary

```
Founder
  Human sovereign. Final authority. Decisions recorded as Founder Records (FR).

Librarian (gpt_librarian)
  Institutional custodian. Speaker of the AI Assembly.
  AiiD: gpt_librarian | Model: GPT | Status: active
  Capability: GitHub repository read access (added 2026-03-13)

Proposer (claude_proposer)
  Generates institutional proposals. AI Assembly Member Seat 2.
  AiiD: claude_proposer | Model: Claude | Status: active

Registrar (claude_registrar)
  Executes authorized institutional changes via Claude Code on VM-A.
  AiiD: claude_registrar | Model: Claude | Status: active

Collector (collector_core)
  Observation Layer. Does not modify institutional state.
  AiiD: collector_core | Occupant: OpenClaw | Deployment: VM-A
  Phase: Phase A (kabuStation only) | Status: active
```

## 5. AI Assembly Framework (P-20260313-001)

Established: 2026-03-13 | trace_event: 80

```
Ordinary Session     : Opened/closed by Founder via Librarian declaration.
Emergency Session    : Convened by Librarian. Ends to idle.
Constitutional Review: Auto-elevated when constitutional amendment is on agenda.
Single-Agenda Rule   : Only one agenda item under deliberation at a time.
```

### Current Assembly Seats

```
aiid             | role                    | model | trace_event
gpt_librarian    | Assembly Member Seat 1  | GPT   | 84
claude_proposer  | Assembly Member Seat 2  | Claude| 85
```

## 6. AiiD Registry Summary (P-20260313-002)

Established: 2026-03-13 | trace_event: 81
Registry: docs/aiid_registry.md (Layer B)

```
aiid             | role                               | model     | status
claude_proposer  | Proposer / Assembly Member Seat 2  | Claude    | active
claude_registrar | Registrar                          | Claude    | active
gpt_librarian    | Assembly Member Seat 1 / Librarian | GPT       | active
collector_core   | Collector / Primary Collector      | OpenClaw  | active
```

## 7. Observation Layer (CRC-05 / P-20260313-005)

Established: 2026-03-13 | trace_event: 91

### Instrument Model

```
Instrument = market-level institutional object
instrument_id format: {asset_class}_{symbol_canonical}  e.g., equity_7203
Phase A scope: equity only
```

### Observation Model

```
observation_type : price_bar | interval: 1m | unit: JPY
source           : kabuStation (canonical, Phase A)
```

### Observation Integrity Rules (1-6)

```
Rule 1: Source policy governs before comparison policy
Rule 2: kabuStation = canonical source (Phase A)
Rule 3: Supplemental observations do not override canonical
Rule 4: Conflict = same instrument_id/timestamp/type, different payload
Rule 5: Conflict resolution deferred to Phase B+
Rule 6: All Phase A canonical_observation carry integrity_role = "canonical"
```

### canonical_observation trace_event (key fields)

```json
{
  "event_type": "canonical_observation",
  "agent_id": "collector_core",
  "metadata": {
    "instrument_id": "equity_7203",
    "observation_type": "price_bar",
    "source": "kabuStation",
    "integrity_role": "canonical",
    "phase": "Phase A"
  }
}
```

## 8. Hypothesis Layer (CRC-06 / P-20260313-006)

Established: 2026-03-13 | trace_event: 92

### Hypothesis Object (summary)

```
hypothesis_id      : UUID
instrument_id      : CRC-05 canonical object
direction          : long | short | neutral
confidence         : 0.0 - 1.0 (AI self-assessment, Phase A)
confidence_basis   : Natural language rationale (required)
status             : generated | active | expired | invalidated
expiry_timestamp   : ISO8601 (required)
phase              : Phase A
```

### Bet Proposal Object (summary)

```
bet_id              : UUID
hypothesis_id       : required
position_size_type  : fixed_units (Phase A only)
bet_status          : proposed | accepted | rejected | executed | expired
acceptance_authority: Founder only (Phase A)
```

Rules B1-B6 in effect. Rules E1-E5 (Evaluation) in effect.

## 9. Execution Layer (CRC-07 / P-20260313-008)

Established: 2026-03-13 | trace_event: 94

### Execution Definition

Execution = any act causing irreversible or quasi-irreversible change
to the external state or internal institutional state of ATOS.
Execution requires explicit authorization. No implicit inheritance.

### Execution Modes

```
Simulation Mode    : Full simulation. No external impact.
Paper Mode         : Live data reference. No real orders.
Shadow Mode        : Theoretical decisions without orders.
                     Candidates recorded as shadow_execution_candidate.
Assisted Live Mode : Real execution with mandatory Founder approval per order.
                     [Phase A TARGET MODE]
Autonomous Live    : NOT OPEN. Requires independent CRC.
```

### Minimum Approval Rules

```
Rule A: Simulation/Paper/Shadow -- Founder individual approval not required
Rule B: Assisted Live -- execution_request + Risk Manager review +
        Founder final approval + trace_event before/after + kill switch confirmed
Rule C: Autonomous Live -- NOT APPROVED in CRC-07
```

### execution_request (key fields)

```yaml
execution_request_id: ER-YYYYMMDD-NNN
mode: simulation | paper | shadow | assisted_live
source_hypotheses: []  # minimum 1 required for assisted_live
approval_required_from: []
status: drafted | submitted | under_review | approved | denied |
        expired | executed | partially_executed | cancelled | emergency_blocked
```

### Risk Constraints (execution_policy references)

```
max_notional_per_order | max_daily_loss | max_position_per_instrument
max_open_orders | trading_session_boundary | instrument_allowlist
mode_allowlist | broker_route_allowlist
```

### Emergency Powers

```
Kill Switch: required. Stops orders, loops, jobs, autonomous chains.
kill_switch_state_changed trace_event: mandatory on every state change
  new_state values: enabled | disabled | partially_restricted | emergency_locked
Final stop authority: Founder
```

### New trace_event types (CRC-07)

```
kill_switch_state_changed   : kill switch state transition
shadow_execution_candidate  : hypothetical execution under Shadow Mode
```

### Policy / Adapter Boundary

```
execution_policy = institutional layer (CRC-07 scope)
broker_adapter   = infrastructure layer (outside CRC-07 scope)
```

### Reserved Future Constitutional Agenda

```
Article H (candidate): Autonomous Execution Conditions
Article I (candidate): Execution Override Rights
Article J (candidate): Accountability Chain for Autonomous Execution
```

## 10. Accepted Proposal Registry (Complete)

### 2026-03-10

```
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
```

### 2026-03-11

```
P-20260311-001  Registrar Operational Authorization
```

### 2026-03-12

```
P-20260312-001  CRC Framework
P-20260312-002  Execution Authority Clarification (CRC01)        TE:65
P-20260312-003  AI Identity and Institutional Continuity (CRC02) TE:68,69
P-20260312-004  Delegated Institutional Seats (CRC03)
P-20260312-005  Anchor Governance Framework
P-20260312-006  Collector Governance Framework
P-20260312-007  CLAUDE.md Registrar Execution Protocol
```

### 2026-03-13

```
P-20260313-001  AI Assembly Establishment Framework              TE:80
P-20260313-002  AiiD Specification                               TE:81
P-20260313-003  Collector Core Seat Establishment                TE:86,87
P-20260313-004  OpenClaw Operational Integration                 TE:88
P-20260313-005  Market Observation Governance (CRC-05)           TE:91
P-20260313-006  Hypothesis Governance Framework (CRC-06)         TE:92
P-20260313-007  Master Anchor Update (Phase A Completion)        TE:93
P-20260313-008  Execution Governance Framework (CRC-07)          TE:94
P-20260313-009  Master Anchor Update (CRC-07 Sync)               [this update]
```

## 11. CRC Deliberation History

```
CRC01  Execution Authority Gap         Articles A-D enacted    P-20260312-002  TE:65
CRC02  AI Identity (Exploratory)       Articles E-G enacted    P-20260312-003  TE:68,69
CRC03  Delegated Institutional Seats   Enacted                 P-20260312-004
CRC04  Anchor Governance               Framework enacted       P-20260312-005
CRC05  Market Observation Governance   CLOSED                  P-20260313-005  TE:91
CRC06  Hypothesis Object Model         CLOSED                  P-20260313-006  TE:92
CRC07  Execution Governance            CLOSED                  P-20260313-008  TE:94
```

## 12. Registrar Operational Architecture

```
Host: VM-A | Directory: C:\ai-trading-os | Agent: Claude Code
Authentication: billyinocean@gmail.com
Database role: claude_registrar
Permissions: INSERT/SELECT on research.trace_event
Credentials: .env.registrar (gitignored, local only)
```

### Standard Execution Procedure (per CLAUDE.md Layer C)

```
1. git pull
2. git status (must be clean)
3. Review task JSON
4. dry-run: python scripts/registrar/apply_registrar_task.py --task <file> --dry-run
5. Present dry-run result to Founder
6. Await Founder confirmation
7. Live execution
8. git log --oneline -3
9. Confirm trace_event id
```

### Known Issue

```
apply_registrar_task.py stdout.strip() may misparse leading space in
git status --porcelain with create_file + overwrite:true. Future fix candidate.
```

## 13. trace_event Key Milestones

```
id | event_type                           | content
48 | registrar_operationalized             | Registrar capability established
49 | registrar_pipeline                    | Execution pipeline milestone
50 | registrar_safety_controls             | Idempotency, dry-run, processed isolation
51 | registrar_baseline_validation         | REG-20260312-001 end-to-end
52 | registrar_operational_learning        | REG-20260312-002
65 | crc_recommendation                    | CRC01 Execution Authority
68 | founder_enactment                     | CRC02 AI Identity FR-20260312-004
69 | constitution_update                   | Articles E-G enacted
80 | operational_governance_rule_enacted   | P-20260313-001 AI Assembly
81 | operational_governance_rule_enacted   | P-20260313-002 AiiD Specification
84 | aiid_appointed                        | gpt_librarian confirmed
85 | aiid_appointed                        | claude_proposer confirmed
86 | aiid_appointed                        | collector_core (OpenClaw / VM-A)
87 | operational_governance_rule_enacted   | P-20260313-003 enacted
88 | operational_governance_rule_enacted   | P-20260313-004 enacted
90 | repository_governance_update          | Dual repo model, canonical = private
91 | operational_governance_rule_enacted   | P-20260313-005 Market Observation (CRC-05)
92 | operational_governance_rule_enacted   | P-20260313-006 Hypothesis Governance (CRC-06)
93 | documentation_governance_update       | Master Anchor v2026-03-13-r2 (Phase A complete)
94 | operational_governance_rule_enacted   | P-20260313-008 Execution Governance (CRC-07)
```

## 14. Institutional Layer Model (Phase A Complete)

```
Layer A -- Institutional Records (Source of Truth)
  constitution.md / proposals/* / founder_records/*
  research.trace_event

Layer B -- Institutional State Snapshot
  docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md  (this document)
  docs/aiid_registry.md

Layer C -- AI Operational Context
  CLAUDE.md

Layer D -- Market Observation Layer  [CRC-05 / P-20260313-005]
  canonical_observation / Instrument Model / Integrity Rules 1-6

Layer E -- Hypothesis Layer          [CRC-06 / P-20260313-006]
  Hypothesis Object / Bet Proposal Object / Evaluation Framework

Layer F -- Execution Layer           [CRC-07 / P-20260313-008]
  execution_request / execution_policy / Execution Modes
  kill_switch / shadow_execution_candidate / Auditability
```

## 15. Full Institutional Pipeline (Phase A — Complete)

```
Market
  |
  v
Collector (OpenClaw / collector_core)
  | kabuStation API
  v
Mapping Layer
  | api_symbol -> instrument_id
  v
Canonical Observation
  | trace_event: canonical_observation
  v
Proposer (AI Reasoning)
  | trace_event: hypothesis_generated
  v
Bet Proposal
  | trace_event: bet_proposed
  v
Founder Review
  | trace_event: bet_accepted / bet_rejected
  v
Execution Layer (Trading VM)
  | execution_request + Risk Manager review + Founder approval
  | trace_event: execution events
  v
Hypothesis Evaluation
  | trace_event: hypothesis_evaluated
  v
Institutional Learning Record
```

End-to-end pipeline is fully governed as of 2026-03-13.

## 16. Phase A Governance Status (COMPLETE)

```
Phase A governance is complete as of 2026-03-13.

Completed:
  [x] Constitution v1.3
  [x] AI Assembly (CRC03)
  [x] AiiD Registry (P-20260313-002)
  [x] Execution Authority separation (CRC01)
  [x] AI Identity governance (CRC02)
  [x] Repository governance (dual repo model)
  [x] Anchor governance framework (CRC04)
  [x] Collector governance (P-20260312-006)
  [x] Market Observation Layer (CRC05)
  [x] Hypothesis Layer (CRC06)
  [x] Execution Governance (CRC07)

Pending (requires separate proposals):
  [ ] OpenClaw VM-A technical implementation (operational)
  [ ] Observation frequency determination (Founder decision)
  [ ] apply_registrar_task.py bug fix (Founder judgment)
  [ ] Broker adapter definition (operational proposal)
  [ ] Phase B: Statistical confidence calibration
  [ ] Phase B: AI-assisted Risk Manager
  [ ] Phase B: Autonomous execution (requires independent CRC)
```

## 17. Next Thread Entry

Next thread must begin with:

```
ANCHOR
https://github.com/pulp39/ai-trading-os-private/blob/main/docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md
```

Note: Authenticated GitHub access required (private repository).

Recommended reading order:

```
1. constitution.md
2. docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md  (this document)
3. docs/aiid_registry.md
4. CLAUDE.md
5. docs/registrar_preflight_standard.md
```

```
Phase A governance complete.
Next session: operational implementation or new CRC as Founder directs.
```

---

Layer B document. Not authoritative. Derived from Layer A records.

Updated: 2026-03-13-r3 by Registrar (REG-20260313-011)
Authority: Founder (P-20260313-009)
