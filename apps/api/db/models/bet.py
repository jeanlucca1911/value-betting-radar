from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime
from db.session import Base

class Bet(Base):
    __tablename__ = "bets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True, nullable=False)
    match_id = Column(String, nullable=False)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    selection = Column(String, nullable=False)  # Outcome selected
    bookmaker = Column(String, nullable=False)
    odds = Column(Float, nullable=False)
    stake = Column(Float, nullable=False)
    edge = Column(Float, nullable=False)  # Edge percentage at time of bet
    potential_return = Column(Float, nullable=False)  # stake * odds
    status = Column(String, default="pending")  # pending, won, lost
    placed_at = Column(DateTime, default=datetime.utcnow)
    settled_at = Column(DateTime, nullable=True)
