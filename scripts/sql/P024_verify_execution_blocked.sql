-- P-024 verification query
-- Verifies success conditions and invariants for execution_blocked

WITH target AS (
  SELECT *
  FROM research.trace_event
  WHERE event_type = 'execution_blocked'
    AND metadata->>'linked_gate_event_id' = '275'
  ORDER BY id DESC
  LIMIT 1
),
no_execution AS (
  SELECT COUNT(*) AS real_order_exec_count
  FROM research.trace_event
  WHERE event_type = 'execution_recorded'
    AND content ILIKE '%real_order%'
)
SELECT
  t.id AS execution_blocked_event_id,
  t.event_type,
  t.metadata->>'rejection_reason' AS rejection_reason,
  t.metadata->>'blocked_by_design' AS blocked_by_design,
  t.metadata->>'linked_gate_event_id' AS linked_gate_event_id,
  t.metadata->>'linked_preview_event_id' AS linked_preview_event_id,
  CASE WHEN t.metadata->>'rejection_reason' = 'B-4_real_order_not_authorized' THEN 'OK' ELSE 'NG' END AS check_rejection_reason,
  CASE WHEN t.metadata->>'blocked_by_design' = 'true' THEN 'OK' ELSE 'NG' END AS check_blocked_by_design,
  CASE WHEN t.metadata->>'linked_gate_event_id' = '275' THEN 'OK' ELSE 'NG' END AS check_gate_link,
  CASE WHEN n.real_order_exec_count = 0 THEN 'OK' ELSE 'NG' END AS check_no_real_order_execution
FROM target t, no_execution n;
