import pytest
from services.math import PowerMethod

def test_power_method_basic():
    # Fair coin: 2.0, 2.0 -> Prob 0.5, 0.5
    odds = [2.0, 2.0]
    probs = PowerMethod.calculate_true_probabilities(odds)
    assert probs == [0.5, 0.5]

def test_power_method_with_margin():
    # Coin with margin: 1.90, 1.90 -> Implied 0.526, 0.526 -> Sum 1.05
    # Should normalize back to 0.5, 0.5
    odds = [1.90, 1.90]
    probs = PowerMethod.calculate_true_probabilities(odds)
    assert round(probs[0], 2) == 0.50
    assert round(probs[1], 2) == 0.50

def test_power_method_favorite_longshot():
    # Favorite 1.20, Longshot 6.00
    # Implied: 0.833 + 0.166 = 1.0
    # With margin: 1.15, 5.50 -> Implied 0.869 + 0.181 = 1.05
    odds = [1.15, 5.50]
    probs = PowerMethod.calculate_true_probabilities(odds)
    assert sum(probs) == pytest.approx(1.0, 0.001)
    # Power method should reduce favorite prob less than longshot prob (relative to implied)
    
def test_calculate_edge():
    # True prob 0.5, Odds 2.10 -> Edge 0.05 (5%)
    edge = PowerMethod.calculate_edge(2.10, 0.5)
    assert edge == pytest.approx(0.05)

    # True prob 0.5, Odds 1.90 -> Edge -0.05 (-5%)
    edge = PowerMethod.calculate_edge(1.90, 0.5)
    assert edge == pytest.approx(-0.05)
