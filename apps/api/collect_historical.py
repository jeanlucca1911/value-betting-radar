"""
Historical Odds Collection System

Automated daily snapshots of odds from The Odds API
Stores data for:
- Bayesian prior calculation
- CLV (Closing Line Value) tracking
- Bookmaker accuracy analysis
- Market efficiency scoring
"""

import asyncio
import sqlite3
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional
import os
from pathlib import Path

from services.odds_api import TheOddsApiClient
from core.config import settings


class HistoricalDataCollector:
    """
    Collects and stores historical odds data
    
    Runs daily to:
    1. Snapshot current odds for upcoming matches
    2. Collect closing odds (right before match start)
    3. Collect match results
    """
    
    def __init__(self, db_path: str = "db/historical.db"):
        self.db_path = db_path
        self.api_client = TheOddsApiClient()
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Create database and tables if they don't exist"""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
        
        # Create tables if they don't exist
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Just ensure key tables exist - schema creates them with IF NOT EXISTS
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='matches'")
        if not cursor.fetchone():
            # Database is new, run full schema
            schema_path = Path(__file__).parent / "db" / "schema.sql"
            if schema_path.exists():
                with open(schema_path, 'r') as f:
                    schema = f.read()
                conn.executescript(schema)
                print(f"[OK] Database initialized: {self.db_path}")
            else:
                print(f"Warning: Schema file not found at {schema_path}")
        
        conn.commit()
        conn.close()
    
    async def run_daily_snapshot(
        self, 
        sports: List[str] = None,
        markets: List[str] = None
    ) -> Dict:
        """
        Main daily collection job
        
        Cost: ~20-30 credits (for 4 sports × 1 market)
        """
        if not sports:
            sports = [
                'soccer_epl',
                'soccer_uefa_champions_league',
                'basketball_nba',
                'americanfootball_nfl'
            ]
        
        if not markets:
            markets = ['h2h']  # Start with H2H only
        
        # Create collection run record
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO collection_runs 
            (run_type, start_time, status)
            VALUES ('daily_snapshot', ?, 'running')
        """, (datetime.now(timezone.utc),))
        run_id = cursor.lastrowid
        conn.commit()
        
        total_matches = 0
        total_odds = 0
        total_credits = 0
        
        try:
            for sport in sports:
                for market in markets:
                    result = await self._collect_sport_market(
                        sport=sport,
                        market=market,
                        region='us'
                    )
                    
                    total_matches += result['matches']
                    total_odds += result['odds']
                    total_credits += result['credits']
            
            # Update run record
            cursor.execute("""
                UPDATE collection_runs
                SET end_time = ?,
                    status = 'completed',
                    matches_processed = ?,
                    odds_collected = ?,
                    api_credits_used = ?
                WHERE id = ?
            """, (
                datetime.now(timezone.utc),
                total_matches,
                total_odds,
                total_credits,
                run_id
            ))
            conn.commit()
            
            print(f"""
            [OK] Daily snapshot completed
            Matches: {total_matches}
            Odds collected: {total_odds}
            API credits used: {total_credits}
            """)
            
            return {
                'status': 'success',
                'matches': total_matches,
                'odds': total_odds,
                'credits': total_credits
            }
            
        except Exception as e:
            cursor.execute("""
                UPDATE collection_runs
                SET end_time = ?,
                    status = 'failed',
                    error_message = ?
                WHERE id = ?
            """, (datetime.now(timezone.utc), str(e), run_id))
            conn.commit()
            
            print(f"[ERROR] Collection failed: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
        
        finally:
            conn.close()
    
    async def _collect_sport_market(
        self,
        sport: str,
        market: str,
        region: str = 'us'
    ) -> Dict:
        """Collect odds for one sport/market combination"""
        
        print(f"Collecting {sport} ({market})...")
        
        # Fetch from API
        matches = await self.api_client.get_odds(
            sport=sport,
            regions=region,
            markets=market
        )
        
        if not matches:
            print(f"  No matches found for {sport}")
            return {'matches': 0, 'odds': 0, 'credits': 1}
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        snapshot_time = datetime.now(timezone.utc)
        
        matches_inserted = 0
        odds_inserted = 0
        
        for match in matches:
            # Insert match record
            cursor.execute("""
                INSERT OR IGNORE INTO matches
                (id, sport_key, commence_time, home_team, away_team)
                VALUES (?, ?, ?, ?, ?)
            """, (
                match.id,
                match.sport_key,
                match.commence_time,
                match.home_team,
                match.away_team
            ))
            
            if cursor.rowcount > 0:
                matches_inserted += 1
            
            # Calculate time to event
            # Ensure timezone aware comparison
            commence_tz = match.commence_time.replace(tzinfo=timezone.utc) if match.commence_time.tzinfo is None else match.commence_time
            time_to_event = (commence_tz - snapshot_time).total_seconds() / 3600
            
            # Insert odds snapshots
            for bookmaker in match.bookmakers:
                for mkt in bookmaker.markets:
                    if mkt.key == market:
                        for outcome in mkt.outcomes:
                            cursor.execute("""
                                INSERT INTO odds_snapshots
                                (match_id, bookmaker_key, market_key, outcome_name, 
                                 odds, snapshot_time, time_to_event_hours)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                            """, (
                                match.id,
                                bookmaker.key,
                                mkt.key,
                                outcome.name,
                                outcome.price,
                                snapshot_time,
                                time_to_event
                            ))
                            odds_inserted += 1
        
        conn.commit()
        conn.close()
        
        print(f"  [OK] {sport}: {matches_inserted} matches, {odds_inserted} odds")
        
        return {
            'matches': matches_inserted,
            'odds': odds_inserted,
            'credits': 1  # 1 credit per API call
        }
    
    async def collect_closing_odds(self) -> Dict:
        """
        Collect closing odds for matches starting in next 2 hours
        
        Run this every 30 minutes
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Find matches starting soon that don't have closing odds yet
        cursor.execute("""
            SELECT DISTINCT m.id, m.sport_key
            FROM matches m
            WHERE m.commence_time BETWEEN ? AND ?
            AND m.completed = FALSE
            AND NOT EXISTS (
                SELECT 1 FROM closing_odds co
                WHERE co.match_id = m.id
            )
        """, (
            datetime.now(timezone.utc),
            datetime.now(timezone.utc) + timedelta(hours=2)
        ))
        
        matches_to_close = cursor.fetchall()
        
        if not matches_to_close:
            print("No matches need closing odds")
            return {'status': 'success', 'matches': 0}
        
        print(f"Collecting closing odds for {len(matches_to_close)} matches...")
        
        # For each match, get latest odds
        for match_id, sport_key in matches_to_close:
            # Get latest snapshot for this match
            cursor.execute("""
                SELECT bookmaker_key, market_key, outcome_name, odds, snapshot_time
                FROM odds_snapshots
                WHERE match_id = ?
                AND snapshot_time = (
                    SELECT MAX(snapshot_time)
                    FROM odds_snapshots
                    WHERE match_id = ?
                )
            """, (match_id, match_id))
            
            latest_odds = cursor.fetchall()
            
            # Insert as closing odds
            for bookie, market, outcome, odds, snap_time in latest_odds:
                cursor.execute("""
                    INSERT OR REPLACE INTO closing_odds
                    (match_id, bookmaker_key, market_key, outcome_name, 
                     closing_odds, snapshot_time)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (match_id, bookie, market, outcome, odds, snap_time))
        
        conn.commit()
        conn.close()
        
        print(f"[OK] Closing odds collected for {len(matches_to_close)} matches")
        
        return {
            'status': 'success',
            'matches': len(matches_to_close)
        }
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about collected data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total matches
        cursor.execute("SELECT COUNT(*) FROM matches")
        total_matches = cursor.fetchone()[0]
        
        # Total odds snapshots
        cursor.execute("SELECT COUNT(*) FROM odds_snapshots")
        total_odds = cursor.fetchone()[0]
        
        # Matches by sport
        cursor.execute("""
            SELECT sport_key, COUNT(*)
            FROM matches
            GROUP BY sport_key
        """)
        by_sport = dict(cursor.fetchall())
        
        # Latest collection run
        cursor.execute("""
            SELECT run_type, start_time, status, matches_processed, api_credits_used
            FROM collection_runs
            ORDER BY start_time DESC
            LIMIT 1
        """)
        latest_run = cursor.fetchone()
        
        conn.close()
        
        return {
            'total_matches': total_matches,
            'total_odds_snapshots': total_odds,
            'matches_by_sport': by_sport,
            'latest_run': {
                'type': latest_run[0] if latest_run else None,
                'time': latest_run[1] if latest_run else None,
                'status': latest_run[2] if latest_run else None,
                'matches': latest_run[3] if latest_run else None,
                'credits': latest_run[4] if latest_run else None
            } if latest_run else None
        }


async def main():
    """Test the collector"""
    collector = HistoricalDataCollector()
    
    print("=" * 60)
    print("Historical Odds Collection - Test Run")
    print("=" * 60)
    
    # Run daily snapshot
    result = await collector.run_daily_snapshot()
    
    print("\n" + "=" * 60)
    print("Collection Statistics")
    print("=" * 60)
    
    # Show stats
    stats = collector.get_collection_stats()
    print(f"\nTotal matches: {stats['total_matches']}")
    print(f"Total odds snapshots: {stats['total_odds_snapshots']}")
    print(f"\nBy sport:")
    for sport, count in stats['matches_by_sport'].items():
        print(f"  {sport}: {count} matches")
    
    if stats['latest_run']:
        print(f"\nLatest run:")
        print(f"  Type: {stats['latest_run']['type']}")
        print(f"  Time: {stats['latest_run']['time']}")
        print(f"  Status: {stats['latest_run']['status']}")
        print(f"  Credits used: {stats['latest_run']['credits']}")


if __name__ == "__main__":
    asyncio.run(main())
