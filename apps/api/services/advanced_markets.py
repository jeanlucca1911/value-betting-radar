import httpx
from typing import List, Dict, Any
from core.config import settings
from core.schemas import ValueBet

class AdvancedMarketsService:
    def __init__(self):
        self.api_key = settings.THE_ODDS_API_KEY
        self.base_url = "https://api.the-odds-api.com/v4"
        
    async def get_player_props(self, sport_key: str, game_id: str) -> List[Dict[str, Any]]:
        """
        Fetch player props for a specific game.
        Markets: player_goal_scorer, player_assists, etc.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/sports/{sport_key}/events/{game_id}/odds",
                params={
                    "apiKey": self.api_key,
                    "regions": "uk,eu",
                    "markets": "player_goal_scorer", # Focus on goal scorers first
                    "oddsFormat": "decimal"
                }
            )
            
            if response.status_code != 200:
                print(f"Error fetching player props: {response.text}")
                return []
                
            data = response.json()
            # Process data to find value bets (simplified logic for now)
            # In a real scenario, we'd compare against a sharp bookmaker or statistical model
            return self._process_player_props(data)

    def _process_player_props(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        props = []
        # Mock logic to extract props - The Odds API structure is complex for props
        # We'll need to parse bookmakers -> markets -> outcomes
        bookmakers = data.get('bookmakers', [])
        for bookmaker in bookmakers:
            for market in bookmaker.get('markets', []):
                if market['key'] == 'player_goal_scorer':
                    for outcome in market['outcomes']:
                        # Simplified: Just return the raw prop for now
                        props.append({
                            "player": outcome['name'],
                            "team": outcome.get('description', 'Unknown'), # Sometimes description holds team
                            "odds": outcome['price'],
                            "bookmaker": bookmaker['title'],
                            "market": "Anytime Goalscorer"
                        })
        return props

    async def get_correct_score_odds(self, sport_key: str, game_id: str) -> List[Dict[str, Any]]:
        """
        Fetch correct score odds for a game.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/sports/{sport_key}/events/{game_id}/odds",
                params={
                    "apiKey": self.api_key,
                    "regions": "uk,eu",
                    "markets": "correct_score",
                    "oddsFormat": "decimal"
                }
            )
            
            if response.status_code != 200:
                return []
                
            data = response.json()
            return self._process_correct_score(data)

    def _process_correct_score(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        scores = []
        bookmakers = data.get('bookmakers', [])
        for bookmaker in bookmakers:
            for market in bookmaker.get('markets', []):
                if market['key'] == 'correct_score':
                    for outcome in market['outcomes']:
                        scores.append({
                            "score": outcome['name'], # e.g., "2-1"
                            "odds": outcome['price'],
                            "bookmaker": bookmaker['title']
                        })
        return scores

    def calculate_parlay_edge(self, bets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate the combined odds and edge for a parlay.
        Assumes independent events.
        """
        combined_odds = 1.0
        combined_true_prob = 1.0
        
        for bet in bets:
            combined_odds *= bet.get('odds', 1.0)
            
            # Use provided true_probability if available, otherwise implied probability
            if 'true_probability' in bet:
                combined_true_prob *= bet['true_probability']
            else:
                # Fallback: Implied probability (no edge assumed)
                combined_true_prob *= (1 / bet.get('odds', 1.0))
            
        # Edge = (True Prob * Odds) - 1
        edge = (combined_true_prob * combined_odds) - 1
        
        return {
            "combined_odds": round(combined_odds, 2),
            "true_probability": round(combined_true_prob, 4),
            "edge_percent": round(edge * 100, 2),
            "legs": len(bets)
        }
