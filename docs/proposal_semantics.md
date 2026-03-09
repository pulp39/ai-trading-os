AI Trading OS
Document: proposal_semantics
Version: 1.1
Phase: proposal_layer_initialization
Status: draft
Maintainer: Librarian

Purpose

This document defines the institutional meaning and semantics of
proposal objects within AI Trading OS.

The proposal layer exists to enable structured research reasoning
without granting execution authority to any AI system.

It also establishes the safe institutional conditions under which
proposal-producing agents may participate in the system.

The proposal layer is intentionally separated from observation,
execution, and governance responsibilities.

Relationship to Collector Layer

Collector and Proposal are strictly separated layers.

Collector responsibilities:

observe system-relevant events

record institutional history

write trace_event entries

Collectors must not:

interpret observations

generate hypotheses

rank significance

propose actions

Collectors produce trace_event only.

Proposal layer begins where interpretation and hypothesis generation begin.

Definition of Proposal

A proposal is a structured research object representing:

interpretation of observed conditions

a hypothesis about system-relevant dynamics

a suggested research direction

possible experimental steps

A proposal is NOT:

a command

an execution order

a trading instruction

a risk decision

a system control signal

Proposals exist to expand institutional understanding.

They do not control the system.

Proposal Object Structure

A proposal should contain the following conceptual elements:

proposal_type

research_hypothesis

context_reference

supporting_observations

possible_experiments

confidence_statement

limitations

These elements describe reasoning rather than instructions.

Proposal vs Trace Event

trace_event

institutional memory

factual record

no interpretation

produced by collectors

proposal

research reasoning

interpretation

future-oriented thinking

produced by proposers

The two objects must remain conceptually separate.

Proposal Lifecycle

A proposal may pass through the following conceptual states:

draft

proposal_submitted

under_review

revision_requested

revised

research_accepted

research_rejected

archived

State transitions are institutional decisions.

AI agents do not autonomously finalize proposals.

Authority Boundaries

Proposal-producing agents have limited authority.

They may:

interpret observations

generate hypotheses

suggest research directions

suggest possible experiments

They may not:

execute trades

modify system architecture

alter database schema

trigger automated actions

issue commands to execution systems

All proposals must remain advisory.

First Proposer Role

The first expected proposal-producing role is:

Proposer

Initial assigned agent:

Claude

Proposer responsibilities:

generate structured research proposals

reference institutional trace_event history

suggest future research directions

clarify interpretations of system observations

Proposer limitations:

no execution authority

no database modification authority

no institutional memory control

no system governance authority

Institutional Roles

The current institutional structure is:

Founder

system sovereignty

long-term direction

AI participation approval

Librarian

institutional memory consistency

documentation integrity

role boundary supervision

Proposer

research proposal generation

hypothesis development

interpretation of observations

Future roles may include:

Researcher

Evaluator

Consensus agents

Risk manager

Execution agents

These roles are not yet implemented.

Relationship Between Proposer and Librarian

The proposal layer operates under institutional supervision
to ensure that research activity remains active while the
system remains stable.

The Proposer is responsible for generating research proposals.

The Librarian is responsible for maintaining institutional
consistency and role boundaries.

The Librarian does not control the intellectual content
of proposals.

The Proposer is free to explore hypotheses, interpretations,
and experimental ideas.

The Librarian supervises structural integrity.

The Librarian ensures that:

role boundaries are respected

proposal objects follow defined semantics

institutional documentation remains consistent

database integrity is preserved

Librarian Review Principle

The Librarian may review proposals to verify institutional
consistency.

Review is not censorship.

The Librarian does not suppress research ideas but may request:

clarification

structural improvements

additional trace_event references

clearer hypothesis formulation

Proposal Challenge Principle

The Librarian may challenge proposals when reasoning clarity
or institutional consistency is uncertain.

Challenge exists to strengthen proposals, not suppress them.

Proposers are encouraged to respond with refined proposals
or additional supporting reasoning.

Archival Authority

Proposals are research objects.

The decision to include proposals in long-term institutional
archives is managed by the Librarian.

This ensures that institutional memory remains structured
and interpretable over time.

Proposal Debate Mechanism

AI Trading OS encourages structured intellectual exchange
between the Proposer and the Librarian.

The typical research dialogue pattern is:

Proposer → proposal

Librarian → challenge or clarification request

Proposer → revision

This loop exists to improve research quality and reasoning clarity.

The debate mechanism is cooperative rather than adversarial.

The objective is refinement of understanding rather than
competition between agents.

Safety Principle

AI agents participate through defined roles only.

No AI agent may operate outside its role boundary.

All outputs must correspond to defined institutional objects.

This structure ensures that adding additional AI agents
does not destabilize the institutional system.