from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from services.advanced_markets import AdvancedMarketsService
from pydantic import BaseModel

router = APIRouter()
service = AdvancedMarketsService()

class ParlayRequest(BaseModel):
    bets: List[Dict[str, Any]] # List of bets with 'odds' key

@router.get("/player-props/{sport_key}/{game_id}")
async def get_player_props(sport_key: str, game_id: str):
    """Get player props for a specific game"""
    props = await service.get_player_props(sport_key, game_id)
    return props

@router.get("/correct-score/{sport_key}/{game_id}")
async def get_correct_scores(sport_key: str, game_id: str):
    """Get correct score odds for a specific game"""
    scores = await service.get_correct_score_odds(sport_key, game_id)
    return scores

@router.post("/parlay-calculator")
async def calculate_parlay(request: ParlayRequest):
    """Calculate edge for a given parlay"""
    result = service.calculate_parlay_edge(request.bets)
    return result
