# Phase 5 Live Order Test Conditions

Date: 2026-03-22
Status: draft
Scope: P-028 Phase 5 live-order boundary definition

## Objective

Define the minimal and safest possible live-order test conditions for the first bounded external order transmission.

This document does not authorize execution.
It only defines the conditions that must be satisfied before any Phase 5 live-order test may proceed.

---

## 1. Institutional Preconditions

The following must already be true:

- external_order_allowed is established
- Phase 5 draft is recorded
- Registrar task execution path is validated
- OpenClaw bounded execution path is validated
- Founder explicit authorization is still required

---

## 2. Symbol Conditions

The first live-order test symbol must satisfy all of the following:

- liquid enough for immediate cancel/confirmation handling
- operationally familiar
- simple spot-equity handling preferred
- no special settlement or unusual market structure
- no leverage-dependent requirement for the first test

Symbol is not yet fixed.

---

## 3. Quantity Conditions

The first live-order test must use:

- minimum valid quantity only
- single order only
- no scaling
- no batch execution
- no repeated attempt under the same authorization

Quantity is not yet fixed.

---

## 4. Order Type Conditions

The first live-order test should prefer the simplest possible order type.

Constraints:

- one order only
- no strategy logic
- no chained orders
- no automatic retry
- no autonomous follow-up order

Order type is not yet fixed.

---

## 5. Time Window Conditions

The first live-order test must occur within a bounded execution window.

Conditions:

- explicit start and stop time
- Founder-approved window
- short duration only
- no carry-over beyond the approved window
- if the window expires, execution returns to blocked

---

## 6. Safety Conditions

The following must remain true:

- one authorization = one transmission
- authorization_consumed is irreversible
- transmission_unknown prohibits new order submission
- post_submit_safety_lock is mandatory
- block fallback remains available at all times

---

## 7. Market Rollback Conditions

If a live order is submitted, the following rollback handling must be available:

- cancel request path
- cancel confirmation path
- status inquiry path
- bounded trace_event recording path

---

## 8. Explicit Non-Goals

This Phase 5 test is not for:

- profit seeking
- strategy validation
- repeated execution
- capital deployment escalation
- autonomous trading start

---

## 9. Remaining Items To Fix

The following must be explicitly defined next:

- symbol
- quantity
- order_type
- execution window
- transmission timeout
- cancel timeout