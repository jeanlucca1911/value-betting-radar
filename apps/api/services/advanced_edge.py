"""
Advanced Edge Calculator

Multi-factor edge model that considers:
1. Raw mathematical edge (classical Kelly numerator)
2. Uncertainty penalty (wider CI = require higher edge)
3. Market liquidity (more bookmakers = more reliable)
4. Bookmaker reliability (execution risk)
5. Historical CLV (track record of valueadded)

Returns risk-adjusted edge instead of naive edge.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.bayesian_consensus import BayesianResult


@dataclass
class MarketData:
    """Market liquidity and depth information"""
    bookmakers: List[Dict]  # List of {' bookie': str, 'price': float}
    num_bookmakers: int
    spread_percentage: float  # (max - min) / min
    avg_overround: float  # Average vig across bookmakers


@dataclass
class EdgeAnalysis:
    """Comprehensive edge analysis result"""
    raw_edge: float  # Pure mathematical edge
    risk_adjusted_edge: float  # After all adjustments
    ev_per_dollar: float  # Expected value per $1 bet
    sharpe_ratio: float  # Return / Risk ratio
    
    # Individual components
    uncertainty_penalty: float
    liquidity_factor: float
    fill_probability: float
    
    # Quality assessment
    confidence: str  # A/B/C/D from Bayesian result
    components: Dict[str, float]  # Breakdown of adjustments
    
    @property
    def quality_score(self) -> str:
        """
        Overall quality rating combining edge and confidence
        
        A = Excellent: High edge (>5%), high confidence
        B = Good: Moderate edge (3-5%), good confidence
        C = Fair: Low edge (1-3%), moderate confidence
        D = Poor: Very low edge (<1%) or low confidence
        """
        if self.confidence == 'D':
            return 'D'  # Low confidence = D regardless of edge
        
        if self.risk_adjusted_edge > 0.05:
            return 'A' if self.confidence in ['A', 'B'] else 'B'
        elif self.risk_adjusted_edge > 0.03:
            return 'B' if self.confidence == 'A' else 'C'
        elif self.risk_adjusted_edge > 0.01:
            return 'C'
        else:
            return 'D'


class AdvancedEdgeCalculator:
    """
    Sophisticated edge calculation with risk adjustments
    
    Philosophy: Raw edge is optimistic. Real world has:
    - Uncertainty (can't be 100% sure of true probability)
    - Liquidity risk (will the bet get filled?)
    - Execution risk (will bookmaker honor it?)
    - Alpha decay (edge disappears as sharp money moves in)
    """
    
    def calculate_comprehensive_edge(
        self,
        bet_odds: float,
        true_prob: BayesianResult,
        market_data: MarketData,
        bookie_reliability: float,
        historical_clv: Optional[float] = None
    ) -> EdgeAnalysis:
        """
        Calculate risk-adjusted edge with full component breakdown
        
        Args:
            bet_odds: Decimal odds being offered
            true_prob: Bayesian probability estimate
            market_data: Market liquidity information
            bookie_reliability: 0-1 score for bookmaker quality
            historical_clv: Optional historical closing line value
        
        Returns:
            EdgeAnalysis with all components
        """
        # 1. Raw mathematical edge (Kelly numerator)
        raw_edge = (true_prob.probability * bet_odds) - 1.0
        
        # 2. Uncertainty penalty
        # Higher variance = less confident = require higher edge
        # PHASE 2: Standard penalties for robust model (7,000+ matches)
        uncertainty_penalty = 1.0 * true_prob.std_error
        
        # 3. Market liquidity factor
        liquidity_factor = self._calculate_liquidity_factor(market_data)
        
        # Illiquid markets penalize edge
        # PHASE 2: Standard 1% penalty for mature model
        liquidity_penalty = (1 - liquidity_factor) * 0.01
        
        # 4. Bookmaker fill probability
        # Unreliable bookmakers may not honor large bets
        # Scales from 0.7 (very unreliable) to 1.0 (pinnacle-level)
        fill_probability = 0.7 + (bookie_reliability * 0.3)
        # Positive historical CLV = you've been good at finding value
        # Negative = you've been off (alpha decay)
        if historical_clv is not None:
            clv_adjustment = max(0.5, min(1.5, 1.0 + historical_clv))
        else:
            clv_adjustment = 1.0
        
        # Composite risk-adjusted edge
        risk_adjusted_edge = (
            raw_edge
            - uncertainty_penalty
            - liquidity_penalty
        ) * fill_probability * clv_adjustment
        
        # Expected value per dollar bet
        ev_per_dollar = risk_adjusted_edge
        
        # Sharpe ratio (return / risk)
        # Risk = standard deviation of bet outcome
        bet_variance = (
            true_prob.probability * (bet_odds - 1)**2 +
            (1 - true_prob.probability)
        )
        std_dev = np.sqrt(bet_variance)
        sharpe_ratio = raw_edge / std_dev if std_dev > 0 else 0
        
        # Component breakdown
        components = {
            'mathematics': raw_edge,
            'uncertainty': -uncertainty_penalty,
            'liquidity': -liquidity_penalty,
            'reliability': (fill_probability - 1) * raw_edge,
            'clv': (clv_adjustment - 1) * raw_edge
        }
        
        return EdgeAnalysis(
            raw_edge=raw_edge,
            risk_adjusted_edge=risk_adjusted_edge,
            ev_per_dollar=ev_per_dollar,
            sharpe_ratio=sharpe_ratio,
            uncertainty_penalty=uncertainty_penalty,
            liquidity_factor=liquidity_factor,
            fill_probability=fill_probability,
            confidence=true_prob.confidence_score,
            components=components
        )
    
    def _calculate_liquidity_factor(self, market_data: MarketData) -> float:
        """
        Liquidity score from 0 (illiquid) to 1 (very liquid)
        
        Factors:
        - Number of bookmakers: More = more liquid
        - Spread tightness: Tighter = more efficient
        """
        num_bookies = market_data.num_bookmakers
        spread_pct = market_data.spread_percentage
        
        # Normalize to 10 bookmakers as "very liquid"
        bookie_factor = min(num_bookies / 10, 1.0)
        
        # Tight spread (<5%) = good, wide spread (>20%) = bad
        # Penalty increases with spread width
        spread_factor = max(0, 1.0 - spread_pct * 5)
        
        # Average the two factors
        return (bookie_factor + spread_factor) / 2
    
    def calculate_market_efficiency(
        self,
        all_odds: List[float]
    ) -> float:
        """
        Market efficiency score from 0 (inefficient) to 1 (very efficient)
        
        Efficient market = low variance in odds across bookmakers
        """
        if len(all_odds) < 2:
            return 0.5  # Default if insufficient data
        
        # Convert to implied probabilities
        implied_probs = [1.0 / odds for odds in all_odds]
        
        # Calculate variance
        variance = np.var(implied_probs)
        
        # Lower variance = more efficient
        # Scale: variance < 0.001 = very efficient
        efficiency = 1.0 - min(variance * 1000, 1.0)
        
        return efficiency


# Example usage and testing
if __name__ == "__main__":
    from services.bayesian_consensus import BayesianConsensus, BayesianResult
    
    print("=" * 60)
    print("Advanced Edge Calculator - Test")
    print("=" * 60)
    
    # Mock Bayesian result
    bayesian_result = BayesianResult(
        probability=0.55,
        variance=0.001,
        credible_interval=(0.52, 0.58),
        alpha=55,
        beta=45,
        effective_samples=100
    )
    
    # Mock market data
    market_data = MarketData(
        bookmakers=[
            {'bookie': 'pinnacle', 'price': 1.90},
            {'bookie': 'draftkings', 'price': 1.92},
            {'bookie': 'fanduel', 'price': 1.95},
            {'bookie': 'betmgm', 'price': 1.93},
        ],
        num_bookmakers=4,
        spread_percentage=0.026,  # (1.95 - 1.90) / 1.90 = 2.6%
        avg_overround=0.05
    )
    
    calculator = AdvancedEdgeCalculator()
    
    # Calculate edge for bet at 1.95 odds
    edge_analysis = calculator.calculate_comprehensive_edge(
        bet_odds=1.95,
        true_prob=bayesian_result,
        market_data=market_data,
        bookie_reliability=0.85,  # FanDuel reliability
        historical_clv=0.02  # 2% historical CLV
    )
    
    print(f"\nBet Analysis:")
    print(f"  Odds: 1.95")
    print(f"  True Probability: {bayesian_result.probability:.4f} (55.00%)")
    print(f"  Confidence: {bayesian_result.confidence_score}")
    
    print(f"\nEdge Breakdown:")
    print(f"  Raw Edge: {edge_analysis.raw_edge * 100:.2f}%")
    print(f"  - Uncertainty Penalty: {edge_analysis.uncertainty_penalty * 100:.2f}%")
    print(f"  - Liquidity Penalty: {(1 - edge_analysis.liquidity_factor) * 2:.2f}%")
    print(f"  × Fill Probability: {edge_analysis.fill_probability:.2f}")
    print(f"  Risk-Adjusted Edge: {edge_analysis.risk_adjusted_edge * 100:.2f}%")
    
    print(f"\nQuality Metrics:")
    print(f"  Quality Score: {edge_analysis.quality_score}")
    print(f"  Sharpe Ratio: {edge_analysis.sharpe_ratio:.3f}")
    print(f"  EV per $1: ${edge_analysis.ev_per_dollar:.3f}")
    
    print(f"\nComponent Breakdown:")
    for component, value in edge_analysis.components.items():
        print(f"  {component.capitalize()}: {value * 100:+.2f}%")
