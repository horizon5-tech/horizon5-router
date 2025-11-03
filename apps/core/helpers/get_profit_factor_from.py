from typing import List


def get_profit_factor_from(
    values: List[float],
) -> float:
    """
    Calculate the Profit Factor from a list of trade returns or P&L values.

    Profit Factor is the ratio of gross profit to gross loss. It measures how much
    profit is generated for each unit of loss, indicating overall profitability.

    Parameters:
        values: List of individual returns or P&L values (e.g., [10, -5, 15, -3, 8])
                Positive values represent gains, negative values represent losses

    Returns:
        Profit factor as a positive float (e.g., 1.16)
        Returns 0.0 if values list has fewer than 2 elements
        Returns infinity if there are only gains and no losses

    Interpretation:
        - Value > 1.5: Excellent profitability
        - Value 1.0-1.5: Acceptable profitability
        - Value = 1.0: Break-even (gains equal losses)
        - Value < 1.0: Losing strategy (losses exceed gains)
        - Example: 1.16 means $1.16 earned for every $1.00 lost
    """
    min_values = 2

    if not values or len(values) < min_values:
        return 0.0

    gains = sum(v for v in values if v > 0)
    losses = abs(sum(v for v in values if v < 0))

    if losses == 0:
        return 0.0 if gains == 0 else float("inf")

    return float(gains / losses)
