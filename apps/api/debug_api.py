import asyncio
from services.odds_api import TheOddsApiClient
from core.config import settings

async def main():
    client = TheOddsApiClient()
    
    print(f"Using API Key: {settings.THE_ODDS_API_KEY[:10]}..." if settings.THE_ODDS_API_KEY else "No API Key")
    
    print("\n--- Checking NBA H2H ---")
    nba = await client.get_odds(sport="basketball_nba", regions="us", markets="h2h")
    print(f"NBA Matches Found: {len(nba)}")
    if nba:
        print(f"Sample Match: {nba[0].home_team} vs {nba[0].away_team}")
        print(f"Bookmakers: {[b.title for b in nba[0].bookmakers]}")
        # Check first match odds
        if nba[0].bookmakers:
            bookie = nba[0].bookmakers[0]
            market = next((m for m in bookie.markets if m.key == "h2h"), None)
            if market:
                print(f"Sample Odds ({bookie.title}): {[(o.name, o.price) for o in market.outcomes]}")

    print("\n--- Checking EPL Player Props ---")
    props = await client.get_odds(sport="soccer_epl", regions="uk,eu,us,au", markets="player_goal_scorer_anytime")
    print(f"EPL Prop Matches Found: {len(props)}")
    if props:
        print(f"Sample Match: {props[0].home_team} vs {props[0].away_team}")
        # Print first few outcomes to see if names are real
        if props[0].bookmakers:
            market = next((m for m in props[0].bookmakers[0].markets if m.key == "player_goal_scorer_anytime"), None)
            if market:
                print(f"Sample Players: {[o.name for o in market.outcomes[:5]]}")
    else:
        print("No player props data available!")

    print("\n--- Checking EPL Correct Score ---")
    scores = await client.get_odds(sport="soccer_epl", regions="uk,eu,us,au", markets="correct_score")
    print(f"EPL Score Matches Found: {len(scores)}")
    if scores:
        print(f"Sample Match: {scores[0].home_team} vs {scores[0].away_team}")
        if scores[0].bookmakers:
            market = next((m for m in scores[0].bookmakers[0].markets if m.key == "correct_score"), None)
            if market:
                print(f"Sample Scores: {[o.name for o in market.outcomes[:5]]}")
    else:
        print("No correct score data available!")

if __name__ == "__main__":
    asyncio.run(main())
