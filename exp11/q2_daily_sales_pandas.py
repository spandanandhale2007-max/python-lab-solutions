"""
Experiment 11 - Question 2: Daily Sales Analysis with Pandas

Scenario: A store records daily sales (in Rs.) for 7 days:
[1200, 1500, 900, 1800, 2100, 1600, 1900].

Task:
  1) Load this into a Pandas Series indexed by weekday.
  2) Find the total sales, average sales and the day with maximum sales.

Note: the question sheet repeats Experiment 10 Question 2 here. Since
Experiment 11 is the Pandas experiment, this solution answers the same
scenario with pandas rather than plain NumPy.

Rubrics covered:
  * Series creation
  * correct use of aggregation functions (sum, mean, idxmax)
  * display of results
  * correct logic

Requires: pandas, numpy
"""

import numpy as np
import pandas as pd

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
        "Saturday", "Sunday"]
RAW = [1200, 1500, 900, 1800, 2100, 1600, 1900]


def main():
    sales = pd.Series(RAW, index=DAYS, name="sales_rupees")

    print("=== the Series ===")
    print(sales.to_string())
    print(f"\n  dtype {sales.dtype}, length {len(sales)}")

    total = sales.sum()
    average = sales.mean()
    best_day = sales.idxmax()

    print("\n=== required answers ===")
    print(f"  total sales       : Rs.{total:,}")
    print(f"  average sales     : Rs.{average:,.2f} per day")
    print(f"  maximum sales day : {best_day} (Rs.{sales.max():,})")
    print(f"  idxmax() returns the LABEL, argmax() the position "
          f"({sales.argmax()})")

    print("\n=== describe() ===")
    print(sales.describe().round(2).to_string())

    print("\n=== a DataFrame with derived columns ===")
    frame = pd.DataFrame({"sales": sales})
    frame["share_percent"] = (frame["sales"] / total * 100).round(2)
    frame["vs_average"] = (frame["sales"] - average).round(2)
    frame["cumulative"] = frame["sales"].cumsum()
    frame["change"] = frame["sales"].diff()
    frame["change_percent"] = (frame["sales"].pct_change() * 100).round(1)
    frame["is_weekend"] = frame.index.isin(["Saturday", "Sunday"])
    print(frame.to_string())

    print("\n=== days above the weekly average ===")
    above = sales[sales > average]
    print(above.to_string())
    print(f"  {len(above)} day(s), contributing Rs.{above.sum():,} "
          f"({above.sum() / total * 100:.1f}% of the week)")

    print("\n=== weekday vs weekend (groupby) ===")
    grouped = frame.groupby("is_weekend")["sales"].agg(
        ["count", "sum", "mean", "max"])
    grouped.index = ["Weekday", "Weekend"]
    print(grouped.round(2).to_string())
    uplift = (grouped.loc["Weekend", "mean"] /
              grouped.loc["Weekday", "mean"] - 1) * 100
    print(f"\n  weekend days average {uplift:+.1f}% versus weekdays")

    print("\n=== sorted, ranked ===")
    ranked = pd.DataFrame({
        "sales": sales.sort_values(ascending=False),
    })
    ranked["rank"] = range(1, len(ranked) + 1)
    ranked["gap_to_best"] = ranked["sales"] - ranked["sales"].max()
    print(ranked.to_string())

    print("\n=== rolling 3-day average ===")
    rolling = sales.rolling(window=3).mean().round(2)
    print(rolling.to_string())
    print(f"  best 3-day stretch ends on {rolling.idxmax()} "
          f"(Rs.{rolling.max():,.2f} per day)")

    print("\n=== text bar chart ===")
    for day, amount in sales.items():
        marker = "  <== best" if day == best_day else ""
        print(f"  {day:<11}Rs.{amount:>6,}  "
              f"{'#' * (amount // 100)}{marker}")

    print("\n=== what-if scenarios (vectorised) ===")
    scenarios = pd.DataFrame({
        "actual": sales,
        "plus_10pct": (sales * 1.10).round(0).astype(int),
        "gst_18pct": (sales * 0.18).round(2),
        "after_fixed_cost_300": sales - 300,
    })
    print(scenarios.to_string())
    print(f"\n  profit after Rs.300 daily cost: "
          f"Rs.{scenarios['after_fixed_cost_300'].sum():,}")

    target = 1500
    met = sales >= target
    print(f"\n=== Rs.{target:,} daily target ===")
    print(f"  days met : {int(met.sum())} of 7 "
          f"({met.mean() * 100:.1f}%)")
    print(f"  which    : {sales[met].index.tolist()}")
    print(f"  shortfall on the rest: "
          f"Rs.{int((target - sales[~met]).sum()):,}")

    print("\n=== resampling as a time series ===")
    dated = pd.Series(
        RAW, index=pd.date_range("2026-11-16", periods=7, freq="D"),
        name="sales_rupees")
    print(dated.to_string())
    print(f"\n  weekly total via resample('W'): "
          f"Rs.{int(dated.resample('W').sum().iloc[-1]):,}")
    print(f"  day-of-week labels: "
          f"{dated.index.day_name().tolist()}")


if __name__ == "__main__":
    main()
