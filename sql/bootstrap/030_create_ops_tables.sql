-- AI Trading OS
-- Bootstrap SQL
-- 030_create_ops_tables.sql
-- Version: 1.0
-- Date: 2026-03-08

CREATE TABLE IF NOT EXISTS ops.collector_status (
    id BIGSERIAL PRIMARY KEY,
    ts TIMESTAMPTZ NOT NULL DEFAULT now(),
    collector_name TEXT NOT NULL,
    run_id TEXT,
    symbol TEXT,
    exchange INTEGER,
    status TEXT NOT NULL,
    rows_written INTEGER DEFAULT 0,
    message TEXT,
    error_detail TEXT,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);