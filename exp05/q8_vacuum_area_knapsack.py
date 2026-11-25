"""
Experiment 5 - Question 8: Robot Vacuum Area Coverage (Knapsack)

Scenario: A robot vacuum must cover sections of a room with different energy
costs. Maximise the area cleaned under a battery limit.

Rubrics covered:
  * cost and area generated for each section
  * total energy budget set
  * optimal subset of sections chosen
  * tabulation used to optimise memory use
"""

import random

SECTIONS = 12
BUDGET = 70          # battery units


def generate_sections(seed=23):
    names = ["Hall", "Kitchen", "Bedroom 1", "Bedroom 2", "Study",
             "Balcony", "Corridor", "Bathroom", "Dining", "Store",
             "Puja Room", "Lobby"]
    random.seed(seed)
    out = []
    for name in names[:SECTIONS]:
        cost = random.randint(5, 22)                 # battery units
        area = random.randint(4, 26)                 # square metres
        out.append({"name": name, "cost": cost, "area": area})
    return out


def knapsack_2d(sections, budget):
    """Standard table: (n+1) x (budget+1) cells."""
    n = len(sections)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        cost, area = sections[i - 1]["cost"], sections[i - 1]["area"]
        for b in range(budget + 1):
            dp[i][b] = dp[i - 1][b]
            if cost <= b:
                dp[i][b] = max(dp[i][b], area + dp[i - 1][b - cost])
    chosen, b = [], budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            chosen.append(i - 1)
            b -= sections[i - 1]["cost"]
    chosen.reverse()
    return dp[n][budget], chosen, (n + 1) * (budget + 1)


def knapsack_1d(sections, budget):
    """Memory-optimised tabulation: a single row of budget+1 cells.
    The inner loop runs backwards so each section is used at most once."""
    dp = [0] * (budget + 1)
    keep = [[False] * (budget + 1) for _ in range(len(sections))]
    for i, s in enumerate(sections):
        for b in range(budget, s["cost"] - 1, -1):
            if s["area"] + dp[b - s["cost"]] > dp[b]:
                dp[b] = s["area"] + dp[b - s["cost"]]
                keep[i][b] = True
    chosen, b = [], budget
    for i in range(len(sections) - 1, -1, -1):
        if keep[i][b]:
            chosen.append(i)
            b -= sections[i]["cost"]
    chosen.reverse()
    return dp[budget], chosen, budget + 1


if __name__ == "__main__":
    sections = generate_sections()

    print(f"=== room sections, battery budget {BUDGET} units ===")
    print(f"  {'section':<12}{'energy':>8}{'area (m2)':>11}{'m2 per unit':>13}")
    for s in sections:
        print(f"  {s['name']:<12}{s['cost']:>8}{s['area']:>11}"
              f"{s['area'] / s['cost']:>13.2f}")
    print(f"\n  cleaning the whole flat needs "
          f"{sum(s['cost'] for s in sections)} units for "
          f"{sum(s['area'] for s in sections)} m2 "
          f"(only {BUDGET} units available)")

    area2d, chosen2d, cells2d = knapsack_2d(sections, BUDGET)
    area1d, chosen1d, cells1d = knapsack_1d(sections, BUDGET)

    print("\n=== optimal cleaning plan ===")
    used = sum(sections[i]["cost"] for i in chosen2d)
    for i in chosen2d:
        s = sections[i]
        print(f"  {s['name']:<12} {s['cost']:>3} units -> {s['area']:>3} m2")
    print(f"  total: {used}/{BUDGET} units, {area2d} m2 cleaned")
    skipped = [sections[i]["name"] for i in range(SECTIONS) if i not in chosen2d]
    print(f"  skipped: {', '.join(skipped)}")

    print("\n=== 2-D table vs 1-D tabulation ===")
    print(f"  2-D: {area2d} m2, {cells2d} cells stored "
          f"({SECTIONS + 1} rows x {BUDGET + 1} cols)")
    print(f"  1-D: {area1d} m2, {cells1d} cells stored (one row)")
    print(f"  same answer        : {area2d == area1d}")
    print(f"  same sections      : {chosen2d == chosen1d}")
    print(f"  memory saved       : {(1 - cells1d / cells2d) * 100:.1f}%")

    print("\n=== how much can be cleaned as the battery grows ===")
    for b in range(0, BUDGET + 1, 7):
        area, picks, _ = knapsack_1d(sections, b)
        print(f"  {b:>3} units -> {area:>3} m2 in {len(picks)} section(s)")

    print("\n=== greedy by area-per-unit, for comparison ===")
    order = sorted(sections, key=lambda s: s["area"] / s["cost"], reverse=True)
    g_cost, g_area, g_names = 0, 0, []
    for s in order:
        if g_cost + s["cost"] <= BUDGET:
            g_cost += s["cost"]
            g_area += s["area"]
            g_names.append(s["name"])
    print(f"  greedy cleans {g_area} m2 using {g_cost} units")
    print(f"  DP cleans     {area2d} m2 using {used} units "
          f"({area2d - g_area:+} m2 better)")
