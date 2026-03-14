# DB_STATUS_ANCHOR

Version: 1.2
Date: 2026-03-14
Status: active
Purpose: Database state reference for AI Trading OS

---

## 1. About This Document

This document describes the current database state of AI Trading OS.

It serves as a reference for database host identity, schema structure,
core tables, known users, and current design assumptions relevant to
execution, trace_event recording, and runner design.

This document is intended to be read alongside:

- `constitution.md`
- `docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md`
- `docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md`
- `docs/anchors/EXECUTION_MODEL_ANCHOR.md`

---

## 2. Database Identity

Current canonical database:

- Database name: `trading`
- Confirmed PostgreSQL version: `PostgreSQL 16.13`

Note: The runtime OS distribution was observed during inspection but
has not been precisely confirmed. See Section 14 for unverified items.

---

## 3. Host and Access Context

Canonical DB host: `192.168.250.11`

SSH access: `ssh makoto@192.168.250.11`

At the time of inspection, the SQL session was established via a local
Unix socket connection. When connected through a local Unix socket,
`inet_server_addr()` and `inet_server_port()` return NULL — this is a
property of the connection method, not an indication of missing host
configuration. The host address `192.168.250.11` is confirmed through
network configuration.

---

## 4. Canonical Database

The operational database for AI Trading OS is:

`trading`

Schema interpretation, trace_event design, proposal persistence,
collector status, and registrar-linked DB work all align with this
database unless explicitly updated through institutional procedure.

---

## 5. Schemas

Operational schemas:

- `public`
- `ops`
- `research`

Additional default PostgreSQL schemas (not part of operational scope):
`information_schema`, `pg_catalog`, `pg_toast`

---

## 6. Confirmed Tables

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

---

## 7. Core Tables

| Table | Purpose |
|---|---|
| public.board_snapshots | Market data core |
| ops.collector_status | Collector operational status |
| research.trace_event | Institutional event log |
| research.proposal | Proposal persistence |

---

## 8. Reserved Table (Not Yet Active)

`ops.market_snapshot` was checked and was not present at inspection
time.

It remains a reserved future consolidation target. Current market data
is stored in `public.board_snapshots`. Runner and collector design
should not assume `ops.market_snapshot` is active unless this document
has been updated to reflect a verified change.

---

## 9. Table Structures

### 9.1 public.board_snapshots

| Column | Type | Notes |
|---|---|---|
| id | bigint | primary key |
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

Stores structured market observation records with normalized fields
and raw JSON payload.

### 9.2 ops.collector_status

| Column | Type | Notes |
|---|---|---|
| id | bigint | primary key |
| ts | timestamptz | not null, default now() |
| collector_name | text | not null |
| run_id | text | |
| symbol | text | |
| exchange | integer | |
| status | text | not null |
| rows_written | integer | default 0 |
| message | text | |
| error_detail | text | |
| metadata | jsonb | not null, default '{}' |

Captures collector execution state, run metadata, result counts, and
failure context.

### 9.3 research.trace_event

| Column | Type | Notes |
|---|---|---|
| id | bigint | primary key |
| ts | timestamptz | not null, default now() |
| session_id | text | |
| agent_id | text | not null |
| actor_type | text | not null |
| event_type | text | not null |
| symbol | text | |
| exchange | integer | |
| content | text | |
| parent_event_id | bigint | |
| metadata | jsonb | not null, default '{}' |

The canonical institutional event log. Suitable for recording bounded
execution outcomes and governance-relevant actions.

### 9.4 research.proposal

| Column | Type | Notes |
|---|---|---|
| id | bigint | primary key |
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
| metadata | jsonb | not null, default '{}' |

Supports proposal typing, text persistence, status tracking, and
linkage to events.

---

## 10. Primary Keys

All institutional tables use `id bigint` as the primary key, backed
by a sequence.

---

## 11. Known Database Roles

| Role | Login | Superuser | Notes |
|---|---|---|---|
| trading_user | yes | no | |
| research | yes | no | |
| claude_registrar | yes | no | Privilege scope not yet verified |

`claude_registrar` is a real login role and a candidate integration
target for Assistant Registrar execution. Privilege verification
(INSERT/SELECT scope) is needed before runner implementation proceeds.
See Section 14.

---

## 12. Current Design Note

`public.board_snapshots` is the active market data table.
`ops.market_snapshot` is reserved for future use and is not currently
active.

This distinction is relevant for collector design, runner design, and
DB migration planning.

---

## 13. Relevance to Future Work

This document is a useful reference for:

- trace_event insertion design
- registrar-linked execution reporting
- OpenClaw database access design
- claude_registrar integration
- runner design (e.g., `registrar_task_runner.py`)
- proposal/trace linkage design

---

## 14. Confirmed Facts and Unverified Items

### 14.1 Confirmed

- Database name: `trading`
- PostgreSQL version: `16.13`
- Host: `192.168.250.11`
- Schemas: `public`, `ops`, `research`
- Tables listed in Section 6
- `ops.market_snapshot` not present
- Column structures in Section 9
- Primary key convention
- Existence of roles: `trading_user`, `research`, `claude_registrar`
- Login capability of all three roles
- NULL behavior of `inet_server_addr()` under Unix socket connection

### 14.2 Not Yet Verified

- Exact runtime OS distribution
  (observed as Ubuntu 24.04 series; precise version not confirmed)
- Privilege scope for `claude_registrar`
  (priority item before runner implementation)
- Foreign key relationships
- Row counts and data volumes
- Application-side connection paths

---

## 15. Current Reference State

Until updated through institutional procedure:

- `trading` is the operational database
- `192.168.250.11` is the DB host
- `public.board_snapshots` is the market data table
- `research.trace_event` is the event log
- `research.proposal` is the proposal store
- `claude_registrar` is the target role for Assistant Registrar DB
  integration, pending privilege verification