#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from typing import Any

import psycopg

ALLOWED_TARGETS = {
    ("research", "trace_event"): {"SELECT", "INSERT"},
    ("public", "board_snapshots"): {"INSERT"},
}
FORBIDDEN_PATTERNS = [
    r"\bUPDATE\b",
    r"\bDELETE\b",
    r"\bDROP\b",
    r"\bALTER\b",
    r"\bCREATE\b",
    r"\bTRUNCATE\b",
    r"\bGRANT\b",
    r"\bREVOKE\b",
    r"\bCOPY\b",
    r";\s*[^\s]",  # crude multi-statement guard
]

SELECT_PATTERN = re.compile(
    r"^\s*SELECT\b[\s\S]*\bFROM\s+research\.trace_event\b[\s\S]*$",
    re.IGNORECASE,
)
INSERT_PATTERN = re.compile(
    r"^\s*INSERT\s+INTO\s+research\.trace_event\b[\s\S]*RETURNING\b[\s\S]*$",
    re.IGNORECASE,
)


@dataclass
class DBConfig:
    host: str
    port: int
    dbname: str
    user: str
    password: str


def load_db_config() -> DBConfig:
    missing = [
        name
        for name in [
            "OPENCLAW_TRACE_DB_HOST",
            "OPENCLAW_TRACE_DB_PORT",
            "OPENCLAW_TRACE_DB_NAME",
            "OPENCLAW_TRACE_DB_USER",
            "OPENCLAW_TRACE_DB_PASSWORD",
        ]
        if not os.getenv(name)
    ]
    if missing:
        raise SystemExit(f"Missing required environment variables: {', '.join(missing)}")

    return DBConfig(
        host=os.environ["OPENCLAW_TRACE_DB_HOST"],
        port=int(os.environ["OPENCLAW_TRACE_DB_PORT"]),
        dbname=os.environ["OPENCLAW_TRACE_DB_NAME"],
        user=os.environ["OPENCLAW_TRACE_DB_USER"],
        password=os.environ["OPENCLAW_TRACE_DB_PASSWORD"],
    )


def load_task(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_task(task: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if task.get("task_type") != "bounded_db_test":
        errors.append("task_type must be 'bounded_db_test'")

    db_scope = task.get("db_scope", {})
    schema = db_scope.get("schema")
    table = db_scope.get("table")
    target = (schema, table)

    if target not in ALLOWED_TARGETS:
        errors.append(f"Target {schema}.{table} is not allowed")
        target_actions = set()
    else:
        target_actions = ALLOWED_TARGETS[target]

    allowed_actions = set(task.get("allowed_actions", []))
    if not allowed_actions.issubset(target_actions):
        errors.append(f"allowed_actions contains unsupported actions for {schema}.{table}")

    steps = task.get("steps", [])
    if not steps:
        errors.append("Task must include at least one step")

    for idx, step in enumerate(steps, start=1):
        action = str(step.get("action", "")).upper()
        sql = str(step.get("sql", "")).strip()

        if action not in {"SELECT", "INSERT"}:
            errors.append(f"Step {idx}: action '{action}' is not allowed")
            continue

        for pat in FORBIDDEN_PATTERNS:
            if re.search(pat, sql, re.IGNORECASE | re.DOTALL):
                errors.append(f"Step {idx}: forbidden SQL pattern matched: {pat}")

        if target == ("research", "trace_event"):
            if action == "SELECT" and not SELECT_PATTERN.match(sql):
                errors.append(f"Step {idx}: SELECT must target research.trace_event only")
            if action == "INSERT" and not INSERT_PATTERN.match(sql):
                errors.append(f"Step {idx}: INSERT must target research.trace_event and include RETURNING")

        if target == ("public", "board_snapshots"):
            if action == "SELECT":
                errors.append(f"Step {idx}: SELECT is not allowed for public.board_snapshots")
            if action == "INSERT" and not re.match(
                r"^\s*INSERT\s+INTO\s+public\.board_snapshots\b[\s\S]*$",
                sql,
                re.IGNORECASE,
            ):
                errors.append(f"Step {idx}: INSERT must target public.board_snapshots only")

    return errors

def run_task(task: dict[str, Any], cfg: DBConfig, dry_run: bool) -> int:
    task_id = task.get("task_id", "(no task_id)")
    steps = task.get("steps", [])

    print(f"task_id: {task_id}")
    print(f"dry_run: {dry_run}")
    print(f"db_target: {cfg.host}:{cfg.port}/{cfg.dbname} as {cfg.user}")

    errors = validate_task(task)
    if errors:
        print("validation: failed")
        for err in errors:
            print(f"error: {err}")
        return 2

    print("validation: passed")
    for idx, step in enumerate(steps, start=1):
        print(f"step_{idx}_action: {step['action']}")
        print(f"step_{idx}_sql:\n{step['sql']}")

    if dry_run:
        print("execution: skipped (dry-run)")
        return 0

    with psycopg.connect(
        host=cfg.host,
        port=cfg.port,
        dbname=cfg.dbname,
        user=cfg.user,
        password=cfg.password,
        sslmode="require",
    ) as conn:
        conn.autocommit = False
        with conn.cursor() as cur:
            for idx, step in enumerate(steps, start=1):
                sql = step["sql"]
                cur.execute(sql)
                rows = cur.fetchall() if cur.description else []
                print(f"step_{idx}_rows: {rows}")
        conn.commit()

    print("execution: committed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run bounded DB tasks for OpenClaw")
    parser.add_argument("--task", required=True, help="Path to task JSON")
    parser.add_argument("--dry-run", action="store_true", help="Validate only")
    args = parser.parse_args()

    task = load_task(args.task)
    cfg = load_db_config()
    return run_task(task, cfg, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
