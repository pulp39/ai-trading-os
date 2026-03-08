# Network Design

AI Trading OS

---

# Internal Research Network

Network range

192.168.251.0/24

Gateway

192.168.251.1

---

# Virtual Machine Addresses

VM-A  
Research environment  
IP: TBD

VM-B  
Database server

192.168.251.10

PostgreSQL port

5432

---

# Connectivity

VM-A → VM-B  
Database access

VM-B → Internet  
Package updates

VM-A ↔ VM-B  
SSH access

---

# NAT Structure

Research NAT

192.168.251.0/24

Trading NAT

192.168.250.0/24

---

# Design Goal

The network structure separates:

research activity  
database storage  
future trading execution

---

# Database Endpoint

PostgreSQL server

VM-B

192.168.251.10:5432