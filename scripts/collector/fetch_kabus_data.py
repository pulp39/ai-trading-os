#!/usr/bin/env python3
"""
fetch_kabus_data.py

Purpose:
- Authenticate against kabuステーション API
- Fetch spot market snapshot data for one or more registered instruments
- Save raw JSON locally for later observation building

Usage example:
  python scripts/collector/fetch_kabus_data.py ^
    --base-url "http://localhost:18081/kabusapi" ^
    --symbols "7203@1" ^
    --output-dir data/raw_kabus
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch raw market data from kabuステーション API.")
    parser.add_argument(
        "--symbols",
        nargs="+",
        required=True,
        help='Symbols in "SYMBOL@EXCHANGE" format, e.g. "7203@1"',
    )
    parser.add_argument(
        "--output-dir",
        default="data/raw_kabus",
        help="Directory to write raw JSON snapshots into.",
    )
    parser.add_argument(
        "--api-password-env",
        default=None,
        help=(
            "Environment variable name holding the kabu API password. "
            "If omitted, it is selected strictly by base-url port: "
            "18080 -> KABU_API_PASSWORD, 18081 -> KABU_API_TEST_PASSWORD."
        ),
    )
    parser.add_argument(
        "--base-url",
        default="http://localhost:18080/kabusapi",
        help='Base URL for kabu API, e.g. "http://localhost:18081/kabusapi"',
    )
    return parser.parse_args()


def resolve_api_password_env(base_url: str, explicit_env_name: str | None) -> str:
    if explicit_env_name:
        return explicit_env_name

    parsed = urlparse(base_url)
    port = parsed.port

    if port == 18080:
        return "KABU_API_PASSWORD"
    if port == 18081:
        return "KABU_API_TEST_PASSWORD"

    raise SystemExit(
        "Unable to resolve kabu API password env from base-url port. "
        "Pass --api-password-env explicitly for non-standard ports."
    )



def get_api_password(env_name: str) -> str:
    value = os.getenv(env_name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {env_name}")
    return value


def get_token(base_url: str, api_password: str) -> str:
    token_url = f"{base_url}/token"
    resp = requests.post(
        token_url,
        json={"APIPassword": api_password},
        timeout=10,
    )
    try:
        resp.raise_for_status()
    except requests.HTTPError as exc:
        raise SystemExit(
            f"Token request failed: HTTP {resp.status_code} {resp.text}"
        ) from exc

    data = resp.json()
    token = data.get("Token")
    if not token:
        raise SystemExit(f"Token response did not include 'Token': {data}")
    return token


def fetch_board(base_url: str, token: str, symbol_with_exchange: str) -> dict[str, Any]:
    url = f"{base_url}/board/{symbol_with_exchange}"
    resp = requests.get(
        url,
        headers={"X-API-KEY": token},
        timeout=10,
    )
    try:
        resp.raise_for_status()
    except requests.HTTPError as exc:
        raise SystemExit(
            f"Board request failed for {symbol_with_exchange}: HTTP {resp.status_code} {resp.text}"
        ) from exc
    return resp.json()


def sanitize_filename(symbol_with_exchange: str) -> str:
    return symbol_with_exchange.replace("@", "_").replace("/", "_").replace("\\", "_")


def main() -> int:
    args = parse_args()
    password_env_name = resolve_api_password_env(args.base_url, args.api_password_env)
    api_password = get_api_password(password_env_name)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    token = get_token(args.base_url, api_password)

    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    summary: list[str] = []

    for symbol_with_exchange in args.symbols:
        try:
            payload = fetch_board(args.base_url, token, symbol_with_exchange)
        except Exception as exc:
            print(f"Failed to fetch {symbol_with_exchange}: {exc}", file=sys.stderr)
            continue

        wrapper = {
            "fetched_at_utc": fetched_at,
            "source": "kabu_station_api",
            "base_url": args.base_url,
            "symbol_with_exchange": symbol_with_exchange,
            "payload": payload,
        }

        out_path = output_dir / f"{fetched_at}_{sanitize_filename(symbol_with_exchange)}.json"
        with out_path.open("w", encoding="utf-8", newline="\n") as f:
            json.dump(wrapper, f, ensure_ascii=False, indent=2)

        summary.append(str(out_path))

    if not summary:
        print("No data files were written.", file=sys.stderr)
        return 1

    print("Saved raw kabu API snapshots:")
    for item in summary:
        print(f"  - {item}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())