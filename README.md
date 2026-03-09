# README.md

# AI Trading OS

AI Trading OS is an experimental research operating environment designed to study financial markets through cooperation between human researchers and artificial intelligence agents.

The system integrates:

- market data collection
- AI-assisted research
- traceable decision records
- structured database archives
- controlled trading execution environments

The system is designed as a long-term **AI Trading Research Institute OS**.

---

# Core Principles

The project is based on three fundamental layers.

## Infrastructure
Virtual machines, network topology, and application connectivity.

## Memory
A PostgreSQL database storing observations, events, proposals, and operational history.

## Governance
Institutional rules and role boundaries defined by the council charter.

---

# Research Institution

The system is governed by the **AI Trading Research Council**.

Current principal holders:

- Founder: `makoto`
- Librarian: `gpt54_librarian`

Council rules are defined in:

- `constitution.md`

---

# System Components

## Host Machine
Windows 11 Hyper-V environment

## VM-A
Research and development environment

Current role:

- Python research environment
- Git working copy
- DB client / application validation node
- shared library development
- future collector and research tooling host

## VM-B
PostgreSQL research database

Current role:

- institutional memory
- research archive
- agent and role registry
- operational event storage

---

# Current Operational State

The foundation phase is complete, and the first verified application-level connection between VM-A and VM-B has been achieved.

Confirmed current state:

- public GitHub repository established
- foundation governance documents committed
- PostgreSQL foundation schema established on VM-B
- bootstrap SQL stored in repository
- VM-A Python environment operational
- VM-A to VM-B PostgreSQL connectivity verified
- `research` application role operational
- handshake milestone recorded in `research.trace_event`

---

# Architectural Interpretation

AI Trading OS now exists as:

- institutional charter
- historical archive
- foundation database
- bootstrap specification
- public versioned repository
- validated application-to-database communication path

The system should now be understood as a functioning research infrastructure, not merely a design concept.

---

# Repository Structure

## Governance
- `constitution.md`
- `docs/governance/roles.md`

## Architecture
- `docs/architecture/system_overview.md`
- `docs/architecture/vm_architecture.md`
- `docs/architecture/network_design.md`

## Database
- `docs/database/database_design.md`
- `sql/bootstrap/`

## Application Code
- `src/common/db.py`
- `scripts/db/test_connection.py`

---

# Runtime / Local Development Notes

The repository contains reproducible infrastructure and documentation.

Sensitive runtime configuration must remain local only.

Examples:

- `.env`
- local credentials
- local virtual environments

Text files in this repository should be saved as **UTF-8 without BOM** whenever possible.

---

# Current Milestone

**Milestone achieved:**  
First verified application-level database handshake between:

- **VM-A (Laboratory)**
- **VM-B (Memory)**

This milestone is the first operational bridge between research execution and institutional memory.

---

# Next Phase

The next development phase remains intentionally narrow.

Immediate target:

- shared DB access library
- reusable connection logic
- clean separation between test scripts and application modules

Not yet in scope:

- collector implementation
- execution engine
- risk manager
- CI/CD
- advanced orchestration

---

# Foundation Timeline Reference

Foundation date:
2026-03-08

First application-level handshake achieved:
2026-03-09