from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path


REQUIRED_TOP_LEVEL = [
    "proposal_id",
    "proposal_status",
    "trace_event",
    "proposal_file",
    "git"
]


def validate(payload: dict) -> None:

    missing = [k for k in REQUIRED_TOP_LEVEL if k not in payload]
    if missing:
        raise ValueError(f"Missing required keys: {missing}")

    if payload["proposal_status"] != "accepted":
        raise ValueError("proposal_status must be 'accepted'")

    trace_event = payload["trace_event"]

    for key in ["agent_id", "actor_type", "event_type", "content", "metadata"]:
        if key not in trace_event:
            raise ValueError(f"trace_event missing '{key}'")

    proposal_file = payload["proposal_file"]

    for key in ["source_path", "target_path"]:
        if key not in proposal_file:
            raise ValueError(f"proposal_file missing '{key}'")

    git = payload["git"]

    if "commit_message" not in git:
        raise ValueError("git.commit_message missing")


def main() -> int:

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)

    args = parser.parse_args()

    path = Path(args.input)

    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 1

    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        return 1

    try:
        validate(payload)
    except Exception as e:
        print(f"Validation error: {e}", file=sys.stderr)
        return 1

    print("institution_update.json validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
