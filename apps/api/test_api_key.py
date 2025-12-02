import httpx
import asyncio
import os

API_KEY = "0271fa2d82b80c745f946a8911ced8b7"

async def test_api():
    print(f"Testing API Key: {API_KEY}")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.the-odds-api.com/v4/sports/soccer_epl/odds",
            params={
                "apiKey": API_KEY,
                "regions": "uk,eu",
                "markets": "h2h",
                "oddsFormat": "decimal",
            }
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Found {len(data)} matches.")
            print("Sample match:", data[0]['home_team'] if data else "No matches")
        else:
            print(f"Error: {response.text}")

if __name__ == "__main__":
    asyncio.run(test_api())
