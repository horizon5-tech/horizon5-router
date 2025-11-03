from typing import List

import numpy as np


def get_expected_shortfall_from(
    values: List[float],
    cutoff: float = 0.05,
) -> float:
    """
    Calculate the Expected Shortfall (Conditional Value at Risk - CVaR) from portfolio values.

    Expected Shortfall represents the average loss in the worst-case scenarios beyond
    a specified confidence level. It measures tail risk by averaging the losses that
    occur in the worst X% of cases.

    Parameters:
        values: List of portfolio values over time (e.g., [100, 105, 98, 95, 110])
        cutoff: Confidence level as a decimal (default: 0.05 for 5% worst cases)

    Returns:
        Expected shortfall as a negative float (e.g., -0.0387 represents -3.87%)
        Returns 0.0 if values list has fewer than 2 elements or no shortfall returns

    Interpretation:
        - Value closer to 0: Lower tail risk, smaller expected losses in worst scenarios
        - More negative value: Higher tail risk, larger expected losses in worst scenarios
        - Example: -0.0387 means in the worst 5% of cases, average loss is 3.87%
        - Used to understand potential catastrophic losses
    """
    min_values = 2

    if not values or len(values) < min_values:
        return 0.0

    returns = np.diff(values) / values[:-1]
    var_cutoff = np.percentile(returns, cutoff * 100)
    shortfall_returns = returns[returns <= var_cutoff]

    if len(shortfall_returns) == 0:
        return 0.0

    return float(np.mean(shortfall_returns))
