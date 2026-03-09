from __future__ import annotations

from typing import Any

from psycopg.types.json import Json
from src.common.db import db_connection


class BaseCollector:
    def __init__(self, collector_name: str) -> None:
        self.collector_name = collector_name

    def record_event(
        self,
        event_type: str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        metadata_value = Json(metadata) if metadata is not None else None

        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO research.trace_event (
                        agent_id,
                        actor_type,
                        event_type,
                        content,
                        metadata
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        self.collector_name,
                        "ai",
                        event_type,
                        content,
                        metadata_value,
                    ),
                )
            conn.commit()

    def record_startup_event(self) -> None:
        self.record_event(
            event_type="collector_foundation",
            content=(
                "Initialized first collector foundation module and verified "
                "reusable event recording path through shared DB access layer."
            ),
            metadata={
                "phase": "collector_foundation",
                "scope": "minimal",
                "purpose": "foundation_validation",
            },
        )

    def record_validation_event(
        self,
        event_type: str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.record_event(
            event_type=event_type,
            content=content,
            metadata=metadata,
        )