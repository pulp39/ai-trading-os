#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from typing import List

KABU_PORT = 18080
DEFAULT_EXCHANGE = 1


@dataclass(frozen=True)
class SymbolSpec:
    symbol: str
    exchange: int = DEFAULT_EXCHANGE


# ============================================================
# Founder-maintained registration list
# Edit this list directly when adding/removing symbols.
# ============================================================
SYMBOLS_TO_REGISTER: List[SymbolSpec] = [
    SymbolSpec("8306", 1),
]


def run_powershell(ps_script: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", ps_script],
        capture_output=True,
        text=True,
        encoding="cp932",
        errors="replace",
    )


def normalize_symbol_specs(symbols: List[SymbolSpec]) -> List[SymbolSpec]:
    normalized: List[SymbolSpec] = []
    seen = set()

    for spec in symbols:
        symbol = str(spec.symbol).strip()
        exchange = int(spec.exchange)

        if not symbol:
            continue

        key = (symbol, exchange)
        if key in seen:
            continue

        seen.add(key)
        normalized.append(SymbolSpec(symbol=symbol, exchange=exchange))

    if not normalized:
        raise ValueError("SYMBOLS_TO_REGISTER is empty. Add at least one symbol.")

    return normalized


def build_register_body(symbols: List[SymbolSpec]) -> dict:
    return {
        "Symbols": [
            {"Symbol": spec.symbol, "Exchange": spec.exchange}
            for spec in symbols
        ]
    }


def register_symbols_via_powershell(symbols: List[SymbolSpec]) -> dict:
    password = os.environ.get("KABU_API_PASSWORD")
    if not password:
        raise RuntimeError("KABU_API_PASSWORD is missing or empty.")

    payload = build_register_body(symbols)
    reg_json = json.dumps(payload, ensure_ascii=False)

    ps_script = f"""
$ErrorActionPreference = "Stop"
$env:KABU_API_PASSWORD = {json.dumps(password)}

$tokenBody = @{{ APIPassword = $env:KABU_API_PASSWORD }} | ConvertTo-Json
$tokenResponse = Invoke-RestMethod -Method Post -Uri "http://localhost:{KABU_PORT}/kabusapi/token" -ContentType "application/json" -Body $tokenBody
$token = $tokenResponse.Token

$regBody = @'
{reg_json}
'@

$result = Invoke-RestMethod -Method Put -Uri "http://localhost:{KABU_PORT}/kabusapi/register" -Headers @{{ "X-API-KEY" = $token }} -ContentType "application/json" -Body $regBody

@{{
    TokenAcquired = $true
    RegisterResult = $result
    SymbolCount = {len(symbols)}
}} | ConvertTo-Json -Depth 10
"""

    result = run_powershell(ps_script)
    if result.returncode != 0:
        raise RuntimeError(
            "PowerShell symbol registration failed\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )

    stdout = result.stdout.strip()
    if not stdout:
        return {"ok": True, "raw_stdout": ""}

    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return {"ok": True, "raw_stdout": stdout}


def main() -> None:
    specs = normalize_symbol_specs(SYMBOLS_TO_REGISTER)

    print("Registering symbols via Windows PowerShell...")
    print(
        json.dumps(
            {
                "symbols": [
                    {"symbol": spec.symbol, "exchange": spec.exchange}
                    for spec in specs
                ],
                "count": len(specs),
                "kabu_port": KABU_PORT,
            },
            ensure_ascii=False,
            indent=2,
        )
    )

    result = register_symbols_via_powershell(specs)

    print("Registration completed.")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)