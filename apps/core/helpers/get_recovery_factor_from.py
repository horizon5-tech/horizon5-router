from typing import List

import empyrical as ep
import numpy as np


def get_recovery_factor_from(
    values: List[float],
) -> float:
    """
    Calculate the Recovery Factor from portfolio values.

    Recovery Factor measures how efficiently a strategy recovers from losses by dividing
    total net profit by maximum drawdown. It indicates how many units of profit are
    generated for each unit of maximum loss.

    Parameters:
        values: List of portfolio values over time (e.g., [100, 110, 85, 120, 130])

    Returns:
        Recovery factor as a positive float (e.g., 4.22)
        Returns 0.0 if values list has fewer than 2 elements or max drawdown is 0

    Interpretation:
        - Higher value: Better ability to recover from losses
        - Value > 3.0: Excellent recovery capability
        - Value 2.0-3.0: Good recovery capability
        - Value < 2.0: Poor recovery capability
        - Example: 4.22 means the strategy generates 4.22 units of profit for every
          unit of maximum drawdown experienced
    """
    min_values = 2

    if not values or len(values) < min_values:
        return 0.0

    values_array = np.array(values)
    max_dd = abs(ep.max_drawdown(values_array))

    if max_dd == 0:
        return 0.0

    total_return = (values_array[-1] - values_array[0]) / values_array[0] if values_array[0] != 0 else 0.0

    return float(total_return / max_dd)
