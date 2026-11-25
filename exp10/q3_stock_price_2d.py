"""
Experiment 10 - Question 3: Stock Price Analysis

Scenario: Closing stock prices for 5 companies are stored in a 2D array (5x5),
one row per company and one column per trading day.

Task:
  1) Find the average stock price of each company (row-wise).
  2) Find the day with the highest overall stock price.

Rubrics covered:
  * 2D array handling
  * correct row-wise average (axis=1)
  * highest price logic
  * result display

Requires: numpy
"""

import numpy as np

COMPANIES = ["TCS", "INFY", "RELIANCE", "HDFCBANK", "WIPRO"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]


def main():
    prices = np.array([
        [3850.00, 3920.50, 3870.25, 3990.00, 4015.75],   # TCS
        [1480.00, 1495.25, 1460.50, 1510.00, 1525.50],   # INFY
        [2890.50, 2935.00, 2910.75, 2880.25, 2955.00],   # RELIANCE
        [1620.00, 1605.50, 1640.00, 1655.75, 1648.25],   # HDFCBANK
        [ 452.00,  448.75,  455.50,  461.00,  458.25],   # WIPRO
    ])

    print("=== 2D price array ===")
    print(f"  shape {prices.shape}, dtype {prices.dtype}, "
          f"{prices.size} values, {prices.nbytes} bytes")
    print(f"\n  {'company':<10}" + "".join(f"{d:>11}" for d in DAYS))
    print("  " + "-" * 65)
    for name, row in zip(COMPANIES, prices):
        print(f"  {name:<10}" + "".join(f"{v:>11,.2f}" for v in row))

    # 1) row-wise average, axis=1 collapses the columns
    row_avg = prices.mean(axis=1)
    print("\n=== 1) average price per company (axis=1) ===")
    print(f"  prices.mean(axis=1) -> {np.round(row_avg, 2)}")
    print(f"\n  {'company':<10}{'average':>12}{'low':>11}{'high':>11}"
          f"{'swing':>9}")
    for name, avg, lo, hi in zip(COMPANIES, row_avg,
                                 prices.min(axis=1), prices.max(axis=1)):
        print(f"  {name:<10}{avg:>12,.2f}{lo:>11,.2f}{hi:>11,.2f}"
              f"{hi - lo:>9,.2f}")
    print(f"\n  costliest company on average : "
          f"{COMPANIES[row_avg.argmax()]} (Rs.{row_avg.max():,.2f})")
    print(f"  cheapest company on average  : "
          f"{COMPANIES[row_avg.argmin()]} (Rs.{row_avg.min():,.2f})")

    # 2) the single highest price in the whole array
    flat_index = prices.argmax()
    company_i, day_i = np.unravel_index(flat_index, prices.shape)

    print("\n=== 2) highest overall stock price ===")
    print(f"  prices.max()             : Rs.{prices.max():,.2f}")
    print(f"  prices.argmax()          : {flat_index} (flattened index)")
    print(f"  np.unravel_index(...)    : row {company_i}, column {day_i}")
    print(f"  that is {COMPANIES[company_i]} on {DAYS[day_i]} "
          f"at Rs.{prices[company_i, day_i]:,.2f}")

    col_sum = prices.sum(axis=0)
    print("\n=== the day with the highest total market value (axis=0) ===")
    print(f"  prices.sum(axis=0) -> {np.round(col_sum, 2)}")
    for day, total in zip(DAYS, col_sum):
        print(f"  {day:<5}Rs.{total:>12,.2f}  {'#' * int(total / 400)}")
    print(f"\n  strongest day : {DAYS[col_sum.argmax()]} "
          f"(Rs.{col_sum.max():,.2f})")
    print(f"  weakest day   : {DAYS[col_sum.argmin()]} "
          f"(Rs.{col_sum.min():,.2f})")

    print("\n=== column-wise average (axis=0) ===")
    col_avg = prices.mean(axis=0)
    for day, avg in zip(DAYS, col_avg):
        print(f"  {day:<5}Rs.{avg:>11,.2f}")

    print("\n=== axis recap ===")
    print(f"  prices.mean()        : {prices.mean():,.2f}  (every value)")
    print(f"  prices.mean(axis=0)  : shape {col_avg.shape} -> per day")
    print(f"  prices.mean(axis=1)  : shape {row_avg.shape} -> per company")

    print("\n=== weekly return per company ===")
    returns = (prices[:, -1] - prices[:, 0]) / prices[:, 0] * 100
    for name, open_, close, pct in zip(COMPANIES, prices[:, 0],
                                       prices[:, -1], returns):
        arrow = "up  " if pct > 0 else "down"
        print(f"  {name:<10}{open_:>10,.2f} -> {close:>10,.2f}  "
              f"{pct:>+7.2f}%  {arrow}")
    print(f"\n  best performer  : {COMPANIES[returns.argmax()]} "
          f"({returns.max():+.2f}%)")
    print(f"  worst performer : {COMPANIES[returns.argmin()]} "
          f"({returns.min():+.2f}%)")

    print("\n=== volatility (standard deviation per company) ===")
    vol = prices.std(axis=1)
    for name, v, avg in zip(COMPANIES, vol, row_avg):
        print(f"  {name:<10}Rs.{v:>8,.2f}  "
              f"({v / avg * 100:.2f}% of its average price)")
    print(f"  most volatile : {COMPANIES[vol.argmax()]}")

    print("\n=== slicing the 2D array ===")
    print(f"  prices[0]        (TCS row)      : {prices[0]}")
    print(f"  prices[:, 0]     (Monday col)   : {prices[:, 0]}")
    print(f"  prices[1:3, 2:4] (sub-block)    :\n{prices[1:3, 2:4]}")
    print(f"  diagonal                        : {np.round(prices.diagonal(), 2)}")
    print(f"  transpose shape                 : {prices.T.shape}")

    print("\n=== prices above Rs.2,000 ===")
    mask = prices > 2000
    print(f"  count : {int(mask.sum())} of {prices.size}")
    rows, cols = np.where(mask)
    for r, c in zip(rows, cols):
        print(f"    {COMPANIES[r]:<10}{DAYS[c]:<5}Rs.{prices[r, c]:,.2f}")


if __name__ == "__main__":
    main()
