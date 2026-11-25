"""
Experiment 4 - Question 9: Diet Calorie Balance

Scenario: A diet app tracks calorie intake per meal over a week
(3 meals per day). Review the diet balance.

Rubrics covered:
  * calorie data generated (21 values)
  * specific meals indexed (for example every breakfast)
  * average per meal type computed
  * high-calorie meals (above 700 calories) filtered
"""

import random

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MEALS = ["Breakfast", "Lunch", "Dinner"]
HIGH_CAL = 700


def generate_calories(seed=42):
    """21 values: day 0 breakfast, lunch, dinner, day 1 breakfast, ..."""
    random.seed(seed)
    typical = {"Breakfast": (280, 520), "Lunch": (520, 880), "Dinner": (430, 760)}
    data = []
    for day in DAYS:
        for meal in MEALS:
            lo, hi = typical[meal]
            bump = 180 if day in ("Sat", "Sun") else 0     # weekend treats
            data.append(random.randint(lo, hi) + bump)
    return data


def meal_index(day_i, meal_i):
    """Flat index for a (day, meal) pair in the 21-value list."""
    return day_i * len(MEALS) + meal_i


if __name__ == "__main__":
    calories = generate_calories()
    assert len(calories) == 21

    print("=== weekly calorie log (21 meals) ===")
    print(f"  {'Day':<6}" + "".join(f"{m:>12}" for m in MEALS) +
          f"{'TOTAL':>10}")
    for d, day in enumerate(DAYS):
        row = calories[d * 3:d * 3 + 3]
        print(f"  {day:<6}" + "".join(f"{v:>12}" for v in row) +
              f"{sum(row):>10}")

    print("\n=== indexing specific meals (slicing with a step) ===")
    breakfasts = calories[0::3]
    lunches = calories[1::3]
    dinners = calories[2::3]
    print(f"  every Breakfast (index 0::3) : {breakfasts}")
    print(f"  every Lunch     (index 1::3) : {lunches}")
    print(f"  every Dinner    (index 2::3) : {dinners}")
    print(f"  Wednesday lunch (index {meal_index(2, 1)})      : "
          f"{calories[meal_index(2, 1)]} kcal")
    print(f"  Sunday dinner   (index {meal_index(6, 2)})      : "
          f"{calories[meal_index(6, 2)]} kcal")

    print("\n=== average per meal type ===")
    for name, series in (("Breakfast", breakfasts), ("Lunch", lunches),
                         ("Dinner", dinners)):
        print(f"  {name:<10} avg {sum(series) / len(series):>7.1f} kcal   "
              f"min {min(series):>4}   max {max(series):>4}   "
              f"share {sum(series) / sum(calories) * 100:>5.1f}%")

    print("\n=== daily totals against a 2000 kcal target ===")
    for d, day in enumerate(DAYS):
        total = sum(calories[d * 3:d * 3 + 3])
        verdict = "over " if total > 2000 else "under"
        bar = "#" * (total // 60)
        print(f"  {day:<4} {total:>5} kcal  {verdict}  |{bar}")

    weekly = sum(calories)
    print(f"\n  weekly intake   : {weekly:,} kcal")
    print(f"  daily average   : {weekly / 7:.1f} kcal")
    print(f"  per-meal average: {weekly / 21:.1f} kcal")

    heavy = [(DAYS[i // 3], MEALS[i % 3], c)
             for i, c in enumerate(calories) if c > HIGH_CAL]
    print(f"\n=== high-calorie meals (above {HIGH_CAL} kcal): {len(heavy)} ===")
    for day, meal, c in heavy:
        print(f"  {day:<4} {meal:<10} {c:>5} kcal  "
              f"({c - HIGH_CAL:+} over the limit)")
    if heavy:
        print(f"  heaviest meal: {max(heavy, key=lambda t: t[2])}")

    print("\n=== balance check ===")
    weekend = sum(calories[15:])              # Sat + Sun
    weekdays = sum(calories[:15])
    print(f"  weekdays (Mon-Fri): {weekdays:,} kcal, "
          f"{weekdays / 5:.1f} per day")
    print(f"  weekend  (Sat-Sun): {weekend:,} kcal, "
          f"{weekend / 2:.1f} per day")
    print(f"  weekend excess    : {weekend / 2 - weekdays / 5:+.1f} kcal/day")
    print("  balance verdict   : " +
          ("well balanced across meal types"
           if max(sum(breakfasts), sum(lunches), sum(dinners)) /
           min(sum(breakfasts), sum(lunches), sum(dinners)) < 1.6
           else "intake is skewed towards one meal of the day"))
