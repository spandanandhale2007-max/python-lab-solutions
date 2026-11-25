"""
Experiment 11 - Question 6: Weather Dataset Operations with Pandas

Scenario: Rainfall data (in mm) for 12 months.

Task:
  1) Compute the total and average annual rainfall.
  2) Identify the months with rainfall above 100 mm.

Note: the sheet repeats Experiment 10 Question 6 here; this version answers it
with Pandas, the topic of Experiment 11.

Rubrics covered:
  * Series handling
  * use of aggregation functions (sum, mean)
  * boolean indexing (> 100)
  * correct output

Requires: pandas, numpy
"""

import numpy as np
import pandas as pd

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
THRESHOLD = 100.0


def main():
    rainfall = pd.Series(
        [2.5, 1.0, 3.5, 12.0, 38.5, 142.0, 187.5, 164.0, 128.5, 74.0,
         21.5, 6.0],
        index=MONTHS, name="rainfall_mm")
    rainfall.index.name = "month"

    print("=== the Series ===")
    print(rainfall.to_string())
    print(f"\n  dtype {rainfall.dtype}, {len(rainfall)} months")

    total = rainfall.sum()
    average = rainfall.mean()

    print("\n=== 1) annual totals ===")
    print(f"  total annual rainfall    : {total:,.1f} mm")
    print(f"  average monthly rainfall : {average:,.2f} mm")
    print(f"  median                   : {rainfall.median():,.2f} mm")
    print(f"  standard deviation       : {rainfall.std():,.2f} mm")
    print(f"  wettest month            : {rainfall.idxmax()} "
          f"({rainfall.max():,.1f} mm)")
    print(f"  driest month             : {rainfall.idxmin()} "
          f"({rainfall.min():,.1f} mm)")

    print("\n=== describe() ===")
    print(rainfall.describe().round(2).to_string())

    print("\n=== monthly frame with derived columns ===")
    frame = pd.DataFrame({"rainfall_mm": rainfall})
    frame["share_percent"] = (frame["rainfall_mm"] / total * 100).round(1)
    frame["cumulative_mm"] = frame["rainfall_mm"].cumsum()
    frame["change"] = frame["rainfall_mm"].diff()
    frame["above_threshold"] = frame["rainfall_mm"] > THRESHOLD
    frame["category"] = pd.cut(
        frame["rainfall_mm"],
        bins=[-0.01, 10, 50, 100, 150, np.inf],
        labels=["negligible", "light", "moderate", "heavy", "very heavy"])
    print(frame.to_string())

    # 2) boolean indexing
    heavy = rainfall[rainfall > THRESHOLD]

    print(f"\n=== 2) months above {THRESHOLD:.0f} mm ===")
    print(heavy.to_string())
    print(f"\n  count          : {len(heavy)} of {len(rainfall)}")
    print(f"  months         : {heavy.index.tolist()}")
    print(f"  combined total : {heavy.sum():,.1f} mm "
          f"({heavy.sum() / total * 100:.1f}% of the annual rainfall)")
    print(f"  their average  : {heavy.mean():,.2f} mm")
    for month, mm in heavy.items():
        print(f"    {month:<5}{mm:>8.1f} mm  "
              f"({mm - THRESHOLD:+.1f} mm above the threshold)")

    print("\n=== how the count changes with the threshold ===")
    for t in (50, 75, 100, 125, 150, 175):
        picked = rainfall[rainfall > t]
        print(f"  above {t:>3} mm : {len(picked)} month(s)  "
              f"{picked.index.tolist()}")

    print("\n=== quarterly split (groupby) ===")
    quarter_map = {m: f"Q{i // 3 + 1}" for i, m in enumerate(MONTHS)}
    by_quarter = rainfall.groupby(rainfall.index.map(quarter_map)).agg(
        ["sum", "mean", "max"]).round(2)
    by_quarter["share_percent"] = (by_quarter["sum"] / total * 100).round(1)
    print(by_quarter.to_string())
    print(f"\n  wettest quarter : {by_quarter['sum'].idxmax()} "
          f"({by_quarter['sum'].max():,.1f} mm)")

    print("\n=== monsoon (Jun-Sep) vs the rest of the year ===")
    is_monsoon = rainfall.index.isin(["Jun", "Jul", "Aug", "Sep"])
    monsoon = rainfall[is_monsoon]
    rest = rainfall[~is_monsoon]
    season = pd.DataFrame({
        "months": [len(monsoon), len(rest)],
        "total_mm": [monsoon.sum(), rest.sum()],
        "avg_mm": [monsoon.mean().round(2), rest.mean().round(2)],
        "share_percent": [round(monsoon.sum() / total * 100, 1),
                          round(rest.sum() / total * 100, 1)],
    }, index=["Monsoon Jun-Sep", "Rest of year"])
    print(season.to_string())

    print("\n=== 3-month rolling average ===")
    rolling = rainfall.rolling(window=3).mean().round(2)
    print(rolling.to_string())
    print(f"\n  wettest 3-month window ends in {rolling.idxmax()} "
          f"({rolling.max():.2f} mm/month)")

    print("\n=== category counts ===")
    counts = frame["category"].value_counts().sort_index()
    for label, n in counts.items():
        print(f"  {str(label):<12}{n:>3} month(s)  {'#' * n}")

    print("\n=== rank and sort ===")
    ranked = pd.DataFrame({
        "rainfall_mm": rainfall.sort_values(ascending=False),
    })
    ranked["rank"] = range(1, len(ranked) + 1)
    print(ranked.to_string())

    print("\n=== text chart ===")
    for month, mm in rainfall.items():
        flag = "  <== above 100 mm" if mm > THRESHOLD else ""
        print(f"  {month:<5}{mm:>8.1f}  {'#' * int(mm / 4)}{flag}")

    print("\n=== as a proper time series ===")
    dated = pd.Series(
        rainfall.to_numpy(),
        index=pd.date_range("2026-01-31", periods=12, freq="ME"),
        name="rainfall_mm")
    print(f"  quarterly resample:")
    print(dated.resample("QE").sum().round(1).to_string())


if __name__ == "__main__":
    main()
