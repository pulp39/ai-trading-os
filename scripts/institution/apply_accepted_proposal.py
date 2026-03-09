from __future__ import annotations
import argparse
import json
import subprocess
import sys
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    return parser.parse_args()


def load_payload(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def run(cmd: list[str]) -> None:
    completed = subprocess.run(cmd, check=False, text=True)
    if completed.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 1

    try:
        payload = load_payload(input_path)
    except Exception as e:
        print(f"Failed to load JSON: {e}", file=sys.stderr)
        return 1

    if payload.get("proposal_status") != "accepted":
        print("proposal_status must be 'accepted'", file=sys.stderr)
        return 1

    proposal_file = payload.get("proposal_file", {})
    source_path = REPO_ROOT / proposal_file.get("source_path", "")
    target_path = REPO_ROOT / proposal_file.get("target_path", "")

    if not source_path.exists():
        print(f"Source proposal file not found: {source_path}", file=sys.stderr)
        return 1

    ensure_parent_dir(target_path)
    shutil.copy2(source_path, target_path)

    trace_event = payload.get("trace_event", {})
    metadata_path = REPO_ROOT / "tmp" / f"{payload['proposal_id']}_metadata.json"
    ensure_parent_dir(metadata_path)
    metadata_path.write_text(
        json.dumps(trace_event.get("metadata", {}), ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    run([
        sys.executable,
        str(REPO_ROOT / "scripts" / "institution" / "record_trace_event.py"),
        "--agent-id", trace_event["agent_id"],
        "--actor-type", trace_event["actor_type"],
        "--event-type", trace_event["event_type"],
        "--content", trace_event["content"],
        "--metadata-file", str(metadata_path),
    ])

    print("Accepted proposal applied successfully.")
    print(f"Copied: {source_path} -> {target_path}")
    print("trace_event recorded.")
    print("Git add / commit / push remain manual for now.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
