anchor_id: PHASE_9B_HANDOFF
title: Phase 9B Operational Learnings
type: handoff
status: active
date: 2026-04-01
---

# PHASE 9B HANDOFF

## Scope

Covers Phase 9B-1 and 9B-2 discoveries.

---

## Phase 9B-1

### Key Insight

env exists ≠ env is used

### Boundary Model

WSL → Python → subprocess → PowerShell → Invoke-RestMethod

Each boundary is independent.

---

## Port / Password Rules

- 18081 → KABU_API_TEST_PASSWORD
- 18080 → KABU_API_PASSWORD

Rules:
- no fallback
- no cross-use

---

## Anti-Pattern

.env re-diagnosis loop is prohibited.

Always reuse known working path first.

---

## Phase 9B-2

### Stable Execution Path

collector → freshness → preview → simulated_order

---

### Findings

- collector is required for fresh state
- 8306 reaches READY consistently
- 7203 / 6758 may not reach READY

---

### Execution Behavior

- READY does not imply execution
- execution can be delayed after READY

---

## Critical Discovery

Duplicate execution was possible on same READY context.

---

## Resolution

Resolved in:

P-20260401-001

---

## Status

All knowledge here has been validated in live market conditions.

---