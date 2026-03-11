import sys
import os
import json
from datetime import datetime, timezone

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.common.db import get_connection


def insert_trace_event(conn, agent_id, actor_type, event_type, content, metadata):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO research.trace_event
            (ts, agent_id, actor_type, event_type, content, metadata)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            datetime.now(timezone.utc),
            agent_id,
            actor_type,
            event_type,
            content,
            json.dumps(metadata)
        ))
        return cur.fetchone()[0]


def main():
    conn = get_connection()

    event1_id = insert_trace_event(
        conn,
        agent_id="claude_registrar",
        actor_type="ai",
        event_type="institutional_change",
        content="Introduction of Registrar role and authorization of Claude as Registrar following Founder acceptance of proposal P-20260311-001.",
        metadata={
            "role": "Registrar",
            "registrar_execution": True,
            "proposal_id": "P-20260311-001",
            "institutional_change_type": "role_introduction",
            "new_role": "Registrar",
            "authorized_agent": "Claude",
            "authorization_basis": "Founder decision 2026-03-11",
            "librarian_authorization": True
        }
    )
    print(f"trace_event registered: id={event1_id} (institutional_change / P-20260311-001)")

    event2_id = insert_trace_event(
        conn,
        agent_id="claude_registrar",
        actor_type="ai",
        event_type="founder_record_created",
        content="Founder record FR-20260310-002 registered under founder_records/proposals/. Retroactive record of Founder's OpenClaw temporary invitation proposal (2026-03-10).",
        metadata={
            "role": "Registrar",
            "registrar_execution": True,
            "founder_record_id": "FR-20260310-002",
            "record_type": "proposal",
            "file_path": "founder_records/proposals/FR-20260310-002.md",
            "related_proposal_id": "P-20260310-011",
            "retroactive": True,
            "original_date": "2026-03-10",
            "librarian_authorization": True
        }
    )
    print(f"trace_event registered: id={event2_id} (founder_record_created / FR-20260310-002)")

    conn.commit()
    conn.close()
    print("All trace_events committed successfully.")


if __name__ == "__main__":
    main()