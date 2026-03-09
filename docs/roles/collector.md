Collector Role Definition
=========================

Purpose
-------

The collector role is responsible for recording observation-side system events into the institutional memory layer through the shared database access module.

Collectors serve as the first operational role within the AI Trading OS architecture.

Their responsibility is not to analyze markets, generate trading signals, or execute trades.
Instead, collectors ensure that system-relevant observational events are consistently recorded into the historical memory of the system.


Responsibilities
---------------

A collector is responsible for:

• Initializing itself as a named operational role  
• Recording structured events into the research.trace_event table  
• Using the shared database access layer (src/common/db.py)  
• Ensuring system-relevant observational events are preserved in institutional memory  


Non-Responsibilities
--------------------

Collectors explicitly do NOT perform:

• Market analysis  
• Signal generation  
• Trading decisions  
• Trade execution  
• Risk management  


Boundary
--------

Collectors observe and record system-relevant events only.

Collectors do not interpret observations, rank significance, generate hypotheses, or recommend actions.

Those responsibilities belong to future proposal-producing or research-oriented roles.


Architectural Position
----------------------

Within the AI Trading OS architecture, collectors represent the first operational role module.

Architecture progression currently follows this structure:

Infrastructure
→ Shared Memory Layer (PostgreSQL)
→ Shared DB Access Layer
→ Collector Role (first operational role)


This means collectors operate on top of the shared DB access layer and contribute to the institutional event history.


Operational Discipline
----------------------

Collectors must follow these architectural constraints:

• Database connections must use the shared DB module (src/common/db.py)  
• Scripts must remain thin entry points and must not embed collector logic  
• Collector modules must remain minimal and role-focused  
• Event recording must follow trace_event semantic rules  


Philosophy
----------

Collectors are designed to establish reliable institutional memory before introducing higher-level system intelligence.

The AI Trading OS intentionally prioritizes memory discipline over early system complexity.


Japanese Reference
------------------

Collectorは共有DB層を通じて観測側のシステム事象を記録する最小役割である。

Collectorは分析・売買判断・執行を行わない。

Collectorの責務は、システム運用に関わる観測事象を制度的記憶に一貫して記録することである。