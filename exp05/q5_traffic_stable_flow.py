"""
Experiment 5 - Question 5: Longest Stable Traffic Flow

Scenario: A traffic monitoring system counts cars each minute at a junction.
Find the longest stable flow.

Rubrics covered:
  * minute-wise traffic counts generated
  * a stable flow range defined (40-60 cars)
  * the longest sequence within that range identified
  * DP used to track stable streaks
"""

import random

MINUTES = 40
STABLE_LOW, STABLE_HIGH = 40, 60


def generate_counts(seed=25):
    """Mostly stable traffic with a few surges and lulls."""
    random.seed(seed)
    data = []
    for minute in range(MINUTES):
        roll = random.random()
        if roll < 0.18:
            data.append(random.randint(61, 95))        # surge
        elif roll < 0.30:
            data.append(random.randint(12, 39))        # lull
        else:
            data.append(random.randint(STABLE_LOW, STABLE_HIGH))
    return data


def longest_stable_dp(counts, low, high):
    """dp[i] = length of the stable run ending at minute i.
    dp[i] = dp[i-1] + 1 if counts[i] is in range, else 0."""
    dp = [0] * len(counts)
    for i, v in enumerate(counts):
        if low <= v <= high:
            dp[i] = (dp[i - 1] + 1) if i > 0 else 1
        else:
            dp[i] = 0
    best = max(dp) if dp else 0
    end = dp.index(best) if best else -1
    return best, end - best + 1, dp


def all_stable_runs(counts, low, high):
    runs, start = [], None
    for i, v in enumerate(counts):
        inside = low <= v <= high
        if inside and start is None:
            start = i
        elif not inside and start is not None:
            runs.append((start, i - 1))
            start = None
    if start is not None:
        runs.append((start, len(counts) - 1))
    return runs


def lcs_with_stable_pattern(counts, low, high):
    """LCS-style view: compare the real series against an ideal stable
    series of the same length and count how much of it lines up."""
    ideal = [(low + high) // 2] * len(counts)
    n = len(counts)
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if low <= counts[i - 1] <= high and abs(counts[i - 1] - ideal[j - 1]) <= 10:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[n][n]


if __name__ == "__main__":
    counts = generate_counts()

    print(f"=== car counts per minute (stable band {STABLE_LOW}-"
          f"{STABLE_HIGH}) ===")
    for i, v in enumerate(counts):
        inside = STABLE_LOW <= v <= STABLE_HIGH
        tag = "stable" if inside else ("SURGE " if v > STABLE_HIGH else "lull  ")
        print(f"  min {i:>2}: {v:>3} cars  {tag} |{'#' * (v // 3)}")

    stable_values = [v for v in counts if STABLE_LOW <= v <= STABLE_HIGH]
    print("\n=== overall ===")
    print(f"  minutes monitored : {MINUTES}")
    print(f"  average flow      : {sum(counts) / MINUTES:.2f} cars/min")
    print(f"  minutes in band   : {len(stable_values)} "
          f"({len(stable_values) / MINUTES * 100:.1f}%)")
    print(f"  surges (> {STABLE_HIGH})    : "
          f"{sum(1 for v in counts if v > STABLE_HIGH)}")
    print(f"  lulls  (< {STABLE_LOW})    : "
          f"{sum(1 for v in counts if v < STABLE_LOW)}")

    best, start, dp = longest_stable_dp(counts, STABLE_LOW, STABLE_HIGH)
    print("\n=== DP streak table ===")
    for i in range(0, MINUTES, 10):
        print(f"  minutes {i:>2}-{i + 9:>2} counts: " +
              " ".join(f"{v:>3}" for v in counts[i:i + 10]))
        print(f"  {'':>17}dp    : " +
              " ".join(f"{v:>3}" for v in dp[i:i + 10]))

    print(f"\n=== longest stable flow ===")
    print(f"  length   : {best} minute(s)")
    print(f"  minutes  : {start} to {start + best - 1}")
    print(f"  counts   : {counts[start:start + best]}")
    if best:
        window = counts[start:start + best]
        print(f"  average  : {sum(window) / len(window):.2f} cars/min")

    print("\n=== every stable run ===")
    for a, b in all_stable_runs(counts, STABLE_LOW, STABLE_HIGH):
        length = b - a + 1
        marker = "  <- longest" if length == best else ""
        print(f"  minutes {a:>2}-{b:>2} ({length} min): "
              f"{counts[a:b + 1]}{marker}")

    print("\n=== LCS-style match against an ideal stable pattern ===")
    match = lcs_with_stable_pattern(counts, STABLE_LOW, STABLE_HIGH)
    print(f"  longest common stable subsequence: {match} of {MINUTES} minutes "
          f"({match / MINUTES * 100:.1f}% similarity to steady flow)")

    print("\n=== verdict ===")
    print("  flow quality:",
          "steady, signal timing is fine" if best >= 8 else
          "moderately stable, minor tuning needed" if best >= 5 else
          "unstable, the junction needs signal retiming")
