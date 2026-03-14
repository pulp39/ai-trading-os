DB_STATUS_ANCHOR.md 完全版をコピペ

ファイル名：

docs/anchors/DB_STATUS_ANCHOR.md

本文はこれです。

# DB_STATUS_ANCHOR

Version: 1.0  
Date: 2026-03-14  
Status: active  
Purpose: Canonical database state reference for AI Trading OS

---

## 1. Purpose

This document defines the canonical database state currently recognized by AI Trading OS.

It serves as the institutional reference for database host identity, schema structure, core tables, known users, and current design assumptions relevant to execution, trace_event recording, and future registrar-linked runner design.

This anchor must be interpreted consistently with:

- `constitution.md`
- `docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md`
- `docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md`
- `docs/anchors/EXECUTION_MODEL_ANCHOR.md`

---

## 2. Database Identity

Current canonical database:

- Database name: `trading`
- Confirmed PostgreSQL version: `PostgreSQL 16.13`
- Runtime environment: `Ubuntu 24.04` family environment
- Observed connection context at inspection time: connected as `postgres`

This anchor describes the database state of the AI Trading OS institutional environment and is not merely a generic PostgreSQL description.

---

## 3. Host and Access Context

Canonical DB host:

`192.168.250.11`

Canonical SSH access path:

```text
ssh makoto@192.168.250.11

This host is the current canonical database node for the AI Trading OS environment.

At the time of inspection, the SQL session confirmed the trading database but did not return populated server address or server port values through inet_server_addr() / inet_server_port() in the observed local session context.

4. Canonical Database Rule

For institutional purposes, the canonical operational database is:

trading

All schema interpretation, trace_event design, proposal persistence, collector status interpretation, and future registrar-linked DB work must align with this database unless explicitly superseded through institutional procedure.

5. Schemas

Confirmed schemas relevant to AI Trading OS:

public

ops

research

Additional default PostgreSQL schemas were also present during inspection:

information_schema

pg_catalog

pg_toast

For institutional interpretation, the operational schema focus is:

public

ops

research

6. Confirmed Base Tables

Confirmed base tables in the institutional schemas at inspection time:

6.1 ops

ops.collector_status

6.2 public

public.board_snapshots

6.3 research

research.agent

research.agent_role

research.proposal

research.role

research.trace_event

These tables are part of the currently observed database state.

7. Core Institutional Tables

The following tables are the core tables relevant to the current institutional operating model.

7.1 public.board_snapshots

Market data core table.

7.2 ops.collector_status

Collector operational status table.

7.3 research.trace_event

Institutional event recording table.

7.4 research.proposal

Proposal persistence table.

These four tables form the minimum database backbone for current collector, governance, and execution-linked institutional recording.

8. Confirmed Non-Present Reserved Table

The following table was checked and was not present at inspection time:

ops.market_snapshot

Institutional interpretation:

ops.market_snapshot remains a reserved future consolidation target

it is not currently the active market-data core table

current market-data core status belongs to public.board_snapshots

This distinction is important for future runner design and DB evolution.

9. Table Structure Summary
9.1 public.board_snapshots

Confirmed columns:

id — bigint — primary key — default sequence

captured_at — timestamptz — not null — default now()

symbol — text — not null

exchange — integer — not null

current_price — numeric

bid_price — numeric

ask_price — numeric

bid_qty — numeric

ask_qty — numeric

trading_volume — numeric

vwap — numeric

payload — jsonb — not null

Interpretation:

board_snapshots stores structured market observation records with both normalized fields and raw/extended JSON payload.

9.2 ops.collector_status

Confirmed columns:

id — bigint — primary key — default sequence

ts — timestamptz — not null — default now()

collector_name — text — not null

run_id — text

symbol — text

exchange — integer

status — text — not null

rows_written — integer — default 0

message — text

error_detail — text

metadata — jsonb — not null — default '{}'::jsonb

Interpretation:

collector_status captures collector execution state, run metadata, result counts, and failure context.

9.3 research.trace_event

Confirmed columns:

id — bigint — primary key — default sequence

ts — timestamptz — not null — default now()

session_id — text

agent_id — text — not null

actor_type — text — not null

event_type — text — not null

symbol — text

exchange — integer

content — text

parent_event_id — bigint

metadata — jsonb — not null — default '{}'::jsonb

Interpretation:

trace_event is the canonical institutional event log for AI Trading OS.
It is suitable for recording bounded execution outcomes, governance-relevant actions, and institutional traceability.

9.4 research.proposal

Confirmed columns:

id — bigint — primary key — default sequence

ts — timestamptz — not null — default now()

session_id — text

agent_id — text — not null

proposal_type — text — not null

symbol — text

exchange — integer

title — text

proposal_text — text — not null

confidence — numeric

status — text — not null — default 'proposed'

linked_event_id — bigint

metadata — jsonb — not null — default '{}'::jsonb

Interpretation:

proposal is the canonical proposal log table and supports proposal typing, text persistence, confidence annotation, status tracking, linkage to events, and structured metadata.

10. Primary Key State

Confirmed primary keys in relevant schemas:

ops.collector_status → primary key on id

public.board_snapshots → primary key on id

research.agent → primary key on id

research.agent_role → primary key on id

research.proposal → primary key on id

research.role → primary key on id

research.trace_event → primary key on id

Institutional interpretation:

The database currently uses a simple and legible primary-key convention centered on id bigint sequence-backed identifiers.

11. Known Users

Confirmed database roles relevant to the institutional environment:

trading_user

research

claude_registrar

Observed role properties at inspection time:

all three are non-superuser roles

none has CREATEROLE

none has CREATEDB

all three have login capability

Institutional interpretation:

claude_registrar is present as a real database login role and can therefore be treated as a concrete DB integration target for Assistant Registrar execution design, subject to privilege confirmation and implementation rules.

12. Current Design Rule

Current canonical design rule:

public.board_snapshots is the active market-data core table.

ops.market_snapshot is reserved for future consolidation and is not currently active.

This rule must be respected by:

collector design

runner design

DB migration planning

trace_event-linked execution design

registrar task automation planning

No new component should assume ops.market_snapshot is already active unless the database state has actually changed and the anchor has been updated institutionally.

13. Use in Future Execution Design

This DB anchor must be consulted for future work involving:

trace_event insertion design

registrar-linked execution reporting

OpenClaw database access design

claude_registrar integration validation

runner design such as registrar_task_runner.py

proposal/trace linkage design

collector-to-governance data path interpretation

This file is the canonical DB reference for institutional alignment.

14. Current Confidence Level

Confidence in the following facts is high because they were directly verified from the live DB session:

database name

PostgreSQL version

schema list

confirmed table list

absence of ops.market_snapshot

core table column structures

primary keys

existence of known roles

Open items not fully established in this anchor:

detailed privilege matrix for each role

foreign key relationships, if any

row counts / operational volumes

application-side connection path used by each runtime participant

These can be added in future revisions if needed.

15. Final Rule

Until superseded by later verified institutional update:

trading is the canonical DB

192.168.250.11 is the canonical DB host

public.board_snapshots is the market-data core

research.trace_event is the institutional event log core

research.proposal is the proposal persistence core

claude_registrar is a real login-role integration target for future Assistant Registrar execution design

This file is the canonical database state reference for AI Trading OS.