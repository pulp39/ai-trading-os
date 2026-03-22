# P028_PHASE4_AUTHORIZATION_CONSUMPTION_RULES

Status: draft  
Date: 2026-03-22  
Phase: P-028 Phase 4

---

## Purpose

This document defines the institutional meaning of:

- `authorization_consumed`
- `external_order_allowed`
- minimal live real_order safety boundaries

This is a design document only.

It does **not** authorize live execution.

---

## 1. Authorization Consumption

### Definition

`authorization_consumed = true` becomes valid only when an actual
external order transmission is performed under an active authorization.

### Interpretation

The following do **not** consume authorization:

- authorization-only validation
- execution simulation
- real_order dry-run
- payload formation
- internal routing validation
- non-sending API connectivity checks

The following **does** consume authorization:

- first actual externally transmitted real_order under the active
  `single_execution` authorization scope

### Rule

If authorization scope is:

```text
single_execution