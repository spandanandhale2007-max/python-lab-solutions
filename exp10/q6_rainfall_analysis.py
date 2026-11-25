"""
Experiment 10 - Question 6: Weather Dataset Operations

Scenario: Rainfall data (in mm) is available for 12 months.

Task:
  1) Compute the total and average annual rainfall.
  2) Identify the months with rainfall above 100 mm.

Rubrics covered:
  * array handling
  * use of aggregation functions (sum, mean)
  * logical indexing (> 100)
  * correct output

Requires: numpy
"""

import numpy as np

MONTHS = np.array(["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
THRESHOLD = 100.0


def main():
    # Pune-like monsoon pattern, mm per month
    rainfall = np.array([2.5, 1.0, 3.5, 12.0, 38.5, 142.0,
                         187.5, 164.0, 128.5, 74.0, 21.5, 6.0])

    print("=== the rainfall array ===")
    print(f"  values : {rainfall}")
    print(f"  shape {rainfall.shape}, dtype {rainfall.dtype}")

    total = rainfall.sum()
    average = rainfall.mean()

    print("\n=== 1) annual totals ===")
    print(f"  total annual rainfall   : {total:,.1f} mm")
    print(f"  average monthly rainfall: {average:,.2f} mm")
    print(f"  median                  : {np.median(rainfall):,.2f} mm")
    print(f"  standard deviation      : {rainfall.std():,.2f} mm")
    print(f"  wettest month           : {MONTHS[rainfall.argmax()]} "
          f"({rainfall.max():,.1f} mm)")
    print(f"  driest month            : {MONTHS[rainfall.argmin()]} "
          f"({rainfall.min():,.1f} mm)")

    print("\n=== monthly chart ===")
    print(f"  {'month':<7}{'mm':>8}{'share':>9}  bar")
    for month, mm in zip(MONTHS, rainfall):
        flag = "  <== above 100 mm" if mm > THRESHOLD else ""
        print(f"  {month:<7}{mm:>8.1f}{mm / total * 100:>8.1f}%  "
              f"{'#' * int(mm / 4)}{flag}")

    # 2) logical indexing
    mask = rainfall > THRESHOLD
    heavy_months = MONTHS[mask]
    heavy_values = rainfall[mask]

    print(f"\n=== 2) months above {THRESHOLD:.0f} mm (logical indexing) ===")
    print(f"  mask            : {mask}")
    print(f"  np.where(mask)  : {np.where(mask)[0]}")
    print(f"  months          : {heavy_months.tolist()}")
    print(f"  values          : {heavy_values}")
    print(f"  count           : {int(mask.sum())} of {rainfall.size}")
    print(f"  they carry      : {heavy_values.sum():,.1f} mm "
          f"({heavy_values.sum() / total * 100:.1f}% of the annual rainfall)")
    print(f"  their average   : {heavy_values.mean():,.2f} mm")

    print("\n  month by month:")
    for month, mm in zip(heavy_months, heavy_values):
        print(f"    {month:<5}{mm:>8.1f} mm  ({mm - THRESHOLD:+.1f} mm "
              f"above the threshold)")

    print("\n=== how the count changes with the threshold ===")
    for t in (50, 75, 100, 125, 150, 175):
        picked = MONTHS[rainfall > t]
        print(f"  above {t:>3} mm : {len(picked)} month(s)  "
              f"{picked.tolist()}")

    print("\n=== seasonal split (reshape into quarters) ===")
    quarters = rainfall.reshape(4, 3)
    labels = ["Q1 Jan-Mar", "Q2 Apr-Jun", "Q3 Jul-Sep", "Q4 Oct-Dec"]
    print(f"  reshaped to {quarters.shape}")
    for label, row, q_total in zip(labels, quarters, quarters.sum(axis=1)):
        print(f"  {label:<12}{row}  total {q_total:>7.1f} mm  "
              f"({q_total / total * 100:>5.1f}%)")
    print(f"\n  wettest quarter : {labels[quarters.sum(axis=1).argmax()]}")

    monsoon = rainfall[5:9]            # Jun to Sep
    rest = np.concatenate([rainfall[:5], rainfall[9:]])
    print("\n=== monsoon (Jun-Sep) vs the rest of the year ===")
    print(f"  monsoon    : {monsoon.sum():>7.1f} mm over 4 months  "
          f"(avg {monsoon.mean():.1f} mm)")
    print(f"  other      : {rest.sum():>7.1f} mm over 8 months  "
          f"(avg {rest.mean():.1f} mm)")
    print(f"  monsoon share: {monsoon.sum() / total * 100:.1f}% of the year")

    print("\n=== cumulative rainfall ===")
    cumulative = rainfall.cumsum()
    for month, value in zip(MONTHS, cumulative):
        print(f"  by end of {month} : {value:>8.1f} mm  "
              f"({value / total * 100:>5.1f}% of the year)")

    print("\n=== month-on-month change ===")
    change = np.diff(rainfall)
    print(f"  biggest rise : {MONTHS[change.argmax() + 1]} "
          f"({change.max():+.1f} mm)")
    print(f"  biggest fall : {MONTHS[change.argmin() + 1]} "
          f"({change.min():+.1f} mm)")

    print("\n=== dry months (under 10 mm) ===")
    dry = rainfall < 10
    print(f"  {MONTHS[dry].tolist()} -> {rainfall[dry]} mm")
    print(f"  {int(dry.sum())} effectively dry month(s)")

    print("\n=== np.select classification ===")
    labels_rain = np.select(
        [rainfall > 150, rainfall > 100, rainfall > 50, rainfall > 10],
        ["very heavy", "heavy", "moderate", "light"], default="negligible")
    for month, mm, label in zip(MONTHS, rainfall, labels_rain):
        print(f"  {month:<5}{mm:>8.1f} mm  {label}")


if __name__ == "__main__":
    main()
