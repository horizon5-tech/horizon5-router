from typing import List

import numpy as np
from scipy.stats import linregress


def get_r2_from(
    values: List[float],
) -> float:
    min_values = 2

    if not values or len(values) < min_values:
        return 0.0

    values_array = np.array(values)
    x = np.arange(len(values_array))
    result = linregress(x, values_array)

    return float(result.rvalue**2)  # type: ignore[attr-defined]
