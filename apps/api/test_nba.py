import asyncio
from services.odds_service import OddsService

async def test_nba_value_detection():
    """Test NBA value bet detection with new weights and thresholds"""
    service = OddsService()
    
    print("=" * 60)
    print("Testing NBA Value Detection")
    print("=" * 60)
    
    # Test NBA
    nba_bets = await service.get_value_bets(sport="basketball_nba", region="us")
    
    print(f"\n[OK] NBA Results: {len(nba_bets)} value bets found")
    
    if nba_bets:
        print("\nTop 10 NBA Value Bets:")
        for i, bet in enumerate(nba_bets[:10], 1):
            print(f"\n{i}. {bet.home_team} vs {bet.away_team}")
            print(f"   Outcome: {bet.outcome}")
            print(f"   Bookmaker: {bet.bookmaker}")
            print(f"   Odds: {bet.odds}")
            print(f"   True Prob: {bet.true_probability:.2%}")
            print(f"   Edge: {bet.edge}%")
            print(f"   Kelly: {bet.kelly_percentage}% (${bet.recommended_stake})")
    else:
        print("\n[!] No NBA value bets found")
        print("Debugging info:")
        print("1. Edge threshold for NBA: 0.5%")
        print("2. Sharp bookmaker weights: DraftKings (3.5), FanDuel (3.0)")
        print("3. This means the market is VERY efficient (no edges > 0.5%)")
        print("4. OR the consensus model is filtering everything out")
        print("\nNext steps:")
        print("- Check raw odds to see if there's variance")
        print("- May need to lower NBA threshold to 0.3% or even 0.1%")
        print("- Or adjust bookmaker weights further")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(test_nba_value_detection())
