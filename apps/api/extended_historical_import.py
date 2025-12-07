"""
Extended Historical Import - Add More Training Data

Now that we have 60 days, let's go for 90+ days to maximize model accuracy.

Strategy:
- Already have: 60 days (smart sampling)
- Add now: Days 61-180 (6 months total)
- Sampling: 1 snapshot per week for months 3-6

Cost: ~300-400 more credits (well within budget)
"""

import asyncio
import sqlite3
import httpx
from datetime import datetime, timedelta, timezone
from typing import List, Dict
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.config import settings


class ExtendedHistoricalImporter:
    """Add 90 more days of historical data"""
    
    def __init__(self):
        self.db_path = Path(__file__).parent / "db" / "historical.db"
        
    async def import_extended_data(self, sports: List[str] = None):
        """Import months 3-6 of historical data"""
        if sports is None:
            sports = ['basketball_nba', 'americanfootball_nfl', 'soccer_epl']
        
        print("=" * 60)
        print("EXTENDED HISTORICAL IMPORT (Months 3-6)")
        print("=" * 60)
        print(f"Sports: {', '.join(sports)}")
        print(f"Adding: 90 more days (4 months total)")
        print()
        
        total_snapshots = 0
        total_credits = 0
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            for sport in sports:
                print(f"\n[{sport.upper()}] Extending historical coverage...")
                
                # Generate schedule for days 61-180 (weekly snapshots)
                snapshots = await self._generate_extended_schedule()
                
                print(f"  Fetching {len(snapshots)} additional snapshots...")
                
                for i, snapshot_time in enumerate(snapshots):
                    try:
                        url = f"https://api.the-odds-api.com/v4/historical/sports/{sport}/odds"
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
                        
                        events = data if isinstance(data, list) else data.get('data', [])
                        
                        if events:
                            await self._store_snapshot(sport, snapshot_time, events)
                            total_snapshots += 1
                            total_credits += 10
                            
                            if (i + 1) % 5 == 0:
                                print(f"    Progress: {i + 1}/{len(snapshots)} snapshots")
                        
                        await asyncio.sleep(1)
                        
                    except Exception as e:
                        print(f"    Error at {snapshot_time}: {e}")
                        continue
                
                print(f"  [SUCCESS] {sport} extended: +{total_snapshots} snapshots")
        
        print("\n" + "=" * 60)
        print("EXTENDED IMPORT COMPLETE")
        print("=" * 60)
        print(f"Additional snapshots: {total_snapshots}")
        print(f"API credits used: {total_credits}")
        print(f"Database: {self.db_path}")
        print()
    
    async def _generate_extended_schedule(self) -> List[datetime]:
        """Generate weekly snapshots for days 61-180"""
        schedule = []
        now = datetime.now(timezone.utc)
        
        # Days 61-180: Weekly snapshots on Sundays at noon
        for weeks_ago in range(9, 26):  # Weeks 9-25 (months 3-6)
            days_ago = weeks_ago * 7
            date = now - timedelta(days=days_ago)
            # Find previous Sunday
            days_since_sunday = date.weekday() + 1 if date.weekday() != 6 else 0
            sunday = date - timedelta(days=days_since_sunday)
            snapshot_time = sunday.replace(hour=12, minute=0, second=0, microsecond=0)
            schedule.append(snapshot_time)
        
        return sorted(schedule, reverse=True)
    
    async def _store_snapshot(self, sport: str, snapshot_time: datetime, events: List[Dict]) -> int:
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
                
                cursor.execute("""
                    INSERT OR IGNORE INTO matches (
                        id, sport_key, home_team, away_team, commence_time
                    ) VALUES (?, ?, ?, ?, ?)
                """, (event_id, sport, home_team, away_team, commence_time))
                
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
                continue
        
        conn.commit()
        conn.close()
        
        return stored_count


async def main():
    """Run extended import"""
    importer = ExtendedHistoricalImporter()
    await importer.import_extended_data()


if __name__ == "__main__":
    asyncio.run(main())
