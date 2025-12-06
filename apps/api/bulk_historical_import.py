"""
Bulk Historical Data Importer

Fetches historical odds from The Odds API to instantly train the Bayesian model
instead of waiting 30-60 days for daily collection.

Strategy: Smart sampling over 60 days
- Week 1 (recent): 4 snapshots/day  
- Weeks 2-4: 1 snapshot/day
- Months 2-3: 1 snapshot/week

Total cost: ~1,800 credits vs 7,200 for full density
"""

import asyncio
import sqlite3
import httpx
from datetime import datetime, timedelta, timezone
from typing import List, Dict
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.config import settings


class BulkHistoricalImporter:
    """Import historical odds data in bulk"""
    
    def __init__(self):
        self.db_path = Path(__file__).parent / "db" / "historical.db"
        
    async def import_historical_data(self, sports: List[str] = None):
        """
        Import historical data for specified sports
        
        Args:
            sports: List of sport keys. Defaults to main sports.
        """
        if sports is None:
            sports = ['basketball_nba', 'americanfootball_nfl', 'soccer_epl']
        
        print("=" * 60)
        print("BULK HISTORICAL IMPORT")
        print("=" * 60)
        print(f"Sports: {', '.join(sports)}")
        print(f"Strategy: Smart sampling over 60 days")
        print()
        
        total_snapshots = 0
        total_matches = 0
        total_credits = 0
        
        # Create a dedicated HTTP client for all requests
        async with httpx.AsyncClient(timeout=30.0) as client:
            for sport in sports:
                print(f"\n[{sport.upper()}] Importing historical data...")
                
                # Generate sampling schedule
                snapshots = await self._generate_sampling_schedule(sport)
                
                print(f"  Fetching {len(snapshots)} historical snapshots...")
                
                for i, snapshot_time in enumerate(snapshots):
                    try:
                        # Fetch historical odds directly
                        url = f"https://api.the-odds-api.com/v4/historical/sports/{sport}/odds"
                        
                        # Format date with Z suffix (required by API)
                        date_str = snapshot_time.strftime("%Y-%m-%dT%H:%M:%SZ")
                        
                        params = {
                            "apiKey": settings.THE_ODDS_API_KEY,
                            "regions": "us",
                            "markets": "h2h",
                            "oddsFormat": "decimal",
                            "date": date_str
                        }
                        
                        response = await client.get(url, params=params)
                        response.raise_for_status()
                        data = response.json()
                        
                        if data and 'data' in data:
                            events = data['data']
                        elif isinstance(data, list):
                            events = data
                        else:
                            print(f"    No data returned for {snapshot_time}")
                            continue
                            
                        # Store in database
                        stored = await self._store_snapshot(
                            sport=sport,
                            snapshot_time=snapshot_time,
                            events=events
                        )
                        
                        total_matches += len(events)
                        total_snapshots += 1
                        
                        # Track credits (10 per request)
                        total_credits += 10
                        
                        if (i + 1) % 10 == 0:
                            print(f"    Progress: {i + 1}/{len(snapshots)} snapshots, {total_matches} matches so far")
                    
                        # Rate limiting: 1 request per second
                        await asyncio.sleep(1)
                        
                    except Exception as e:
                        print(f"    Error at {snapshot_time}: {e}")
                        continue
                
                print(f"  [SUCCESS] {sport} complete: {total_snapshots} snapshots")
        
        print("\n" + "=" * 60)
        print("IMPORT COMPLETE")
        print("=" * 60)
        print(f"Total matches: {total_matches}")
        print(f"Total snapshots: {total_snapshots}")
        print(f"API credits used: {total_credits}")
        print(f"Database: {self.db_path}")
        print()
        
    async def _generate_sampling_schedule(self, sport: str) -> List[datetime]:
        """
        Generate smart sampling schedule
        
        - Week 1: 4 snapshots/day (6am, 12pm, 6pm, 10pm)
        - Weeks 2-4: 1 snapshot/day (12pm)
        - Months 2-3: 1 snapshot/week (Sunday 12pm)
        """
        schedule = []
        now = datetime.now(timezone.utc)
        
        # Week 1 (last 7 days) - 4 snapshots/day
        for days_ago in range(7):
            date = now - timedelta(days=days_ago)
            for hour in [6, 12, 18, 22]:
                snapshot_time = date.replace(hour=hour, minute=0, second=0, microsecond=0)
                schedule.append(snapshot_time)
        
        # Weeks 2-4 (days 7-28) - 1 snapshot/day at noon
        for days_ago in range(7, 28):
            date = now - timedelta(days=days_ago)
            snapshot_time = date.replace(hour=12, minute=0, second=0, microsecond=0)
            schedule.append(snapshot_time)
        
        # Months 2-3 (days 28-90) - 1 snapshot/week on Sundays
        for weeks_ago in range(4, 13):
            days_ago = weeks_ago * 7
            date = now - timedelta(days=days_ago)
            # Find previous Sunday
            days_since_sunday = date.weekday() + 1 if date.weekday() != 6 else 0
            sunday = date - timedelta(days=days_since_sunday)
            snapshot_time = sunday.replace(hour=12, minute=0, second=0, microsecond=0)
            schedule.append(snapshot_time)
        
        return sorted(schedule, reverse=True)  # Most recent first
    
    async def _store_snapshot(
        self,
        sport: str,
        snapshot_time: datetime,
        events: List[Dict]
    ) -> int:
        """Store snapshot in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stored_count = 0
        
        for event in events:
            try:
                event_id = event['id']
                home_team = event['home_team']
                away_team = event['away_team']
                commence_time = datetime.fromisoformat(event['commence_time'].replace('Z', '+00:00'))
                
                # Insert match if not exists (using 'id' not 'match_id')
                cursor.execute("""
                    INSERT OR IGNORE INTO matches (
                        id, sport_key, home_team, away_team, commence_time
                    ) VALUES (?, ?, ?, ?, ?)
                """, (event_id, sport, home_team, away_team, commence_time))
                
                # Insert odds for all bookmakers
                if 'bookmakers' in event:
                    for bookmaker in event['bookmakers']:
                        bookie_name = bookmaker['key']
                        
                        for market in bookmaker['markets']:
                            if market['key'] == 'h2h':
                                for outcome in market['outcomes']:
                                    cursor.execute("""
                                        INSERT INTO odds_snapshots (
                                            match_id, bookmaker_key, market_key,
                                            outcome_name, odds, snapshot_time
                                        ) VALUES (?, ?, ?, ?, ?, ?)
                                    """, (
                                        event_id,
                                        bookie_name,
                                        'h2h',
                                        outcome['name'],
                                        outcome['price'],
                                        snapshot_time
                                    ))
                
                stored_count += 1
                
            except Exception as e:
                print(f"      Error storing {event.get('id')}: {e}")
                continue
        
        conn.commit()
        conn.close()
        
        return stored_count


async def main():
    """Run bulk import"""
    importer = BulkHistoricalImporter()
    await importer.import_historical_data()


if __name__ == "__main__":
    asyncio.run(main())
