# docs/architecture/system_overview.md

# System Overview

AI Trading OS  
Version 1.2  
Date 2026-03-09

---

# System Purpose

The system exists to support cooperative research between humans and artificial intelligence in financial market analysis.

The platform integrates:

- market observation
- AI-assisted hypothesis generation
- traceable research records
- controlled trading execution design
- long-term institutional memory

The system is not intended to be merely a trading bot.  
It is designed as a durable research operating environment.

---

# Institutional Structure

The system operates as a research institution.

## Governance
Defined by the AI Trading Research Council Charter.

## Memory
Maintained by a PostgreSQL database on VM-B.

## Research Activity
Performed within the VM-A environment.

## Archive
Maintained through both Git-tracked documentation and database-resident event history.

---

# Architectural Layers

## Infrastructure Layer
Host machine, Hyper-V, internal virtual network, and VM layout.

## Memory Layer
PostgreSQL database storing research events, proposals, operational records, and agent registry data.

## Knowledge Layer
Git repository containing governance documents, architecture records, and bootstrap SQL.

## Agent Layer
Human and AI agents participating in the research council.

## Research Layer
Hypothesis generation, experimentation, validation, and institutional interpretation.

## Execution Layer
Future controlled trading execution environment.  
This layer is not yet implemented.

---

# Current Operating Nodes

## Host Machine
Windows 11 with Hyper-V

## VM-A
Research / development / validation environment

Current confirmed uses:

- Python research environment
- application-level database client
- local repository working copy
- shared DB access code
- future collector prototype development

## VM-B
PostgreSQL research database

Current confirmed uses:

- database `trading`
- storage of institutional events
- archive of research activity
- registry of agents and roles
- operational persistence

---

# Current System State

The foundation phase has moved into an operationally validated state.

Confirmed current state:

- governance foundation established
- public Git repository established
- bootstrap SQL defined
- database foundation schema established
- VM-A development environment established
- VM-A to VM-B PostgreSQL handshake achieved
- shared DB access module introduced
- first infrastructure validation event recorded in `research.trace_event`

This means the system now possesses both designed structure and verified internal communication.

---

# System Philosophy

The system is designed for:

- traceability
- institutional memory
- structured research
- reproducibility
- long-term evolution

The guiding principle remains:

**Do not expand scope prematurely.**

Each phase should become operationally true before the next phase is introduced.

---

# Documentation Structure

System documentation is organized into the following sections.

## Architecture
System structure, infrastructure topology, VM roles, and network design.

## Database
PostgreSQL schema, archive model, and research record design.

## Governance
Institutional roles and council structure.

## Bootstrap
Reproducible SQL defining the initial database foundation.

---

# Current Interpretation

AI Trading OS is now beyond concept-only status.

It exists simultaneously as:

- institutional charter
- historical archive
- foundation database
- reproducible bootstrap definition
- public versioned repository
- verified application-to-database communication path

The first operational bridge between laboratory and memory has been established.

---

# Immediate Next Phase

The next phase remains intentionally narrow.

Immediate target:

- shared database access library refinement
- reusable connection module
- clean separation between validation scripts and application code

Not yet in scope:

- collector implementation
- market ingestion engine
- proposal engine
- risk engine
- execution engine
- CI/CD
- multi-agent runtime