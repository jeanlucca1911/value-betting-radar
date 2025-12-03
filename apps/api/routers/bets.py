from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from db.models.bet import Bet
from datetime import datetime, timedelta
from typing import List

router = APIRouter()

class PlaceBetRequest(BaseModel):
    match_id: str
    home_team: str
    away_team: str
    selection: str
    odds: float
    stake: float
    bookmaker: str
    edge: float

class PortfolioStats(BaseModel):
    total_bets: int
    settled_bets: int
    pending_bets: int
    total_staked: float
    total_returned: float
    net_profit: float
    roi: float  # Return on Investment percentage
    win_rate: float  # Percentage of winning bets
    
class DailyProfit(BaseModel):
    date: str
    profit: float
    cumulative_profit: float

class PortfolioResponse(BaseModel):
    stats: PortfolioStats
    daily_profits: List[DailyProfit]

@router.get("/stats", response_model=PortfolioResponse)
async def get_portfolio_stats(
    user_email: str = "test@example.com",  # TODO: Get from JWT
    db: AsyncSession = Depends(get_db)
):
    """Get portfolio statistics for a user"""
    
    # Get all bets for user
    result = await db.execute(
        select(Bet).where(Bet.user_email == user_email)
    )
    bets = result.scalars().all()
    
    if not bets:
        # Return empty stats
        return PortfolioResponse(
            stats=PortfolioStats(
                total_bets=0,
                settled_bets=0,
                pending_bets=0,
                total_staked=0.0,
                total_returned=0.0,
                net_profit=0.0,
                roi=0.0,
                win_rate=0.0
            ),
            daily_profits=[]
        )
    
    # Calculate stats
    total_bets = len(bets)
    settled_bets = sum(1 for bet in bets if bet.status != "pending")
    pending_bets = total_bets - settled_bets
    total_staked = sum(bet.stake for bet in bets)
    
    # Calculate returns (only for settled bets)
    settled_bets_list = [b for b in bets if b.status in ["won", "lost"]]
    settled_staked = sum(b.stake for b in settled_bets_list)
    
    total_returned = sum(
        bet.potential_return for bet in settled_bets_list if bet.status == "won"
    )
    
    # Net profit is total returned - total staked (on settled bets only)
    net_profit = total_returned - settled_staked
    
    # ROI based on settled turnover
    roi = (net_profit / settled_staked * 100) if settled_staked > 0 else 0.0
    win_rate = (sum(1 for bet in settled_bets_list if bet.status == "won") / len(settled_bets_list) * 100) if settled_bets_list else 0.0
    
    # Calculate daily profits
    daily_data = {}
    for bet in bets:
        if bet.placed_at:
            date_key = bet.placed_at.strftime("%Y-%m-%d")
            if date_key not in daily_data:
                daily_data[date_key] = 0.0
            
            # Add profit/loss for this bet
            if bet.status == "won":
                daily_data[date_key] += (bet.potential_return - bet.stake)
            elif bet.status == "lost":
                daily_data[date_key] -= bet.stake
    
    # Convert to cumulative profits
    sorted_dates = sorted(daily_data.keys())
    cumulative = 0.0
    daily_profits = []
    
    for date in sorted_dates:
        profit = daily_data[date]
        cumulative += profit
        daily_profits.append(DailyProfit(
            date=date,
            profit=round(profit, 2),
            cumulative_profit=round(cumulative, 2)
        ))
    
    return PortfolioResponse(
        stats=PortfolioStats(
            total_bets=total_bets,
            settled_bets=settled_bets,
            pending_bets=pending_bets,
            total_staked=round(total_staked, 2),
            total_returned=round(total_returned, 2),
            net_profit=round(net_profit, 2),
            roi=round(roi, 2),
            win_rate=round(win_rate, 2)
        ),
        daily_profits=daily_profits
    )

@router.post("/place")
async def place_bet(
    bet_request: PlaceBetRequest,
    user_email: str = "test@example.com",  # TODO: Get from JWT
    db: AsyncSession = Depends(get_db)
):
    """Place a new bet (paper trading)"""
    
    # Create new bet
    new_bet = Bet(
        user_email=user_email,
        match_id=bet_request.match_id,
        home_team=bet_request.home_team,
        away_team=bet_request.away_team,
        selection=bet_request.selection,
        odds=bet_request.odds,
        stake=bet_request.stake,
        bookmaker=bet_request.bookmaker,
        edge=bet_request.edge,
        potential_return=bet_request.stake * bet_request.odds,
        status="pending",
        placed_at=datetime.utcnow()
    )
    
    db.add(new_bet)
    await db.commit()
    await db.refresh(new_bet)
    
    return {
        "success": True,
        "bet_id": new_bet.id,
        "message": f"Bet placed: {bet_request.selection} @ {bet_request.odds}"
    }
