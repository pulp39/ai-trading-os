-- AI Trading OS
-- Bootstrap SQL
-- 020_create_board_snapshots.sql
-- Version: 1.0
-- Date: 2026-03-08
--
-- NOTE:
-- board_snapshots currently exists in the public schema as a prototype market data table.
-- Future migration may move this table into a dedicated schema such as ops or market.

CREATE TABLE IF NOT EXISTS public.board_snapshots (
    id BIGSERIAL PRIMARY KEY,
    captured_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    symbol TEXT NOT NULL,
    exchange INTEGER NOT NULL,
    current_price NUMERIC(18,4),
    bid_price NUMERIC(18,4),
    ask_price NUMERIC(18,4),
    bid_qty NUMERIC(18,4),
    ask_qty NUMERIC(18,4),
    trading_volume NUMERIC(20,4),
    vwap NUMERIC(18,6),
    payload JSONB NOT NULL
);