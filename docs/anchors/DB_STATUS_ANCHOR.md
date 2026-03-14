# DB_STATUS_ANCHOR

Version: 1.1
Date: 2026-03-14
Status: active
Purpose: Canonical database state reference for AI Trading OS

---

## 1. Purpose

This document defines the canonical database state currently recognized
by AI Trading OS.

It serves as the institutional reference for database host identity,
schema structure, core tables, known users, and current design assumptions
relevant to execution, trace_event recording, and future registrar-linked
runner design.

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

This anchor describes the database state of the AI Trading OS
institutional environment and is not merely a generic PostgreSQL
description.

Note: The runtime OS distribution was observed during inspection but
has not been precisely confirmed. See Section 14 for unverified items.

---

## 3. Host and Access Context

Canonical DB host:

`192.168.250.11`

Canonical SSH access path:
```text
ssh makoto@192.168.250.11
```

This host is the current canonical database node for the AI Trading OS
environment.

At the time of inspection, the SQL session was established via a local
Unix socket connection. When connected through a local Unix socket,
the PostgreSQL functions `inet_server_addr()` and `inet_server_port()`
return NULL, as they reflect the TCP network address rather than the
socket path. This NULL result is a property of the connection method,
not an indication of missing host configuration.

The canonical host address `192.168.250.11` is confirmed through network
configuration, not through these SQL functions.

---

## 4. Canonical Database Rule

For institutional purposes, the canonical operational database is:

`trading`

All schema interpretation, trace_event design, proposal persistence,
collector status interpretation, and future registrar-linked DB work
must align with this database unless explicitly superseded through
institutional procedure.

---

## 5. Schemas

Confirmed schemas relevant to AI Trading OS:

- `public`
- `ops`
- `research`

Additional default PostgreSQL schemas were also present during inspection:

- `information_schema`
- `pg_catalog`
- `pg_toast`

For institutional interpretation, the operational schema focus is:

- `public`
- `ops`
- `research`

---

## 6. Confirmed Base Tables

Confirmed base tables in the institutional schemas at inspection time:

### 6.1 ops

- `ops.collector_status`

### 6.2 public

- `public.board_snapshots`

### 6.3 research

- `research.agent`
- `research.agent_role`
- `research.proposal`
- `research.role`
- `research.trace_event`

These tables are part of the currently observed database state.

---

## 7. Core Institutional Tables

The following tables are the core tables relevant to the current
institutional operating model.

### 7.1 public.board_snapshots

Market data core table.

### 7.2 ops.collector_status

Collector operational status table.

### 7.3 research.trace_event

Institutional event recording table.

### 7.4 research.proposal

Proposal persistence table.

These four tables form the minimum database backbone for current
collector, governance, and execution-linked institutional recording.

---

## 8. Confirmed Non-Present Reserved Table

The following table was checked and was not present at inspection time:

`ops.market_snapshot`

Institutional interpretation:

- `ops.market_snapshot` remains a reserved future consolidation target
- it is not currently the active market-data core table
- current market-data core status belongs to `public.board_snapshots`

This distinction is important for future runner design and DB evolution.

---

## 9. Table Structure Summary

### 9.1 public.board_snapshots

Confirmed columns:

| Column | Type | Constraints |
|---|---|---|
| id | bigint | primary key, default sequence |
| captured_at | timestamptz | not null, default now() |
| symbol | text | not null |
| exchange | integer | not null |
| current_price | numeric | |
| bid_price | numeric | |
| ask_price | numeric | |
| bid_qty | numeric | |
| ask_qty | numeric | |
| trading_volume | numeric | |
| vwap | numeric | |
| payload | jsonb | not null |

Interpretation: board_snapshots stores structured market observation
records with both normalized fields and raw/extended JSON payload.

### 9.2 ops.collector_status

Confirmed columns:

| Column | Type | Constraints |
|---|---|---|
| id | bigint | primary key, default sequence |
| ts | timestamptz | not null, default now() |
| collector_name | text | not null |
| run_id | text | |
| symbol | text | |
| exchange | integer | |
| status | text | not null |
| rows_written | integer | default 0 |
| message | text | |
| error_detail | text | |
| metadata | jsonb | not null, default '{}'::jsonb |

Interpretation: collector_status captures collector execution state,
run metadata, result counts, and failure context.

### 9.3 research.trace_event

Confirmed columns:

| Column | Type | Constraints |
|---|---|---|
| id | bigint | primary key, default sequence |
| ts | timestamptz | not null, default now() |
| session_id | text | |
| agent_id | text | not null |
| actor_type | text | not null |
| event_type | text | not null |
| symbol | text | |
| exchange | integer | |
| content | text | |
| parent_event_id | bigint | |
| metadata | jsonb | not null, default '{}'::jsonb |

Interpretation: trace_event is the canonical institutional event log
for AI Trading OS. It is suitable for recording bounded execution
outcomes, governance-relevant actions, and institutional traceability.

### 9.4 research.proposal

Confirmed columns:

| Column | Type | Constraints |
|---|---|---|
| id | bigint | primary key, default sequence |
| ts | timestamptz | not null, default now() |
| session_id | text | |
| agent_id | text | not null |
| proposal_type | text | not null |
| symbol | text | |
| exchange | integer | |
| title | text | |
| proposal_text | text | not null |
| confidence | numeric | |
| status | text | not null, default 'proposed' |
| linked_event_id | bigint | |
| metadata | jsonb | not null, default '{}'::jsonb |

Interpretation: proposal is the canonical proposal log table and
supports proposal typing, text persistence, confidence annotation,
status tracking, linkage to events, and structured metadata.

---

## 10. Primary Key State

Confirmed primary keys in relevant schemas:

| Table | Primary Key |
|---|---|
| ops.collector_status | id |
| public.board_snapshots | id |
| research.agent | id |
| research.agent_role | id |
| research.proposal | id |
| research.role | id |
| research.trace_event | id |

Institutional interpretation: The database currently uses a simple and
legible primary-key convention centered on `id` bigint sequence-backed
identifiers.

---

## 11. Known Users

Confirmed database roles relevant to the institutional environment:

| Role | Superuser | CREATEROLE | CREATEDB | Login |
|---|---|---|---|---|
| trading_user | no | no | no | yes |
| research | no | no | no | yes |
| claude_registrar | no | no | no | yes |

Institutional interpretation:

`claude_registrar` is present as a real database login role and can
therefore be treated as a concrete DB integration target for Assistant
Registrar execution design, subject to privilege confirmation and
implementation rules.

Note: The detailed privilege scope of `claude_registrar` — including
which schemas and tables it may read from or write to — has not yet
been verified. Confirmation of INSERT/SELECT scope is required before
runner implementation proceeds. See Section 14.

---

## 12. Current Design Rule

Current canonical design rule:

`public.board_snapshots` is the active market-data core table.

`ops.market_snapshot` is reserved for future consolidation and is not
currently active.

This rule must be respected by:

- collector design
- runner design
- DB migration planning
- trace_event-linked execution design
- registrar task automation planning

No new component should assume `ops.market_snapshot` is already active
unless the database state has actually changed and this anchor has been
updated institutionally.

---

## 13. Use in Future Execution Design

This DB anchor must be consulted for future work involving:

- trace_event insertion design
- registrar-linked execution reporting
- OpenClaw database access design
- claude_registrar integration validation
- runner design such as `registrar_task_runner.py`
- proposal/trace linkage design
- collector-to-governance data path interpretation

This file is the canonical DB reference for institutional alignment.

---

## 14. Confirmed Facts and Unverified Items

### 14.1 Confirmed Facts

The following facts are considered confirmed because they were directly
verified from a live DB session:

- database name: `trading`
- PostgreSQL version: `PostgreSQL 16.13`
- canonical DB host: `192.168.250.11`
- schema list: `public`, `ops`, `research`
- confirmed table list (Section 6)
- absence of `ops.market_snapshot`
- core table column structures (Section 9)
- primary key conventions (Section 10)
- existence of known roles: `trading_user`, `research`, `claude_registrar`
- login capability of all three roles
- NULL behavior of `inet_server_addr()` under local Unix socket connection

### 14.2 Unverified Items

The following items were not fully established during inspection and
should be verified before dependent implementation proceeds:

- exact runtime OS distribution
  (observed as Ubuntu 24.04 series; precise distribution not confirmed)
- detailed privilege matrix for each role
  (INSERT/SELECT scope for `claude_registrar` is a priority item
   before runner implementation; see Section 11)
- foreign key relationships, if any
- row counts and operational data volumes
- application-side connection path used by each runtime participant

---

## 15. Final Rule

Until superseded by a later verified institutional update:

- `trading` is the canonical DB
- `192.168.250.11` is the canonical DB host
- `public.board_snapshots` is the market-data core
- `research.trace_event` is the institutional event log core
- `research.proposal` is the proposal persistence core
- `claude_registrar` is a real login-role integration target for future
  Assistant Registrar execution design, pending privilege verification

This file is the canonical database state reference for AI Trading OS.
```

---

## 変更サマリー
```
Section 2  : "Ubuntu 24.04 family environment" 削除
             → Section 14.2 へ移動、注記追加
Section 3  : inet_server_addr() の NULL 挙動を説明補足
             (local Unix socket の性質として明示)
Section 9  : 表形式に整理 (内容変更なし)
Section 10 : 表形式に整理 (内容変更なし)
Section 11 : claude_registrar 権限未確認の注記追加
             runner実装前に確認必要と明示
Section 14 : タイトルを "Confirmed Facts and Unverified Items" に変更
             14.1 確認済み / 14.2 未確認 に分離
             未確認項目に2項目追加
Version    : 1.0 → 1.1