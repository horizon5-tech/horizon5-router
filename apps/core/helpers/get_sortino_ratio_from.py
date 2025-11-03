from typing import List

import empyrical as ep
import numpy as np


def get_sortino_ratio_from(
    values: List[float],
    required_return: float = 0.0,
    period: str = "daily",
) -> float:
    """
    Calculate the Sortino Ratio from portfolio values.

    Sortino Ratio is similar to Sharpe Ratio but only penalizes downside volatility,
    not total volatility. It measures risk-adjusted returns considering only harmful
    volatility (returns below the required return).

    Parameters:
        values: List of portfolio values over time (e.g., [100, 105, 98, 110])
        required_return: Minimum acceptable return threshold (default: 0.0)
        period: Frequency of values - "daily", "weekly", "monthly", or
                "yearly" (default: "daily")

    Returns:
        Sortino ratio as a float (e.g., 1.07)
        Returns 0.0 if values list has fewer than 2 elements

    Interpretation:
        - Higher value: Better downside risk-adjusted performance
        - Value > 2.0: Excellent performance with minimal downside risk
        - Value 1.0-2.0: Good risk-adjusted returns
        - Value < 1.0: Poor risk-adjusted returns
        - Example: 1.07 means 1.07 units of return per unit of downside risk
    """
    min_values = 2

    if not values or len(values) < min_values:
        return 0.0

    values_array = np.array(values)

    return float(
        ep.sortino_ratio(
            values_array,
            required_return=required_return,  # pyright: ignore[reportArgumentType]
            period=period,
        )
    )
