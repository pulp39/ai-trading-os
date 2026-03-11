import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import psycopg


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ENV_FILE = REPO_ROOT / ".env.registrar"
DEFAULT_QUEUE_DIR = REPO_ROOT / "registrar_queue"


class RegistrarError(Exception):
    pass


def load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        raise RegistrarError(f".env file not found: {env_path}")

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ[key.strip()] = value.strip()


def get_connection() -> psycopg.Connection:
    required = ["PGHOST", "PGPORT", "PGDATABASE", "PGUSER", "PGPASSWORD"]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        raise RegistrarError(f"Missing DB env vars: {', '.join(missing)}")

    return psycopg.connect(
        host=os.environ["PGHOST"],
        port=os.environ["PGPORT"],
        dbname=os.environ["PGDATABASE"],
        user=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
    )


def run_git(args: List[str]) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return completed.stdout.strip()


def repo_rel_to_abs(path_str: str) -> Path:
    p = (REPO_ROOT / path_str).resolve()
    try:
        p.relative_to(REPO_ROOT)
    except ValueError as e:
        raise RegistrarError(f"Path escapes repository root: {path_str}") from e
    return p


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def replace_exact_line(text: str, old_line: str, new_line: str) -> str:
    pattern = rf"(?m)^{re.escape(old_line)}$"
    new_text, count = re.subn(pattern, new_line, text, count=1)
    if count != 1:
        raise RegistrarError(f"Could not find exact line: {old_line}")
    return new_text

def update_status(file_path: Path, from_value: str, to_value: str) -> str:
    if not file_path.exists():
        raise RegistrarError(f"File not found for status update: {file_path}")

    text = file_path.read_text(encoding="utf-8")

    if re.search(rf"(?m)^status: {re.escape(to_value)}$", text):
        return "already_target"

    if not re.search(rf"(?m)^status: {re.escape(from_value)}$", text):
        raise RegistrarError(
            f"Could not find status: {from_value} and file is not already status: {to_value}"
        )

    updated = replace_exact_line(text, f"status: {from_value}", f"status: {to_value}")
    file_path.write_text(updated, encoding="utf-8", newline="\n")
    return "updated"

def create_file_from_text(file_path: Path, content: str, overwrite: bool = False, skip_if_exists: bool = False) -> str:
    if file_path.exists():
        if overwrite:
            ensure_parent(file_path)
            file_path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")
            return "overwritten"
        if skip_if_exists:
            return "already_exists"
        raise RegistrarError(f"Refusing to overwrite existing file: {file_path}")

    ensure_parent(file_path)
    file_path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")
    return "created"

def update_trace_event_id(file_path: Path, placeholder: str, trace_event_id: int) -> str:
    if not file_path.exists():
        raise RegistrarError(f"File not found for trace_event_id update: {file_path}")

    text = file_path.read_text(encoding="utf-8")

    if re.search(rf"(?m)^trace_event_id: {trace_event_id}$", text):
        return "already_target"

    if not re.search(rf"(?m)^trace_event_id: {re.escape(placeholder)}$", text):
        raise RegistrarError(
            f"Could not find trace_event_id placeholder: {placeholder} and file is not already trace_event_id: {trace_event_id}"
        )

    updated = replace_exact_line(
        text,
        f"trace_event_id: {placeholder}",
        f"trace_event_id: {trace_event_id}",
    )
    file_path.write_text(updated, encoding="utf-8", newline="\n")
    return "updated"


def event_already_exists(
    conn: psycopg.Connection,
    event_type: str,
    metadata_match: Dict[str, Any],
) -> Optional[int]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id
            FROM research.trace_event
            WHERE event_type = %s
              AND metadata @> %s::jsonb
            ORDER BY id DESC
            LIMIT 1
            """,
            (event_type, json.dumps(metadata_match, ensure_ascii=False)),
        )
        row = cur.fetchone()
        return int(row[0]) if row else None


def insert_trace_event(
    conn: psycopg.Connection,
    agent_id: str,
    actor_type: str,
    event_type: str,
    content: str,
    metadata: Dict[str, Any],
) -> int:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO research.trace_event
                (ts, agent_id, actor_type, event_type, content, metadata)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                datetime.now(timezone.utc),
                agent_id,
                actor_type,
                event_type,
                content,
                json.dumps(metadata, ensure_ascii=False),
            ),
        )
        return int(cur.fetchone()[0])


@dataclass
class ActionResult:
    action_type: str
    detail: str
    trace_event_id: Optional[int] = None


def render_template(template_name: str, data: Dict[str, Any]) -> str:
    if template_name == "founder_record_fr_20260310_002":
        return f"""---
founder_record_id: {data["founder_record_id"]}
record_type: proposal
date: {data["date"]}
original_date: {data["original_date"]}
retroactive: true
related_proposal_id: {data["related_proposal_id"]}
trace_event_id: {data["trace_event_id_placeholder"]}
author: Founder
edit_authority: Founder only
---

# {data["founder_record_id"]}

Founderは{data["original_date"]}に、OpenClawをAI Collector候補として制度審査に一時招待することを提案した。この提案は口頭（テキスト）による制度的意思表明として記録される。

提案の主旨: OpenClawをP-20260310-009のAI Collector候補審査フレームワークの最初の審査対象として招待し、制度の強度を試すこと。

この記録はP-20260310-011の制度的先行記録として機能する。
"""
    raise RegistrarError(f"Unknown template: {template_name}")


def process_actions(task: Dict[str, Any], commit_changes: bool, push_changes: bool) -> List[ActionResult]:
    results: List[ActionResult] = []
    pending_trace_event_updates: List[Tuple[Path, str, int]] = []

    conn = get_connection()
    try:
        for action in task["actions"]:
            action_type = action["type"]

            if action_type == "update_status":
                file_path = repo_rel_to_abs(action["file"])
                status_result = update_status(file_path, action["from"], action["to"])
                if status_result == "already_target":
                    results.append(
                        ActionResult(
                            action_type,
                            f"Status already {action['to']} in {action['file']}"
                        )
                    )
                else:
                    results.append(
                        ActionResult(
                            action_type,
                            f"Updated status in {action['file']}"
                        )
                    )

            elif action_type == "create_file":
                file_path = repo_rel_to_abs(action["file"])
                if "content" in action:
                    content = action["content"]
                else:
                    content = render_template(action["template"], action["data"])

                create_result = create_file_from_text(
                    file_path,
                    content,
                    overwrite=action.get("overwrite", False),
                    skip_if_exists=action.get("skip_if_exists", False),
                )

                if create_result == "already_exists":
                    results.append(
                        ActionResult(
                            action_type,
                            f"File already exists: {action['file']}"
                        )
                    )
                elif create_result == "overwritten":
                    results.append(
                        ActionResult(
                            action_type,
                            f"Overwritten file {action['file']}"
                        )
                    )
                else:
                    results.append(
                        ActionResult(
                            action_type,
                            f"Created file {action['file']}"
                        )
                    )

            elif action_type == "insert_trace_event":
                metadata = dict(action["metadata"])
                metadata.setdefault("registrar_execution", True)
                metadata.setdefault("task_id", task["task_id"])

                existing_id = None
                metadata_match = action.get("metadata_match")
                if metadata_match:
                    existing_id = event_already_exists(conn, action["event_type"], metadata_match)

                if existing_id is not None:
                    event_id = existing_id
                    detail = f"Reused existing trace_event id={event_id} for {action['event_type']}"
                else:
                    event_id = insert_trace_event(
                        conn=conn,
                        agent_id=action["agent_id"],
                        actor_type=action["actor_type"],
                        event_type=action["event_type"],
                        content=action["content"],
                        metadata=metadata,
                    )
                    detail = f"Inserted trace_event id={event_id} for {action['event_type']}"

                for target in action.get("post_update_files", []):
                    pending_trace_event_updates.append(
                        (
                            repo_rel_to_abs(target["file"]),
                            target["placeholder"],
                            event_id,
                        )
                    )

                results.append(ActionResult(action_type, detail, trace_event_id=event_id))

            elif action_type == "update_trace_event_id":
                file_path = repo_rel_to_abs(action["file"])
                update_trace_event_id(file_path, action["placeholder"], int(action["trace_event_id"]))
                results.append(
                    ActionResult(
                        action_type,
                        f"Updated trace_event_id in {action['file']}"
                    )
                )

            else:
                raise RegistrarError(f"Unknown action type: {action_type}")

        for file_path, placeholder, event_id in pending_trace_event_updates:
            update_trace_event_id(file_path, placeholder, event_id)
            results.append(
                ActionResult(
                    "update_trace_event_id",
                    f"Updated trace_event_id in {file_path.relative_to(REPO_ROOT)} to {event_id}",
                    trace_event_id=event_id,
                )
            )

        conn.commit()

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    changed_files = run_git(["status", "--porcelain"]).splitlines()
    changed_paths = [line[3:] for line in changed_files if line]

    if commit_changes and changed_paths:
        run_git(["add", *changed_paths])
        run_git(["commit", "-m", task["git"]["commit_message"]])

        if push_changes:
            run_git(["push", task["git"].get("remote", "origin"), task["git"].get("branch", "main")])

    return results


def load_task(task_path: Path) -> Dict[str, Any]:
    if not task_path.exists():
        raise RegistrarError(f"Task file not found: {task_path}")

    task = json.loads(task_path.read_text(encoding="utf-8"))

    required_top = ["task_id", "authorized_by", "role", "actions", "git"]
    missing = [k for k in required_top if k not in task]
    if missing:
        raise RegistrarError(f"Task missing required keys: {', '.join(missing)}")

    if task["role"] != "Registrar":
        raise RegistrarError("Task role must be Registrar")

    return task


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply a registrar task JSON.")
    parser.add_argument("--task", required=True, help="Path to registrar task JSON")
    parser.add_argument("--env-file", default=str(DEFAULT_ENV_FILE), help="Path to registrar env file")
    parser.add_argument("--no-commit", action="store_true", help="Do not commit git changes")
    parser.add_argument("--no-push", action="store_true", help="Do not push git changes")
    args = parser.parse_args()

    task_path = Path(args.task)
    if not task_path.is_absolute():
        task_path = (REPO_ROOT / task_path).resolve()

    env_path = Path(args.env_file)
    if not env_path.is_absolute():
        env_path = (REPO_ROOT / env_path).resolve()

    load_env_file(env_path)
    task = load_task(task_path)

    print(f"[Registrar] task_id={task['task_id']}")
    print(f"[Registrar] authorized_by={task['authorized_by']}")

    results = process_actions(
        task=task,
        commit_changes=not args.no_commit,
        push_changes=not args.no_push,
    )

    print("[Registrar] results:")
    for r in results:
        print(f"  - {r.action_type}: {r.detail}")

    try:
        commit_hash = run_git(["rev-parse", "HEAD"])
        print(f"[Registrar] HEAD={commit_hash}")
    except Exception:
        pass

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"[Registrar][ERROR] {e}", file=sys.stderr)
        raise SystemExit(1)