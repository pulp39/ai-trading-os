import os
from datetime import datetime

import psycopg
from psycopg.types.json import Json


def insert_board_snapshot(board: dict) -> dict:
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
    ON CONFLICT (symbol, captured_at) DO UPDATE
    SET
        exchange = EXCLUDED.exchange,
        current_price = EXCLUDED.current_price,
        bid_price = EXCLUDED.bid_price,
        ask_price = EXCLUDED.ask_price,
        bid_qty = EXCLUDED.bid_qty,
        ask_qty = EXCLUDED.ask_qty,
        trading_volume = EXCLUDED.trading_volume,
        vwap = EXCLUDED.vwap,
        payload = EXCLUDED.payload
    RETURNING id, captured_at
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
            row = cur.fetchone()

    conn.close()

    snapshot_id, captured_at_value = row

    if isinstance(captured_at_value, str):
        captured_at_value = datetime.fromisoformat(captured_at_value)

    return {
        "snapshot_id": snapshot_id,
        "captured_at": captured_at_value,
    }