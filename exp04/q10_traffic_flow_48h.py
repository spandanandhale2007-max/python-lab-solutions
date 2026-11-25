"""
Experiment 4 - Question 10: Traffic Flow Analysis

Scenario: A traffic monitoring system logs the vehicle count per hour at a
junction over 48 hours. Analyse the traffic flow.

Rubrics covered:
  * vehicle count data generated
  * day period compared with night period
  * moving averages computed using the DP running-sum idea
  * congestion hours (more than 150 vehicles per hour) filtered
"""

import random

HOURS = 48
CONGESTION = 150
DAY_HOURS = range(6, 22)          # 06:00 - 21:59 counts as day


def generate_counts(seed=8):
    """Two rush-hour peaks per day, quiet nights."""
    random.seed(seed)
    shape = {0: 18, 1: 12, 2: 9, 3: 8, 4: 14, 5: 35, 6: 78, 7: 142,
             8: 188, 9: 165, 10: 120, 11: 108, 12: 115, 13: 110, 14: 104,
             15: 118, 16: 148, 17: 182, 18: 195, 19: 160, 20: 112, 21: 74,
             22: 44, 23: 26}
    data = []
    for h in range(HOURS):
        base = shape[h % 24]
        weekend_factor = 0.8 if h >= 24 else 1.0      # day 2 is quieter
        data.append(max(0, int(base * weekend_factor + random.gauss(0, 12))))
    return data


def moving_average(data, window):
    """DP running sum: each step reuses the previous window total,
    so the whole series costs O(n) instead of O(n*window)."""
    if window > len(data):
        return []
    out = []
    running = sum(data[:window])
    out.append(running / window)
    for i in range(window, len(data)):
        running += data[i] - data[i - window]          # reuse
        out.append(running / window)
    return out


def max_subarray(data, window):
    running = sum(data[:window])
    best, best_at = running, 0
    for i in range(window, len(data)):
        running += data[i] - data[i - window]
        if running > best:
            best, best_at = running, i - window + 1
    return best_at, best


if __name__ == "__main__":
    counts = generate_counts()

    print("=== hourly vehicle counts over 48 hours ===")
    for day in range(2):
        print(f"  day {day + 1}:")
        for block in range(0, 24, 12):
            row = counts[day * 24 + block:day * 24 + block + 12]
            print(f"    {block:02d}:00-{block + 11:02d}:00  " +
                  " ".join(f"{v:>4}" for v in row))

    print("\n=== day vs night ===")
    day_counts = [v for h, v in enumerate(counts) if h % 24 in DAY_HOURS]
    night_counts = [v for h, v in enumerate(counts) if h % 24 not in DAY_HOURS]
    print(f"  day   (06-21): {len(day_counts)} hours, total {sum(day_counts):>6,}, "
          f"avg {sum(day_counts) / len(day_counts):>7.1f} veh/h, "
          f"peak {max(day_counts)}")
    print(f"  night (22-05): {len(night_counts)} hours, total "
          f"{sum(night_counts):>6,}, "
          f"avg {sum(night_counts) / len(night_counts):>7.1f} veh/h, "
          f"peak {max(night_counts)}")
    print(f"  the junction carries "
          f"{sum(day_counts) / max(sum(night_counts), 1):.1f}x more traffic "
          f"by day")

    print("\n=== day 1 vs day 2 ===")
    for d in range(2):
        chunk = counts[d * 24:(d + 1) * 24]
        print(f"  day {d + 1}: total {sum(chunk):>6,}  "
              f"avg {sum(chunk) / 24:>6.1f}  peak {max(chunk):>4} at "
              f"{chunk.index(max(chunk)):02d}:00")

    print("\n=== 3-hour moving average (DP running sum) ===")
    ma3 = moving_average(counts, 3)
    for i, v in enumerate(ma3):
        if i % 4 == 0:
            print(f"  hours {i:02d}-{i + 2:02d}: {v:>7.2f} veh/h  "
                  f"|{'#' * int(v / 6)}")

    print("\n=== 6-hour moving average, smoothest view of the trend ===")
    ma6 = moving_average(counts, 6)
    print(f"  computed {len(ma6)} windows; peak smoothed flow "
          f"{max(ma6):.2f} veh/h starting at hour {ma6.index(max(ma6)):02d}:00")
    print(f"  quietest 6-hour stretch: {min(ma6):.2f} veh/h starting at hour "
          f"{ma6.index(min(ma6)):02d}:00")

    start, best = max_subarray(counts, 4)
    print(f"\n=== busiest 4-hour window ===")
    print(f"  hours {start:02d}:00-{start + 3:02d}:59 carried {best:,} vehicles "
          f"({best / 4:.1f} veh/h)")
    print(f"  readings: {counts[start:start + 4]}")

    congested = [(h, v) for h, v in enumerate(counts) if v > CONGESTION]
    print(f"\n=== congestion hours (above {CONGESTION} veh/h): "
          f"{len(congested)} of {HOURS} ===")
    for h, v in congested:
        day = h // 24 + 1
        print(f"  day {day} {h % 24:02d}:00  {v:>4} veh/h  "
              f"({v - CONGESTION:+} over the threshold)")
    if congested:
        worst = max(congested, key=lambda t: t[1])
        print(f"\n  worst hour: day {worst[0] // 24 + 1} "
              f"{worst[0] % 24:02d}:00 with {worst[1]} vehicles")
        print(f"  congestion share: "
              f"{len(congested) / HOURS * 100:.1f}% of all hours")
