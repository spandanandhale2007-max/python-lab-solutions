"""
Experiment 11 - Question 10: Electricity Consumption Analysis with Pandas

Scenario: A housing society records electricity consumption (in kWh) for
6 apartments over 7 days.

Task:
  1) Find the total consumption for each apartment (row-wise).
  2) Identify the apartment with the highest total consumption.

Note: the sheet repeats Experiment 10 Question 10 here; this version answers it
with Pandas, the topic of Experiment 11.

Rubrics covered:
  * correct DataFrame representation
  * row-wise operation using axis
  * correct identification of the highest consumer
  * output clarity

Requires: pandas, numpy
"""

import pandas as pd

FLATS = ["A-101", "A-102", "B-201", "B-202", "C-301", "C-302"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
TARIFF = 8.40          # Rs. per kWh


def main():
    df = pd.DataFrame(
        [[12.4, 11.8, 13.1, 12.0, 14.2, 18.5, 17.9],
         [8.2, 7.9, 8.6, 8.1, 9.0, 11.4, 10.8],
         [21.5, 22.8, 20.9, 23.4, 24.1, 27.6, 26.2],
         [5.1, 4.8, 5.4, 5.0, 5.6, 7.2, 6.9],
         [15.8, 16.4, 15.2, 16.9, 17.5, 20.3, 19.1],
         [10.2, 10.8, 9.9, 11.1, 11.8, 14.0, 13.2]],
        index=FLATS, columns=DAYS)
    df.index.name = "flat"
    df.columns.name = "day"

    print("=== consumption table (kWh) ===")
    print(df.to_string())
    print(f"\n  shape {df.shape}, {df.size} readings, tariff "
          f"Rs.{TARIFF:.2f}/kWh")

    # 1) row-wise total
    per_flat = df.sum(axis=1)
    print("\n=== 1) weekly total per apartment (axis=1) ===")
    print(per_flat.round(1).to_string())

    bills = pd.DataFrame({
        "total_kwh": per_flat.round(1),
        "daily_avg": df.mean(axis=1).round(2),
        "peak_day": df.idxmax(axis=1),
        "peak_kwh": df.max(axis=1),
        "weekly_bill": (per_flat * TARIFF).round(2),
        "share_percent": (per_flat / per_flat.sum() * 100).round(1),
    })
    print("\n" + bills.to_string())

    # 2) highest consumer
    top = per_flat.idxmax()
    print("\n=== 2) highest consumer ===")
    print(f"  per_flat.idxmax() -> {top}")
    print(f"  weekly total   : {per_flat.max():.1f} kWh")
    print(f"  daily average  : {df.loc[top].mean():.2f} kWh")
    print(f"  weekly bill    : Rs.{per_flat.max() * TARIFF:,.2f}")
    print(f"  readings       : {df.loc[top].tolist()}")
    print(f"  it used {per_flat.max() / per_flat.mean():.2f}x the society "
          f"average and {per_flat.max() / per_flat.min():.2f}x the lowest flat")
    print(f"\n  lowest consumer: {per_flat.idxmin()} "
          f"({per_flat.min():.1f} kWh, "
          f"Rs.{per_flat.min() * TARIFF:,.2f})")

    print("\n=== ranking ===")
    ranking = bills.sort_values("total_kwh", ascending=False).copy()
    ranking.insert(0, "rank", range(1, len(ranking) + 1))
    print(ranking[["rank", "total_kwh", "share_percent",
                   "weekly_bill"]].to_string())

    print("\n=== daily totals for the whole society (axis=0) ===")
    per_day = df.sum(axis=0)
    day_frame = pd.DataFrame({
        "total_kwh": per_day.round(1),
        "flat_avg": df.mean(axis=0).round(2),
        "top_flat": df.idxmax(axis=0),
    })
    print(day_frame.to_string())
    print(f"\n  busiest day : {per_day.idxmax()} ({per_day.max():.1f} kWh)")
    print(f"  quietest day: {per_day.idxmin()} ({per_day.min():.1f} kWh)")

    print("\n=== table with margins ===")
    with_margins = df.copy()
    with_margins["TOTAL"] = per_flat
    with_margins.loc["TOTAL"] = with_margins.sum(axis=0)
    print(with_margins.round(1).to_string())

    print("\n=== weekday vs weekend ===")
    weekday = df[["Mon", "Tue", "Wed", "Thu", "Fri"]]
    weekend = df[["Sat", "Sun"]]
    split = pd.DataFrame({
        "total_kwh": [weekday.to_numpy().sum().round(1),
                      weekend.to_numpy().sum().round(1)],
        "days": [5, 2],
        "per_day": [round(weekday.to_numpy().sum() / 5, 1),
                    round(weekend.to_numpy().sum() / 2, 1)],
    }, index=["Weekday", "Weekend"])
    print(split.to_string())
    uplift = split.loc["Weekend", "per_day"] / split.loc["Weekday", "per_day"]
    print(f"\n  weekend days use {(uplift - 1) * 100:+.1f}% more than weekdays")

    print("\n=== wing-level summary (groupby on the flat prefix) ===")
    wings = df.groupby(df.index.str[0]).sum()
    wing_summary = pd.DataFrame({
        "total_kwh": wings.sum(axis=1).round(1),
        "flats": df.groupby(df.index.str[0]).size(),
    })
    wing_summary["avg_per_flat"] = (
        wing_summary["total_kwh"] / wing_summary["flats"]).round(1)
    wing_summary["bill"] = (wing_summary["total_kwh"] * TARIFF).round(2)
    wing_summary.index.name = "wing"
    print(wing_summary.to_string())

    print("\n=== society billing summary ===")
    total = df.to_numpy().sum()
    print(f"  total units consumed : {total:.1f} kWh")
    print(f"  total bill           : Rs.{total * TARIFF:,.2f}")
    print(f"  average per flat     : {per_flat.mean():.2f} kWh "
          f"(Rs.{per_flat.mean() * TARIFF:,.2f})")
    print(f"  median per flat      : {per_flat.median():.2f} kWh")
    print(f"  standard deviation   : {per_flat.std():.2f} kWh")

    print("\n=== flats above the society average ===")
    above = per_flat[per_flat > per_flat.mean()]
    for flat, value in above.items():
        excess = value - per_flat.mean()
        print(f"  {flat:<8}{value:>8.1f} kWh  {excess:+.1f} above average "
              f"(Rs.{excess * TARIFF:,.2f} extra)")

    print("\n=== monthly slab projection ===")
    projection = pd.DataFrame({
        "weekly_kwh": per_flat.round(1),
        "projected_monthly": (per_flat / 7 * 30).round(1),
    })
    projection["slab"] = pd.cut(
        projection["projected_monthly"],
        bins=[0, 100, 150, float("inf")],
        labels=["low slab", "mid slab", "high slab"])
    print(projection.to_string())

    print("\n=== text chart of weekly totals ===")
    for flat, value in per_flat.sort_values(ascending=False).items():
        marker = "  <== highest" if flat == top else ""
        print(f"  {flat:<8}{value:>7.1f} kWh  "
              f"{'#' * int(value / 4)}{marker}")


if __name__ == "__main__":
    main()
