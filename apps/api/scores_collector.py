"""
Scores Collector

Fetches actual match results from The Odds API to train the Bayesian model
with real outcomes instead of just odds.

Uses the /scores endpoint which is FREE (doesn't count against quota!)
"""

import asyncio
import sqlite3
from datetime import datetime, timezone
from typing import List, Dict
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from services.odds_api import TheOddsApiClient
from core.config import settings


class ScoresCollector:
    """Collect actual match results"""
    
    def __init__(self):
        self.api_client = TheOddsApiClient(api_key=settings.THE_ODDS_API_KEY)
        self.db_path = Path(__file__).parent / "db" / "historical.db"
        
    async def collect_scores(self, sports: List[str] = None, days_from: int = 3):
        """
        Collect match scores for recent games
        
        Args:
            sports: List of sport keys
            days_from: How many days back to fetch (max 3)
        """
        if sports is None:
            sports = ['basketball_nba', 'americanfootball_nfl', 'soccer_epl']
        
        print("=" * 60)
        print("SCORES COLLECTION")
        print("=" * 60)
        print(f"Sports: {', '.join(sports)}")
        print(f"Looking back: {days_from} days")
        print()
        
        total_updated = 0
        
        for sport in sports:
            print(f"\n📊 Fetching {sport} scores...")
            
            try:
                # Fetch scores (FREE endpoint!)
                response = await self.api_client._make_request(
                    f"/v4/sports/{sport}/scores",
                    params={
                        "daysFrom": days_from
                    }
                )
                
                if response and isinstance(response, list):
                    completed_games = [g for g in response if g.get('completed', False)]
                    
                    print(f"  Found {len(completed_games)} completed games")
                    
                    # Store results
                    updated = await self._store_results(sport, completed_games)
                    total_updated += updated
                    
                    print(f"  ✅ Updated {updated} matches")
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")
                continue
        
        print("\n" + "=" * 60)
        print(f"Total matches updated: {total_updated}")
        print("=" * 60)
        print()
        
    async def _store_results(self, sport: str, games: List[Dict]) -> int:
        """Store match results in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Ensure match_results table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS match_results (
                match_id TEXT PRIMARY KEY,
                sport_key TEXT,
                home_team TEXT,
                away_team TEXT,
                home_score INTEGER,
                away_score INTEGER,
                winner TEXT,
                completed BOOLEAN,
                completed_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        updated_count = 0
        
        for game in games:
            try:
                match_id = game['id']
                home_team = game['home_team']
                away_team = game['away_team']
                
                scores = game.get('scores', [])
                if len(scores) < 2:
                    continue
                
                # Find home and away scores
                home_score = None
                away_score = None
                
                for score in scores:
                    if score['name'] == home_team:
                        home_score = int(score['score'])
                    elif score['name'] == away_team:
                        away_score = int(score['score'])
                
                if home_score is None or away_score is None:
                    continue
                
                # Determine winner
                if home_score > away_score:
                    winner = 'home'
                elif away_score > home_score:
                    winner = 'away'
                else:
                    winner = 'draw'
                
                completed_at = datetime.now(timezone.utc)
                
                # Insert or update
                cursor.execute("""
                    INSERT OR REPLACE INTO match_results (
                        match_id, sport_key, home_team, away_team,
                        home_score, away_score, winner, completed, completed_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    match_id, sport, home_team, away_team,
                    home_score, away_score, winner, True, completed_at
                ))
                
                updated_count += 1
                
            except Exception as e:
                print(f"    Error storing result for {game.get('id')}: {e}")
                continue
        
        conn.commit()
        conn.close()
        
        return updated_count


async def main():
    """Run scores collection"""
    collector = ScoresCollector()
    await collector.collect_scores(days_from=3)


if __name__ == "__main__":
    asyncio.run(main())
