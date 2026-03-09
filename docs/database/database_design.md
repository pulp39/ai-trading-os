# docs/database/database_design.md

# Database Design

AI Trading OS  
Database System: PostgreSQL 16  
Host: VM-B

---

# Purpose

The database stores the institutional memory of the research system.

Categories of stored information include:

- market observations
- operational logs
- research records
- governance-adjacent agent metadata
- historical infrastructure milestones

The database is the factual memory layer of the system.

---

# Database Identity

## Host VM
VM-B

## Database name
`trading`

## Primary access pattern
Application access from VM-A using the `research` role

---

# Schemas

## `ops`
Operational system records and service-state information.

## `research`
Research council activity, trace events, proposals, agent registry, and role assignments.

## `public`
Currently contains prototype market-oriented structures such as `board_snapshots`.

---

# Current Important Tables

## `public.board_snapshots`
Prototype market data table currently used as an early foundation structure.

## `ops.collector_status`
Operational state table for future collector processes.

## `research.trace_event`
Chronological research and infrastructure event archive.

## `research.proposal`
Structured research hypotheses and proposal records.

## `research.agent`
Registry of participating human and AI agents.

## `research.role`
Registry of institutional role types.

## `research.agent_role`
Mapping between agents and roles.

---

# `research.trace_event` Structure

The `research.trace_event` table is a central archive table and currently includes:

- `id`
- `ts`
- `session_id`
- `agent_id`
- `actor_type`
- `event_type`
- `symbol`
- `exchange`
- `content`
- `parent_event_id`
- `metadata`

Important note:

The narrative field in this table is named **`content`**, not `description`.

This distinction matters for operational SQL and for future client libraries.

---

# Current Recorded History

The database already contains foundation-era institutional history, including:

- appointment of the librarian
- naming convention update
- schema creation
- bootstrap definition
- VM-A environment setup
- first application-level handshake validation

This makes the database not only a storage system, but an active historical ledger for system evolution.

---

# Access Model

Current application access is based on the `research` role.

Validated connection path:

- client: VM-A
- server: VM-B
- database: `trading`
- role: `research`

This role has been configured for current research-layer interaction and validation work.

---

# Development Notes

A shared DB access module now exists in:

- `src/common/db.py`

A thin validation script exists in:

- `scripts/db/test_connection.py`

This separation keeps reusable connection logic out of experiment scripts.

`.env` loading is handled locally and should remain out of version control.

The DB loader is designed to tolerate Windows UTF-8 BOM in `.env` files.

---

# Design Philosophy

The repository and the database serve distinct but complementary purposes.

## Git repository
Stores:

- governance text
- architecture documents
- bootstrap SQL
- reproducible source definitions

## Database
Stores:

- factual events
- operational state
- research records
- runtime institutional memory

This distinction should remain clear as the system evolves.

---

# Current Operational Notes

PostgreSQL is configured for internal network access within the validated Hyper-V segment.

Current database endpoint:

- `192.168.250.11:5432`

Current validated application role:

- `research`

Current validated application database:

- `trading`

---

# Evolution Path

The present database design is intentionally foundational.

Future evolution may include:

- dedicated market-data schemas
- stricter privilege segmentation
- collector-owned write paths
- execution-only audit schemas
- derived analytics tables
- policy-aware proposal storage

Those expansions are intentionally deferred until the shared DB library is stabilized and current foundations are committed cleanly.

---

# Current Interpretation

The database should now be understood as an operational institutional memory layer with validated application access, not merely a schema draft.