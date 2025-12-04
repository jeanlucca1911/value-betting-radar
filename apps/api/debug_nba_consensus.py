import asyncio
from services.odds_api import TheOddsApiClient
from services.math import PowerMethod
from core.config import settings

async def debug_nba_consensus():
    """Deep dive into NBA consensus calculation"""
    client = TheOddsApiClient()
    
    print("=" * 70)
    print("NBA Consensus Model Debug")
    print("=" * 70)
    
    # Fetch NBA odds
    matches = await client.get_odds(sport="basketball_nba", regions="us", markets="h2h")
    
    if not matches:
        print("No NBA matches found!")
        return
    
    print(f"\nFound {len(matches)} NBA matches\n")
    
    # Analyze first match in detail
    match = matches[0]
    print(f"Analyzing: {match.home_team} vs {match.away_team}")
    print(f"Commence time: {match.commence_time}")
    print(f"\nBookmakers offering odds: {len(match.bookmakers)}")
    
    # Build consensus for this match
    outcome_odds = {}
    
    print("\n" + "-" * 70)
    print("STEP 1: Collecting odds from all bookmakers")
    print("-" * 70)
    
    for bookie in match.bookmakers:
        market = next((m for m in bookie.markets if m.key == "h2h"), None)
        if not market:
            continue
        
        weight = settings.BOOKMAKER_WEIGHTS.get(bookie.key.lower(), settings.BOOKMAKER_WEIGHTS["default"])
        
        print(f"\n{bookie.title} (weight: {weight}):")
        
        for outcome in market.outcomes:
            if outcome.name not in outcome_odds:
                outcome_odds[outcome.name] = []
            outcome_odds[outcome.name].append({"price": outcome.price, "weight": weight})
            print(f"  {outcome.name}: {outcome.price}")
    
    print("\n" + "-" * 70)
    print("STEP 2: Calculating weighted consensus probabilities")
    print("-" * 70)
    
    consensus_probs = {}
    for outcome_name, prices in outcome_odds.items():
        total_weight = sum(p["weight"] for p in prices)
        weighted_sum_prob = sum((1/p["price"]) * p["weight"] for p in prices)
        consensus_probs[outcome_name] = weighted_sum_prob / total_weight
        
        print(f"\n{outcome_name}:")
        print(f"  Implied probs: {[round(1/p['price'], 4) for p in prices]}")
        print(f"  Weights: {[p['weight'] for p in prices]}")
        print(f"  Weighted avg prob: {consensus_probs[outcome_name]:.4f}")
    
    # Normalize
    total_prob = sum(consensus_probs.values())
    true_probs = {k: v/total_prob for k, v in consensus_probs.items()}
    
    print(f"\nTotal implied prob (before normalization): {total_prob:.4f}")
    print(f"Vig: {(total_prob - 1) * 100:.2f}%")
    
    print("\n" + "-" * 70)
    print("STEP 3: TRUE PROBABILITIES (after removing vig)")
    print("-" * 70)
    for outcome_name, prob in true_probs.items():
        print(f"{outcome_name}: {prob:.4f} ({prob * 100:.2f}%)")
    
    print("\n" + "-" * 70)
    print("STEP 4: Looking for value bets (edge > 0.5%)")
    print("-" * 70)
    
    edge_threshold = settings.EDGE_THRESHOLDS["basketball_nba"]
    
    value_bets_found = []
    
    for bookie in match.bookmakers:
        market = next((m for m in bookie.markets if m.key == "h2h"), None)
        if not market:
            continue
        
        for outcome in market.outcomes:
            true_prob = true_probs.get(outcome.name)
            if not true_prob:
                continue
            
            # Skip garbage odds
            if outcome.price > 100.0 or outcome.price < 1.01:
                continue
            
            edge = PowerMethod.calculate_edge(outcome.price, true_prob)
            
            if edge > edge_threshold:
                value_bets_found.append({
                    "bookmaker": bookie.title,
                    "outcome": outcome.name,
                    "odds": outcome.price,
                    "true_prob": true_prob,
                    "edge": edge * 100
                })
                print(f"\n[VALUE FOUND] {bookie.title}")
                print(f"  Outcome: {outcome.name}")
                print(f"  Odds: {outcome.price}")
                print(f"  True Prob: {true_prob:.4f} ({true_prob * 100:.2f}%)")
                print(f"  Edge: {edge * 100:.2f}%")
            else:
                # Show near-misses
                if edge > edge_threshold * 0.5:  # Within 50% of threshold
                    print(f"\n[Near Miss] {bookie.title} - {outcome.name}")
                    print(f"  Odds: {outcome.price}, Edge: {edge * 100:.3f}% (threshold: {edge_threshold * 100}%)")
    
    print("\n" + "=" * 70)
    print(f"RESULT: {len(value_bets_found)} value bets found for this match")
    print("=" * 70)
    
    if not value_bets_found:
        print("\nConclusion:")
        print("- NBA market is extremely efficient")
        print(f"- No bookmaker offering odds with >{edge_threshold * 100}% edge")
        print("- Consider:")
        print("  1. Lower threshold to 0.3% or 0.1%")
        print("  2. Look at player props instead (less efficient)")
        print("  3. Focus on live betting (more volatile)")

if __name__ == "__main__":
    asyncio.run(debug_nba_consensus())
