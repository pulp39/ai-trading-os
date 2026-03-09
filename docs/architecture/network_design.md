# docs/architecture/network_design.md

# Network Design

AI Trading OS

---

# Current Network Topology

The current working topology is a **single shared internal Hyper-V research network** used to establish reliable laboratory-to-memory connectivity.

Working segment:

- `192.168.250.0/24`

This segment currently provides the validated path between VM-A and VM-B.

---

# Virtual Switch State

## Active internal switch
- `vSwitch-Trading`

Both primary system VMs are currently attached to this switch.

## Historical note
A prior split-switch state existed:

- VM-A on `vSwitch-Trading`
- VM-B on `vSwitch-Research`

That topology prevented direct reachability and blocked the initial application-level database handshake.

The current aligned switch state is intentional for the present phase.

---

# Virtual Machine Addresses

## VM-A
Research environment  
IP: `192.168.250.10`

## VM-B
Database server  
IP: `192.168.250.11`

PostgreSQL endpoint:

- `192.168.250.11:5432`

---

# Connectivity Goals

The validated connectivity model is now:

- VM-A → VM-B PostgreSQL access
- VM-A ↔ VM-B administrative reachability
- VM-A ↔ VM-B low-latency internal communication
- VM-B → package/update access as required by system administration

---

# Confirmed Working Paths

The following paths have been validated:

- ICMP reachability from VM-A to VM-B
- TCP 5432 reachability from VM-A to VM-B
- SSH reachability to VM-B
- application-level PostgreSQL connection from VM-A to VM-B

---

# Database Access Policy

Current intended database access pattern:

- VM-A acts as laboratory / client environment
- VM-B acts as memory / PostgreSQL host

Primary application path:

- VM-A Python process
- `research` application role
- database `trading`
- PostgreSQL on VM-B

---

# Addressing Notes

A previous VM-B static configuration used the `192.168.251.x` segment.  
That configuration was updated during handshake validation to match the current active internal network.

Current canonical addressing:

- VM-A: `192.168.250.10`
- VM-B: `192.168.250.11`

---

# Design Principle

At the current project stage, network design is optimized for:

- correctness
- repeatability
- low-complexity validation
- successful internal research communication

Future network segmentation may reintroduce separation between:

- research activity
- database services
- trading execution

However, that expansion is intentionally deferred until after the shared DB access layer is stabilized.

---

# Current Interpretation

The network is no longer a planned abstraction only.

It is now a working internal path enabling the first validated bridge between:

- Laboratory (VM-A)
- Memory (VM-B)