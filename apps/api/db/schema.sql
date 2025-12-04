-- Historical Odds Data Warehouse Schema
-- Purpose: Store odds snapshots for Bayesian priors and CLV analysis

-- ============================================
-- CORE TABLES
-- ============================================

-- Sports and leagues reference
CREATE TABLE IF NOT EXISTS sports (
    sport_key TEXT PRIMARY KEY,
    sport_title TEXT NOT NULL,
    has_outrights BOOLEAN DEFAULT FALSE,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Matches (events)
CREATE TABLE IF NOT EXISTS matches (
    id TEXT PRIMARY KEY,  -- From API
    sport_key TEXT NOT NULL,
    commence_time TIMESTAMP NOT NULL,
    home_team TEXT NOT NULL,
    away_team TEXT NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    home_score INTEGER,
    away_score INTEGER,
    winner TEXT,  -- 'home', 'away', 'draw'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sport_key) REFERENCES sports(sport_key)
);

CREATE INDEX idx_matches_sport ON matches(sport_key);
CREATE INDEX idx_matches_commence ON matches(commence_time);
CREATE INDEX idx_matches_teams ON matches(home_team, away_team);

-- Bookmakers
CREATE TABLE IF NOT EXISTS bookmakers (
    key TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    region TEXT,  -- 'us', 'uk', 'eu', 'au'
    reliability_score REAL DEFAULT 1.0,  -- 0-1, updated based on performance
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- HISTORICAL ODDS SNAPSHOTS
-- ============================================

-- Odds snapshots (time series)
CREATE TABLE IF NOT EXISTS odds_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id TEXT NOT NULL,
    bookmaker_key TEXT NOT NULL,
    market_key TEXT NOT NULL,  -- 'h2h', 'spreads', 'totals', 'player_points'
    outcome_name TEXT NOT NULL,  -- Team name or 'Over'/'Under'
    odds REAL NOT NULL,  -- Decimal odds
    point REAL,  -- For spreads/totals (e.g., -3.5, 215.5)
    snapshot_time TIMESTAMP NOT NULL,
    time_to_event_hours REAL,  -- Hours until match starts
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id) REFERENCES matches(id),
    FOREIGN KEY (bookmaker_key) REFERENCES bookmakers(key)
);

CREATE INDEX idx_snapshots_match ON odds_snapshots(match_id);
CREATE INDEX idx_snapshots_time ON odds_snapshots(snapshot_time);
CREATE INDEX idx_snapshots_bookmaker ON odds_snapshots(bookmaker_key);
CREATE INDEX idx_snapshots_market ON odds_snapshots(market_key);

-- Closing odds (final snapshot before game starts)
CREATE TABLE IF NOT EXISTS closing_odds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id TEXT NOT NULL,
    bookmaker_key TEXT NOT NULL,
    market_key TEXT NOT NULL,
    outcome_name TEXT NOT NULL,
    closing_odds REAL NOT NULL,
    point REAL,
    snapshot_time TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id) REFERENCES matches(id),
    FOREIGN KEY (bookmaker_key) REFERENCES bookmakers(key),
    UNIQUE(match_id, bookmaker_key, market_key, outcome_name)
);

-- ============================================
-- VALUE BETS TRACKING
-- ============================================

-- Value bets we recommended
CREATE TABLE IF NOT EXISTS recommended_bets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id TEXT NOT NULL,
    bookmaker_key TEXT NOT NULL,
    market_key TEXT NOT NULL,
    outcome_name TEXT NOT NULL,
    recommended_odds REAL NOT NULL,
    true_probability REAL NOT NULL,  -- Our consensus probability
    edge REAL NOT NULL,  -- Calculated edge at time of recommendation
    kelly_fraction REAL,
    recommended_stake REAL,
    recommendation_time TIMESTAMP NOT NULL,
    closing_odds REAL,  -- Filled after match
    clv REAL,  -- Closing Line Value, filled after match
    result TEXT,  -- 'win', 'loss', 'push', filled after match
    profit_loss REAL,  -- Actual P&L if user bet
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id) REFERENCES matches(id),
    FOREIGN KEY (bookmaker_key) REFERENCES bookmakers(key)
);

CREATE INDEX idx_recommended_match ON recommended_bets(match_id);
CREATE INDEX idx_recommended_time ON recommended_bets(recommendation_time);

-- ============================================
-- BOOKMAKER PERFORMANCE TRACKING
-- ============================================

-- Track bookmaker accuracy over time
CREATE TABLE IF NOT EXISTS bookmaker_performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bookmaker_key TEXT NOT NULL,
    sport_key TEXT NOT NULL,
    market_key TEXT NOT NULL,
    measurement_period_start DATE NOT NULL,
    measurement_period_end DATE NOT NULL,
    total_bets INTEGER NOT NULL,
    avg_implied_prob REAL,
    avg_actual_prob REAL,  -- Actual win rate
    calibration_error REAL,  -- |implied - actual|
    brier_score REAL,  -- Accuracy metric
    log_loss REAL,  -- Another accuracy metric
    avg_overround REAL,  -- Average vig
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bookmaker_key) REFERENCES bookmakers(key),
    FOREIGN KEY (sport_key) REFERENCES sports(sport_key),
    UNIQUE(bookmaker_key, sport_key, market_key, measurement_period_start)
);

-- ============================================
-- BAYESIAN MODEL DATA
-- ============================================

-- Historical matchup outcomes (for priors)
CREATE TABLE IF NOT EXISTS historical_matchups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sport_key TEXT NOT NULL,
    team1 TEXT NOT NULL,
    team2 TEXT NOT NULL,
    team1_wins INTEGER DEFAULT 0,
    team2_wins INTEGER DEFAULT 0,
    draws INTEGER DEFAULT 0,
    total_games INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sport_key) REFERENCES sports(sport_key),
    UNIQUE(sport_key, team1, team2)
);

-- ============================================
-- METADATA & LOGS
-- ============================================

-- Data collection runs
CREATE TABLE IF NOT EXISTS collection_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_type TEXT NOT NULL,  -- 'daily_snapshot', 'closing_odds', 'results'
    sport_key TEXT,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    status TEXT NOT NULL,  -- 'running', 'completed', 'failed'
    matches_processed INTEGER DEFAULT 0,
    odds_collected INTEGER DEFAULT 0,
    api_credits_used INTEGER DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_collection_runs_time ON collection_runs(start_time);

-- ============================================
-- VIEWS FOR COMMON QUERIES
-- ============================================

-- Latest odds for each match
CREATE VIEW IF NOT EXISTS latest_odds AS
SELECT 
    os.*,
    m.home_team,
    m.away_team,
    m.commence_time
FROM odds_snapshots os
INNER JOIN matches m ON os.match_id = m.id
INNER JOIN (
    SELECT match_id, bookmaker_key, market_key, outcome_name, MAX(snapshot_time) as max_time
    FROM odds_snapshots
    GROUP BY match_id, bookmaker_key, market_key, outcome_name
) latest ON 
    os.match_id = latest.match_id AND
    os.bookmaker_key = latest.bookmaker_key AND
    os.market_key = latest.market_key AND
    os.outcome_name = latest.outcome_name AND
    os.snapshot_time = latest.max_time;

-- CLV summary
CREATE VIEW IF NOT EXISTS clv_summary AS
SELECT 
    bookmaker_key,
    market_key,
    COUNT(*) as total_bets,
    AVG(clv) as avg_clv,
    SUM(CASE WHEN clv > 0 THEN 1 ELSE 0 END) as positive_clv_count,
    AVG(CASE WHEN result = 'win' THEN 1.0 ELSE 0.0 END) as win_rate,
    SUM(profit_loss) as total_profit
FROM recommended_bets
WHERE closing_odds IS NOT NULL
GROUP BY bookmaker_key, market_key;

-- ============================================
-- INITIAL DATA
-- ============================================

-- Insert major sports
INSERT OR IGNORE INTO sports (sport_key, sport_title, active) VALUES
('soccer_epl', 'Premier League', TRUE),
('soccer_uefa_champions_league', 'UEFA Champions League', TRUE),
('basketball_nba', 'NBA', TRUE),
('americanfootball_nfl', 'NFL', TRUE),
('icehockey_nhl', 'NHL', TRUE);

-- Insert major bookmakers
INSERT OR IGNORE INTO bookmakers (key, title, region, reliability_score) VALUES
-- US Books
('draftkings', 'DraftKings', 'us', 0.95),
('fanduel', 'FanDuel', 'us', 0.95),
('betmgm', 'BetMGM', 'us', 0.90),
('caesars', 'Caesars', 'us', 0.90),
('betrivers', 'BetRivers', 'us', 0.88),
('pointsbetus', 'PointsBet (US)', 'us', 0.85),
('wynnbet', 'WynnBET', 'us', 0.85),

-- Sharp Books
('pinnacle', 'Pinnacle', 'eu', 1.00),
('bookmaker', 'Bookmaker', 'us', 0.95),

-- UK/EU Books
('williamhill', 'William Hill', 'uk', 0.92),
('bet365', 'Bet365', 'uk', 0.95),
('unibet', 'Unibet', 'eu', 0.90),
('betfair', 'Betfair', 'uk', 0.98),

-- Soft Books
('mybookieag', 'MyBookie.ag', 'us', 0.75),
('bovada', 'Bovada', 'us', 0.80),
('betonlineag', 'BetOnline.ag', 'us', 0.80);
