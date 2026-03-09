from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.common.db import get_connection


ALLOWED_ACTOR_TYPES = {"human", "ai"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent-id", required=True)
    parser.add_argument("--actor-type", required=True)
    parser.add_argument("--event-type", required=True)
    parser.add_argument("--content", required=True)
    parser.add_argument("--metadata")
    parser.add_argument("--metadata-file")
    return parser.parse_args()


def load_metadata(args: argparse.Namespace) -> dict:
    if args.metadata and args.metadata_file:
        raise ValueError("Use either --metadata or --metadata-file, not both.")

    if args.metadata_file:
        path = Path(args.metadata_file)
        return json.loads(path.read_text(encoding="utf-8"))

    if args.metadata:
        return json.loads(args.metadata)

    raise ValueError("Either --metadata or --metadata-file is required.")


def main() -> int:
    args = parse_args()

    if args.actor_type not in ALLOWED_ACTOR_TYPES:
        print(f"Invalid actor_type: {args.actor_type}", file=sys.stderr)
        return 1

    try:
        metadata = load_metadata(args)
    except Exception as e:
        print(f"Invalid metadata JSON: {e}", file=sys.stderr)
        return 1

    sql = """
    INSERT INTO trace_event (
        agent_id,
        actor_type,
        event_type,
        content,
        metadata
    )
    VALUES (%s, %s, %s, %s, %s::jsonb)
    """

    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    sql,
                    (
                        args.agent_id,
                        args.actor_type,
                        args.event_type,
                        args.content,
                        json.dumps(metadata, ensure_ascii=False),
                    ),
                )
    finally:
        conn.close()

    print("trace_event recorded successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
