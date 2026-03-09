# trace_event Semantics

This document defines the minimal semantic rules for writing events into the `research.trace_event` table.

The purpose of these rules is to maintain **institutional memory consistency** across roles, agents, and system components within the AI Trading OS.


---

# Purpose

`research.trace_event` functions as the **institutional historical record** of the AI Trading OS.

Events recorded in this table represent meaningful operational or architectural occurrences in the system's lifecycle.

The goal is not to record every technical detail, but to preserve **structural and operational milestones** that help explain how the system evolved.


---

# Event Record Structure

A typical trace event contains the following fields.

| Field | Meaning |
|------|------|
| `event_type` | Stable classification of the event |
| `agent_id` | Identifier of the role or agent that generated the event |
| `content` | Human-readable description of the event |
| `metadata` | Optional structured information describing context |

These fields together form a durable historical record.


---

# Field Semantics

## event_type

`event_type` identifies the type of event that occurred.

The name should be **stable and descriptive**, allowing future readers to understand the nature of the event without additional interpretation.

Examples:

- `environment_setup`
- `infrastructure_validation`
- `codebase_refactor`
- `collector_foundation`

Event types should avoid temporary wording or experimental naming.


---

## agent_id

`agent_id` identifies the role or system component responsible for generating the event.

Examples:

- `base_collector`
- `system`
- `gpt54_librarian`

The identifier should remain stable across time whenever possible.


---

## content

`content` is a human-readable explanation of the event.

Guidelines:

- Write complete sentences.
- Describe the meaning of the event, not just the action.
- Avoid internal shorthand or temporary debugging notes.

Good example:
