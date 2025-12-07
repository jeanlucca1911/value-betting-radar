import requests

# Check live games
r = requests.get(
    'https://api.the-odds-api.com/v4/sports/basketball_nba/odds',
    params={
        'apiKey': 'ef9454de639f0f85998d42d56f5817f8',
        'regions': 'us',
        'markets': 'h2h'
    }
)

print(f"Live NBA games: {len(r.json())}")
for g in r.json()[:5]:
    print(f"  {g['home_team']} vs {g['away_team']}")
