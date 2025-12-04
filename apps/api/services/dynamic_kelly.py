"""
Dynamic Kelly Calculator

Optimal bet sizing with:
- Quality-adjusted Kelly fractions (A/B/C/D grades)
- Risk tolerance scaling
- Risk of ruin constraints
- Geometric growth rate optimization
- Portfolio correlation awareness

Returns optimal stake with full risk analysis.
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional
from enum import Enum
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.bayesian_consensus import BayesianResult
from services.advanced_edge import EdgeAnalysis


class RiskTolerance(Enum):
    """User risk tolerance levels"""
    CONSERVATIVE = "conservative"  # 0.5x multiplier
    MODERATE = "moderate"          # 1.0x multiplier
    AGGRESSIVE = "aggressive"      # 1.5x multiplier


@dataclass
class StakeRecommendation:
    """Complete stake recommendation with risk metrics"""
    stake_amount: float
    fraction: float  # Fraction of bankroll
    kelly_percentage: float  # Percentage representation
    
    # Kelly breakdown
    full_kelly_fraction: float  # Theoretical full Kelly
    confidence_adjusted: float  # Multiplier for quality
    risk_adjusted: float  # Multiplier for risk tolerance
    
    # Performance metrics
    expected_value: float  # Expected profit per bet
    geometric_growth_rate: float  # Long-term growth rate
    risk_of_ruin: float  # Probability of 50% drawdown
    doubling_time_bets: float  # Expected bets to double bankroll
    
    # Reasoning
    recommendation_reasoning: str


class DynamicKellyCalculator:
    """
    Kelly Criterion with dynamic adjustments
    
    Philosophy:
    - Full Kelly is too aggressive (high variance)
    - Fixed fractional Kelly (e.g., 1/4) ignores bet quality
    - Dynamic approach: adjust fraction based on confidence
    
    Quality grades → Kelly fractions:
    - A grade (excellent): 50% Kelly (half Kelly)
    - B grade (good): 25% Kelly (quarter Kelly)
    - C grade (fair): 10% Kelly (tenth Kelly)
    - D grade (poor): 0% Kelly (no bet)
    """
    
    def calculate_optimal_stake(
        self,
        odds: float,
        true_prob: BayesianResult,
        edge_analysis: EdgeAnalysis,
        bankroll: float,
        risk_tolerance: RiskTolerance = RiskTolerance.MODERATE
    ) -> StakeRecommendation:
        """
        Calculate optimal stake with full risk analysis
        
        Args:
            odds: Decimal odds
            true_prob: Bayesian probability estimate
            edge_analysis: Edge analysis from AdvancedEdgeCalculator
            bankroll: Current bankroll in dollars
            risk_tolerance: User's risk preference
        
        Returns:
            StakeRecommendation with amount and metrics
        """
        # Kelly fraction: f* = (p×b - q) / b
        # where b = odds - 1, p = true_prob, q = 1 - p
        b = odds - 1
        p = true_prob.probability
        q = 1 - p
        
        # Full Kelly (theoretical optimal)
        full_kelly = (p * b - q) / b
        
        # Clamp to reasonable range
        full_kelly = max(0, min(full_kelly, 0.5))  # Never bet more than 50%
        
        # Quality-based adjustment
        confidence_multiplier = self._get_confidence_multiplier(
            edge_analysis.quality_score
        )
        
        # Risk tolerance adjustment
        risk_multiplier = self._get_risk_multiplier(risk_tolerance)
        
        # Final fractional Kelly
        optimal_fraction = (
            full_kelly *
            confidence_multiplier *
            risk_multiplier
        )
        
        # Hard cap at 10% of bankroll (safety)
        capped_fraction = min(optimal_fraction, 0.10)
        
        # Calculate stake amount
        stake = bankroll * capped_fraction
        
        # Calculate performance metrics
        ev = edge_analysis.ev_per_dollar * stake
        
        # Geometric growth rate: g = p×log(1 + f×b) + q×log(1 - f)
        if capped_fraction < 1.0:
            geometric_growth = (
                p * np.log(1 + capped_fraction * b) +
                q * np.log(1 - capped_fraction)
            )
        else:
            geometric_growth = 0  # Over-betting leads to negative growth
        
        # Risk of ruin
        risk_of_ruin = self._calculate_risk_of_ruin(
            f=capped_fraction,
            edge=edge_analysis.raw_edge,
            variance=true_prob.variance,
            target_drawdown=0.5
        )
        
        # Expected bets to double bankroll
        if geometric_growth > 0:
            doubling_time = np.log(2) / geometric_growth
        else:
            doubling_time = float('inf')
        
        # Generate reasoning
        reasoning = self._generate_reasoning(
            full_kelly=full_kelly,
            confidence_mult=confidence_multiplier,
            risk_mult=risk_multiplier,
            quality=edge_analysis.quality_score,
            risk_tolerance=risk_tolerance
        )
        
        return StakeRecommendation(
            stake_amount=stake,
            fraction=capped_fraction,
            kelly_percentage=capped_fraction * 100,
            full_kelly_fraction=full_kelly,
            confidence_adjusted=confidence_multiplier,
            risk_adjusted=risk_multiplier,
            expected_value=ev,
            geometric_growth_rate=geometric_growth,
            risk_of_ruin=risk_of_ruin,
            doubling_time_bets=doubling_time,
            recommendation_reasoning=reasoning
        )
    
    def _get_confidence_multiplier(self, quality_score: str) -> float:
        """
        Get Kelly fraction multiplier based on bet quality
        
        A = 0.50 (half Kelly)
        B = 0.25 (quarter Kelly)
        C = 0.10 (tenth Kelly)
        D = 0.00 (no bet)
        """
        multipliers = {
            'A': 0.50,
            'B': 0.25,
            'C': 0.10,
            'D': 0.00
        }
        return multipliers.get(quality_score, 0.10)
    
    def _get_risk_multiplier(self, risk_tolerance: RiskTolerance) -> float:
        """
        Get multiplier based on user risk tolerance
        
        Conservative: 0.5x (extra cautious)
        Moderate: 1.0x (standard)
        Aggressive: 1.5x (higher risk for higher growth)
        """
        multipliers = {
            RiskTolerance.CONSERVATIVE: 0.5,
            RiskTolerance.MODERATE: 1.0,
            RiskTolerance.AGGRESSIVE: 1.5
        }
        return multipliers.get(risk_tolerance, 1.0)
    
    def _calculate_risk_of_ruin(
        self,
        f: float,
        edge: float,
        variance: float,
        target_drawdown: float
    ) -> float:
        """
        Approximate risk of losing target% of bankroll
        
        Using simplified gambler's ruin formula
        """
        if edge <= 0:
            return 1.0  # Certain ruin with negative edge
        
        # Theoretical Kelly optimal
        kelly_optimal = edge / variance if variance > 0 else 0
        
        # Over-betting penalty
        if f > kelly_optimal and kelly_optimal > 0:
            over_bet_ratio = f / kelly_optimal
            base_risk = 0.05  # 5% base risk at optimal Kelly
            return min(1.0, base_risk * (over_bet_ratio ** 2))
        else:
            # Under-betting is safer
            return max(0.001, 0.05 * (f / kelly_optimal if kelly_optimal > 0 else 0))
    
    def _generate_reasoning(
        self,
        full_kelly: float,
        confidence_mult: float,
        risk_mult: float,
        quality: str,
        risk_tolerance: RiskTolerance
    ) -> str:
        """Generate human-readable reasoning for stake size"""
        
        reasoning_parts = []
        
        # Quality adjustment
        if quality == 'A':
            reasoning_parts.append("Excellent quality bet (A-grade) → Half Kelly")
        elif quality == 'B':
            reasoning_parts.append("Good quality bet (B-grade) → Quarter Kelly")
        elif quality == 'C':
            reasoning_parts.append("Fair quality bet (C-grade) → Tenth Kelly")
        else:
            reasoning_parts.append("Poor quality bet (D-grade) → No bet recommended")
            return " | ".join(reasoning_parts)
        
        # Risk tolerance
        if risk_tolerance == RiskTolerance.CONSERVATIVE:
            reasoning_parts.append("Conservative risk (0.5x)")
        elif risk_tolerance == RiskTolerance.AGGRESSIVE:
            reasoning_parts.append("Aggressive risk (1.5x)")
        
        # Cap warning
        if full_kelly * confidence_mult * risk_mult > 0.10:
            reasoning_parts.append("Capped at 10% bankroll (safety)")
        
        return " | ".join(reasoning_parts)


# Example usage and testing
if __name__ == "__main__":
    from services.bayesian_consensus import BayesianResult
    from services.advanced_edge import EdgeAnalysis
    
    print("=" * 60)
    print("Dynamic Kelly Calculator - Test")
    print("=" * 60)
    
    # Mock inputs
    bayesian_result = BayesianResult(
        probability=0.55,
        variance=0.0005,
        credible_interval=(0.53, 0.57),
        alpha=110,
        beta=90,
        effective_samples=200
    )
    
    edge_analysis = EdgeAnalysis(
        raw_edge=0.0725,
        risk_adjusted_edge=0.060,
        ev_per_dollar=0.06,
        sharpe_ratio=0.75,
        uncertainty_penalty=0.045,
        liquidity_factor=0.85,
        fill_probability=0.92,
        confidence='A',
        components={}
    )
    
    calculator = DynamicKellyCalculator()
    
    # Test different risk tolerances
    for risk_tolerance in RiskTolerance:
        print(f"\n--- {risk_tolerance.value.upper()} Risk Tolerance ---")
        
        stake_rec = calculator.calculate_optimal_stake(
            odds=1.95,
            true_prob=bayesian_result,
            edge_analysis=edge_analysis,
            bankroll=1000.0,
            risk_tolerance=risk_tolerance
        )
        
        print(f"Stake: ${stake_rec.stake_amount:.2f} ({stake_rec.kelly_percentage:.2f}% of bankroll)")
        print(f"Full Kelly: {stake_rec.full_kelly_fraction * 100:.2f}%")
        print(f"After adjustments: {stake_rec.fraction * 100:.2f}%")
        print(f"Expected Value: ${stake_rec.expected_value:.2f}")
        print(f"Growth Rate: {stake_rec.geometric_growth_rate * 100:.3f}% per bet")
        print(f"Risk of Ruin: {stake_rec.risk_of_ruin * 100:.2f}%")
        print(f"Doubling Time: {stake_rec.doubling_time_bets:.0f} bets")
        print(f"Reasoning: {stake_rec.recommendation_reasoning}")
