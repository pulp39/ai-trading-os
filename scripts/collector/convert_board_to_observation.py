import json
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: python convert_board_to_observation.py <board_json_path>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    board = json.loads(input_path.read_text(encoding="utf-8-sig"))
    
    observation = {
        "observation_type": "price_board",
        "source": "kabusapi_board",
        "symbol": board["Symbol"],
        "exchange": board["Exchange"],
        "captured_at": board["CurrentPriceTime"],
        "summary": {
            "symbol_name": board["SymbolName"],
            "current_price": board["CurrentPrice"],
            "previous_close": board["PreviousClose"],
            "trading_volume": board["TradingVolume"],
            "bid_price": board["BidPrice"],
            "ask_price": board["AskPrice"],
            "vwap": board["VWAP"]
        },
        "payload": board
    }

    output_path = input_path.with_name(input_path.stem + "_observation.json")
    output_path.write_text(
        json.dumps(observation, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(output_path)


if __name__ == "__main__":
    main()