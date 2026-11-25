"""
Experiment 11 - Question 5: Product Inventory Check with Pandas

Scenario: A shop records the number of products sold in 4 categories across
5 days.

Task:
  1) Represent this as a DataFrame.
  2) Find the total items sold per category and per day.

Note: the sheet repeats Experiment 10 Question 5 here; this version answers it
with Pandas, the topic of Experiment 11.

Rubrics covered:
  * DataFrame creation
  * row-wise and column-wise sum (axis=1, axis=0)
  * clear display of both results
  * accuracy

Requires: pandas, numpy
"""

import pandas as pd

CATEGORIES = ["Medicines", "Devices", "Protective", "Supplements"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]


def main():
    sold = pd.DataFrame(
        [[142, 158, 131, 177, 190],
         [18, 22, 15, 27, 31],
         [64, 71, 58, 83, 92],
         [35, 41, 29, 46, 52]],
        index=CATEGORIES, columns=DAYS)
    sold.index.name = "category"
    sold.columns.name = "day"

    print("=== the DataFrame ===")
    print(sold.to_string())
    print(f"\n  shape {sold.shape}, {sold.size} values")

    per_category = sold.sum(axis=1)     # collapse days
    per_day = sold.sum(axis=0)          # collapse categories
    grand_total = sold.to_numpy().sum()

    print("\n=== 1) total per category (axis=1) ===")
    print(per_category.to_string())

    cat_summary = pd.DataFrame({
        "total": per_category,
        "daily_avg": sold.mean(axis=1).round(1),
        "best_day": sold.idxmax(axis=1),
        "peak": sold.max(axis=1),
        "share_percent": (per_category / grand_total * 100).round(1),
    })
    print("\n" + cat_summary.to_string())

    print("\n=== 2) total per day (axis=0) ===")
    print(per_day.to_string())

    day_summary = pd.DataFrame({
        "total": per_day,
        "category_avg": sold.mean(axis=0).round(1),
        "top_category": sold.idxmax(axis=0),
        "share_percent": (per_day / grand_total * 100).round(1),
    })
    print("\n" + day_summary.to_string())

    print("\n=== cross-check ===")
    print(f"  grand total              : {grand_total:,}")
    print(f"  sum of category totals   : {per_category.sum():,}")
    print(f"  sum of day totals        : {per_day.sum():,}")
    print(f"  all three agree          : "
          f"{grand_total == per_category.sum() == per_day.sum()}")

    print("\n=== table with margins (the Pandas way) ===")
    with_margins = sold.copy()
    with_margins["TOTAL"] = per_category
    with_margins.loc["TOTAL"] = with_margins.sum(axis=0)
    print(with_margins.to_string())

    print("\n=== highlights ===")
    print(f"  best-selling category : {per_category.idxmax()} "
          f"({per_category.max():,} units)")
    print(f"  slowest category      : {per_category.idxmin()} "
          f"({per_category.min():,} units)")
    print(f"  busiest day           : {per_day.idxmax()} "
          f"({per_day.max():,} units)")
    print(f"  quietest day          : {per_day.idxmin()} "
          f"({per_day.min():,} units)")
    peak = sold.stack().idxmax()
    print(f"  single biggest cell   : {peak[0]} on {peak[1]} "
          f"({sold.stack().max()} units)")

    print("\n=== percentage of each day's sales, by category ===")
    share = (sold / per_day * 100).round(1)
    print(share.to_string())

    print("\n=== day-on-day change, whole shop ===")
    change = pd.DataFrame({
        "total": per_day,
        "change": per_day.diff(),
        "change_percent": (per_day.pct_change() * 100).round(1),
    })
    print(change.to_string())

    print("\n=== cumulative sales through the week ===")
    print(sold.cumsum(axis=1).to_string())

    print("\n=== long format and groupby ===")
    long = sold.reset_index().melt(id_vars="category", var_name="day",
                                   value_name="units")
    print(long.head(6).to_string(index=False))
    print(f"\n  rows: {len(long)}")
    print("\n  groupby category:")
    print(long.groupby("category")["units"].agg(
        ["sum", "mean", "max"]).round(1).to_string())
    print("\n  groupby day:")
    print(long.groupby("day", sort=False)["units"].agg(
        ["sum", "mean"]).round(1).to_string())

    print("\n=== pivot_table reproduces the original layout ===")
    pivot = long.pivot_table(index="category", columns="day",
                             values="units", aggfunc="sum")
    pivot = pivot[DAYS]
    print(pivot.to_string())
    print(f"  identical to the source frame: "
          f"{pivot.equals(sold)}")

    print("\n=== restocking signal: categories averaging over 50 a day ===")
    avg = sold.mean(axis=1)
    for name, value in avg[avg > 50].items():
        print(f"  {name:<13}{value:>6.1f} units/day -> order "
              f"{int(round(value * 7))} for next week")

    print("\n=== text bar chart of category totals ===")
    for name, total in per_category.sort_values(ascending=False).items():
        print(f"  {name:<13}{total:>6,}  {'#' * (total // 25)}")


if __name__ == "__main__":
    main()
