AI Trading OS Research Process

This document defines the research workflow used by AI Trading OS.

The system operates as an institutional research environment for AI-assisted market analysis.

Research proceeds through structured observation, interpretation, and debate.

Related documents:

constitution.md

docs/proposal_semantics.md

docs/institutional_model.md

Core Principle

Observation must remain separate from interpretation.

Collectors record observations.

Proposers interpret observations.

The research process exists to preserve this separation.

Research Cycle

The standard research cycle is:

Observation
↓
trace_event recorded by Collector
↓
interpretation by Proposer
↓
proposal generated
↓
challenge or clarification by Librarian
↓
proposal revision

This loop may repeat multiple times until a research direction becomes clear.

Step 1 — Observation

System-relevant events occur.

Examples:

market conditions

system milestones

research outcomes

infrastructure events

These observations are recorded by Collectors.

Step 2 — trace_event Recording

Collectors record observations as trace_event.

trace_event entries must contain:

factual observation

event description

timestamp

relevant system context

trace_event must not contain interpretation.

Example trace_event

event_type: infrastructure_validation
content: First database connection established between research VM and DB server.

The trace_event becomes part of institutional memory.

Step 3 — Interpretation

Proposers review trace_event history.

Proposers may interpret:

patterns

relationships

anomalies

emerging research opportunities

Interpretation must occur through proposal objects.

Step 4 — Proposal Generation

A proposal is a structured research hypothesis.

A proposal may contain:

interpretation of observations

research hypothesis

possible experiments

expected outcomes

Proposals are advisory research artifacts only.

They must not act as execution commands.

See: docs/proposal_semantics.md

Step 5 — Librarian Challenge

The Librarian may respond to proposals with:

clarification requests

logical challenges

requests for stronger reasoning

identification of missing context

Challenges exist to strengthen reasoning.

They are not censorship.

Step 6 — Proposal Revision

Proposers may revise proposals based on:

additional reasoning

new observations

librarian feedback

debate with other proposers

The research cycle may repeat multiple times.

Institutional Memory

All trace_event entries and proposals contribute to institutional knowledge.

The system maintains a traceable history of:

observations

reasoning

research directions

Research Freedom

Proposers are encouraged to explore strong hypotheses.

The system values:

intellectual rigor

traceable reasoning

institutional discipline

Institutional Safety

The following boundaries must remain stable.

Collectors do not interpret.

Proposers do not execute.

Librarians do not control research outcomes.

Founder governs the system.

These boundaries protect the integrity of the research process.