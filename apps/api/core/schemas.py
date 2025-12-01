from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
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
    key: MarketType
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
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    affiliate_url: Optional[str] = None

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
