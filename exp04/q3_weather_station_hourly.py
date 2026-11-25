"""
Experiment 4 - Question 3: Weather Station Daily Trend

Scenario: A weather station records the temperature every hour for a day
(24 hours). Analyse the daily trend.

Rubrics covered:
  * temperature data generated
  * min, max and average computed
"""

import random

HOURS = 24


def generate_temperatures(seed=11):
    """Realistic daily curve: cool at dawn, hottest mid-afternoon."""
    random.seed(seed)
    base = [22, 21.5, 21, 20.5, 20, 20.5, 22, 24, 26.5, 29, 31, 33,
            34.5, 35.5, 35, 34, 32.5, 30.5, 28.5, 27, 26, 25, 24, 23]
    return [round(t + random.uniform(-1.2, 1.2), 1) for t in base]


def summarise(temps):
    return {
        "count": len(temps),
        "min": min(temps),
        "min_hour": temps.index(min(temps)),
        "max": max(temps),
        "max_hour": temps.index(max(temps)),
        "avg": sum(temps) / len(temps),
        "range": max(temps) - min(temps),
    }


def bar(value, lo, hi, width=40):
    filled = int((value - lo) / (hi - lo) * width) if hi > lo else 0
    return "#" * filled


if __name__ == "__main__":
    temps = generate_temperatures()

    print("=== hourly temperature log (24 readings, degrees C) ===")
    for hour, t in enumerate(temps):
        print(f"  {hour:02d}:00  {t:>5.1f} C")

    s = summarise(temps)
    print("\n=== daily summary ===")
    print(f"  readings        : {s['count']}")
    print(f"  minimum         : {s['min']:.1f} C at {s['min_hour']:02d}:00")
    print(f"  maximum         : {s['max']:.1f} C at {s['max_hour']:02d}:00")
    print(f"  average         : {s['avg']:.2f} C")
    print(f"  diurnal range   : {s['range']:.1f} C")

    print("\n=== shape of the day ===")
    lo, hi = s["min"], s["max"]
    for hour, t in enumerate(temps):
        mark = ""
        if t == hi:
            mark = "  <- hottest"
        elif t == lo:
            mark = "  <- coldest"
        print(f"  {hour:02d}:00 {t:>5.1f} |{bar(t, lo, hi):<40}|{mark}")

    print("\n=== above / below the daily average ===")
    above = [(h, t) for h, t in enumerate(temps) if t > s["avg"]]
    below = [(h, t) for h, t in enumerate(temps) if t <= s["avg"]]
    print(f"  {len(above)} hour(s) above {s['avg']:.2f} C: "
          f"{[f'{h:02d}:00' for h, _ in above]}")
    print(f"  {len(below)} hour(s) at or below average")

    print("\n=== hour-to-hour change ===")
    deltas = [round(temps[i] - temps[i - 1], 1) for i in range(1, len(temps))]
    steepest_rise = max(deltas)
    steepest_fall = min(deltas)
    print(f"  fastest warming : {steepest_rise:+.1f} C/h between "
          f"{deltas.index(steepest_rise):02d}:00 and "
          f"{deltas.index(steepest_rise) + 1:02d}:00")
    print(f"  fastest cooling : {steepest_fall:+.1f} C/h between "
          f"{deltas.index(steepest_fall):02d}:00 and "
          f"{deltas.index(steepest_fall) + 1:02d}:00")

    print("\n=== three-hour blocks ===")
    for start in range(0, HOURS, 3):
        block = temps[start:start + 3]
        print(f"  {start:02d}:00-{start + 2:02d}:59  "
              f"avg {sum(block) / len(block):>5.1f} C  "
              f"min {min(block):>5.1f}  max {max(block):>5.1f}")
