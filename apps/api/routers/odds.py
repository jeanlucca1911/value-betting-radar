from fastapi import APIRouter, Depends
from typing import List
from core.schemas import ValueBet
from services.odds_service import OddsService

router = APIRouter()
odds_service = OddsService()

@router.get("/live", response_model=List[ValueBet])
async def get_live_value_bets(
    sport: str = "soccer_epl",
    region: str = "uk"
):
    """
    Get live value bets.
    """
    return await odds_service.get_value_bets(sport=sport, region=region)
