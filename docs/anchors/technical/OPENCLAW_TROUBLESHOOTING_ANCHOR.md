anchor_id: OPENCLAW_INCIDENT_PATTERNS
title: OpenClaw Incident Patterns
type: technical
status: active
date: 2026-04-01
---

# OPENCLAW INCIDENT PATTERNS

## Purpose

Capture recurring failure patterns and their correct resolution approach.

---

## Pattern 1: Environment Misinterpretation

env exists ≠ env is used

WSL environment visibility does not guarantee PowerShell usage.

---

## Pattern 2: Boundary Separation

WSL → Python → subprocess → PowerShell → API

Each layer must be treated independently.

---

## Pattern 3: Port / Password Mapping

- 18081 → test
- 18080 → production

No fallback allowed.

---

## Pattern 4: Infinite Diagnosis Loop

Do not return to env investigation.

Reuse known working path.

---

## Pattern 5: Trace Event Failure

- use nextval()
- avoid setval()
- ensure minimal privilege compatibility

---

## Pattern 6: Metadata vs Content Mismatch

Gate reads metadata.

State must exist in metadata, not only content.

---

## Reference

For execution rules, see:
EXECUTION_SAFETY_ANCHOR.md

---