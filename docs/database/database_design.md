# Database Design

AI Trading OS

Database System  
PostgreSQL 16

Host  
VM-B

---

# Purpose

The database stores the institutional memory of the research system.

Categories of stored information:

market observations  
operational logs  
research records

---

# Schemas

ops  
Operational system logs.

research  
Research council activity.

---

# ops schema

Used for operational monitoring.

Example tables

collector_status

---

# research schema

Used for institutional research records.

Tables

agent  
Registered participants of the research council.

role  
Defined responsibility domains.

agent_role  
Assignment of roles to agents.

trace_event  
Chronological record of research events.

proposal  
Research hypotheses and proposals.

---

# Design Philosophy

Git repository

Holds governance and documentation.

Database

Stores factual research records and system events.

---

# Prototype Tables

The table `public.board_snapshots` currently acts as a prototype
market data table.

Future system evolution may migrate this table to a dedicated
schema such as:

`ops.market_snapshot`
`market.board_snapshots`