"""
Automated Scheduler for Historical Data Collection

Runs:
- Daily snapshot at 2:00 AM (all sports, H2H market)
- Closing odds collection every 30 minutes

Usage:
    python scheduler.py

Keep running in background to maintain data collection.
"""

import schedule
import time
import asyncio
from datetime import datetime, timezone
from collect_historical import HistoricalDataCollector


def run_daily_collection():
    """Run daily snapshot collection"""
    print(f"\n[{datetime.now(timezone.utc)}] Starting daily collection...")
    try:
        collector = HistoricalDataCollector()
        result = asyncio.run(collector.run_daily_snapshot())
        print(f"Daily collection completed: {result}")
    except Exception as e:
        print(f"Error in daily collection: {e}")


def run_closing_odds():
    """Run closing odds collection"""
    print(f"[{datetime.now(timezone.utc)}] Checking for closing odds...")
    try:
        collector = HistoricalDataCollector()
        result = asyncio.run(collector.collect_closing_odds())
        if result['matches'] > 0:
            print(f"Closing odds collected for {result['matches']} matches")
    except Exception as e:
        print(f"Error in closing odds collection: {e}")


# Schedule jobs
schedule.every().day.at("02:00").do(run_daily_collection)  # 2 AM daily
schedule.every(30).minutes.do(run_closing_odds)  # Every 30 minutes

print("=" * 60)
print("Historical Data Collection Scheduler")
print("=" * 60)
print("\nScheduled jobs:")
print("  - Daily snapshot: 2:00 AM UTC")
print("  - Closing odds: Every 30 minutes")
print("\nScheduler is running. Press Ctrl+C to stop.")
print("=" * 60)

# Run closing odds immediately on startup
print("\nRunning initial closing odds check...")
run_closing_odds()

# Main loop
try:
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
except KeyboardInterrupt:
    print("\n\nScheduler stopped by user.")
