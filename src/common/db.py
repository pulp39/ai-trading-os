from __future__ import annotations

from pathlib import Path
from typing import Dict

import psycopg


REPO_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = REPO_ROOT / ".env"


def load_env_file(env_path: Path = ENV_PATH) -> Dict[str, str]:
    """
    Load a simple KEY=VALUE .env file safely.

    Uses utf-8-sig so that UTF-8 with BOM is also handled correctly.
    This avoids the Windows BOM issue where DB_HOST may be parsed incorrectly.
    """
    if not env_path.exists():
        raise FileNotFoundError(f".env file not found: {env_path}")

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
            config[key.strip()] = value.strip()

    return config


def get_db_config() -> Dict[str, str]:
    config = load_env_file()

    required_keys = [
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
    ]

    missing = [key for key in required_keys if not config.get(key)]
    if missing:
        raise ValueError(f"Missing required DB config keys: {', '.join(missing)}")

    return config


def get_connection():
    config = get_db_config()

    return psycopg.connect(
        host=config["DB_HOST"],
        port=config["DB_PORT"],
        dbname=config["DB_NAME"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        connect_timeout=5,
    )