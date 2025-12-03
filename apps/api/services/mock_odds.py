import random
from services.affiliate_urls import get_affiliate_url
from datetime import datetime, timedelta
from typing import List
from core.schemas import Match, Bookmaker, Market, Outcome, MarketType, ValueBet
from services.math import PowerMethod

class MockOddsService:
    def __init__(self):
        self.sports_data = {
            "soccer_epl": {
                "title": "EPL",
                "teams": [
                    "Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton",
                    "Chelsea", "Crystal Palace", "Everton", "Fulham", "Liverpool",
                    "Luton Town", "Man City", "Man Utd", "Newcastle", "Nottm Forest",
                    "Sheffield Utd", "Tottenham", "West Ham", "Wolves"
                ]
            },
            "basketball_nba": {
                "title": "NBA",
                "teams": [
                    "Boston Celtics", "Brooklyn Nets", "New York Knicks", "Philadelphia 76ers", "Toronto Raptors",
                    "Chicago Bulls", "Cleveland Cavaliers", "Detroit Pistons", "Indiana Pacers", "Milwaukee Bucks",
                    "Denver Nuggets", "Minnesota Timberwolves", "Oklahoma City Thunder", "Portland Trail Blazers", "Utah Jazz",
                    "Golden State Warriors", "LA Clippers", "Los Angeles Lakers", "Phoenix Suns", "Sacramento Kings"
                ]
            },
            "americanfootball_nfl": {
                "title": "NFL",
                "teams": [
                    "Arizona Cardinals", "Atlanta Falcons", "Baltimore Ravens", "Buffalo Bills", "Carolina Panthers",
                    "Chicago Bears", "Cincinnati Bengals", "Cleveland Browns", "Dallas Cowboys", "Denver Broncos",
                    "Detroit Lions", "Green Bay Packers", "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars",
                    "Kansas City Chiefs", "Las Vegas Raiders", "Los Angeles Chargers", "Los Angeles Rams", "Miami Dolphins"
                ]
            },
            "mma_mixed_martial_arts": {
                "title": "MMA",
                "teams": [
                    "Jon Jones", "Stipe Miocic", "Islam Makhachev", "Charles Oliveira", "Alex Pereira",
                    "Israel Adesanya", "Sean O'Malley", "Marlon Vera", "Leon Edwards", "Colby Covington"
                ]
            },
            "tennis_atp_wimbledon": {
                "title": "Tennis",
                "teams": [
                    "Novak Djokovic", "Carlos Alcaraz", "Daniil Medvedev", "Jannik Sinner", "Andrey Rublev",
                    "Stefanos Tsitsipas", "Alexander Zverev", "Holger Rune", "Hubert Hurkacz", "Taylor Fritz"
                ]
            },
            "soccer_uefa_champions_league": {
                "title": "Champions League",
                "teams": [
                    "Man City", "Real Madrid", "Bayern Munich", "PSG", "Arsenal",
                    "Barcelona", "Inter Milan", "Atletico Madrid", "Dortmund", "Napoli"
                ]
            }
        }
        
        self.bookmakers = [
            {"key": "pinnacle", "title": "Pinnacle", "is_sharp": True},
            {"key": "bet365", "title": "Bet365", "is_sharp": False},
            {"key": "williamhill", "title": "William Hill", "is_sharp": False},
            {"key": "unibet", "title": "Unibet", "is_sharp": False},
        ]
        self._cache = {} # Keyed by sport
        self._last_update = {} # Keyed by sport
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

    def get_live_matches(self, sport_key: str = "soccer_epl") -> List[Match]:
        # Return cached data if valid
        if sport_key in self._cache and sport_key in self._last_update:
             if datetime.utcnow() - self._last_update[sport_key] < self._cache_duration:
                return self._cache[sport_key]

        sport_info = self.sports_data.get(sport_key, self.sports_data["soccer_epl"])
        teams = sport_info["teams"]
        
        matches = []
        # Generate fewer matches for individual sports to avoid duplicates if list is small
        num_matches = 3 if len(teams) < 10 else 5
        
        for i in range(num_matches):
            home, away = random.sample(teams, 2)
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
                
                # For 2-way sports (Tennis, MMA, etc.), remove Draw if needed, 
                # but for simplicity in mock we keep 3-way or just ignore draw logic for now.
                # A better mock would check sport type.
                
                match_bookmakers.append(Bookmaker(
                    key=bookie["key"],
                    title=bookie["title"],
                    last_update=datetime.utcnow(),
                    markets=[Market(key=MarketType.H2H, outcomes=outcomes)]
                ))

            matches.append(Match(
                id=match_id,
                sport_key=sport_key,
                sport_title=sport_info["title"],
                commence_time=datetime.utcnow() + timedelta(hours=random.randint(1, 24)),
                home_team=home,
                away_team=away,
                bookmakers=match_bookmakers
            ))
        
        self._cache[sport_key] = matches
        self._last_update[sport_key] = datetime.utcnow()
        return matches

    def find_value_bets(self, sport: str = "soccer_epl", region: str = "uk") -> List[ValueBet]:
        matches = self.get_live_matches(sport_key=sport)
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
                            affiliate_url=get_affiliate_url(bookie.title),
                            is_mock=True
                        ))
        
        return sorted(value_bets, key=lambda x: x.edge, reverse=True)

    def get_player_props(self, sport: str = "soccer_epl", region: str = "uk") -> List[dict]:
        # Mock player props
        sport_info = self.sports_data.get(sport, self.sports_data["soccer_epl"])
        teams = sport_info["teams"]
        
        props = []
        players = ["Star Player A", "Striker B", "Winger C", "Midfielder D"]
        
        for _ in range(10):
            team = random.choice(teams)
            player = f"{random.choice(players)} ({team})"
            odds = round(random.uniform(1.8, 4.5), 2)
            edge = round(random.uniform(2.0, 15.0), 1)
            
            props.append({
                "player": player,
                "team": team,
                "market": "Anytime Goalscorer",
                "odds": odds,
                "bookmaker": random.choice(self.bookmakers)["title"],
                "edge": edge,
                "match_name": f"{team} vs {random.choice(teams)}"
            })
            
        return sorted(props, key=lambda x: x["edge"], reverse=True)

    def get_correct_scores(self, sport: str = "soccer_epl", region: str = "uk") -> List[dict]:
        # Mock correct scores
        scores_list = ["1-0", "2-0", "2-1", "1-1", "0-0", "0-1", "1-2"]
        scores = []
        
        for _ in range(10):
            score = random.choice(scores_list)
            odds = round(random.uniform(5.0, 15.0), 2)
            edge = round(random.uniform(5.0, 25.0), 1)
            
            scores.append({
                "score": score,
                "odds": odds,
                "bookmaker": random.choice(self.bookmakers)["title"],
                "edge": edge,
                "match_name": "Mock Match"
            })
            
        return sorted(scores, key=lambda x: x["edge"], reverse=True)
