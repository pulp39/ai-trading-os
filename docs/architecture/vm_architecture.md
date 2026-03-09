# docs/architecture/vm_architecture.md

# VM Architecture

AI Trading OS

---

# Host Environment

## Host machine
Windows 11

## Hypervisor
Hyper-V

The host machine provides persistent virtualization infrastructure for the research system.

---

# Virtual Machine Model

The system is divided into specialized virtual machines.

This separation is intentional and foundational.

The current architecture distinguishes between:

- active research / application environment
- persistent institutional memory environment

---

# VM-A Role

## VM-A
Research and development environment

VM-A acts as the **active laboratory environment**.

Current responsibilities:

- Python research environment
- experiment scripts
- application validation
- database client testing
- Git working copy
- shared DB access library development
- future collector prototype development

VM-A is the node where new research tooling is first made operational.

---

# VM-B Role

## VM-B
PostgreSQL research database server

VM-B acts as the **memory and archive** of the system.

Current responsibilities:

- storage of market observations
- operational logs
- research records
- agent registry
- role registry
- institutional trace history
- persistence of governance-adjacent research metadata

VM-B is the durable memory substrate of AI Trading OS.

---

# Separation Principle

Research environment and database infrastructure must remain separated.

This separation ensures:

- system stability
- traceable data management
- operational clarity
- explicit institutional boundaries
- reduced coupling between experimentation and persistence

---

# Current Verified Connection Model

A validated application path now exists:

- VM-A Python runtime
- PostgreSQL client library (`psycopg`)
- application role `research`
- database `trading`
- PostgreSQL server on VM-B

This path constitutes the first verified application-level handshake in the system.

---

# Current Addressing

## VM-A
- `192.168.250.10`

## VM-B
- `192.168.250.11`

## Database
- `trading`

## PostgreSQL port
- `5432`

---

# Operational Interpretation

VM-A should be understood as:

**Laboratory**

VM-B should be understood as:

**Memory**

The significance of the current architecture is that the laboratory can now reliably write to and read from memory through an intended application identity.

---

# Future Expansion

Additional VMs may later be introduced for clearer separation of duties, such as:

- collector runtime
- execution engine
- risk control environment
- backtesting environment

However, those roles are intentionally deferred until the shared DB access layer is stabilized.

---

# Current Milestone

The VM architecture is no longer only conceptual.

It has now been validated through successful end-to-end communication between:

- VM-A research environment
- VM-B PostgreSQL memory system