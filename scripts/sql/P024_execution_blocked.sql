-- P-024 execution_blocked generation (controlled block)
-- Preconditions (checked in-query):
--  - Gate exists (275)
--  - Preview exists (269)
--  - B-4 condition holds: real_order_authorized = false AND blocked_by_design = true
--  - NO real_order execution is performed here

WITH precheck AS (
  SELECT
    EXISTS (SELECT 1 FROM research.trace_event WHERE id = 275) AS gate_exists,
    EXISTS (SELECT 1 FROM research.trace_event WHERE id = 269) AS preview_exists
),
block_condition AS (
  SELECT
    FALSE::boolean AS real_order_authorized,
    TRUE::boolean  AS blocked_by_design
),
ins AS (
  INSERT INTO research.trace_event (
    agent_id,
    actor_type,
    event_type,
    content,
    parent_event_id,
    metadata
  )
  SELECT
    'collector_core' AS agent_id,
    'system'         AS actor_type,
    'execution_blocked' AS event_type,
    'real_order blocked' AS content,
    275 AS parent_event_id,
    jsonb_build_object(
      'linked_gate_event_id', 275,
      'linked_preview_event_id', 269,
      'rejection_reason', 'B-4_real_order_not_authorized',
      'attempted_task', 'real_order',
      'execution_intent', true,
      'blocked_by_design', (SELECT blocked_by_design FROM block_condition)
    ) AS metadata
  FROM precheck p, block_condition b
  WHERE p.gate_exists = TRUE
    AND p.preview_exists = TRUE
    AND b.real_order_authorized = FALSE
    AND b.blocked_by_design = TRUE
  RETURNING id
)
SELECT id AS execution_blocked_event_id FROM ins;
