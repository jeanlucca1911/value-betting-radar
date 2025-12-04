import asyncio
from services.odds_api import TheOddsApiClient

async def test_event_specific_endpoint():
    """Test fetching player props for NBA"""
    client = TheOddsApiClient()
    
    print("=" * 70)
    print("Testing Event-Specific Endpoint (Player Props)")
    print("=" * 70)
    
    # Step 1: Get events
    print("\nStep 1: Fetching NBA events (FREE - 0 credits)...")
    events = await client.get_events(sport="basketball_nba")
    
    if not events:
        print("No events found!")
        return
    
    print(f"Found {len(events)} events")
    
    # Step 2: Get player props for first event
    event = events[0]
    print(f"\nStep 2: Fetching player props for: {event['home_team']} vs {event['away_team']}")
    print(f"Event ID: {event['id']}")
    
    # Test with player_points market
    match_data = await client.get_event_odds(
        sport="basketball_nba",
        event_id=event['id'],
        regions="us",
        markets="player_points"
    )
    
    if not match_data:
        print("\nNo player props found!")
        print("This could mean:")
        print("1. Event hasn't opened props yet")
        print("2. Market key is wrong")
        print("3. Region doesn't support this market")
        return
    
    print(f"\n✓ Got player props data!")
    print(f"Bookmakers: {len(match_data.bookmakers)}")
    
    # Display sample props
    for bookie in match_data.bookmakers[:3]:  # First 3 bookmakers
        print(f"\n{bookie.title}:")
        for market in bookie.markets:
            print(f"  Market: {market.key}")
            print(f"  Props: {len(market.outcomes)}")
            if market.outcomes:
                for prop in market.outcomes[:5]:  # First 5 props
                    print(f"    {prop.name}: {prop.price}")
    
    print("\n" + "=" * 70)
    print("SUCCESS: Event-specific endpoint working!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(test_event_specific_endpoint())
