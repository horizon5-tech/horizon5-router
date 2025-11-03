from typing import List

import empyrical as ep
import numpy as np


def get_sharpe_ratio_from_orders(
    values: List[float],
    risk_free_rate: float = 0.0,
) -> float:
    min_values = 2

    if not values or len(values) < min_values:
        return 0.0

    values_array = np.array(values)

    return float(ep.sharpe_ratio(values_array, risk_free=risk_free_rate))  # type: ignore[arg-type]
