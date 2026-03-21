BEGIN;

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
    'gpt_librarian',
    'ai',
    'execution_recorded',
    'first execution_gate_passed successfully recorded without triggering real_order',
    275,
    jsonb_build_object(
        'execution_subtype', 'execution_gate_verification',
        'linked_gate_event_id', 275,
        'linked_preview_event_id', 269,
        'linked_proposal_trace_event_id', 274,
        'proposal_id', 'P-20260321-022',
        'verification_result', 'success',
        'real_order_triggered', false,
        'notes', 'first controlled verification of execution_gate passage completed successfully'
    )
)
RETURNING id;

COMMIT;