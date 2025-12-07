"""Quick test of historical API with correct date format"""
import httpx
import asyncio
from datetime import datetime, timezone

async def test_historical():
    # Test with proper date formatting
    test_date = "2024-12-01T12:00:00Z"  
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        url = "https://api.the-odds-api.com/v4/historical/sports/basketball_nba/odds"
        params = {
            "apiKey": "ef9454de639f0f85998d42d56f5817f8",
            "regions": "us",
            "markets": "h2h",
            "date": test_date
        }
        
        print(f"Testing: {url}")
        print(f"Date: {test_date}")
        print()
        
        try:
            response = await client.get(url, params=params)
            print(f"Status: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            print()
            
            if response.status_code == 200:
                data = response.json()
                print(f"SUCCESS! Got {len(data) if isinstance(data, list) else 'data'}")
                if isinstance(data, list) and len(data) > 0:
                    print(f"First event: {data[0].get('home_team')} vs {data[0].get('away_team')}")
            else:
                print(f"Error response: {response.text[:500]}")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_historical())
