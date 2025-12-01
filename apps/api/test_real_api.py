import requests
import sys

API_KEY = "0271fa2d82b80c745f946a8911ced8b7"
BASE_URL = "https://api.the-odds-api.com/v4"

def test_api():
    print("[1/3] Testing API Connection...")
    
    # Test 1: Sports endpoint
    sports_url = f"{BASE_URL}/sports"
    params = {"apiKey": API_KEY}
    
    try:
        res = requests.get(sports_url, params=params)
        if res.status_code == 200:
            sports = res.json()
            print(f"   [OK] Found {len(sports)} sports")
            soccer_sports = [s for s in sports if 'soccer' in s['key'].lower()]
            print(f"   [OK] Found {len(soccer_sports)} soccer leagues")
        else:
            print(f"   [FAIL] Status: {res.status_code}, {res.text}")
            return False
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        return False
    
    # Test 2: Get odds for a soccer league
    print("\n[2/3] Testing Odds Retrieval...")
    
    if not soccer_sports:
        print("   [WARN] No soccer leagues available")
        return False
    
    sport_key = soccer_sports[0]['key']
    print(f"   Testing with: {sport_key}")
    
    odds_url = f"{BASE_URL}/sports/{sport_key}/odds"
    params = {
        "apiKey": API_KEY,
        "regions": "uk,eu",
        "markets": "h2h",
        "oddsFormat": "decimal"
    }
    
    try:
        res = requests.get(odds_url, params=params)
        if res.status_code == 200:
            games = res.json()
            print(f"   [OK] Found {len(games)} live matches")
            if games:
                game = games[0]
                print(f"   Sample: {game['home_team']} vs {game['away_team']}")
                bookmakers = len(game.get('bookmakers', []))
                print(f"   Bookmakers: {bookmakers}")
                
                # Check for remaining requests
                remaining = res.headers.get('x-requests-remaining')
                if remaining:
                    print(f"   API Quota: {remaining} requests remaining")
            else:
                print("   [WARN] No live matches currently")
        else:
            print(f"   [FAIL] Status: {res.status_code}, {res.text}")
            return False
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        return False
    
    # Test 3: Test our backend
    print("\n[3/3] Testing Backend Integration...")
    
    try:
        backend_res = requests.get("http://localhost:8000/api/v1/odds/live")
        if backend_res.status_code == 200:
            data = backend_res.json()
            if isinstance(data, list):
                print(f"   [OK] Backend returning {len(data)} value bets")
                if data:
                    bet = data[0]
                    print(f"   Sample: {bet.get('outcome')} @ {bet.get('odds')} (Edge: {bet.get('edge')}%)")
            else:
                print(f"   [WARN] Unexpected response format")
        else:
            print(f"   [FAIL] Backend error: {backend_res.status_code}")
            return False
    except Exception as e:
        print(f"   [FAIL] Backend not running or error: {e}")
        return False
    
    print("\n[SUCCESS] All tests passed! Real data is flowing.")
    return True

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)
