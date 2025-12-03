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

@router.get("/props")
async def get_player_props(
    sport: str = "soccer_epl",
    region: str = "uk"
):
    """
    Get player prop value bets (Anytime Goalscorer).
    """
    try:
        return await odds_service.get_player_props(sport=sport, region=region)
    except Exception as e:
        print(f"Error fetching player props: {e}")
        return []

@router.get("/scores")
async def get_correct_scores(
    sport: str = "soccer_epl",
    region: str = "uk"
):
    """
    Get correct score value bets.
    """
    try:
        return await odds_service.get_correct_scores(sport=sport, region=region)
    except Exception as e:
        print(f"Error fetching correct scores: {e}")
        return []
