import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from db.session import SessionLocal
from db.models.historical import HistoricalMatch, HistoricalOdds
from services.odds_api import TheOddsApiClient
from core.config import settings

class DataCollector:
    def __init__(self):
        self.api_client = TheOddsApiClient()
        self.db = SessionLocal()

    async def collect_odds(self, sport_key: str = "soccer_epl", regions: str = "uk,eu,us"):
        """
        Fetches current odds for a sport and saves them to the historical database.
        """
        print(f"Starting data collection for {sport_key}...")
        try:
            matches = await self.api_client.get_odds(sport=sport_key, regions=regions)
            
            if not matches:
                print(f"No matches found for {sport_key}.")
                return

            for match_data in matches:
                # 1. Update or Create Match
                match = self.db.query(HistoricalMatch).filter(HistoricalMatch.id == match_data.id).first()
                if not match:
                    match = HistoricalMatch(
                        id=match_data.id,
                        sport_key=match_data.sport_key,
                        sport_title=match_data.sport_title,
                        home_team=match_data.home_team,
                        away_team=match_data.away_team,
                        commence_time=match_data.commence_time
                    )
                    self.db.add(match)
                    self.db.commit() # Commit to get ID if needed (though ID is string here)
                
                # 2. Save Odds Snapshots
                for bookmaker in match_data.bookmakers:
                    for market in bookmaker.markets:
                        for outcome in market.outcomes:
                            odds_entry = HistoricalOdds(
                                match_id=match.id,
                                bookmaker=bookmaker.title,
                                market_key=market.key,
                                outcome_name=outcome.name,
                                price=outcome.price,
                                timestamp=datetime.utcnow()
                            )
                            self.db.add(odds_entry)
            
            self.db.commit()
            print(f"Successfully saved data for {len(matches)} matches in {sport_key}.")

        except Exception as e:
            print(f"Error collecting data for {sport_key}: {e}")
            self.db.rollback()
        finally:
            self.db.close()

    async def collect_all_sports(self):
        """
        Collects data for all configured sports.
        """
        sports = [
            "soccer_epl",
            "basketball_nba",
            "americanfootball_nfl",
            "mma_mixed_martial_arts",
            "tennis_atp_wimbledon"
        ]
        
        for sport in sports:
            await self.collect_odds(sport_key=sport)

# For manual execution
if __name__ == "__main__":
    collector = DataCollector()
    asyncio.run(collector.collect_all_sports())
