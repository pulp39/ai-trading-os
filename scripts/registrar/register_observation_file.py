import json
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: python register_observation_file.py <observation_json_path>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    observation = json.loads(input_path.read_text(encoding="utf-8"))

    event = {
        "task_id": "REG-20260317-OBS-001",
        "task_type": "bounded_db_test",
        "db_scope": {
            "schema": "research",
            "table": "trace_event"
        },
        "allowed_actions": ["INSERT"],
        "steps": [
            {
                "step": 1,
                "action": "INSERT",
                "sql": (
                    "INSERT INTO research.trace_event "
                    "(session_id, agent_id, actor_type, event_type, symbol, exchange, content, metadata) "
                    "VALUES "
                    f"('kabu-observation-001', 'openclaw_aux', 'ai', 'market_observation', "
                    f"'{observation['symbol']}', {observation['exchange']}, "
                    f"'{observation['symbol']} {observation['summary']['symbol_name']} "
                    f"price={observation['summary']['current_price']} "
                    f"prev={observation['summary']['previous_close']} "
                    f"vol={observation['summary']['trading_volume']} "
                    f"captured_at={observation['captured_at']}', "
                    f"$json${json.dumps(observation, ensure_ascii=False)}$json$::jsonb) "
                    "RETURNING id, ts"
                )
            }
        ]
    }

    output_path = input_path.with_name(input_path.stem + "_task.json")
    output_path.write_text(
        json.dumps(event, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(output_path)


if __name__ == "__main__":
    main()