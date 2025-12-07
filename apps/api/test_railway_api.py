import requests
import json

# Test Railway API directly
print("Testing Railway API...")
print("=" * 60)

try:
    response = requests.get(
        'https://value-betting-radar-production.up.railway.app/api/odds/value-bets',
        params={'sport': 'basketball_nba'},
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print()
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total bets returned: {len(data)}")
        print()
        
        if data:
            print("First 3 bets:")
            for i, bet in enumerate(data[:3], 1):
                print(f"\n{i}. {bet.get('home_team', 'N/A')} vs {bet.get('away_team', 'N/A')}")
                print(f"   Edge: {bet.get('edge', 0):.4%}")
                print(f"   True Prob: {bet.get('true_probability', 0):.4%}")
                print(f"   Bookmaker: {bet.get('bookmaker', 'N/A')}")
                print(f"   Odds: {bet.get('odds', 0)}")
                print(f"   Confidence: {bet.get('confidence', 'N/A')}")
        else:
            print("No bets returned!")
            print("\nPossible reasons:")
            print("1. No live games currently")
            print("2. All edges filtered out by penalties")
            print("3. Bayesian model not initializing")
    else:
        print(f"Error: {response.text[:500]}")
        
except Exception as e:
    print(f"Request failed: {e}")
