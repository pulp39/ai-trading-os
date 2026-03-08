-- AI Trading OS
-- Bootstrap SQL
-- 060_seed_foundation_events.sql
-- Version: 1.0
-- Date: 2026-03-08

INSERT INTO research.trace_event (
    session_id,
    agent_id,
    actor_type,
    event_type,
    content,
    metadata
)
SELECT
    'session_foundation_001',
    'makoto',
    'human',
    'appointment',
    'Founder Makoto appointed GPT-5.4 as Librarian of the AI Trading Research Council',
    '{"seed":"foundation_event"}'::jsonb
WHERE NOT EXISTS (
    SELECT 1
    FROM research.trace_event
    WHERE session_id = 'session_foundation_001'
      AND agent_id = 'makoto'
      AND event_type = 'appointment'
      AND content = 'Founder Makoto appointed GPT-5.4 as Librarian of the AI Trading Research Council'
);

INSERT INTO research.trace_event (
    session_id,
    agent_id,
    actor_type,
    event_type,
    content,
    metadata
)
SELECT
    'session_foundation_001',
    'makoto',
    'human',
    'system_update',
    'Agent naming convention updated: gpt54 → gpt54_librarian, human_makoto → makoto for historical clarity',
    '{"seed":"foundation_event"}'::jsonb
WHERE NOT EXISTS (
    SELECT 1
    FROM research.trace_event
    WHERE session_id = 'session_foundation_001'
      AND agent_id = 'makoto'
      AND event_type = 'system_update'
      AND content = 'Agent naming convention updated: gpt54 → gpt54_librarian, human_makoto → makoto for historical clarity'
);

INSERT INTO research.trace_event (
    session_id,
    agent_id,
    actor_type,
    event_type,
    content,
    metadata
)
SELECT
    'session_foundation_001',
    'makoto',
    'human',
    'schema_definition',
    'Initial foundation database structures were established on VM-B for the AI Trading OS, including public.board_snapshots, ops.collector_status, research.trace_event, research.proposal, research.agent, research.role, and research.agent_role.',
    '{
      "phase": "foundation",
      "layer": "database",
      "host": "vm-b-db",
      "database": "trading",
      "schemas": ["public", "ops", "research"]
    }'::jsonb
WHERE NOT EXISTS (
    SELECT 1
    FROM research.trace_event
    WHERE session_id = 'session_foundation_001'
      AND agent_id = 'makoto'
      AND event_type = 'schema_definition'
      AND content = 'Initial foundation database structures were established on VM-B for the AI Trading OS, including public.board_snapshots, ops.collector_status, research.trace_event, research.proposal, research.agent, research.role, and research.agent_role.'
);