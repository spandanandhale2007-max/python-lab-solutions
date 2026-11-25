"""
Experiment 4 - Question 4: Robotic Vacuum Efficiency

Scenario: A robotic vacuum logs the distance covered every minute during a
45-minute cleaning session. Evaluate its efficiency.

Rubrics covered:
  * distance data generated
  * total distance computed
  * idle minutes (0 movement) found
  * the 5-minute window with maximum movement identified
"""

import random

MINUTES = 45
WINDOW = 5


def generate_distances(seed=5):
    """Metres covered each minute; some minutes are idle (docking, stuck)."""
    random.seed(seed)
    data = []
    for minute in range(MINUTES):
        if random.random() < 0.15:          # idle minute
            data.append(0.0)
        else:
            data.append(round(random.uniform(3.5, 12.0), 1))
    return data


def max_window(data, size):
    """Sliding window sum - the running total is a one-line DP state."""
    if len(data) < size:
        return 0, 0.0
    window_sum = sum(data[:size])
    best_sum, best_start = window_sum, 0
    for i in range(size, len(data)):
        window_sum += data[i] - data[i - size]      # reuse the previous sum
        if window_sum > best_sum:
            best_sum, best_start = window_sum, i - size + 1
    return best_start, round(best_sum, 1)


def idle_streaks(data):
    streaks, start = [], None
    for i, v in enumerate(data):
        if v == 0 and start is None:
            start = i
        elif v != 0 and start is not None:
            streaks.append((start, i - 1))
            start = None
    if start is not None:
        streaks.append((start, len(data) - 1))
    return streaks


if __name__ == "__main__":
    distances = generate_distances()

    print("=== per-minute distance log (metres) ===")
    for row_start in range(0, MINUTES, 9):
        row = distances[row_start:row_start + 9]
        label = f"  min {row_start:02d}-{row_start + len(row) - 1:02d}"
        print(f"{label:<14}" + " ".join(f"{v:>6.1f}" for v in row))

    total = round(sum(distances), 1)
    active = [v for v in distances if v > 0]
    print("\n=== totals ===")
    print(f"  session length      : {MINUTES} minutes")
    print(f"  total distance      : {total} m")
    print(f"  average per minute  : {total / MINUTES:.2f} m")
    print(f"  average when moving : {sum(active) / len(active):.2f} m")
    print(f"  best single minute  : {max(distances):.1f} m at minute "
          f"{distances.index(max(distances))}")

    idle = [i for i, v in enumerate(distances) if v == 0]
    print("\n=== idle minutes (0 movement) ===")
    print(f"  count   : {len(idle)} of {MINUTES} "
          f"({len(idle) / MINUTES * 100:.1f}% of the session)")
    print(f"  minutes : {idle}")
    streaks = idle_streaks(distances)
    print("  streaks :")
    for a, b in streaks:
        print(f"    minutes {a:02d}-{b:02d} ({b - a + 1} min)")
    if streaks:
        longest = max(streaks, key=lambda s: s[1] - s[0])
        print(f"  longest stall: minutes {longest[0]:02d}-{longest[1]:02d}")

    start, best = max_window(distances, WINDOW)
    print(f"\n=== best {WINDOW}-minute window ===")
    print(f"  minutes {start}-{start + WINDOW - 1}: {best} m "
          f"(avg {best / WINDOW:.2f} m/min)")
    print(f"  readings: {distances[start:start + WINDOW]}")

    print(f"\n=== every {WINDOW}-minute window, for comparison ===")
    for i in range(0, MINUTES - WINDOW + 1, 5):
        chunk = distances[i:i + WINDOW]
        marker = "  <- best" if i == start else ""
        print(f"  min {i:02d}-{i + WINDOW - 1:02d}  {sum(chunk):>6.1f} m{marker}")

    print("\n=== efficiency verdict ===")
    coverage_rate = len(active) / MINUTES * 100
    print(f"  moving {coverage_rate:.1f}% of the time, "
          f"{total / 60:.2f} m per second of motion on average")
    print("  verdict:", "good coverage" if coverage_rate > 85 else
          "acceptable" if coverage_rate > 70 else
          "poor - the robot stalled too often")
