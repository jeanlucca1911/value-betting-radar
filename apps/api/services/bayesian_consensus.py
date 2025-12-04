"""
Bayesian Consensus Engine

Hierarchical Bayesian model for calculating true probabilities:
1. Prior: Historical matchup outcomes (Beta distribution)
2. Likelihood: Bookmaker odds (weighted by accuracy)
3. Posterior: True probability estimate with confidence intervals

This is significantly more sophisticated than simple weighted averages.
"""

import numpy as np
from scipy.stats import beta as beta_dist
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import sqlite3
from pathlib import Path


@dataclass
class BayesianResult:
    """Result of Bayesian probability calculation"""
    probability: float  # Posterior mean
    variance: float  # Posterior variance
    credible_interval: Tuple[float, float]  # 95% credible interval
    alpha: float  # Beta distribution alpha parameter
    beta: float  # Beta distribution beta parameter
    effective_samples: int  # Effective sample size
    
    @property
    def confidence_score(self) -> str:
        """
        Quality rating based on credible interval width
        
        A = Very confident (CI < 10%)
        B = Confident (CI < 20%)
        C = Moderate (CI < 30%)
        D = Low confidence (CI > 30%)
        """
        ci_width = self.credible_interval[1] - self.credible_interval[0]
        
        if ci_width < 0.10:
            return 'A'
        elif ci_width < 0.20:
            return 'B'
        elif ci_width < 0.30:
            return 'C'
        else:
            return 'D'
    
    @property
    def std_error(self) -> float:
        """Standard error of the estimate"""
        return np.sqrt(self.variance)


@dataclass
class HistoricalPrior:
    """Prior distribution from historical data"""
    alpha: float
    beta: float
    total_games: int
    win_rate: float


class BayesianConsensus:
    """
    Hierarchical Bayesian consensus model
    
    Advantages over simple weighted average:
    - Incorporates historical knowledge (priors)
    - Quantifies uncertainty (credible intervals)
    - Adapts to bookmaker accuracy over time
    - Provides confidence scores for bet quality
    """
    
    def __init__(self, db_path: str = "db/historical.db"):
        self.db_path = db_path
        self.bookmaker_precision = self._load_bookmaker_precision()
    
    def _load_bookmaker_precision(self) -> Dict[str, float]:
        """
        Load bookmaker accuracy from historical data
        
        Precision = 1 / variance of prediction errors
        Higher precision = more weight in Bayesian updating
        """
        # Default precisions (will be updated as we collect data)
        defaults = {
            'pinnacle': 10.0,      # Very sharp
            'bookmaker': 10.0,
            'draftkings': 8.0,     # Sharp for US markets
            'fanduel': 8.0,
            'betfair': 9.0,
            'bet365': 7.0,
            'williamhill': 6.0,
            'caesars': 5.0,
            'betmgm': 5.0,
            'betrivers': 4.0,
            'mybookieag': 2.0,     # Soft book
            'bovada': 2.5,
            'betonlineag': 2.5,
            'default': 3.0
        }
        
        # TODO: Update from historical performance in database
        # After 30+ days of data, calculate actual accuracy
        
        return defaults
    
    def calculate_true_probability(
        self,
        sport: str,
        home_team: str,
        away_team: str,
        outcome_name: str,
        bookmaker_odds: List[Dict]
    ) -> BayesianResult:
        """
        Calculate posterior probability using Bayesian updating
        
        Args:
            sport: Sport key (e.g., 'basketball_nba')
            home_team: Home team name
            away_team: Away team name
            outcome_name: Outcome to calculate probability for
            bookmaker_odds: List of {'bookie': str, 'price': float, 'weight': float}
        
        Returns:
            BayesianResult with probability and confidence metrics
        """
        # Step 1: Get historical prior
        prior = self._get_historical_prior(sport, home_team, away_team, outcome_name)
        
        # Step 2: Bayesian updating with bookmaker odds
        alpha = prior.alpha
        beta_param = prior.beta
        
        for odds_data in bookmaker_odds:
            bookie_key = odds_data.get('bookie', 'default')
            price = odds_data['price']
            
            # Get bookmaker precision (accuracy)
            precision = self.bookmaker_precision.get(
                bookie_key.lower(), 
                self.bookmaker_precision['default']
            )
            
            # Convert odds to implied probability
            implied_prob = 1.0 / price
            
            # Effective sample size from this bookmaker
            # More accurate bookmakers contribute more "pseudo-observations"
            n_effective = precision * 10
            
            # Beta-Binomial conjugate prior update
            alpha += implied_prob * n_effective
            beta_param += (1 - implied_prob) * n_effective
        
        # Step 3: Calculate posterior statistics
        posterior_mean = alpha / (alpha + beta_param)
        posterior_variance = (alpha * beta_param) / (
            (alpha + beta_param)**2 * (alpha + beta_param + 1)
        )
        
        # 95% credible interval
        credible_interval = beta_dist.interval(0.95, alpha, beta_param)
        
        return BayesianResult(
            probability=posterior_mean,
            variance=posterior_variance,
            credible_interval=credible_interval,
            alpha=alpha,
            beta=beta_param,
            effective_samples=int(alpha + beta_param)
        )
    
    def _get_historical_prior(
        self,
        sport: str,
        home_team: str,
        away_team: str,
        outcome_name: str
    ) -> HistoricalPrior:
        """
        Calculate informed prior from historical matchup data
        
        Returns Beta distribution parameters based on past games
        If no historical data, returns uninformed prior Beta(1, 1)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Query historical head-to-head results
            cursor.execute("""
                SELECT COUNT(*) as total,
                       SUM(CASE WHEN winner = ? THEN 1 ELSE 0 END) as wins
                FROM matches
                WHERE sport_key = ?
                AND ((home_team = ? AND away_team = ?)
                     OR (home_team = ? AND away_team = ?))
                AND completed = TRUE
            """, (
                self._outcome_to_side(outcome_name, home_team, away_team),
                sport,
                home_team, away_team,
                away_team, home_team
            ))
            
            result = cursor.fetchone()
            conn.close()
            
            if result and result[0] > 0:
                total_games, wins = result
                
                # Add pseudo-counts to prevent extreme priors
                # Jeffrey's prior: add 0.5 to both
                alpha = wins + 0.5
                beta = (total_games - wins) + 0.5
                
                return HistoricalPrior(
                    alpha=alpha,
                    beta=beta,
                    total_games=total_games,
                    win_rate=wins / total_games if total_games > 0 else 0.5
                )
            
        except Exception as e:
            print(f"Error loading historical prior: {e}")
        
        # Uninformed prior (uniform distribution)
        return HistoricalPrior(
            alpha=1.0,
            beta=1.0,
            total_games=0,
            win_rate=0.5
        )
    
    def _outcome_to_side(self, outcome_name: str, home_team: str, away_team: str) -> str:
        """Convert outcome name to 'home', 'away', or 'draw'"""
        if outcome_name == home_team:
            return 'home'
        elif outcome_name == away_team:
            return 'away'
        elif outcome_name.lower() in ['draw', 'tie']:
            return 'draw'
        else:
            # Default to home if unclear
            return 'home'
    
    def calculate_consensus_probabilities(
        self,
        sport: str,
        home_team: str,
        away_team: str,
        outcomes_odds: Dict[str, List[Dict]]
    ) -> Dict[str, BayesianResult]:
        """
        Calculate Bayesian probabilities for all outcomes in a match
        
        Args:
            outcomes_odds: {
                'Team A': [{'bookie': 'pinnacle', 'price': 2.5, 'weight': 5.0}, ...],
                'Team B': [...]
            }
        
        Returns:
            {
                'Team A': BayesianResult(...),
                'Team B': BayesianResult(...)
            }
        """
        results = {}
        
        for outcome_name, odds_list in outcomes_odds.items():
            result = self.calculate_true_probability(
                sport=sport,
                home_team=home_team,
                away_team=away_team,
                outcome_name=outcome_name,
                bookmaker_odds=odds_list
            )
            results[outcome_name] = result
        
        # Normalize probabilities to sum to 1
        total_prob = sum(r.probability for r in results.values())
        
        if total_prob > 0:
            for outcome_name in results:
                old_prob = results[outcome_name].probability
                normalized_prob = old_prob / total_prob
                
                # Update probability while keeping other fields
                results[outcome_name] = BayesianResult(
                    probability=normalized_prob,
                    variance=results[outcome_name].variance / (total_prob ** 2),
                    credible_interval=results[outcome_name].credible_interval,
                    alpha=results[outcome_name].alpha,
                    beta=results[outcome_name].beta,
                    effective_samples=results[outcome_name].effective_samples
                )
        
        return results


# Example usage
if __name__ == "__main__":
    # Test the Bayesian consensus
    consensus = BayesianConsensus()
    
    # Mock odds data
    odds_data = {
        'Los Angeles Lakers': [
            {'bookie': 'pinnacle', 'price': 1.80, 'weight': 5.0},
            {'bookie': 'draftkings', 'price': 1.83, 'weight': 3.5},
            {'bookie': 'fanduel', 'price': 1.85, 'weight': 3.0},
        ],
        'Boston Celtics': [
            {'bookie': 'pinnacle', 'price': 2.10, 'weight': 5.0},
            {'bookie': 'draftkings', 'price': 2.08, 'weight': 3.5},
            {'bookie': 'fanduel', 'price': 2.05, 'weight': 3.0},
        ]
    }
    
    results = consensus.calculate_consensus_probabilities(
        sport='basketball_nba',
        home_team='Los Angeles Lakers',
        away_team='Boston Celtics',
        outcomes_odds=odds_data
    )
    
    print("Bayesian Consensus Results:")
    print("=" * 60)
    for outcome, result in results.items():
        print(f"\n{outcome}:")
        print(f"  Probability: {result.probability:.4f} ({result.probability * 100:.2f}%)")
        print(f"  95% CI: [{result.credible_interval[0]:.4f}, {result.credible_interval[1]:.4f}]")
        print(f"  Confidence: {result.confidence_score}")
        print(f"  Effective samples: {result.effective_samples}")
