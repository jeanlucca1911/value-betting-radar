import asyncio
import sys
import os

# Add the current directory to sys.path so imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.data_collector import DataCollector

async def main():
    print("Starting manual data collection...")
    collector = DataCollector()
    await collector.collect_all_sports()
    print("Data collection completed.")

if __name__ == "__main__":
    asyncio.run(main())
