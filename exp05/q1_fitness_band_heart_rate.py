"""
Experiment 5 - Question 1: Fitness Band Heart Rate

Scenario: A fitness band records the heart rate every minute for 10 minutes.
Analyse this data.

Rubrics covered:
  * random heart rate data generated
  * first 5 minutes indexed
  * min, max and average computed
  * high heart rate values (above 120 bpm) filtered
"""

import random

MINUTES = 10
HIGH_BPM = 120


def generate_heart_rate(seed=4):
    """Resting -> warm-up -> effort -> cool-down over 10 minutes."""
    random.seed(seed)
    shape = [72, 78, 88, 104, 118, 131, 138, 126, 108, 94]
    return [max(50, int(v + random.gauss(0, 5))) for v in shape]


def zone(bpm, age=20):
    max_hr = 220 - age
    pct = bpm / max_hr * 100
    if pct < 50:
        return "resting"
    if pct < 60:
        return "very light"
    if pct < 70:
        return "light"
    if pct < 80:
        return "moderate"
    if pct < 90:
        return "hard"
    return "maximum"


if __name__ == "__main__":
    bpm = generate_heart_rate()

    print("=== 10-minute heart rate log ===")
    for minute, value in enumerate(bpm, 1):
        bar = "#" * (value // 4)
        flag = "  HIGH" if value > HIGH_BPM else ""
        print(f"  min {minute:>2}: {value:>3} bpm  {zone(value):<11} "
              f"|{bar}{flag}")

    first5 = bpm[:5]                       # indexing / slicing
    last5 = bpm[5:]
    print("\n=== slices ===")
    print(f"  first 5 minutes : {first5}  avg {sum(first5) / 5:.1f} bpm")
    print(f"  last 5 minutes  : {last5}  avg {sum(last5) / 5:.1f} bpm")
    print(f"  minute 1 (bpm[0]) : {bpm[0]} bpm")
    print(f"  minute 10 (bpm[-1]): {bpm[-1]} bpm")
    print(f"  every 2nd minute   : {bpm[::2]}")

    print("\n=== statistics ===")
    print(f"  readings : {len(bpm)}")
    print(f"  minimum  : {min(bpm)} bpm at minute {bpm.index(min(bpm)) + 1}")
    print(f"  maximum  : {max(bpm)} bpm at minute {bpm.index(max(bpm)) + 1}")
    print(f"  average  : {sum(bpm) / len(bpm):.2f} bpm")
    print(f"  range    : {max(bpm) - min(bpm)} bpm")
    srt = sorted(bpm)
    median = (srt[4] + srt[5]) / 2
    print(f"  median   : {median:.1f} bpm")

    high = [(i + 1, v) for i, v in enumerate(bpm) if v > HIGH_BPM]
    print(f"\n=== high heart rate filter (above {HIGH_BPM} bpm) ===")
    print(f"  {len(high)} of {MINUTES} minutes exceeded the threshold")
    for minute, value in high:
        print(f"    minute {minute:>2}: {value} bpm ({value - HIGH_BPM:+} over)")
    if high:
        print(f"  time in the high zone: {len(high)} minute(s) "
              f"({len(high) / MINUTES * 100:.0f}% of the session)")
        print(f"  average while high   : "
              f"{sum(v for _, v in high) / len(high):.1f} bpm")
    else:
        print("  the user stayed in a safe zone throughout")

    print("\n=== recovery check ===")
    peak = max(bpm)
    recovery = peak - bpm[-1]
    print(f"  peak {peak} bpm -> final {bpm[-1]} bpm, dropped {recovery} bpm")
    print("  recovery:", "excellent" if recovery >= 30 else
          "good" if recovery >= 20 else "slow, cool down longer")

    print("\n=== time in each zone ===")
    zones = {}
    for v in bpm:
        zones[zone(v)] = zones.get(zone(v), 0) + 1
    for name, count in zones.items():
        print(f"  {name:<12} {count} minute(s)")
