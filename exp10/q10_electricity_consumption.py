"""
Experiment 10 - Question 10: Electricity Consumption Analysis

Scenario: A housing society records electricity consumption (in kWh) for
6 apartments over 7 days in a 6x7 NumPy array.

Task:
  1) Find the total consumption for each apartment (row-wise).
  2) Identify the apartment with the highest total consumption.

Rubrics covered:
  * correct 2D array representation
  * row-wise operation using axis
  * correct identification of the highest consumer
  * output clarity

Requires: numpy
"""

import numpy as np

FLATS = ["A-101", "A-102", "B-201", "B-202", "C-301", "C-302"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
TARIFF = 8.40          # Rs. per kWh


def main():
    usage = np.array([
        [12.4, 11.8, 13.1, 12.0, 14.2, 18.5, 17.9],    # A-101
        [ 8.2,  7.9,  8.6,  8.1,  9.0, 11.4, 10.8],    # A-102
        [21.5, 22.8, 20.9, 23.4, 24.1, 27.6, 26.2],    # B-201
        [ 5.1,  4.8,  5.4,  5.0,  5.6,  7.2,  6.9],    # B-202
        [15.8, 16.4, 15.2, 16.9, 17.5, 20.3, 19.1],    # C-301
        [10.2, 10.8,  9.9, 11.1, 11.8, 14.0, 13.2],    # C-302
    ])

    print("=== 6x7 consumption array (kWh) ===")
    print(f"  shape {usage.shape} -> "
          f"{usage.shape[0]} apartments x {usage.shape[1]} days")
    print(f"  dtype {usage.dtype}, {usage.size} readings")
    print(f"\n  {'flat':<8}" + "".join(f"{d:>8}" for d in DAYS))
    print("  " + "-" * 64)
    for name, row in zip(FLATS, usage):
        print(f"  {name:<8}" + "".join(f"{v:>8.1f}" for v in row))

    # 1) row-wise total, axis=1 collapses the days
    per_flat = usage.sum(axis=1)

    print("\n=== 1) weekly total per apartment (axis=1) ===")
    print(f"  usage.sum(axis=1) -> {np.round(per_flat, 1)}")
    print(f"\n  {'flat':<8}{'total kWh':>11}{'daily avg':>12}"
          f"{'peak day':>11}{'bill':>12}  bar")
    for name, total, avg, peak in zip(FLATS, per_flat, usage.mean(axis=1),
                                      usage.argmax(axis=1)):
        print(f"  {name:<8}{total:>11.1f}{avg:>12.2f}"
              f"{DAYS[peak]:>11}{total * TARIFF:>11,.2f}  "
              f"{'#' * int(total / 4)}")

    # 2) the highest consumer
    top = per_flat.argmax()

    print("\n=== 2) highest consumer ===")
    print(f"  per_flat.argmax() -> index {top}")
    print(f"  apartment         : {FLATS[top]}")
    print(f"  weekly total      : {per_flat[top]:.1f} kWh")
    print(f"  daily average     : {usage[top].mean():.2f} kWh")
    print(f"  weekly bill       : Rs.{per_flat[top] * TARIFF:,.2f}")
    print(f"  readings          : {usage[top]}")
    print(f"  it used {per_flat[top] / per_flat.mean():.2f}x the society "
          f"average and {per_flat[top] / per_flat.min():.2f}x the lowest flat")

    print(f"\n  lowest consumer   : {FLATS[per_flat.argmin()]} "
          f"({per_flat.min():.1f} kWh, Rs.{per_flat.min() * TARIFF:,.2f})")

    print("\n=== consumption ranking ===")
    order = np.argsort(-per_flat)
    print(f"  {'rank':<6}{'flat':<8}{'kWh':>9}{'share':>9}{'bill':>12}")
    for rank, i in enumerate(order, 1):
        print(f"  {rank:<6}{FLATS[i]:<8}{per_flat[i]:>9.1f}"
              f"{per_flat[i] / per_flat.sum() * 100:>8.1f}%"
              f"{per_flat[i] * TARIFF:>11,.2f}")

    print("\n=== daily totals for the whole society (axis=0) ===")
    per_day = usage.sum(axis=0)
    print(f"  usage.sum(axis=0) -> {np.round(per_day, 1)}")
    for day, total in zip(DAYS, per_day):
        print(f"  {day:<5}{total:>8.1f} kWh  {'#' * int(total / 3)}")
    print(f"\n  busiest day : {DAYS[per_day.argmax()]} "
          f"({per_day.max():.1f} kWh)")
    print(f"  quietest day: {DAYS[per_day.argmin()]} "
          f"({per_day.min():.1f} kWh)")

    print("\n=== weekday vs weekend ===")
    weekday = usage[:, :5]
    weekend = usage[:, 5:]
    print(f"  weekday total : {weekday.sum():>8.1f} kWh over 5 days "
          f"(avg {weekday.sum() / 5:.1f} kWh/day)")
    print(f"  weekend total : {weekend.sum():>8.1f} kWh over 2 days "
          f"(avg {weekend.sum() / 2:.1f} kWh/day)")
    print(f"  weekend uplift: "
          f"{(weekend.sum() / 2) / (weekday.sum() / 5) * 100 - 100:+.1f}%")

    print("\n=== full table with margins ===")
    print(f"  {'flat':<8}" + "".join(f"{d:>8}" for d in DAYS) +
          f"{'TOTAL':>10}")
    print("  " + "-" * 74)
    for name, row, total in zip(FLATS, usage, per_flat):
        print(f"  {name:<8}" + "".join(f"{v:>8.1f}" for v in row) +
              f"{total:>10.1f}")
    print("  " + "-" * 74)
    print(f"  {'TOTAL':<8}" + "".join(f"{v:>8.1f}" for v in per_day) +
          f"{usage.sum():>10.1f}")

    print("\n=== society billing summary ===")
    print(f"  total units consumed : {usage.sum():.1f} kWh")
    print(f"  tariff               : Rs.{TARIFF:.2f} per kWh")
    print(f"  total bill           : Rs.{usage.sum() * TARIFF:,.2f}")
    print(f"  average per flat     : {per_flat.mean():.2f} kWh "
          f"(Rs.{per_flat.mean() * TARIFF:,.2f})")
    print(f"  median per flat      : {np.median(per_flat):.2f} kWh")
    print(f"  standard deviation   : {per_flat.std():.2f} kWh")

    print("\n=== flats above the society average ===")
    mask = per_flat > per_flat.mean()
    for name, total in zip(np.array(FLATS)[mask], per_flat[mask]):
        excess = total - per_flat.mean()
        print(f"  {name:<8}{total:>8.1f} kWh  "
              f"{excess:+.1f} kWh above average "
              f"(Rs.{excess * TARIFF:,.2f} extra)")

    print("\n=== slab check (over 150 kWh a month attracts a higher tariff) ===")
    projected = per_flat / 7 * 30
    for name, month in zip(FLATS, projected):
        slab = ("high slab" if month > 150 else
                "mid slab" if month > 100 else "low slab")
        print(f"  {name:<8}projected {month:>7.1f} kWh/month  {slab}")


if __name__ == "__main__":
    main()
