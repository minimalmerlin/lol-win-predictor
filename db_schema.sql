-- ========================================
-- LoL Coaching System - Database Schema
-- Version: 1.0
-- Created: 2025-12-29 22:42 CET
-- Database: Supabase PostgreSQL 17.6
-- ========================================

-- Drop existing tables if they exist (for clean re-runs)
DROP TABLE IF EXISTS match_snapshots CASCADE;
DROP TABLE IF EXISTS match_champions CASCADE;
DROP TABLE IF EXISTS matches CASCADE;

-- ========================================
-- 1. MATCHES TABLE
-- ========================================
-- Stores basic match metadata
-- Primary Key: match_id (prevents duplicates)

CREATE TABLE matches (
    match_id VARCHAR(50) PRIMARY KEY,
    game_duration FLOAT NOT NULL,
    blue_win BOOLEAN NOT NULL,
    patch_version VARCHAR(20),
    queue_id INTEGER DEFAULT 420,
    crawled_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),

    -- Data Quality Constraints
    CHECK (game_duration >= 3),        -- Min. 3 minutes (Remake)
    CHECK (game_duration <= 120)       -- Max. 120 minutes (unrealistic)
);

-- Indices for Performance
CREATE INDEX idx_matches_crawled_at ON matches(crawled_at);
CREATE INDEX idx_matches_blue_win ON matches(blue_win);
CREATE INDEX idx_matches_patch ON matches(patch_version);

COMMENT ON TABLE matches IS 'Match metadata - one row per match';
COMMENT ON COLUMN matches.match_id IS 'Unique match identifier from Riot API (e.g., EUW1_6543210987)';
COMMENT ON COLUMN matches.blue_win IS 'True if blue team won, false if red team won';
COMMENT ON COLUMN matches.patch_version IS 'Game patch version (e.g., 15.24.1)';

-- ========================================
-- 2. MATCH CHAMPIONS TABLE
-- ========================================
-- Stores champion picks (normalized structure)
-- 10 rows per match (5 blue + 5 red)

CREATE TABLE match_champions (
    id SERIAL PRIMARY KEY,
    match_id VARCHAR(50) NOT NULL REFERENCES matches(match_id) ON DELETE CASCADE,
    team VARCHAR(4) NOT NULL,
    champion_id INTEGER NOT NULL,
    position INTEGER NOT NULL,

    -- Constraints
    UNIQUE(match_id, team, position),  -- Each position only once per team
    CHECK (team IN ('blue', 'red')),
    CHECK (position >= 1 AND position <= 5)
);

-- Indices for Champion Queries
CREATE INDEX idx_champions_match_id ON match_champions(match_id);
CREATE INDEX idx_champions_champion_id ON match_champions(champion_id);
CREATE INDEX idx_champions_team ON match_champions(team);

COMMENT ON TABLE match_champions IS 'Champion picks - 10 rows per match (5 blue + 5 red)';
COMMENT ON COLUMN match_champions.champion_id IS 'Champion ID from Riot API (e.g., 157 = Yasuo)';
COMMENT ON COLUMN match_champions.position IS 'Position 1-5 (Top, Jungle, Mid, ADC, Support)';

-- ========================================
-- 3. MATCH SNAPSHOTS TABLE
-- ========================================
-- Stores game state at specific time intervals
-- 1-3 rows per match (10min, 15min, 20min snapshots)

CREATE TABLE match_snapshots (
    id SERIAL PRIMARY KEY,
    match_id VARCHAR(50) NOT NULL REFERENCES matches(match_id) ON DELETE CASCADE,
    snapshot_time INTEGER NOT NULL,

    -- Gold Features
    blue_gold INTEGER NOT NULL,
    red_gold INTEGER NOT NULL,
    gold_diff INTEGER NOT NULL,

    -- XP Features
    blue_xp INTEGER NOT NULL,
    red_xp INTEGER NOT NULL,
    xp_diff INTEGER NOT NULL,

    -- Level (total for all 5 champions)
    blue_level INTEGER NOT NULL,
    red_level INTEGER NOT NULL,

    -- CS (Creep Score / Minions Killed)
    blue_cs INTEGER NOT NULL,
    red_cs INTEGER NOT NULL,

    -- Objectives
    blue_dragons INTEGER DEFAULT 0,
    red_dragons INTEGER DEFAULT 0,
    blue_barons INTEGER DEFAULT 0,
    red_barons INTEGER DEFAULT 0,
    blue_towers INTEGER DEFAULT 0,
    red_towers INTEGER DEFAULT 0,

    -- Kills
    blue_kills INTEGER DEFAULT 0,
    red_kills INTEGER DEFAULT 0,
    kill_diff INTEGER NOT NULL,

    -- Constraints
    UNIQUE(match_id, snapshot_time),
    CHECK (snapshot_time IN (10, 15, 20)),
    CHECK (blue_level >= 5 AND blue_level <= 90),  -- Total levels (5 champions)
    CHECK (red_level >= 5 AND red_level <= 90)
);

-- Indices for Snapshot Queries
CREATE INDEX idx_snapshots_match_id ON match_snapshots(match_id);
CREATE INDEX idx_snapshots_time ON match_snapshots(snapshot_time);
CREATE INDEX idx_snapshots_gold_diff ON match_snapshots(gold_diff);

COMMENT ON TABLE match_snapshots IS 'Game state snapshots at 10min, 15min, 20min intervals';
COMMENT ON COLUMN match_snapshots.snapshot_time IS 'Time in minutes (10, 15, or 20)';
COMMENT ON COLUMN match_snapshots.gold_diff IS 'Blue gold - Red gold (positive = blue advantage)';

-- ========================================
-- VERIFICATION QUERIES
-- ========================================
-- Run these to verify schema was created correctly

-- Check tables exist
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public' AND table_name IN ('matches', 'match_champions', 'match_snapshots');

-- Check row counts (should be 0 initially)
SELECT
    (SELECT COUNT(*) FROM matches) as matches_count,
    (SELECT COUNT(*) FROM match_champions) as champions_count,
    (SELECT COUNT(*) FROM match_snapshots) as snapshots_count;

-- ========================================
-- END OF SCHEMA
-- ========================================
