# Proposer Role Definition

Purpose
-------

The proposer role is responsible for generating structured research proposals
within the AI Trading OS institutional framework.

Proposers operate on top of the institutional memory layer and the proposal
semantics framework. Their responsibility is to interpret recorded observations,
form hypotheses, and suggest research directions without crossing into execution
authority.

The proposer role exists to expand institutional understanding, not to control
the system.

Responsibilities
----------------

A proposer is responsible for:

- generating structured proposal objects
- interpreting relevant recorded observations and institutional history
- forming research hypotheses about market or system-relevant dynamics
- suggesting possible experiments, validations, or research directions
- referencing supporting trace_event history when appropriate
- participating in structured proposal debate and revision

Non-Responsibilities
--------------------

Proposers explicitly do NOT perform:

- raw observation-side event collection as a collector responsibility
- trade execution
- direct market order generation
- risk approval or risk management
- database schema modification
- governance decisions
- institutional archival control

Boundary
--------

Proposers interpret and propose only.

Proposers do not execute, govern, archive, or unilaterally validate their own
proposals as institutional truth.

Proposal output must remain advisory and research-oriented.

Relationship to Collector
-------------------------

Collectors and proposers are separate roles.

Collectors:
- observe system-relevant events
- record institutional history
- write trace_event entries
- do not interpret or hypothesize

Proposers:
- interpret recorded observations
- generate hypotheses
- produce proposal objects
- do not replace collectors

Proposal work begins where collector responsibility ends.

Relationship to Librarian
-------------------------

The proposer operates under institutional supervision but not intellectual
control.

The Librarian:
- maintains institutional consistency
- supervises role boundaries
- reviews structural integrity
- may challenge unclear or weakly grounded proposals

The Librarian does not:
- suppress proposals merely for being novel
- own the intellectual content of proposals
- replace the proposer role

The normal institutional dialogue pattern is:

Proposer -> proposal
Librarian -> challenge or clarification request
Proposer -> revision

This debate loop exists to improve clarity, consistency, and research quality.

Proposal Discipline
-------------------

Proposals should follow the institutional semantics defined in:

- docs/proposal_semantics.md

A proposer should aim to include, when applicable:

- proposal_type
- research_hypothesis
- context_reference
- supporting_observations
- possible_experiments
- confidence_statement
- limitations

These elements exist to make proposals interpretable, reviewable, and
historically useful.

Architectural Position
----------------------

Within the AI Trading OS architecture, proposers represent the first explicit
research-reasoning role above collector memory recording.

Current architecture progression:

Infrastructure
-> Shared Memory Layer (PostgreSQL)
-> Shared DB Access Layer
-> Collector Role
-> Proposal Layer
-> Proposer Role

This means the proposer depends on prior institutional memory and does not
replace lower-layer responsibilities.

Initial Assignment
------------------

The first expected proposer assignment is:

- role: Proposer
- initial assigned agent: Claude

This assignment is institutional and may evolve later through explicit system
governance.

Operational Discipline
----------------------

Proposers must follow these architectural constraints:

- proposal objects must remain distinct from trace_event objects
- proposals must not be framed as execution commands
- proposals should be grounded in recorded history whenever possible
- role boundaries must remain explicit in documentation and practice
- proposal debate should strengthen reasoning rather than collapse boundaries

Philosophy
----------

Proposers are designed to introduce structured interpretation into the system
only after reliable institutional memory has been established.

The AI Trading OS intentionally separates observation from interpretation,
and interpretation from execution.

Japanese Reference
------------------

Proposer は AI Trading OS において、記録済み観測や制度的履歴をもとに
仮説・研究提案・検証方向を生成する役割である。

Proposer は collector ではないため、観測事象の生記録そのものを主責務としない。
また execution 権限も持たない。

Proposer の責務は、制度的記憶の上に立って研究的解釈を与え、
将来の知識生成につながる proposal を形成することである。