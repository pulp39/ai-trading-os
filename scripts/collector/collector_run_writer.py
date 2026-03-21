import psycopg
import os
from psycopg.types.json import Json


def write_collector_run(
    *,
    symbols: list[str],
    snapshot_count: int,
    status: str,
    started_at: str,
    completed_at: str,
    failed_symbols: list[str] | None = None,
    aab_bundle_id: str | None = None,
) -> None:
    if failed_symbols is None:
        failed_symbols = []

    if status not in {"success", "partial_failure", "failure"}:
        raise ValueError(f"invalid collector_run status: {status}")

    conn = psycopg.connect(
        host=os.environ["OPENCLAW_TRACE_DB_HOST"],
        port=os.environ["OPENCLAW_TRACE_DB_PORT"],
        dbname=os.environ["OPENCLAW_TRACE_DB_NAME"],
        user=os.environ["OPENCLAW_TRACE_DB_USER"],
        password=os.environ["OPENCLAW_TRACE_DB_PASSWORD"],
    )

    content = (
        f"collector_run status={status} symbols={symbols} "
        f"snapshot_count={snapshot_count} failed_symbols={failed_symbols}"
    )

    metadata = {
        "actor": "OpenClaw",
        "scope": "board_snapshot_insert",
        "symbols": symbols,
        "snapshot_count": snapshot_count,
        "status": status,
        "started_at": started_at,
        "completed_at": completed_at,
        "failed_symbols": failed_symbols,
        "aab_bundle_id": aab_bundle_id,
    }

    sql = """
    INSERT INTO research.trace_event (
        agent_id,
        actor_type,
        event_type,
        content,
        metadata
    )
    VALUES (
        %(agent_id)s,
        %(actor_type)s,
        %(event_type)s,
        %(content)s,
        %(metadata)s
    )
    """

    params = {
        "agent_id": "openclaw_aux",
        "actor_type": "ai",
        "event_type": "collector_run",
        "content": content,
        "metadata": Json(metadata),
    }

    with conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)

    conn.close()