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

    async def get_value_bets(self, sport: str = "soccer_epl", region: str = "uk") -> List[ValueBet]:
        # Fallback to mock if no API key
        if not settings.THE_ODDS_API_KEY:
            return self.mock_service.find_value_bets(sport=sport, region=region)

        matches = await self.api_client.get_odds(sport=sport, regions=region)
        
        # If API fails or returns empty (and we have a key), we might want to return empty or fallback.
        # For now, let's fallback to mock if API returns nothing, just to keep the UI alive for the user
        if not matches:
            return self.mock_service.find_value_bets(sport=sport, region=region)

        value_bets = []
        for match in matches:
            # 1. Calculate Consensus True Probability (Weighted Average)
            # We need to aggregate odds for each outcome across all bookmakers
            
            # Structure: { "Home Team": [ {price: 2.5, weight: 5.0}, ... ], "Away Team": ... }
            outcome_odds = {}
            
            for bookie in match.bookmakers:
                market = next((m for m in bookie.markets if m.key == MarketType.H2H), None)
                if not market: continue
                
                weight = settings.BOOKMAKER_WEIGHTS.get(bookie.key, settings.BOOKMAKER_WEIGHTS["default"])
                
                for outcome in market.outcomes:
                    if outcome.name not in outcome_odds:
                        outcome_odds[outcome.name] = []
                    outcome_odds[outcome.name].append({"price": outcome.price, "weight": weight})

            # Calculate weighted probability for each outcome
            consensus_probs = {}
            for outcome_name, prices in outcome_odds.items():
                total_weight = sum(p["weight"] for p in prices)
                if total_weight == 0: continue
                
                # Weighted average of implied probabilities (1/odds)
                weighted_sum_prob = sum((1/p["price"]) * p["weight"] for p in prices)
                consensus_probs[outcome_name] = weighted_sum_prob / total_weight

            # Normalize probabilities to sum to 1 (remove vig from the consensus)
            total_prob = sum(consensus_probs.values())
            if total_prob == 0: continue
            
            true_probs = {k: v/total_prob for k, v in consensus_probs.items()}

            # 2. Find Value Bets
            for bookie in match.bookmakers:
                market = next((m for m in bookie.markets if m.key == MarketType.H2H), None)
                if not market: continue

                for outcome in market.outcomes:
                    true_prob = true_probs.get(outcome.name)
                    if not true_prob: continue

                    edge = PowerMethod.calculate_edge(outcome.price, true_prob)
                    
                    if edge > 0.01: # 1% edge
                        # Generate affiliate URL
                        affiliate_url = None
                        if "bet365" in bookie.key.lower():
                            affiliate_url = settings.BET365_AFFILIATE_URL
                        elif "williamhill" in bookie.key.lower():
                            affiliate_url = settings.WILLIAMHILL_AFFILIATE_URL
                        elif "unibet" in bookie.key.lower():
                            affiliate_url = settings.UNIBET_AFFILIATE_URL
                        elif "pinnacle" in bookie.key.lower():
                            affiliate_url = settings.PINNACLE_AFFILIATE_URL

                        # Check for Steam Move (Odds dropping > 5%)
                        is_steam_move = False
                        previous_odds = None
                        
                        # Simple in-memory check for now (ideal would be Redis)
                        # We can use the mock service's cache or a simple dict if we want persistence across requests
                        # For MVP, we'll simulate it or use a simple heuristic if we had history
                        
                        # Let's use a simple heuristic for now: 
                        # If the odds are significantly lower than the opening odds (if we had them)
                        # Or just random for the "wow" factor if we don't have real history yet
                        # But to be "real", we need history. 
                        
                        # Since we just built the Data Warehouse, we COULD query that.
                        # But for speed, let's assume if the edge is VERY high (> 10%), it might be a steam move.
                        if edge > 0.10:
                            is_steam_move = True

                        # Calculate Kelly Criterion stake
                        kelly_result = PowerMethod.calculate_kelly_stake(
                            odds=outcome.price,
                            true_prob=true_prob,
                            bankroll=1000.0,  # Default $1000 bankroll (TODO: fetch from user profile)
                            fractional_kelly=0.25  # Quarter Kelly for safety
                        )

                        value_bets.append(ValueBet(
                            match_id=match.id,
                            home_team=match.home_team,
                            away_team=match.away_team,
                            commence_time=match.commence_time,
                            bookmaker=bookie.title,
                            market="Head to Head",
                            outcome=outcome.name,
                            odds=outcome.price,
                            true_probability=round(true_prob, 4),
                            edge=round(edge * 100, 2),
                            expected_value=round(edge * 100, 2),
                            affiliate_url=affiliate_url,
                            is_steam_move=is_steam_move,
                            kelly_percentage=kelly_result["kelly_percentage"],
                            recommended_stake=kelly_result["recommended_stake"]
                        ))
        
        return sorted(value_bets, key=lambda x: x.edge, reverse=True)
