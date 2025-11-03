from typing import List

from scipy.stats import linregress


def get_r2_from(
    values: List[float],
) -> float:
    min_values = 2

    if not values or len(values) < min_values:
        return 0.0

    x = list(range(len(values)))
    result = linregress(x, values)

    return float(result.rvalue**2)  # type: ignore[attr-defined]
