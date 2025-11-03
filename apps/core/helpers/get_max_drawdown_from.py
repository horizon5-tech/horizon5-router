from typing import List

import empyrical as ep
import numpy as np


def get_max_drawdown_from(
    values: List[float],
) -> float:
    """
    Calculate the maximum drawdown from a series of portfolio values.

    Maximum drawdown represents the largest peak-to-trough decline in portfolio value,
    expressed as a negative percentage. It measures the worst loss an investor would have
    experienced during the observed period.

    Parameters:
        values: List of portfolio values over time (e.g., [100, 105, 98, 110, 95])

    Returns:
        Maximum drawdown as a negative float (e.g., -0.1364 represents -13.64% drawdown)
        Returns 0.0 if values list has fewer than 2 elements

    Interpretation:
        - Value closer to 0: Lower risk, smaller losses from peak
        - More negative value: Higher risk, larger losses from peak
        - Example: -0.25 means a 25% loss from the highest point
    """
    min_values = 2

    if not values or len(values) < min_values:
        return 0.0

    values_array = np.array(values)

    return float(ep.max_drawdown(values_array))
