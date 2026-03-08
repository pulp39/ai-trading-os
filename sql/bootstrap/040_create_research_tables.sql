-- AI Trading OS
-- Bootstrap SQL
-- 040_create_research_tables.sql
-- Version: 1.0
-- Date: 2026-03-08

CREATE TABLE IF NOT EXISTS research.trace_event (
    id BIGSERIAL PRIMARY KEY,
    ts TIMESTAMPTZ NOT NULL DEFAULT now(),
    session_id TEXT,
    agent_id TEXT NOT NULL,
    actor_type TEXT NOT NULL,
    event_type TEXT NOT NULL,
    symbol TEXT,
    exchange INTEGER,
    content TEXT,
    parent_event_id BIGINT,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS research.proposal (
    id BIGSERIAL PRIMARY KEY,
    ts TIMESTAMPTZ NOT NULL DEFAULT now(),
    session_id TEXT,
    agent_id TEXT NOT NULL,
    proposal_type TEXT NOT NULL,
    symbol TEXT,
    exchange INTEGER,
    title TEXT,
    proposal_text TEXT NOT NULL,
    confidence NUMERIC(5,4),
    status TEXT NOT NULL DEFAULT 'proposed',
    linked_event_id BIGINT,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS research.agent (
    id BIGSERIAL PRIMARY KEY,
    agent_id TEXT UNIQUE NOT NULL,
    agent_name TEXT NOT NULL,
    agent_type TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS research.role (
    id BIGSERIAL PRIMARY KEY,
    role_name TEXT UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS research.agent_role (
    id BIGSERIAL PRIMARY KEY,
    agent_id TEXT NOT NULL,
    role_name TEXT NOT NULL,
    assigned_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    assigned_by TEXT,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);