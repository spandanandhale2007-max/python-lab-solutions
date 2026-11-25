"""
Experiment 10 - Question 5: Product Inventory Check

Scenario: A shop records the number of products sold in 4 categories across
5 days.

Task:
  1) Represent this as a 2D array.
  2) Find the total items sold per category and per day.

Rubrics covered:
  * array creation
  * row-wise and column-wise sum (axis=1, axis=0)
  * clear display of both results
  * accuracy

Requires: numpy
"""

import numpy as np

CATEGORIES = ["Medicines", "Devices", "Protective", "Supplements"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]


def main():
    # 1) the 2D array: rows = categories, columns = days
    sold = np.array([
        [142, 158, 131, 177, 190],     # Medicines
        [ 18,  22,  15,  27,  31],     # Devices
        [ 64,  71,  58,  83,  92],     # Protective
        [ 35,  41,  29,  46,  52],     # Supplements
    ])

    print("=== 2D inventory array ===")
    print(f"  shape {sold.shape} -> "
          f"{sold.shape[0]} categories x {sold.shape[1]} days")
    print(f"  dtype {sold.dtype}, {sold.size} values")
    print(f"\n  {'category':<13}" + "".join(f"{d:>7}" for d in DAYS))
    print("  " + "-" * 48)
    for name, row in zip(CATEGORIES, sold):
        print(f"  {name:<13}" + "".join(f"{v:>7}" for v in row))

    # 2a) per category: sum across the days -> axis=1
    per_category = sold.sum(axis=1)
    # 2b) per day: sum across the categories -> axis=0
    per_day = sold.sum(axis=0)
    grand_total = sold.sum()

    print("\n=== total per category (axis=1, collapses days) ===")
    print(f"  sold.sum(axis=1) -> {per_category}")
    print(f"\n  {'category':<13}{'units':>8}{'share':>9}{'daily avg':>12}  bar")
    for name, total, avg in zip(CATEGORIES, per_category,
                                sold.mean(axis=1)):
        print(f"  {name:<13}{total:>8,}{total / grand_total * 100:>8.1f}%"
              f"{avg:>12.1f}  {'#' * (total // 25)}")

    print("\n=== total per day (axis=0, collapses categories) ===")
    print(f"  sold.sum(axis=0) -> {per_day}")
    print(f"\n  {'day':<6}{'units':>8}{'share':>9}  bar")
    for day, total in zip(DAYS, per_day):
        print(f"  {day:<6}{total:>8,}{total / grand_total * 100:>8.1f}%  "
              f"{'#' * (total // 20)}")

    print("\n=== cross-check ===")
    print(f"  grand total (sold.sum())        : {grand_total:,}")
    print(f"  sum of category totals          : {per_category.sum():,}")
    print(f"  sum of day totals               : {per_day.sum():,}")
    print(f"  all three agree                 : "
          f"{grand_total == per_category.sum() == per_day.sum()}")

    print("\n=== full table with margins ===")
    print(f"  {'category':<13}" + "".join(f"{d:>7}" for d in DAYS) +
          f"{'TOTAL':>9}")
    print("  " + "-" * 58)
    for name, row, total in zip(CATEGORIES, sold, per_category):
        print(f"  {name:<13}" + "".join(f"{v:>7}" for v in row) +
              f"{total:>9,}")
    print("  " + "-" * 58)
    print(f"  {'TOTAL':<13}" + "".join(f"{v:>7}" for v in per_day) +
          f"{grand_total:>9,}")

    print("\n=== highlights ===")
    print(f"  best-selling category : {CATEGORIES[per_category.argmax()]} "
          f"({per_category.max():,} units)")
    print(f"  slowest category      : {CATEGORIES[per_category.argmin()]} "
          f"({per_category.min():,} units)")
    print(f"  busiest day           : {DAYS[per_day.argmax()]} "
          f"({per_day.max():,} units)")
    print(f"  quietest day          : {DAYS[per_day.argmin()]} "
          f"({per_day.min():,} units)")
    r, c = np.unravel_index(sold.argmax(), sold.shape)
    print(f"  single biggest cell   : {CATEGORIES[r]} on {DAYS[c]} "
          f"({sold[r, c]} units)")

    print("\n=== percentage breakdown per day (keepdims broadcasting) ===")
    share = sold / sold.sum(axis=0, keepdims=True) * 100
    print(f"  {'category':<13}" + "".join(f"{d:>8}" for d in DAYS))
    for name, row in zip(CATEGORIES, share):
        print(f"  {name:<13}" + "".join(f"{v:>7.1f}%" for v in row))

    print("\n=== day-on-day growth, whole shop ===")
    change = np.diff(per_day)
    for i, delta in enumerate(change):
        pct = delta / per_day[i] * 100
        print(f"  {DAYS[i]} -> {DAYS[i + 1]} : {delta:>+5} units "
              f"({pct:>+6.1f}%)")

    print("\n=== restocking signal: categories averaging over 50 a day ===")
    avg_per_day = sold.mean(axis=1)
    mask = avg_per_day > 50
    for name, avg in zip(np.array(CATEGORIES)[mask], avg_per_day[mask]):
        print(f"  {name:<13}{avg:>6.1f} units/day -> order "
              f"{int(np.ceil(avg * 7))} for next week")

    print("\n=== cumulative sales through the week ===")
    cumulative = sold.cumsum(axis=1)
    print(f"  {'category':<13}" + "".join(f"{d:>8}" for d in DAYS))
    for name, row in zip(CATEGORIES, cumulative):
        print(f"  {name:<13}" + "".join(f"{v:>8,}" for v in row))


if __name__ == "__main__":
    main()
