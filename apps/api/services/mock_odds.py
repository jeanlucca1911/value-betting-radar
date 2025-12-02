import random
from services.affiliate_urls import get_affiliate_url
from datetime import datetime, timedelta
from typing import List
from core.schemas import Match, Bookmaker, Market, Outcome, MarketType, ValueBet
from services.math import PowerMethod

class MockOddsService:
    def __init__(self):
        self.teams = [
            "Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton",
            "Chelsea", "Crystal Palace", "Everton", "Fulham", "Liverpool",
            "Luton Town", "Man City", "Man Utd", "Newcastle", "Nottm Forest",
            "Sheffield Utd", "Tottenham", "West Ham", "Wolves"
        ]
        self.bookmakers = [
            {"key": "pinnacle", "title": "Pinnacle", "is_sharp": True},
            {"key": "bet365", "title": "Bet365", "is_sharp": False},
            {"key": "williamhill", "title": "William Hill", "is_sharp": False},
            {"key": "unibet", "title": "Unibet", "is_sharp": False},
        ]
        self._cache = None
        self._last_update = None
        self._cache_duration = timedelta(minutes=5)

    def _generate_odds(self, is_sharp: bool) -> List[float]:
        # Generate base probabilities summing to ~1
        p1 = random.uniform(0.1, 0.8)
        p2 = random.uniform(0.1, 0.9 - p1)
        p3 = 1.0 - p1 - p2
        
        probs = [p1, p2, p3]
        
        # Add margin (vig)
        margin = 0.025 if is_sharp else 0.06
        vig_probs = [p / (1 - margin) for p in probs]
        
        # Convert to odds
        return [round(1 / p, 2) for p in vig_probs]

    def get_live_matches(self) -> List[Match]:
        # Return cached data if valid
        if self._cache and self._last_update and datetime.utcnow() - self._last_update < self._cache_duration:
            return self._cache

        matches = []
        for i in range(5):
            home, away = random.sample(self.teams, 2)
            match_id = f"match_{i}_{home}_{away}".replace(" ", "").lower()
            
            match_bookmakers = []
            
            # Generate Pinnacle odds first (Sharp)
            sharp_odds = self._generate_odds(is_sharp=True)
            
            for bookie in self.bookmakers:
                if bookie["is_sharp"]:
                    odds = sharp_odds
                else:
                    # Soft books deviate slightly
                    deviation = [random.uniform(0.95, 1.05) for _ in range(3)]
                    odds = [round(o * d, 2) for o, d in zip(sharp_odds, deviation)]

                outcomes = [
                    Outcome(name=home, price=odds[0]),
                    Outcome(name="Draw", price=odds[1]),
                    Outcome(name=away, price=odds[2]),
                ]
                
                match_bookmakers.append(Bookmaker(
                    key=bookie["key"],
                    title=bookie["title"],
                    last_update=datetime.utcnow(),
                    markets=[Market(key=MarketType.H2H, outcomes=outcomes)]
                ))

            matches.append(Match(
                id=match_id,
                sport_key="soccer_epl",
                sport_title="EPL",
                commence_time=datetime.utcnow() + timedelta(hours=random.randint(1, 24)),
                home_team=home,
                away_team=away,
                bookmakers=match_bookmakers
            ))
        
        self._cache = matches
        self._last_update = datetime.utcnow()
        return matches

    def find_value_bets(self) -> List[ValueBet]:
        matches = self.get_live_matches()
        value_bets = []

        for match in matches:
            # Find sharp bookmaker (Pinnacle)
            pinnacle = next((b for b in match.bookmakers if b.key == "pinnacle"), None)
            if not pinnacle:
                continue
                
            pinnacle_market = next((m for m in pinnacle.markets if m.key == MarketType.H2H), None)
            if not pinnacle_market:
                continue

            # Calculate true probabilities
            sharp_odds = [o.price for o in pinnacle_market.outcomes]
            true_probs = PowerMethod.calculate_true_probabilities(sharp_odds)
            
            if not true_probs:
                continue

            # Compare with soft books
            for bookie in match.bookmakers:
                if bookie.key == "pinnacle":
                    continue
                    
                market = next((m for m in bookie.markets if m.key == MarketType.H2H), None)
                if not market:
                    continue

                for i, outcome in enumerate(market.outcomes):
                    edge = PowerMethod.calculate_edge(outcome.price, true_probs[i])
                    
                    if edge > 0.01: # 1% edge threshold
                        value_bets.append(ValueBet(
                            match_id=match.id,
                            home_team=match.home_team,
                            away_team=match.away_team,
                            commence_time=match.commence_time,
                            bookmaker=bookie.title,
                            market="Head to Head",
                            outcome=outcome.name,
                            odds=outcome.price,
                            true_probability=round(true_probs[i], 4),
                            edge=round(edge * 100, 2), # Percentage
                            expected_value=round(edge * 100, 2),
                            affiliate_url=get_affiliate_url(bookie.title)
                        ))
        
        return sorted(value_bets, key=lambda x: x.edge, reverse=True)
