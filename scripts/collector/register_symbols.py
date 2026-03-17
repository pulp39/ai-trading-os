#!/usr/bin/env python3
# NOTE: Current environment may require running symbol registration from Windows PowerShell instead of WSL.

import json
import os
import urllib.request
from urllib.error import HTTPError, URLError

TOKEN_URL = "http://172.18.240.1:18080/kabusapi/token"
REGISTER_URL = "http://172.18.240.1:18080/kabusapi/register"

PASSWORD = os.environ["KABU_API_PASSWORD"]

SYMBOLS = [
    {"Symbol": "7203", "Exchange": 1},
    {"Symbol": "8306", "Exchange": 1},
    {"Symbol": "6758", "Exchange": 1},
]


def post_json(url: str, payload: dict, token: str | None = None) -> dict:
    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}

    if token:
        headers["X-API-KEY"] = token

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req) as res:
        body = res.read().decode("utf-8")
        return json.loads(body) if body else {}


def main() -> None:
    try:
        token_resp = post_json(TOKEN_URL, {"APIPassword": PASSWORD})
        token = token_resp["Token"]
        print(f"token acquired: {token[:8]}...")

        reg_resp = post_json(REGISTER_URL, {"Symbols": SYMBOLS}, token=token)
        print(json.dumps(reg_resp, ensure_ascii=False, indent=2))

    except KeyError:
        print("Error: environment variable KABU_API_PASSWORD is not set")
    except HTTPError as e:
        print(f"HTTPError: {e.code} {e.reason}")
        try:
            print(e.read().decode("utf-8"))
        except Exception:
            pass
    except URLError as e:
        print(f"URLError: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()