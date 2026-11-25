"""
Experiment 6 - Question 1: Fitness Band Heart Rate Analysis

Scenario: A fitness band records the heart rate every minute for 10 minutes.
Analyse this data.

Note: the question sheet repeats this scenario from Experiment 5 Question 1.
This version answers the same rubrics using the statistics module and a
10-minute session stored as a list of (minute, bpm) pairs, so the two
submissions are not identical code.

Rubrics covered:
  * random heart rate data generated
  * first 5 minutes indexed
  * min, max and average computed
  * high heart rate values (above 120 bpm) filtered
"""

import random
import statistics

MINUTES = 10
HIGH_BPM = 120
RESTING = 68


def generate_session(seed=52):
    """Returns a list of (minute, bpm) tuples for a 10-minute workout."""
    random.seed(seed)
    profile = [0.05, 0.18, 0.42, 0.68, 0.86, 1.00, 0.95, 0.72, 0.44, 0.22]
    peak_extra = 80                       # bpm added at full effort
    return [(minute + 1, int(RESTING + peak_extra * factor + random.gauss(0, 4)))
            for minute, factor in enumerate(profile)]


def effort_label(bpm):
    if bpm > HIGH_BPM:
        return "HIGH"
    if bpm > 100:
        return "moderate"
    if bpm > 80:
        return "light"
    return "resting"


if __name__ == "__main__":
    session = generate_session()
    bpm_values = [bpm for _, bpm in session]

    print("=== session log ===")
    print(f"  {'minute':<8}{'bpm':>6}{'zone':>12}   trace")
    for minute, bpm in session:
        print(f"  {minute:<8}{bpm:>6}{effort_label(bpm):>12}   "
              f"{'*' * ((bpm - 60) // 3)}")

    print("\n=== indexing ===")
    first_five = session[:5]
    second_five = session[5:]
    print(f"  first 5 minutes  : {[b for _, b in first_five]}")
    print(f"  last 5 minutes   : {[b for _, b in second_five]}")
    print(f"  minute 1         : {session[0][1]} bpm")
    print(f"  minute 6 (peak)  : {session[5][1]} bpm")
    print(f"  final minute     : {session[-1][1]} bpm")
    print(f"  first-half avg   : "
          f"{statistics.mean(b for _, b in first_five):.2f} bpm")
    print(f"  second-half avg  : "
          f"{statistics.mean(b for _, b in second_five):.2f} bpm")

    print("\n=== statistics (statistics module) ===")
    print(f"  readings            : {len(bpm_values)}")
    print(f"  minimum             : {min(bpm_values)} bpm "
          f"(minute {bpm_values.index(min(bpm_values)) + 1})")
    print(f"  maximum             : {max(bpm_values)} bpm "
          f"(minute {bpm_values.index(max(bpm_values)) + 1})")
    print(f"  mean                : {statistics.mean(bpm_values):.2f} bpm")
    print(f"  median              : {statistics.median(bpm_values):.1f} bpm")
    print(f"  standard deviation  : {statistics.stdev(bpm_values):.2f} bpm")
    print(f"  spread              : {max(bpm_values) - min(bpm_values)} bpm")

    high = [(m, b) for m, b in session if b > HIGH_BPM]
    print(f"\n=== high heart rate filter (above {HIGH_BPM} bpm) ===")
    if high:
        for minute, bpm in high:
            print(f"  minute {minute:>2}: {bpm} bpm  "
                  f"({bpm - HIGH_BPM:+} over the threshold)")
        print(f"\n  minutes in the high zone : {len(high)}/{MINUTES} "
              f"({len(high) / MINUTES * 100:.0f}%)")
        print(f"  average while high       : "
              f"{statistics.mean(b for _, b in high):.1f} bpm")
        print(f"  peak effort              : {max(b for _, b in high)} bpm")
    else:
        print("  no reading crossed the threshold")

    print("\n=== calorie estimate (rough, 20-year-old, 65 kg) ===")
    # Keytel formula, simplified for a one-minute step
    kcal = sum((-55.0969 + 0.6309 * b + 0.1988 * 65 + 0.2017 * 20) / 4.184
               for _, b in session)
    print(f"  approximately {kcal:.1f} kcal burned in {MINUTES} minutes")

    print("\n=== recovery ===")
    drop = max(bpm_values) - bpm_values[-1]
    print(f"  peak {max(bpm_values)} -> final {bpm_values[-1]} bpm "
          f"(down {drop} bpm)")
    print("  recovery rating:", "excellent" if drop >= 40 else
          "good" if drop >= 25 else "take a longer cool-down")
