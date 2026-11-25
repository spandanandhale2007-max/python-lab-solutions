"""
Experiment 10 - Question 2: Daily Sales Analysis

Scenario: A store records daily sales (in Rs.) for 7 days:
[1200, 1500, 900, 1800, 2100, 1600, 1900].

Task:
  1) Convert this into a NumPy array.
  2) Find the total sales, average sales and the day with maximum sales.

Rubrics covered:
  * array creation
  * correct use of NumPy functions (sum, mean, argmax)
  * display of results
  * correct logic

Requires: numpy
"""

import numpy as np

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
        "Saturday", "Sunday"]
RAW = [1200, 1500, 900, 1800, 2100, 1600, 1900]


def main():
    # 1) convert the Python list into a NumPy array
    sales = np.array(RAW)

    print("=== conversion ===")
    print(f"  python list : {RAW}  (type {type(RAW).__name__})")
    print(f"  numpy array : {sales}  (type {type(sales).__name__})")
    print(f"  dtype {sales.dtype}, shape {sales.shape}, "
          f"{sales.nbytes} bytes")

    # 2) aggregation
    total = sales.sum()
    average = sales.mean()
    best_index = sales.argmax()
    worst_index = sales.argmin()

    print("\n=== required answers ===")
    print(f"  total sales        : Rs.{total:,}")
    print(f"  average sales      : Rs.{average:,.2f} per day")
    print(f"  maximum sales day  : {DAYS[best_index]} "
          f"(index {best_index}) with Rs.{sales[best_index]:,}")

    print("\n=== extra statistics ===")
    print(f"  minimum sales day  : {DAYS[worst_index]} "
          f"with Rs.{sales[worst_index]:,}")
    print(f"  median             : Rs.{np.median(sales):,.2f}")
    print(f"  standard deviation : Rs.{sales.std():,.2f}")
    print(f"  range (np.ptp)     : Rs.{np.ptp(sales):,}")
    print(f"  cumulative total   : {np.cumsum(sales)}")

    print("\n=== day-by-day ===")
    print(f"  {'day':<11}{'sales':>10}{'vs average':>13}{'share':>9}  bar")
    for day, amount in zip(DAYS, sales):
        share = amount / total * 100
        print(f"  {day:<11}{amount:>10,}{amount - average:>+13,.2f}"
              f"{share:>8.1f}%  {'#' * (amount // 100)}")

    print("\n=== days above the weekly average ===")
    mask = sales > average
    print(f"  mask    : {mask}")
    print(f"  days    : {np.array(DAYS)[mask].tolist()}")
    print(f"  amounts : {sales[mask]}")
    print(f"  they contributed Rs.{sales[mask].sum():,} "
          f"({sales[mask].sum() / total * 100:.1f}% of the week)")

    print("\n=== weekday vs weekend ===")
    weekday = sales[:5]
    weekend = sales[5:]
    print(f"  weekdays (Mon-Fri) : Rs.{weekday.sum():,}  "
          f"avg Rs.{weekday.mean():,.2f}")
    print(f"  weekend  (Sat-Sun) : Rs.{weekend.sum():,}  "
          f"avg Rs.{weekend.mean():,.2f}")
    print(f"  weekend uplift     : "
          f"{(weekend.mean() / weekday.mean() - 1) * 100:+.1f}%")

    print("\n=== day-on-day change ===")
    change = np.diff(sales)
    percent = np.round(change / sales[:-1] * 100, 1)
    for i, (delta, pct) in enumerate(zip(change, percent)):
        print(f"  {DAYS[i]:<11}-> {DAYS[i + 1]:<11}"
              f"{delta:>+8,}  {pct:>+7.1f}%")
    print(f"  biggest jump : {DAYS[change.argmax() + 1]} "
          f"({change.max():+,})")
    print(f"  biggest drop : {DAYS[change.argmin() + 1]} "
          f"({change.min():+,})")

    print("\n=== vectorised what-if scenarios ===")
    print(f"  10% growth next week  : {np.round(sales * 1.10).astype(int)} "
          f"-> Rs.{int(round(sales.sum() * 1.10)):,}")
    print(f"  GST at 18% collected  : "
          f"{np.round(sales * 0.18, 2)}")
    print(f"  Rs.300 fixed cost/day : {sales - 300} "
          f"-> profit Rs.{(sales - 300).sum():,}")
    target = 1500
    print(f"  days meeting the Rs.{target:,} target: "
          f"{int((sales >= target).sum())} of 7 -> "
          f"{np.array(DAYS)[sales >= target].tolist()}")

    print("\n=== 3-day moving average (np.convolve) ===")
    window = np.convolve(sales, np.ones(3) / 3, mode="valid")
    for i, value in enumerate(window):
        print(f"  {DAYS[i][:3]}-{DAYS[i + 2][:3]} : Rs.{value:,.2f}")


if __name__ == "__main__":
    main()
