import requests
import json

# Test Railway API with CORRECT endpoint
print("Testing Railway API with correct endpoint...")
print("=" * 60)

try:
    # CORRECT endpoint: /api/v1/odds/live
    response = requests.get(
        'https://value-betting-radar-production.up.railway.app/api/v1/odds/live',
        params={'sport': 'basketball_nba'},
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    print()
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total bets returned: {len(data)}")
        print()
        
        if data:
            print("First 5 value bets:")
            for i, bet in enumerate(data[:5], 1):
                print(f"\n{i}. {bet.get('home_team', 'N/A')} vs {bet.get('away_team', 'N/A')}")
                print(f"   Outcome: {bet.get('outcome', 'N/A')}")
                print(f"   Edge: {bet.get('edge', 0):.4%}")
                print(f"   True Prob: {bet.get('true_probability', {}).get('mean', 0):.4%}")
                print(f"   Bookmaker: {bet.get('bookmaker', 'N/A')}")
                print(f"   Odds: {bet.get('odds', 0)}")
                print(f"   Confidence: {bet.get('confidence_grade', 'N/A')}")
                
            # Count how many have non-zero edges
            non_zero = sum(1 for b in data if b.get('edge', 0) > 0)
            print(f"\n\nBets with edge > 0%: {non_zero} / {len(data)}")
        else:
            print("❌ No bets returned!")
            print("\nThis means:")
            print("1. Either no live games")
            print("2. OR penalties still too aggressive")
            print("3. OR Bayesian model not working")
    else:
        print(f"❌ Error: {response.text[:500]}")
        
except Exception as e:
    print(f"❌ Request failed: {e}")
