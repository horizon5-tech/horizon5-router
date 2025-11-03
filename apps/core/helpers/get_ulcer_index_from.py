from typing import List

import numpy as np


def get_ulcer_index_from(
    values: List[float],
) -> float:
    """
    Calculate the Ulcer Index from portfolio values.

    Ulcer Index measures both the depth and duration of drawdowns, providing a more
    comprehensive view of downside volatility than maximum drawdown alone. It considers
    all drawdowns throughout the period, not just the largest one.

    Parameters:
        values: List of portfolio values over time (e.g., [100, 105, 98, 102, 95, 110])

    Returns:
        Ulcer Index as a positive float percentage (e.g., 0.23 represents 0.23%)
        Returns 0.0 if values list has fewer than 2 elements

    Interpretation:
        - Lower value: Less stress and volatility from drawdowns
        - Higher value: More persistent and deeper drawdowns
        - Value < 1.0: Very low drawdown stress (excellent)
        - Value 1.0-5.0: Moderate drawdown stress (acceptable)
        - Value > 5.0: High drawdown stress (concerning)
        - Example: 0.23 means low stress level with minimal prolonged drawdowns
    """
    min_values = 2

    if not values or len(values) < min_values:
        return 0.0

    values_array = np.array(values)
    running_max = np.maximum.accumulate(values_array)
    drawdowns = ((values_array - running_max) / running_max) * 100
    squared_drawdowns = drawdowns**2
    ulcer_index = np.sqrt(np.mean(squared_drawdowns))

    return float(ulcer_index)
