from __future__ import annotations

from typing import Any, Dict, Optional

from psycopg.types.json import Jsonb

from src.common.db import db_connection


class BaseCollector:
    """
    Minimal collector foundation for AI Trading OS.

    Responsibilities in this phase:
    - identify itself as a collector module
    - reuse shared DB access layer
    - record collector events into research.trace_event

    Not yet in scope:
    - market data ingestion
    - scheduling
    - collector_status updates
    - proposal generation
    - execution logic
    """

    def __init__(self, collector_name: str) -> None:
        if not collector_name.strip():
            raise ValueError("collector_name must not be empty.")

        self.collector_name = collector_name.strip()

    def record_event(
        self,
        *,
        event_type: str,
        content: str,
        session_id: Optional[str] = None,
        parent_event_id: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
        actor_type: str = "ai",
        symbol: Optional[str] = None,
        exchange: Optional[str] = None,
    ) -> int:
        """
        Record a collector event into research.trace_event and return the inserted event id.
        """
        if not event_type.strip():
            raise ValueError("event_type must not be empty.")

        if not content.strip():
            raise ValueError("content must not be empty.")

        event_metadata: Dict[str, Any] = {
            "collector_name": self.collector_name,
            "uses_shared_db_layer": True,
        }

        if metadata:
            event_metadata.update(metadata)

        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    insert into research.trace_event
                    (
                        session_id,
                        agent_id,
                        actor_type,
                        event_type,
                        symbol,
                        exchange,
                        content,
                        parent_event_id,
                        metadata
                    )
                    values
                    (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    returning id
                    """,
                    (
                        session_id,
                        self.collector_name,
                        actor_type,
                        event_type.strip(),
                        symbol,
                        exchange,
                        content.strip(),
                        parent_event_id,
                        Jsonb(event_metadata),
                    ),
                )
                row = cur.fetchone()

            conn.commit()

        if row is None:
            raise RuntimeError("Failed to insert collector event.")

        event_id = row[0]
        if not isinstance(event_id, int):
            raise RuntimeError(f"Unexpected event id type: {type(event_id)!r}")

        return event_id

    def record_startup_event(
        self,
        *,
        session_id: Optional[str] = None,
        parent_event_id: Optional[int] = 11,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> int:
        """
        Record the collector foundation/startup event and return the inserted event id.
        """
        event_metadata: Dict[str, Any] = {
            "phase": "collector_foundation",
            "scope": "minimal",
        }

        if metadata:
            event_metadata.update(metadata)

        return self.record_event(
            event_type="collector_foundation",
            content=(
                "Initialized first collector foundation module and verified "
                "reusable event recording path through shared DB access layer."
            ),
            session_id=session_id,
            parent_event_id=parent_event_id,
            metadata=event_metadata,
        )