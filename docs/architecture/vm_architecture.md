# VM Architecture

AI Trading OS

---

# Host Environment

Host machine

Windows 11

Hypervisor

Hyper-V

---

# Virtual Machines

The system is divided into specialized virtual machines.

---

# VM-A

Role

Research and development environment

Responsibilities

- collector development
- AI research tools
- experiment scripts
- API testing
- Git repository
- interaction with research database

VM-A acts as the **active laboratory environment**.

---

# VM-B

Role

PostgreSQL research database server

Responsibilities

- storage of market observations
- operational logs
- research records
- agent registry
- institutional memory

VM-B acts as the **memory and archive** of the system.

---

# Design Principle

Research environment and database infrastructure must remain separated.

This separation ensures:

system stability  
traceable data management  
clear institutional boundaries

---

# Database Connection

VM-A connects to PostgreSQL running on VM-B.

Database  
trading

Default port  
5432