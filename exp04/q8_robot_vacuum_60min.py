"""
Experiment 4 - Question 8: Robot Vacuum Cleaning Efficiency (60 minutes)

Scenario: A robot vacuum tracks movement in metres every minute over 60
minutes. Analyse the cleaning efficiency.

Rubrics covered:
  * random movement data generated
  * first 20 minutes sliced
  * total and average movement computed
  * idle minutes (0 metres moved) filtered
"""

import random

MINUTES = 60


def generate_movement(seed=17):
    """Metres per minute. The battery fades, so later minutes are slower."""
    random.seed(seed)
    data = []
    for minute in range(MINUTES):
        if random.random() < 0.12:
            data.append(0.0)                              # idle
        else:
            fade = 1.0 - minute / (MINUTES * 2.5)         # battery decay
            data.append(round(random.uniform(4.0, 11.0) * fade, 1))
    return data


if __name__ == "__main__":
    movement = generate_movement()

    print("=== per-minute movement (metres) ===")
    for i in range(0, MINUTES, 10):
        row = movement[i:i + 10]
        print(f"  min {i:02d}-{i + len(row) - 1:02d}  " +
              " ".join(f"{v:>5.1f}" for v in row))

    first20 = movement[:20]                   # slicing
    middle = movement[20:40]
    last20 = movement[-20:]

    print("\n=== slices of 20 minutes each ===")
    for label, chunk in (("first 20 (00-19)", first20),
                         ("middle 20 (20-39)", middle),
                         ("last 20 (40-59)", last20)):
        idle = sum(1 for v in chunk if v == 0)
        print(f"  {label:<20} total {sum(chunk):>7.1f} m   "
              f"avg {sum(chunk) / len(chunk):>5.2f} m/min   idle {idle:>2} min")

    total = round(sum(movement), 1)
    print("\n=== whole session ===")
    print(f"  total distance      : {total} m")
    print(f"  average per minute  : {total / MINUTES:.2f} m")
    print(f"  best minute         : {max(movement):.1f} m at minute "
          f"{movement.index(max(movement))}")

    idle_minutes = [i for i, v in enumerate(movement) if v == 0]
    active = [v for v in movement if v > 0]
    print("\n=== idle filter ===")
    print(f"  idle minutes        : {len(idle_minutes)} -> {idle_minutes}")
    print(f"  active minutes      : {len(active)}")
    print(f"  average while active: {sum(active) / len(active):.2f} m/min")
    print(f"  duty cycle          : {len(active) / MINUTES * 100:.1f}%")

    print("\n=== slowest and fastest active minutes ===")
    slowest = min(active)
    print(f"  slowest active      : {slowest:.1f} m at minute "
          f"{movement.index(slowest)}")
    print(f"  5 slowest active    : {sorted(active)[:5]}")
    print(f"  5 fastest           : {sorted(active, reverse=True)[:5]}")

    print("\n=== battery fade check: 10-minute blocks ===")
    for i in range(0, MINUTES, 10):
        chunk = movement[i:i + 10]
        bar = "#" * int(sum(chunk) / 5)
        print(f"  min {i:02d}-{i + 9:02d}  {sum(chunk):>6.1f} m  |{bar}")
    first_half = sum(movement[:30])
    second_half = sum(movement[30:])
    print(f"\n  first half {first_half:.1f} m vs second half {second_half:.1f} m "
          f"({(second_half - first_half) / first_half * 100:+.1f}%)")

    print("\n=== efficiency verdict ===")
    duty = len(active) / MINUTES * 100
    print(f"  coverage estimate   : {total * 0.25:.1f} sq m "
          f"(assuming a 25 cm brush width)")
    print(f"  verdict             : " +
          ("efficient run" if duty >= 90 else
           "normal run" if duty >= 80 else
           "the robot stalled too often, check for obstacles"))
