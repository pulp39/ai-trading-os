BEGIN;

-- 1) 既存 preview の存在確認
--    id=269 が order_preview_recorded であることを前提にする
DO $$
DECLARE
    v_preview_event_type text;
    v_existing_gate_id bigint;
BEGIN
    SELECT event_type
      INTO v_preview_event_type
      FROM research.trace_event
     WHERE id = 269;

    IF v_preview_event_type IS NULL THEN
        RAISE EXCEPTION 'execution_gate blocked: linked preview event id=269 not found';
    END IF;

    IF v_preview_event_type <> 'order_preview_recorded' THEN
        RAISE EXCEPTION 'execution_gate blocked: linked event id=269 is %, expected order_preview_recorded', v_preview_event_type;
    END IF;

    -- 2) One Gate per Preview の確認
    SELECT id
      INTO v_existing_gate_id
      FROM research.trace_event
     WHERE event_type = 'execution_gate_passed'
       AND metadata->>'linked_preview_event_id' = '269'
     LIMIT 1;

    IF v_existing_gate_id IS NOT NULL THEN
        RAISE EXCEPTION 'execution_gate blocked: gate already exists for preview_event_id=269 (existing gate id=%)', v_existing_gate_id;
    END IF;
END $$;

-- 3) execution_gate_passed の挿入
INSERT INTO research.trace_event (
    ts,
    agent_id,
    actor_type,
    event_type,
    content,
    parent_event_id,
    metadata
)
VALUES (
    NOW(),
    'claude_registrar',
    'ai',
    'execution_gate_passed',
    'Execution gate passed — first controlled verification test (P-20260321-022)',
    269,
    jsonb_build_object(
        'linked_preview_event_id', 269,
        'gate_task_ref', 'registrar_queue/execution_gate_task.json',
        'authorized_by', 'claude_registrar',
        'preconditions_verified', true,
        'real_order_authorized', false,
        'test_context', 'P-20260321-022 controlled verification',
        'gate_role', 'registrar_authorization'
    )
)
RETURNING id;

COMMIT;