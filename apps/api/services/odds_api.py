import httpx
from typing import List, Optional
from core.config import settings
from core.schemas import Match, Bookmaker, Market, Outcome, MarketType
from datetime import datetime

import json
from db.redis import get_redis

class TheOddsApiClient:
    BASE_URL = "https://api.the-odds-api.com/v4"

    def __init__(self):
        self.api_key = settings.THE_ODDS_API_KEY
        self.client = httpx.AsyncClient(base_url=self.BASE_URL, timeout=10.0)


    async def get_odds(self, sport: str = "soccer_epl", regions: str = "uk,eu", markets: str = "h2h") -> List[Match]:
        if not self.api_key:
            print("Warning: No API key provided for The Odds API.")
            return []

        # Try cache first
        redis = await get_redis()
        cache_key = f"odds:{sport}:{regions}:{markets}"
        
        if redis:
            try:
                cached_data = await redis.get(cache_key)
                if cached_data:
                    print(f"Using cached odds for {cache_key}")
                    data = json.loads(cached_data)
                    return self._parse_matches(data, markets)
            except Exception as e:
                print(f"Redis error: {e}")

        try:
            print(f"Fetching fresh odds from API for {sport} ({markets})...")
            response = await self.client.get(
                f"/sports/{sport}/odds",
                params={
                    "apiKey": self.api_key,
                    "regions": regions,
                    "markets": markets,
                    "oddsFormat": "decimal",
                }
            )
            response.raise_for_status()
            data = response.json()
            
            # Cache the raw response data
            if redis and data:
                try:
                    await redis.setex(
                        cache_key,
                        settings.ODDS_CACHE_MINUTES * 60,
                        json.dumps(data)
                    )
                except Exception as e:
                    print(f"Failed to cache odds: {e}")

            return self._parse_matches(data)
        except Exception as e:
            print(f"Error fetching odds: {e}")
            return []

    def _parse_matches(self, data: List[dict]) -> List[Match]:
        matches = []
        for item in data:
            try:
                bookmakers = []
                for bookie in item.get("bookmakers", []):
                    markets = []
                    for market in bookie.get("markets", []):
                        outcomes = [
                            Outcome(name=o["name"], price=o["price"])
                            for o in market.get("outcomes", [])
                        ]
                        markets.append(Market(
                            key=MarketType.H2H, # Assuming h2h for now
                            outcomes=outcomes
                        ))
                    
                    bookmakers.append(Bookmaker(
                        key=bookie["key"],
                        title=bookie["title"],
                        last_update=datetime.fromisoformat(bookie["last_update"].replace("Z", "+00:00")),
                        markets=markets
                    ))

                matches.append(Match(
                    id=item["id"],
                    sport_key=item["sport_key"],
                    sport_title=item["sport_title"],
                    commence_time=datetime.fromisoformat(item["commence_time"].replace("Z", "+00:00")),
                    home_team=item["home_team"],
                    away_team=item["away_team"],
                    bookmakers=bookmakers
                ))
            except Exception as e:
                print(f"Error parsing match {item.get('id')}: {e}")
                continue
        return matches

    async def close(self):
        await self.client.aclose()
