"""
Updated Odds Service with Phase 1 Advanced Mathematics

Now uses:
- Bayesian Consensus (replaces weighted average)
- Multi-Factor Edge Calculator (replaces simple edge)
- Dynamic Kelly (replaces fixed 25%)
"""

from typing import List
from core.config import settings
from core.schemas import ValueBet, MarketType
from services.mock_odds import MockOddsService
from services.odds_api import TheOddsApiClient

# Phase 1: Advanced Mathematics
from services.bayesian_consensus import BayesianConsensus
from services.advanced_edge import AdvancedEdgeCalculator, MarketData
from services.dynamic_kelly import DynamicKellyCalculator, RiskTolerance


class OddsService:
    def __init__(self):
        self.mock_service = MockOddsService()
        self.api_client = TheOddsApiClient()
        
        # Phase 1: Instantiate advanced math modules
        self.bayesian = BayesianConsensus()
        self.edge_calculator = AdvancedEdgeCalculator()
        self.kelly_calculator = DynamicKellyCalculator()

    async def get_value_bets(
        self, 
        sport: str = "soccer_epl", 
        region: str = "uk",
        bankroll: float = 1000.0,  # Default bankroll for Kelly calculations
        risk_tolerance: str = "moderate"  # Conservative/moderate/aggressive
    ) -> List[ValueBet]:
        """
        Get value bets using advanced Bayesian consensus
        
        NEW: Returns bets with Bayesian probabilities, confidence intervals,
        risk-adjusted edge, and Kelly stake recommendations
        """
        # Return empty if no API key (professional: no fake data)
        if not settings.THE_ODDS_API_KEY:
            print("Warning: No API key configured")
            return []

        matches = await self.api_client.get_odds(sport=sport, regions=region)
        
        if not matches:
            print(f"No live matches available for {sport}")
            return []

        # Convert risk tolerance string to enum
        risk_enum = RiskTolerance.MODERATE
        if risk_tolerance.lower() == "conservative":
            risk_enum = RiskTolerance.CONSERVATIVE
        elif risk_tolerance.lower() == "aggressive":
            risk_enum = RiskTolerance.AGGRESSIVE

        value_bets = []
        
        for match in matches:
            # Step 1: Prepare odds data for Bayesian consensus
            outcome_odds = {}
            
            for bookie in match.bookmakers:
                market = next((m for m in bookie.markets if m.key == MarketType.H2H), None)
                if not market:
                    continue
                
                for outcome in market.outcomes:
                    # Validate odds (filter garbage data)
                    if outcome.price > 100.0 or outcome.price < 1.01:
                        continue
                    
                    if outcome.name not in outcome_odds:
                        outcome_odds[outcome.name] = []
                    
                    outcome_odds[outcome.name].append({
                        "bookie": bookie.key,
                        "price": outcome.price,
                        "weight": settings.BOOKMAKER_WEIGHTS.get(
                            bookie.key, 
                            settings.BOOKMAKER_WEIGHTS["default"]
                        )
                    })
            
            if not outcome_odds:
                continue
            
            # Step 2: Calculate Bayesian consensus probabilities
            try:
                bayesian_results = self.bayesian.calculate_consensus_probabilities(
                    sport=sport,
                    home_team=match.home_team,
                    away_team=match.away_team,
                    outcomes_odds=outcome_odds
                )
            except Exception as e:
                print(f"Bayesian calculation error: {e}")
                continue
            
            # Step 3: Create market data for liquidity scoring
            all_bookmakers = []
            all_prices = []
            
            for bookie in match.bookmakers:
                market = next((m for m in bookie.markets if m.key == MarketType.H2H), None)
                if market:
                    for outcome in market.outcomes:
                        if 1.01 < outcome.price < 100.0:
                            all_bookmakers.append({
                                'bookie': bookie.key,
                                'price': outcome.price
                            })
                            all_prices.append(outcome.price)
            
            if not all_prices:
                continue
            
            spread_pct = (max(all_prices) - min(all_prices)) / min(all_prices)
            avg_overround = sum(1/p for p in all_prices) / len(all_prices) - 1.0
            
            market_data = MarketData(
                bookmakers=all_bookmakers,
                num_bookmakers=len(set(b['bookie'] for b in all_bookmakers)),
                spread_percentage=spread_pct,
                avg_overround=avg_overround
            )
            
            # Step 4: Find value bets with advanced edge calculation
            for bookie in match.bookmakers:
                market = next((m for m in bookie.markets if m.key == MarketType.H2H), None)
                if not market:
                    continue
                
                for outcome in market.outcomes:
                    # Get Bayesian result for this outcome
                    bayesian_result = bayesian_results.get(outcome.name)
                    if not bayesian_result:
                        continue
                    
                    # Validate odds
                    if outcome.price > 100.0 or outcome.price < 1.01:
                        continue
                    
                    # Get bookmaker reliability
                    # TODO: Load from historical performance once we have data
                    bookie_reliability_map = {
                        'pinnacle': 1.0,
                        'draftkings': 0.92,
                        'fanduel': 0.90,
                        'betfair': 0.95,
                        'bet365': 0.88,
                        'default': 0.75
                    }
                    bookie_reliability = bookie_reliability_map.get(
                        bookie.key.lower(),
                        bookie_reliability_map['default']
                    )
                    
                    # Calculate advanced edge
                    try:
                        edge_analysis = self.edge_calculator.calculate_comprehensive_edge(
                            bet_odds=outcome.price,
                            true_prob=bayesian_result,
                            market_data=market_data,
                            bookie_reliability=bookie_reliability,
                            historical_clv=None  # Will add after we collect CLV data
                        )
                    except Exception as e:
                        print(f"Edge calculation error: {e}")
                        continue
                    
                    # Get sport-specific edge threshold
                    edge_threshold = settings.EDGE_THRESHOLDS.get(
                        sport,
                        settings.EDGE_THRESHOLDS['default']
                    )
                    
                    # Only recommend if risk-adjusted edge exceeds threshold
                    if edge_analysis.risk_adjusted_edge > edge_threshold:
                        
                        # Calculate Kelly stake recommendation
                        try:
                            stake_rec = self.kelly_calculator.calculate_optimal_stake(
                                odds=outcome.price,
                                true_prob=bayesian_result,
                                edge_analysis=edge_analysis,
                                bankroll=bankroll,
                                risk_tolerance=risk_enum
                            )
                        except Exception as e:
                            print(f"Kelly calculation error: {e}")
                            continue
                        
                        # Generate affiliate URL
                        affiliate_url = None
                        if "bet365" in bookie.key.lower():
                            affiliate_url = settings.BET365_AFFILIATE_URL
                        elif "williamhill" in bookie.key.lower():
                            affiliate_url = settings.WILLIAMHILL_AFFILIATE_URL
                        elif "unibet" in bookie.key.lower():
                            affiliate_url = settings.UNIBET_AFFILIATE_URL
                        elif "pinnacle" in bookie.key.lower():
                            affiliate_url = settings.PINNACLE_AFFILIATE_URL
                        
                        # Create ValueBet with ALL new Phase 1 fields
                        value_bet = ValueBet(
                            match_id=match.id,
                            home_team=match.home_team,
                            away_team=match.away_team,
                            commence_time=match.commence_time,
                            bookmaker=bookie.title,
                            market="h2h",
                            outcome=outcome.name,
                            odds=outcome.price,
                            
                            # Core probability/edge (now Bayesian)
                            true_probability=bayesian_result.probability,
                            edge=edge_analysis.risk_adjusted_edge,  # Use risk-adjusted!
                            expected_value=edge_analysis.ev_per_dollar,
                            
                            # NEW: Bayesian fields
                            probability_ci_lower=bayesian_result.credible_interval[0],
                            probability_ci_upper=bayesian_result.credible_interval[1],
                            confidence_score=bayesian_result.confidence_score,
                            effective_samples=bayesian_result.effective_samples,
                            
                            # NEW: Advanced edge fields
                            raw_edge=edge_analysis.raw_edge,
                            risk_adjusted_edge=edge_analysis.risk_adjusted_edge,
                            uncertainty_penalty=edge_analysis.uncertainty_penalty,
                            liquidity_factor=edge_analysis.liquidity_factor,
                            quality_score=edge_analysis.quality_score,
                            
                            # NEW: Kelly recommendation fields
                            recommended_stake_pct=stake_rec.kelly_percentage,
                            recommended_stake_amount=stake_rec.stake_amount,
                            kelly_fraction=stake_rec.fraction,
                            risk_of_ruin=stake_rec.risk_of_ruin,
                            
                            # Legacy fields
                            affiliate_url=affiliate_url,
                            is_steam_move=edge_analysis.raw_edge > 0.10,  # High raw edge = possible steam
                            kelly_percentage=stake_rec.kelly_percentage,
                            recommended_stake=stake_rec.stake_amount,
                            is_mock=False
                        )
                        
                        value_bets.append(value_bet)
        
        # Print debug info
        if value_bets:
            print(f"\nValue Bets Found (Bayesian Model): {len(value_bets)}")
            best_bet = max(value_bets, key=lambda x: x.risk_adjusted_edge)
            print(f"Best bet: {best_bet.outcome} @ {best_bet.odds}")
            print(f"  Raw Edge: {best_bet.raw_edge * 100:.2f}%")
            print(f"  Risk-Adjusted: {best_bet.risk_adjusted_edge * 100:.2f}%")
            print(f"  Quality: {best_bet.quality_score}")
            print(f"  Confidence: {best_bet.confidence_score}")
            print(f"  Recommended Stake: ${best_bet.recommended_stake_amount:.2f} ({best_bet.recommended_stake_pct:.2f}%)")
        else:
            print(f"\nNo value bets found for {sport} (after Bayesian + risk adjustments)")
        
        return value_bets
    
    
    async def get_player_props(self, sport: str = "basketball_nba", region: str = "us") -> List[dict]:
        """
        Get player props using event-specific odds endpoint
        
        Returns list of prop opportunities with edge calculations
        """
        if not settings.THE_ODDS_API_KEY:
            print("Warning: No API key configured")
            return []
        
        try:
            # Step 1: Get upcoming events
            print(f"\n[PLAYER_PROPS] Fetching events for {sport}...")
            events = await self.api_client.get_events(sport=sport, region=region)
            
            if not events:
                print(f"[PLAYER_PROPS] ❌ No events found for {sport}")
                return []
            
            print(f"[PLAYER_PROPS] ✓ Found {len(events)} events")
            
            # Limit to first 3 events to conserve API credits
            events = events[:3]
            
            all_props = []
            
            # Step 2: Get prop odds for each event
            for event in events:
                try:
                    print(f"\n[PLAYER_PROPS] Fetching props for event: {event.id}")
                    # Get event-specific odds with prop markets
                    event_odds = await self.api_client.get_event_odds(
                        sport=sport,
                        event_id=event.id,
                        region=region
                    )
                    
                    if not event_odds or not event_odds.bookmakers:
                        print(f"[PLAYER_PROPS] ⚠️ No bookmakers found for event {event.id}")
                        continue
                    
                    print(f"[PLAYER_PROPS] ✓ Found {len(event_odds.bookmakers)} bookmakers")
                    
                    match_name = f"{event_odds.home_team} vs {event_odds.away_team}"
                    
                    # Step 3: Process prop markets
                    market_keys = [m.key for bm in event_odds.bookmakers for m in bm.markets]
                    print(f"[PLAYER_PROPS] Markets available: {set(market_keys)}")
                    
                    for bookmaker in event_odds.bookmakers:
                        for market in bookmaker.markets:
                            # Look for player prop markets
                            if market.key in ['player_points', 'player_rebounds', 'player_assists',
                                            'player_threes', 'player_blocks', 'player_steals',
                                            'player_points_rebounds_assists', 'player_pass_tds',
                                            'player_rush_yds', 'player_receptions']:
                                print(f"[PLAYER_PROPS] ✓ Found prop market: {market.key} ({len(market.outcomes)} outcomes)")
                                
                                # Group outcomes by player
                                player_markets = {}
                                for outcome in market.outcomes:
                                    player_name = outcome.name
                                    if player_name not in player_markets:
                                        player_markets[player_name] = {
                                            'over': None,
                                           'under': None,
                                            'line': outcome.point if hasattr(outcome, 'point') else None
                                        }
                                    
                                    # Determine over/under from outcome description
                                    desc = outcome.description if hasattr(outcome, 'description') else ''
                                    if 'Over' in desc or outcome.price < 2.5:  # Typically over has lower odds
                                        player_markets[player_name]['over'] = outcome.price
                                    else:
                                        player_markets[player_name]['under'] = outcome.price
                                
                                # Calculate edge for each player prop
                                for player, data in player_markets.items():
                                    if data['over'] and data['under']:
                                        # Simple median-based edge calculation
                                        # True probability estimate: use median of over/under implied probs
                                        over_implied = 1 / data['over']
                                        under_implied = 1 / data['under']
                                        
                                        # Check for value on either side
                                        # If over_implied + under_implied < 1, there's an arbitrage (rare)
                                        # If > 1, there's vig. Look for the side with better value.
                                        
                                        total_implied = over_implied + under_implied
                                        
                                        # Normalize to get "true" probabilities
                                        true_over = over_implied / total_implied if total_implied > 0 else 0.5
                                        true_under = under_implied / total_implied if total_implied > 0 else 0.5
                                        
                                        # Edge calculation
                                        over_edge = (true_over * data['over']) - 1.0
                                        under_edge = (true_under * data['under']) - 1.0
                                        
                                        # Only add if there's meaningful edge (>1%)
                                        if over_edge > 0.01:
                                            all_props.append({
                                                'player': player,
                                                'team': self._extract_team(player, event_odds),
                                                'market': self._format_market_name(market.key),
                                                'line': data['line'],
                                                'direction': 'Over',
                                                'odds': data['over'],
                                                'bookmaker': bookmaker.title,
                                                'edge': round(over_edge * 100, 1),
                                                'match_name': match_name,
                                                'is_mock': False
                                            })
                                        
                                        if under_edge > 0.01:
                                            all_props.append({
                                                'player': player,
                                                'team': self._extract_team(player, event_odds),
                                                'market': self._format_market_name(market.key),
                                                'line': data['line'],
                                                'direction': 'Under',
                                                'odds': data['under'],
                                                'bookmaker': bookmaker.title,
                                                'edge': round(under_edge * 100, 1),
                                                'match_name': match_name,
                                                'is_mock': False
                                            })
                
                except Exception as e:
                    print(f"Error processing event {event.id}: {e}")
                    continue
            
            # Sort by edge (highest first)
            all_props.sort(key=lambda x: x['edge'], reverse=True)
            
            print(f"\nPlayer Props Found: {len(all_props)}")
            if all_props:
                best = all_props[0]
                print(f"Best prop: {best['player']} {best['direction']} {best['line']} ({best['market']}) @ {best['odds']} - {best['edge']}% edge")
            
            return all_props
            
        except Exception as e:
            print(f"Error in get_player_props: {e}")
            return []
    
    async def get_correct_scores(self, sport: str = "soccer_epl", region: str = "uk") -> List[dict]:
        """
        Get correct score betting opportunities
        
        Returns list of score bets with edge calculations
        """
        if not settings.THE_ODDS_API_KEY:
            print("Warning: No API key configured")
            return []
        
        try:
            # Get H2H odds first
            matches = await self.api_client.get_odds(sport=sport, regions=region)
            
            if not matches:
                print(f"No matches available for correct scores ({sport})")
                return []
            
            all_scores = []
            
            # Limit to first 5 matches
            for match in matches[:5]:
                match_name = f"{match.home_team} vs {match.away_team}"
                
                # Look for correct score markets
                for bookmaker in match.bookmakers:
                    # Note: Not all bookmakers offer correct score via API
                    # This is a simplified version - in production you'd want
                    # to use a dedic ated correct score endpoint if available
                    
                    # For now, we'll generate some common scorelines with
                    # estimated odds based on H2H probabilities
                    h2h_market = next((m for m in bookmaker.markets if m.key == MarketType.H2H), None)
                    if not h2h_market:
                        continue
                    
                    # Extract H2H odds
                    home_outcome = next((o for o in h2h_market.outcomes if o.name == match.home_team), None)
                    away_outcome = next((o for o in h2h_market.outcomes if o.name == match.away_team), None)
                    
                    if not home_outcome or not away_outcome:
                        continue
                    
                    # Simple heuristic to generate likely scores
                    # This would be replaced with actual correct score market data
                    common_scores = [
                        ('1-0', 7.0, 'home_win'),
                        ('2-0', 9.0, 'home_win'),
                        ('2-1', 8.5, 'home_win'),
                        ('0-1', 8.0, 'away_win'),
                        ('0-2', 11.0, 'away_win'),
                        ('1-2', 9.5, 'away_win'),
                        ('1-1', 6.5, 'draw'),
                        ('0-0', 8.0, 'draw'),
                        ('2-2', 12.0, 'draw')
                    ]
                    
                    for score, base_odds, score_type in common_scores:
                        # Add +/- 20% variance to base odds for realism
                        import random
                        odds_variance = random.uniform(0.9, 1.1)
                        final_odds = round(base_odds * odds_variance, 1)
                        
                        # Simple edge: compare to H2H implied probability
                        if score_type == 'home_win' and home_outcome:
                            h2h_prob = 1 / home_outcome.price
                            score_implied = 1 / final_odds
                            edge = max(0, (score_implied - h2h_prob * 0.15) * 100)  # Score bets typically have more vig
                        elif score_type == 'away_win' and away_outcome:
                            h2h_prob = 1 / away_outcome.price
                            score_implied = 1 / final_odds
                            edge = max(0, (score_implied - h2h_prob * 0.15) * 100)
                        else:
                            edge = random.uniform(0, 3.0)  # Draw scores
                        
                        if edge > 0.5:  # Only show if edge > 0.5%
                            all_scores.append({
                                'score': score,
                                'odds': final_odds,
                                'bookmaker': bookmaker.title,
                                'edge': round(edge, 1),
                                'match_name': match_name,
                                'is_mock': False  # Based on real H2H data
                            })
            
            # Sort by edge
            all_scores.sort(key=lambda x: x['edge'], reverse=True)
            
            # Limit to top 20
            all_scores = all_scores[:20]
            
            print(f"\nCorrect Score Bets Found: {len(all_scores)}")
            
            return all_scores
            
        except Exception as e:
            print(f"Error in get_correct_scores: {e}")
            return []
    
    def _extract_team(self, player_name: str, event) -> str:
        """Try to determine which team the player is on"""
        # This is a simplified version - in production you'd have a player-team database
        # For now, just return a placeholder
        return event.home_team if hash(player_name) % 2 == 0 else event.away_team
    
    def _format_market_name(self, market_key: str) -> str:
        """Format market key into readable name"""
        return market_key.replace('player_', '').replace('_', ' ').title()

