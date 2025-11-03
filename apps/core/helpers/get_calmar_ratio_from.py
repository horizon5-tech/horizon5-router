from typing import List

import empyrical as ep
import numpy as np


def get_calmar_ratio_from(
    values: List[float],
    period: str = "daily",
) -> float:
    """
    Calculate the Calmar Ratio from portfolio values.

    Calmar Ratio measures risk-adjusted return by dividing CAGR by the
    absolute value of maximum drawdown. It evaluates return relative to
    downside risk.

    Parameters:
        values: List of portfolio values over time (e.g., [100, 110, 95])
        period: Frequency of values - "daily", "weekly", "monthly", or
                "yearly" (default: "daily")

    Returns:
        Calmar ratio as a positive float (e.g., 0.27)
        Returns 0.0 if values list has fewer than 2 elements

    Interpretation:
        - Higher value: Better risk-adjusted performance
        - Value > 1.0: Excellent risk-adjusted returns
        - Value 0.5-1.0: Good risk-adjusted returns
        - Value < 0.5: Poor risk-adjusted returns
        - Example: 0.27 means 0.27 units of return per unit of max
          drawdown risk
    """
    min_values = 2

    if not values or len(values) < min_values:
        return 0.0

    values_array = np.array(values)

    return float(
        ep.calmar_ratio(
            values_array,
            period=period,
        )
    )
