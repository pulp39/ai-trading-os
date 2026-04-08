from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
KEY_VALUE_RE = re.compile(r"^(?P<key>[A-Za-z0-9_]+):\s*(?P<value>.*)$")


@dataclass
class TaskArtifact:
    path: Path
    metadata: dict[str, Any]
    body: str

    @property
    def task_id(self) -> str:
        return str(self.metadata.get("task_id", self.path.stem))

    @property
    def command(self) -> str:
        command = self.metadata.get("command", "")
        if not isinstance(command, str) or not command.strip():
            raise ValueError(f"Task artifact {self.path} does not contain a usable command")
        return command.strip()

    @property
    def expected_output(self) -> list[str]:
        value = self.metadata.get("expected_output", [])
        if isinstance(value, list):
            return [str(item) for item in value]
        return []

    @property
    def stop_conditions(self) -> list[str]:
        value = self.metadata.get("stop_conditions", [])
        if isinstance(value, list):
            return [str(item) for item in value]
        return []


def _parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"", "null", "None"}:
        return ""
    if value.isdigit():
        return int(value)
    return value.strip('"').strip("'")


def parse_front_matter(text: str) -> tuple[dict[str, Any], str]:
    match = FRONT_MATTER_RE.match(text)
    if not match:
        raise ValueError("Task artifact is missing YAML front matter")

    front_matter = match.group(1)
    body = text[match.end():]
    metadata: dict[str, Any] = {}
    current_key: str | None = None
    current_list_key: str | None = None
    command_lines: list[str] = []

    for raw_line in front_matter.splitlines():
        if not raw_line.strip():
            continue

        if raw_line.startswith("  - ") and current_list_key:
            metadata.setdefault(current_list_key, []).append(raw_line[4:].strip())
            continue

        if raw_line.startswith("  ") and current_key == "command":
            command_lines.append(raw_line[2:])
            continue

        kv_match = KEY_VALUE_RE.match(raw_line)
        if not kv_match:
            raise ValueError(f"Unsupported front matter line: {raw_line}")

        key = kv_match.group("key")
        value = kv_match.group("value")
        current_key = key
        current_list_key = None

        if value == "|":
            metadata[key] = ""
            command_lines = []
            continue

        if value == "":
            metadata[key] = []
            current_list_key = key
            continue

        metadata[key] = _parse_scalar(value)

    if current_key == "command" or command_lines:
        metadata["command"] = "\n".join(command_lines).strip()

    return metadata, body


def load_task(task_path: Path) -> TaskArtifact:
    text = task_path.read_text(encoding="utf-8")
    metadata, body = parse_front_matter(text)
    required_keys = {"task_id", "step", "role", "command", "parent_document"}
    missing = sorted(required_keys - metadata.keys())
    if missing:
        raise ValueError(f"Task artifact {task_path} is missing required keys: {', '.join(missing)}")
    return TaskArtifact(path=task_path, metadata=metadata, body=body)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sanitize_task_id(task_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", task_id)


def compute_status(return_code: int, output_text: str, expected_sections: list[str]) -> tuple[str, list[str]]:
    missing_sections = [section for section in expected_sections if section not in output_text]
    stop_detected = "STOP" in output_text
    if return_code == 0 and not missing_sections and not stop_detected:
        return "completed", missing_sections
    return "aborted", missing_sections


def run_task(task: TaskArtifact, execute: bool) -> dict[str, Any]:
    started_at = utc_now_iso()
    if not execute:
        return {
            "task_id": task.task_id,
            "status": "pending",
            "mode": "validate_only",
            "started_at": started_at,
            "finished_at": started_at,
            "metadata": task.metadata,
            "body_present": bool(task.body.strip()),
        }

    completed = subprocess.run(
        task.command,
        shell=True,
        executable="/bin/bash",
        capture_output=True,
        text=True,
        cwd=os.getcwd(),
    )
    combined_output = "\n".join(part for part in [completed.stdout, completed.stderr] if part)
    status, missing_sections = compute_status(
        return_code=completed.returncode,
        output_text=combined_output,
        expected_sections=task.expected_output,
    )
    finished_at = utc_now_iso()

    return {
        "task_id": task.task_id,
        "status": status,
        "mode": "execute",
        "started_at": started_at,
        "finished_at": finished_at,
        "task_path": str(task.path),
        "step": task.metadata.get("step"),
        "role": task.metadata.get("role"),
        "parent_document": task.metadata.get("parent_document"),
        "writes_state": task.metadata.get("writes_state"),
        "requires_approval": task.metadata.get("requires_approval"),
        "command": task.command,
        "expected_output": task.expected_output,
        "stop_conditions": task.stop_conditions,
        "return_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "missing_sections": missing_sections,
        "stop_detected": "STOP" in combined_output,
    }


def write_result(result: dict[str, Any], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output_path


def build_default_output_path(task: TaskArtifact) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"{sanitize_task_id(task.task_id)}__{timestamp}.json"
    return Path("scripts/openclaw/task_results") / filename


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run or validate an OpenClaw task artifact")
    parser.add_argument("task", help="Path to task artifact markdown file")
    parser.add_argument("--output", help="Path to write JSON result artifact")
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Parse and validate the task artifact without executing the command",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    task_path = Path(args.task)
    task = load_task(task_path)
    result = run_task(task, execute=not args.validate_only)
    output_path = Path(args.output) if args.output else build_default_output_path(task)
    write_result(result, output_path)

    print(f"task_id={result['task_id']}")
    print(f"status={result['status']}")
    print(f"result_artifact={output_path}")

    return 0 if result["status"] in {"completed", "pending"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
