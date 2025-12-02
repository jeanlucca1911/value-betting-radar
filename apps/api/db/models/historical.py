from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.session import Base
from datetime import datetime

class HistoricalMatch(Base):
    __tablename__ = "historical_matches"

    id = Column(String, primary_key=True, index=True) # The Odds API Match ID
    sport_key = Column(String, index=True)
    sport_title = Column(String)
    home_team = Column(String)
    away_team = Column(String)
    commence_time = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to odds
    odds_history = relationship("HistoricalOdds", back_populates="match")

class HistoricalOdds(Base):
    __tablename__ = "historical_odds"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(String, ForeignKey("historical_matches.id"))
    bookmaker = Column(String, index=True)
    market_key = Column(String) # h2h, spreads, etc.
    outcome_name = Column(String)
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    match = relationship("HistoricalMatch", back_populates="odds_history")
