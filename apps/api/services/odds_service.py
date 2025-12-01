from typing import List
from core.config import settings
from core.schemas import ValueBet, MarketType
from services.mock_odds import MockOddsService
from services.odds_api import TheOddsApiClient
from services.math import PowerMethod

class OddsService:
    def __init__(self):
        self.mock_service = MockOddsService()
        self.api_client = TheOddsApiClient()

    async def get_value_bets(self) -> List[ValueBet]:
        # Fallback to mock if no API key
        if not settings.THE_ODDS_API_KEY:
            return self.mock_service.find_value_bets()

        matches = await self.api_client.get_odds()
        
        # If API fails or returns empty (and we have a key), we might want to return empty or fallback.
        # For now, let's fallback to mock if API returns nothing, just to keep the UI alive for the user
        if not matches:
            return self.mock_service.find_value_bets()

        value_bets = []
        for match in matches:
            # Find Pinnacle (sharp)
            pinnacle = next((b for b in match.bookmakers if b.key == "pinnacle"), None)
            if not pinnacle: continue
                
            pinnacle_market = next((m for m in pinnacle.markets if m.key == MarketType.H2H), None)
            if not pinnacle_market: continue

            sharp_odds = [o.price for o in pinnacle_market.outcomes]
            true_probs = PowerMethod.calculate_true_probabilities(sharp_odds)
            
            if not true_probs: continue

            for bookie in match.bookmakers:
                if bookie.key == "pinnacle": continue
                market = next((m for m in bookie.markets if m.key == MarketType.H2H), None)
                if not market: continue

                for i, outcome in enumerate(market.outcomes):
                    # Match outcome index (assuming same order, which is risky in prod but ok for MVP)
                    # Better: match by name
                    
                    # Simple matching by index for H2H (Home, Away, Draw)
                    if i >= len(true_probs): continue

                    edge = PowerMethod.calculate_edge(outcome.price, true_probs[i])
                    
                    if edge > 0.01: # 1% edge
                        value_bets.append(ValueBet(
                            match_id=match.id,
                            home_team=match.home_team,
                            away_team=match.away_team,
                            commence_time=match.commence_time,
                            bookmaker=bookie.title,
                            market="Head to Head",
                            outcome=outcome.name,
                            odds=outcome.price,
                            true_probability=true_probs[i],
                            edge=round(edge * 100, 2),
                            expected_value=round(edge * 100, 2) # Simplified EV
                        ))
        
        return sorted(value_bets, key=lambda x: x.edge, reverse=True)
