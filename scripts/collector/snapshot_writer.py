import json
import os
import psycopg
from psycopg.types.json import Json


def insert_board_snapshot(board: dict) -> None:
    conn = psycopg.connect(
        host=os.environ["OPENCLAW_TRACE_DB_HOST"],
        port=os.environ["OPENCLAW_TRACE_DB_PORT"],
        dbname=os.environ["OPENCLAW_TRACE_DB_NAME"],
        user=os.environ["OPENCLAW_TRACE_DB_USER"],
        password=os.environ["OPENCLAW_TRACE_DB_PASSWORD"],
    )

    captured_at = board.get("CurrentPriceTime")
    if not captured_at:
        raise ValueError("CurrentPriceTime is missing in board payload")

    sql = """
    INSERT INTO public.board_snapshots (
        captured_at,
        symbol,
        exchange,
        current_price,
        bid_price,
        ask_price,
        bid_qty,
        ask_qty,
        trading_volume,
        vwap,
        payload
    )
    VALUES (
        %(captured_at)s,
        %(symbol)s,
        %(exchange)s,
        %(current_price)s,
        %(bid_price)s,
        %(ask_price)s,
        %(bid_qty)s,
        %(ask_qty)s,
        %(trading_volume)s,
        %(vwap)s,
        %(payload)s
    )
    ON CONFLICT (symbol, captured_at) DO NOTHING
    """

    params = {
        "captured_at": captured_at,
        "symbol": str(board.get("Symbol")),
        "exchange": board.get("Exchange", 1),
        "current_price": board.get("CurrentPrice"),
        "bid_price": board.get("BidPrice"),
        "ask_price": board.get("AskPrice"),
        "bid_qty": board.get("BidQty"),
        "ask_qty": board.get("AskQty"),
        "trading_volume": board.get("TradingVolume"),
        "vwap": board.get("VWAP"),
        "payload": Json(board),
    }

    with conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)

    conn.close()