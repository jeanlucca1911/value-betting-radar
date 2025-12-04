from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone
from enum import Enum

class Sport(str, Enum):
    SOCCER = "soccer"

class MarketType(str, Enum):
    H2H = "h2h"
    TOTALS = "totals"
    SPREADS = "spreads"

class Outcome(BaseModel):
    name: str
    price: float
    point: Optional[float] = None

class Bookmaker(BaseModel):
    key: str
    title: str
    last_update: datetime
    markets: List["Market"] = []

class Market(BaseModel):
    key: str
    outcomes: List[Outcome]

class Match(BaseModel):
    id: str
    sport_key: str
    sport_title: str
    commence_time: datetime
    home_team: str
    away_team: str
    bookmakers: List[Bookmaker] = []

class ValueBet(BaseModel):
    match_id: str
    home_team: str
    away_team: str
    commence_time: datetime
    bookmaker: str
    market: str
    outcome: str
    odds: float
    true_probability: float
    edge: float
    expected_value: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Bayesian Consensus Fields (NEW - Phase 1)
    probability_ci_lower: Optional[float] = None  # 95% CI lower bound
    probability_ci_upper: Optional[float] = None  # 95% CI upper bound
    confidence_score: Optional[str] = None  # A/B/C/D quality grade
    effective_samples: Optional[int] = None  # Bayesian effective sample size
    
    # Advanced Edge Fields (NEW - Phase 1)
    raw_edge: Optional[float] = None  # Mathematical edge before adjustments
    risk_adjusted_edge: Optional[float] = None  # After all risk penalties
    uncertainty_penalty: Optional[float] = None  # Penalty for wide CI
    liquidity_factor: Optional[float] = None  # Market liquidity score
    quality_score: Optional[str] = None  # Overall quality (A/B/C/D)
    
    # Kelly Recommendation Fields (NEW - Phase 1)
    recommended_stake_pct: Optional[float] = None  # % of bankroll
    recommended_stake_amount: Optional[float] = None  # Dollar amount (if bankroll known)
    kelly_fraction: Optional[float] = None  # Fractional Kelly used
    risk_of_ruin: Optional[float] = None  # Probability of 50% drawdown
    
    # Legacy fields
    affiliate_url: Optional[str] = None
    is_steam_move: Optional[bool] = False
    previous_odds: Optional[float] = None
    kelly_percentage: float = 0.0
    recommended_stake: float = 0.0
    is_mock: bool = False

# Player Prop specific (for Advanced Markets)
class PlayerProp(BaseModel):
    player_name: str
    team: str
    market: str  # e.g., "player_points", "player_rebounds"
    line: float  # O/U line
    over_odds: float
    under_odds: float
    over_edge: Optional[float] = None
    under_edge: Optional[float] = None
    bookmaker: str
    match_id: str

class BetRequest(BaseModel):
    match_id: str
    selection: str
    odds: float
    stake: float
    bookmaker: str

class BetResponse(BaseModel):
    id: str
    status: str
    timestamp: datetime
    potential_return: float

Bookmaker.model_rebuild()
