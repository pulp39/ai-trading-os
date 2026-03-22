# Phase 5 Symbol Selection Criteria

Date: 2026-03-22  
Status: draft  
Scope: P-028 Phase 5 — first live order symbol selection  

---

## Objective

Define a deterministic and safe selection filter for the first live-order test symbol.

The goal is not optimal trading, but **maximum controllability and minimal risk of system ambiguity**.

---

## 1. Hard Constraints（必須条件）

The symbol MUST satisfy all of the following:

- spot equity (no derivatives)
- no leverage required
- no margin dependency
- no special settlement rules
- available during standard market hours
- supported by kabu API in current environment

---

## 2. Liquidity Requirements

The symbol MUST:

- have sufficient trading volume
- have tight bid/ask spread
- allow immediate cancel confirmation

Reason:
→ minimize `transmission_unknown` risk

---

## 3. Execution Simplicity

The symbol MUST:

- support simple order types (market or limit)
- not require complex routing
- not trigger special exchange conditions

---

## 4. Observability

The symbol MUST allow:

- clear price observation
- clear execution confirmation
- clear cancel confirmation

---

## 5. Familiarity Constraint

The symbol SHOULD:

- be operationally familiar
- have been observed in prior tests or environment checks

---

## 6. Exclusion Criteria

The symbol MUST NOT be:

- illiquid
- halted
- volatile beyond normal range
- newly listed with unstable behavior
- dependent on special trading sessions

---

## 7. Selection Philosophy

The first symbol is not chosen for profit.

It is chosen for:

> determinism, safety, and interpretability

---

## 8. Output Requirement

The selection process must produce:

- symbol (string)
- justification (why it satisfies all constraints)
- known risks (if any)