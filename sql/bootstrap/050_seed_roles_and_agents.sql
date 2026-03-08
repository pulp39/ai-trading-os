-- AI Trading OS
-- Bootstrap SQL
-- 050_seed_roles_and_agents.sql
-- Version: 1.0
-- Date: 2026-03-08

INSERT INTO research.role (role_name, description)
VALUES
    ('founder', 'Founder and ultimate responsible human authority'),
    ('librarian', 'Knowledge organization and record keeper'),
    ('researcher', 'AI or human researcher generating hypotheses'),
    ('executor', 'Execution engine capable of trading actions')
ON CONFLICT (role_name) DO NOTHING;

INSERT INTO research.agent (agent_id, agent_name, agent_type)
VALUES
    ('makoto', 'makoto', 'human'),
    ('gpt54_librarian', 'GPT-5.4 Librarian', 'ai')
ON CONFLICT (agent_id) DO NOTHING;

INSERT INTO research.agent_role (agent_id, role_name, assigned_by, metadata)
SELECT
    'makoto',
    'founder',
    'system',
    '{"seed":"foundation"}'::jsonb
WHERE NOT EXISTS (
    SELECT 1
    FROM research.agent_role
    WHERE agent_id = 'makoto'
      AND role_name = 'founder'
);

INSERT INTO research.agent_role (agent_id, role_name, assigned_by, metadata)
SELECT
    'gpt54_librarian',
    'librarian',
    'makoto',
    '{"seed":"foundation"}'::jsonb
WHERE NOT EXISTS (
    SELECT 1
    FROM research.agent_role
    WHERE agent_id = 'gpt54_librarian'
      AND role_name = 'librarian'
);