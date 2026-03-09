from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterator

import psycopg


REPO_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = REPO_ROOT / ".env"


class DBConfigError(RuntimeError):
    """Raised when required database configuration is missing or invalid."""


def load_env_file(env_path: Path = ENV_PATH) -> Dict[str, str]:
    """
    Load a simple KEY=VALUE .env file safely.

    Uses utf-8-sig so that UTF-8 with BOM is also handled correctly.
    This avoids the Windows BOM issue where the first key may be parsed
    incorrectly if the file was saved with BOM.
    """
    if not env_path.exists():
        return {}

    config: Dict[str, str] = {}

    with env_path.open("r", encoding="utf-8-sig") as f:
        for raw_line in f:
            line = raw_line.strip()

            if not line:
                continue
            if line.startswith("#"):
                continue
            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            if not key:
                continue

            config[key] = value

    return config


def load_runtime_config(env_path: Path = ENV_PATH) -> Dict[str, str]:
    """
    Merge local .env values with OS environment variables.

    Precedence:
    1. .env file values
    2. OS environment variables override .env values

    This keeps local development simple while allowing future automation
    or deployment environments to inject configuration safely.
    """
    config = load_env_file(env_path)

    override_keys = [
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
        "DB_SSLMODE",
        "DB_CONNECT_TIMEOUT",
    ]

    for key in override_keys:
        value = os.getenv(key)
        if value:
            config[key] = value

    return config


def get_db_config(env_path: Path = ENV_PATH) -> Dict[str, Any]:
    """
    Return validated PostgreSQL connection settings.
    """
    config = load_runtime_config(env_path)

    required_keys = [
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
    ]

    missing = [key for key in required_keys if not config.get(key)]
    if missing:
        raise DBConfigError(
            f"Missing required DB config keys: {', '.join(missing)}"
        )

    try:
        port = int(config["DB_PORT"])
    except ValueError as exc:
        raise DBConfigError(f"Invalid DB_PORT: {config['DB_PORT']}") from exc

    sslmode = config.get("DB_SSLMODE", "prefer")

    try:
        connect_timeout = int(config.get("DB_CONNECT_TIMEOUT", "5"))
    except ValueError as exc:
        raise DBConfigError(
            f"Invalid DB_CONNECT_TIMEOUT: {config.get('DB_CONNECT_TIMEOUT')}"
        ) from exc

    return {
        "host": config["DB_HOST"],
        "port": port,
        "dbname": config["DB_NAME"],
        "user": config["DB_USER"],
        "password": config["DB_PASSWORD"],
        "sslmode": sslmode,
        "connect_timeout": connect_timeout,
    }


def get_connection(env_path: Path = ENV_PATH) -> psycopg.Connection:
    """
    Create and return a live PostgreSQL connection.
    """
    config = get_db_config(env_path)
    return psycopg.connect(**config)


@contextmanager
def db_connection(env_path: Path = ENV_PATH) -> Iterator[psycopg.Connection]:
    """
    Context-managed shared database connection helper.
    """
    conn = get_connection(env_path)
    try:
        yield conn
    finally:
        conn.close()