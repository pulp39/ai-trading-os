# WORKING_SPEC_ANCHOR
Version: 0.1
Date: 2026-03-24
Status: active
Purpose: Working specification anchor for ongoing ATOS / AVC design formation

---

## 1. About This Document

This document records the current working specification state of the ATOS execution pipeline.

It is intended to preserve continuity across AI discussions and implementation sessions.

This is not a final specification.
It is a structured record of design formation in progress, based on actual implementation and validation.

---

## 2. Target System

- Name: ATOS Execution Pipeline (Phase 1–4 Established)
- Scope:
  - Market observation
  - Interpretation
  - Execution preparation
  - Human-in-the-loop execution boundary
- Relationship to ATOS:
  - Core operational pipeline of ATOS
  - First fully connected observation → execution preparation loop

---

## 3. Current Objective

- Consolidate Phase 1–4 achievements into a single readable structure
- Establish a stable pre-execution state before Phase 5 (Human Execution)
- Prepare for execution readiness definition refinement

---

## 4. Current Design Focus

- Execution readiness definition (environment + OpenClaw runtime)
- Human-in-the-loop execution protocol (v0.2)
- OpenClaw runtime stability and reproducibility
- Separation of execution capability and authority

---

## 5. Established Understandings

### Phase 1 — Observation Pipeline

- kabuStation API integration established
- Collector retrieves market data (symbol: 7203)
- Data stored in:
  - `public.board_snapshots`
  - `research.trace_event`
- Observation is strictly non-interpretive

---

### Phase 2 — Interpretation Layer

- Indicator generation (e.g., VWAP deviation)
- Hypothesis formation
- Proposal drafting pipeline established

Flow:

trace_event → indicator_observation → hypothesis → proposal_drafted


- Interpretation is separated from observation

---

### Phase 3 — Execution Framework

- AAB (Action Authorization Bundle) defined
- TMP (Trust Message Protocol) defined
- execution_recorded framework established

Key principle:
- Proposal does NOT trigger execution
- Execution requires structured authorization

---

### Phase 4 — Simulated Execution

- `run_simulated_order.py` implemented
- Approved task artifact:
  - `registrar_queue/simulated_order_task.json`
- Input requirement:
  - Script reads AAB JSON (NOT registrar task JSON)

Validated:

- dry-run simulated_order succeeded
  - symbol: 7203
  - side: buy
  - quantity: 100
  - order_type: market

- execution_recorded (simulated_order) confirmed

Critical validation:
- OpenClaw stops before external transmission
- Execution capability ≠ execution authority enforced

---

### OpenClaw Runtime Model (Established)

OpenClaw is a 3-layer runtime:

- Gateway
- Node
- Control UI

Execution readiness requires:

- gateway running
- node connected
- valid token
- runtime path available

Important:
- UI access alone does NOT indicate readiness

---

### Stable Startup Procedure (Confirmed)

WSL:

cd /mnt/c/ai-trading-os-private
source .env.local
source .venv/bin/activate
openclaw gateway --allow-unconfigured --bind lan


Separate WSL terminal:

openclaw dashboard --no-open

→ copy fresh token

Windows browser:

http://localhost:18789/

→ paste token → Connect

Separate WSL terminal:

openclaw node run


If pairing required:

openclaw devices approve --latest


---

### Known Failure Patterns (Established)

- token mismatch after gateway restart
- gateway only (no node) → "No nodes found"
- node process terminated → offline state
- localhost refused → bind / proxy / reachability issues
- registrar task JSON used instead of AAB JSON

---

## 6. Open Questions

- Should execution readiness explicitly include node connectivity?
- Should limit order be allowed in simulated execution?
- How should readiness and authorization be separated formally?
- What is the minimal pre-submit trace_event set?

---

## 7. Deferred / Parked Topics

- AiiD authorization (beyond stub phase)
- Vision layer (long-term architecture)
- Formal specification layer (external interface contracts)

---

## 8. Recent Important Decisions

- Human-in-the-loop Execution Protocol v0.2 defined
- WSL_ENVIRONMENT Section 9–10 added
- OpenClaw runtime model clarified (3-layer structure)
- WORKING_SPEC_ANCHOR introduced (this document)

---

## 9. Implementation Progress

Completed:

- Collector pipeline (kabuStation → DB)
- Interpretation pipeline (indicator → proposal)
- Execution framework (AAB / TMP)
- Simulated execution (dry-run)
- OpenClaw runtime stabilization

Validated:

- End-to-end observation → execution preparation loop
- execution_recorded trace confirmed

Not yet completed:

- Human execution (Phase 5)
- Final execution readiness definition
- Authorization lifecycle enforcement at execution moment

---

## 10. Next Discussion Targets

- Execution Readiness Definition v1.1
  - include node connectivity
  - formal readiness conditions

- Phase 5 Human Execution
  - pre-submit trace_event design
  - post-submit safety lock handling
  - minimal execution scope definition

---

## 11. Related References

- trace_event:
  - 299: protocol_defined
  - 300: WSL Section 9
  - 311: WSL Section 10
  - 312: WORKING_SPEC_ANCHOR introduced

- Anchors:
  - ATOS_BOOTSTRAP_ANCHOR.md
  - AI_TRADING_OS_MASTER_ANCHOR.md
  - EXECUTION_MODEL_ANCHOR.md
  - WSL_ENVIRONMENT_ANCHOR.md

- Scripts:
  - scripts/openclaw/run_simulated_order.py

- Task artifacts:
  - registrar_queue/simulated_order_task.json

  ---

## 12. Execution Readiness v1.1 (Operational Definition)

Execution readiness is defined as:

execution_ready =
  environment_ready
  AND runtime_ready
  AND authorization_granted
  AND market_ready
  AND order_defined

### environment_ready
- .env loaded
- .venv active
- DB reachable
- runtime path valid

### runtime_ready
- gateway running
- node connected
- valid token
- UI reachable

### authorization_granted
- approved execution path exists
- approved task artifact exists
- execution scope fixed

### market_ready
- market open
- symbol tradable

### order_defined
- symbol fixed
- side fixed
- quantity fixed
- order type fixed

---

## 13. Phase 5 Human Execution Protocol (Draft)

### Pre-submit
- Verify execution_ready = true
- Record execution_prepared trace_event

### Execution
- Human submits order via external system

### Post-submit
- Record execution_submitted trace_event
- Mark authorization as consumed
- Apply post_submit_safety_lock

### Safety Lock Definition
- No duplicate submission allowed
- Authorization cannot be reused
- Retry requires new authorization

---

## 14. Phase 5 Execution Checklist

1. Market is open
2. KabuStation running
3. Symbol registration confirmed (re-register if empty)
4. Symbol 7203 is tradable
5. Gateway running
6. Node connected
7. Valid token
8. UI reachable
9. .env loaded
10. .venv active
11. DB reachable
12. Order parameters fixed:
    7203 / buy / 100 / market
13. execution_prepared recorded
14. Human submits order
15. execution_submitted recorded
16. safety_lock applied

---

## 15. Legacy but Still Present Components

### Verified Existing DB Execution Paths

The following components perform direct DB operations:

- scripts/registrar/registrar_db_runner.py
- scripts/collector/collector_run_writer.py
- scripts/collector/indicator_writer.py
- scripts/collector/snapshot_writer.py
- scripts/openclaw/run_simulated_order.py

These scripts use psycopg and OPENCLAW_TRACE_DB_* environment variables.

---

### Verified Existing Collector / Proposal Pipeline

The following pipeline is implemented:

1. kabuStation API (symbol registration + board fetch)
2. board snapshot insertion (public.board_snapshots)
3. indicator_observation (research.trace_event)
4. hypothesis_trigger_once.py
5. proposal_trigger_once.py

This indicates a previously established full observation → interpretation pipeline.

---

### Current Interpretation

The system contains a broader operational pipeline than currently reflected in some anchor documents.

Some components are:
- implemented
- partially verified
- not actively used in current Phase 5 workflow

---

### Open Questions

- Does the "openclaw" DB role still exist?
- What are its privileges?
- Which scripts are currently executable without modification?
- Should legacy pipelines be reintegrated into Phase 5+ execution flow?

---

### Institutional Note

This section exists to reconcile:
- historical implementation state
- current anchor definitions
- future integration decisions

This is not a rollback, but a visibility restoration.

---

---

## 16. Market Data Readiness (KabuStation Constraint)

### Definition

market_data_ready =
  kabuStation running
  AND API token valid
  AND symbol registered

---

### Operational Rule

KabuStation requires symbol registration for each session.

Therefore:

- At the beginning of each session:
  - symbol registration must be verified
- If no symbols are registered:
  - re-registration must be performed before data collection

---

### Institutional Implication

This condition affects:

- Collector pipeline execution
- Indicator generation
- Downstream hypothesis / proposal triggers

Without symbol registration:

- board data cannot be fetched
- entire observation pipeline becomes inactive

---

### Status

This condition is:

- operationally verified
- not yet fully integrated into execution readiness definition
- required for Phase 5+ stable operation

---

## 17. Integrated ATOS Operational Loop (Pre-Phase5)

The system now forms a continuous pipeline:

kabuStation
→ board_snapshot (DB)
→ indicator_observation (DB)
→ hypothesis_proposed (conditional)
→ proposal_drafted (conditional)
→ execution_prepared
→ human execution

---

### Status

- Observation pipeline: active
- Interpretation pipeline: active (conditional triggers)
- Execution pipeline: ready
- Market data readiness: defined

---

### Interpretation

ATOS is no longer a set of independent components.

It now operates as an integrated loop, where:

- observation feeds interpretation
- interpretation feeds proposal
- proposal feeds execution
- execution can feed future observation

---

### Note

This loop is not yet fully automated.
Human-in-the-loop execution remains enforced.

---

## 18. OpenClaw Runtime Requirements (Discovered in Phase 4.5)

### Summary

During Phase 4.5 test execution, several critical runtime requirements were identified.
These are not optional optimizations but mandatory conditions for successful execution.

---

### 1. Repository Root Alignment

OpenClaw must explicitly operate within:

/mnt/c/ai-trading-os-private

Without this:
- scripts may appear missing
- AAB files may not be found
- execution paths fail

---

### 2. Virtual Environment Activation

OpenClaw must activate:

source scripts/registrar/.venv/bin/activate

Without this:
- psycopg import fails
- DB connection is not possible

---

### 3. Environment Variable Loading

OpenClaw must load:

source .env.local

Without this:
- KABU_API_HOST is missing
- API execution fails

---

### 4. Market Data Dependency

market_data_ready is not theoretical.

It is operationally required:

- kabuStation symbol registration is session-scoped
- symbol must be re-registered each session if missing
- collector pipeline must be run when NOT READY

---

### 5. Operator vs Registrar Mode Separation

OpenClaw operates in two distinct modes:

Registrar Mode:
- task-bound execution
- no scope expansion
- strict constraint enforcement

Operator Mode:
- state inspection
- conditional branching
- pipeline execution

Mixing these modes leads to execution ambiguity.

---

### Status

All above conditions were validated in Phase 4.5 test execution.

System behavior:

- READY state correctly detected
- simulated_order successfully executed
- execution_recorded produced
- dry_run constraints preserved

---

### Conclusion

OpenClaw is capable of operating as a session operator,
provided that runtime environment is explicitly prepared.
