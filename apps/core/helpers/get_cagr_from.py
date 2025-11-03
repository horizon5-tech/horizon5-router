from typing import List

import empyrical as ep
import numpy as np


def get_cagr_from(
    values: List[float],
    period: str = "daily",
) -> float:
    """
    Calculate the Compound Annual Growth Rate (CAGR) from portfolio values.

    CAGR represents the mean annual growth rate of an investment over a
    specified period, assuming profits are reinvested at the end of each
    period.

    Parameters:
        values: List of portfolio values over time (e.g., [100, 105, 110])
        period: Frequency of values - "daily", "weekly", "monthly", or
                "yearly" (default: "daily")

    Returns:
        CAGR as a decimal float (e.g., 0.1549 represents 15.49% annual
        return). Returns 0.0 if values list has fewer than 2 elements

    Interpretation:
        - Positive value: Portfolio gained value over time
        - Negative value: Portfolio lost value over time
        - Higher value: Better performance
        - Example: 0.15 means 15% average annual growth
    """
    min_values = 2

    if not values or len(values) < min_values:
        return 0.0

    values_array = np.array(values)

    return float(
        ep.cagr(
            values_array,
            period=period,
        )
    )
