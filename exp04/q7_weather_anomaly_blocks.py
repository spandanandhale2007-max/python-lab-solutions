"""
Experiment 4 - Question 7: Weather Sensor Anomaly Detection

Scenario: A weather sensor logs the temperature every hour over 24 hours.
Detect anomalies.

Rubrics covered:
  * hourly temperature readings generated
  * divided into morning / afternoon / evening
  * average computed for each time block
  * rapid temperature changes (more than 5 C per hour) filtered out
"""

import random

HOURS = 24
BLOCKS = {
    "night   (00-05)": range(0, 6),
    "morning (06-11)": range(6, 12),
    "afternoon (12-17)": range(12, 18),
    "evening (18-23)": range(18, 24),
}
SPIKE_THRESHOLD = 5.0


def generate_readings(seed=33):
    """Normal daily curve with two injected sensor faults."""
    random.seed(seed)
    base = [21, 20.5, 20, 19.5, 19.5, 20, 22, 25, 28, 30, 32, 33.5,
            35, 36, 35.5, 34, 32, 30, 28, 26.5, 25, 24, 23, 22]
    readings = [round(t + random.uniform(-0.8, 0.8), 1) for t in base]
    readings[9] = round(readings[9] + 9.5, 1)      # spike
    readings[19] = round(readings[19] - 8.0, 1)    # dropout
    return readings


def block_averages(readings):
    out = {}
    for label, hours in BLOCKS.items():
        values = [readings[h] for h in hours]
        out[label] = {
            "values": values,
            "avg": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
        }
    return out


def rapid_changes(readings, threshold=SPIKE_THRESHOLD):
    """Returns (hour, previous, current, delta) where |delta| > threshold."""
    flagged = []
    for h in range(1, len(readings)):
        delta = readings[h] - readings[h - 1]
        if abs(delta) > threshold:
            flagged.append((h, readings[h - 1], readings[h], round(delta, 1)))
    return flagged


if __name__ == "__main__":
    readings = generate_readings()

    print("=== 24 hourly readings (degrees C) ===")
    for h in range(0, HOURS, 6):
        row = readings[h:h + 6]
        print(f"  {h:02d}:00-{h + 5:02d}:00  " + " ".join(f"{v:>6.1f}" for v in row))

    print("\n=== block averages ===")
    stats = block_averages(readings)
    for label, s in stats.items():
        print(f"  {label:<18} avg {s['avg']:>6.2f} C   "
              f"min {s['min']:>5.1f}   max {s['max']:>5.1f}")
    hottest = max(stats, key=lambda k: stats[k]["avg"])
    coolest = min(stats, key=lambda k: stats[k]["avg"])
    print(f"\n  hottest block : {hottest} ({stats[hottest]['avg']:.2f} C)")
    print(f"  coolest block : {coolest} ({stats[coolest]['avg']:.2f} C)")

    print(f"\n=== hour-to-hour change (flagging |delta| > "
          f"{SPIKE_THRESHOLD} C/h) ===")
    for h in range(1, HOURS):
        delta = round(readings[h] - readings[h - 1], 1)
        flag = "  <== ANOMALY" if abs(delta) > SPIKE_THRESHOLD else ""
        print(f"  {h - 1:02d}:00 -> {h:02d}:00  {readings[h - 1]:>6.1f} -> "
              f"{readings[h]:>6.1f}  {delta:>+6.1f} C/h{flag}")

    flagged = rapid_changes(readings)
    print(f"\n=== {len(flagged)} anomaly(ies) detected ===")
    for h, prev, cur, delta in flagged:
        kind = "sudden spike" if delta > 0 else "sudden drop"
        print(f"  {h:02d}:00  {prev:.1f} -> {cur:.1f} C  ({delta:+.1f} C/h) "
              f"{kind}")
    if not flagged:
        print("  sensor looks healthy")

    print("\n=== cleaned series (anomalies replaced by the neighbour average) ===")
    cleaned = list(readings)
    for h, prev, cur, delta in flagged:
        nxt = readings[h + 1] if h + 1 < HOURS else prev
        cleaned[h] = round((prev + nxt) / 2, 1)
        print(f"  {h:02d}:00 corrected {cur:.1f} -> {cleaned[h]:.1f} C")
    print(f"\n  raw     daily average: {sum(readings) / HOURS:.2f} C "
          f"(max {max(readings):.1f})")
    print(f"  cleaned daily average: {sum(cleaned) / HOURS:.2f} C "
          f"(max {max(cleaned):.1f})")
    print("  the two spikes alone shifted the daily average by "
          f"{abs(sum(readings) - sum(cleaned)) / HOURS:.2f} C")
