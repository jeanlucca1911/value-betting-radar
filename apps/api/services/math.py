import numpy as np
from scipy.optimize import newton

class PowerMethod:
    @staticmethod
    def calculate_true_probabilities(odds: list[float]) -> list[float]:
        """
        Calculates true probabilities from bookmaker odds using the Power Method.
        Solves for k where sum(1/odds^k) = 1.
        """
        if not odds or any(o <= 1.0 for o in odds):
            return []

        # Target function: sum(p_implied^k) - 1 = 0
        # where p_implied = 1/odd
        implied_probs = np.array([1.0 / o for o in odds])
        
        def equation(k):
            return np.sum(np.power(implied_probs, k)) - 1.0

        try:
            # Solve for k using Newton-Raphson method
            # Initial guess k=1 (which would mean no margin if sum=1)
            k = newton(equation, x0=1.0, maxiter=50)
            
            # Calculate true probabilities: p_true = p_implied^k
            true_probs = np.power(implied_probs, k)
            return true_probs.tolist()
        except RuntimeError:
            # Convergence failed, fallback to basic normalization
            total_implied = np.sum(implied_probs)
            return (implied_probs / total_implied).tolist()

    @staticmethod
    def calculate_edge(soft_odds: float, true_prob: float) -> float:
        """
        Calculates the edge (expected value) of a bet.
        Edge = (Probability * Odds) - 1
        """
        return (true_prob * soft_odds) - 1.0
    
    @staticmethod
    def calculate_kelly_stake(odds: float, true_prob: float, bankroll: float = 1000.0, fractional_kelly: float = 0.25) -> dict:
        """
        Calculate the optimal stake using the Kelly Criterion.
        
        Args:
            odds: Decimal odds (e.g., 2.5)
            true_prob: True probability of winning (0-1)
            bankroll: Total bankroll in dollars
            fractional_kelly: Fraction of full Kelly to use (0.25 = Quarter Kelly, safer)
        
        Returns:
            dict with kelly_percentage and recommended_stake
        """
        # Kelly Formula: f* = (bp - q) / b
        # where b = net odds (odds - 1), p = win prob, q = lose prob (1 - p)
        
        b = odds - 1  # Net odds
        p = true_prob
        q = 1 - p
        
        # Full Kelly percentage
        kelly_full = (b * p - q) / b
        
        # Apply fractional Kelly (e.g., 0.25 for Quarter Kelly)
        kelly_fraction = max(0, kelly_full * fractional_kelly)  # Never negative
        
        # Calculate recommended stake
        recommended_stake = bankroll * kelly_fraction
        
        return {
            "kelly_percentage": round(kelly_fraction * 100, 2),  # As percentage
            "recommended_stake": round(recommended_stake, 2)
        }
