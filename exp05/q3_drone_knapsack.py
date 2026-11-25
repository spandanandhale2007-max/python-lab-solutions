"""
Experiment 5 - Question 3: Delivery Drone Battery Knapsack

Scenario: A delivery drone logs battery consumption for 15 trips. Maximise the
delivery value under a limited battery.

Rubrics covered:
  * trip values and battery costs generated
  * a maximum battery capacity set
  * optimal subset of trips selected
  * top-down and bottom-up results compared
"""

import random
import time
from functools import lru_cache

TRIPS = 15
CAPACITY = 100          # battery units available for the day


def generate_trips(seed=6):
    random.seed(seed)
    trips = []
    for i in range(TRIPS):
        cost = random.randint(8, 32)                  # battery units
        value = random.randint(120, 900)              # delivery fee in rupees
        trips.append({"id": f"T{i + 1:02d}", "cost": cost, "value": value})
    return trips


# ---------------- top-down (memoised recursion) ----------------
def knapsack_topdown(trips, capacity):
    costs = tuple(t["cost"] for t in trips)
    values = tuple(t["value"] for t in trips)
    calls = {"n": 0}

    @lru_cache(maxsize=None)
    def best(i, remaining):
        calls["n"] += 1
        if i == len(costs) or remaining == 0:
            return 0
        skip = best(i + 1, remaining)
        take = 0
        if costs[i] <= remaining:
            take = values[i] + best(i + 1, remaining - costs[i])
        return max(skip, take)

    total = best(0, capacity)

    # walk the decisions back out to recover the chosen trips
    chosen, remaining = [], capacity
    for i in range(len(costs)):
        if costs[i] <= remaining and \
                values[i] + best(i + 1, remaining - costs[i]) >= best(i, remaining):
            chosen.append(i)
            remaining -= costs[i]
    return total, chosen, calls["n"], best.cache_info()


# ---------------- bottom-up (tabulation) ----------------
def knapsack_bottomup(trips, capacity):
    n = len(trips)
    table = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        cost, value = trips[i - 1]["cost"], trips[i - 1]["value"]
        for w in range(capacity + 1):
            table[i][w] = table[i - 1][w]
            if cost <= w:
                table[i][w] = max(table[i][w], value + table[i - 1][w - cost])

    chosen, w = [], capacity
    for i in range(n, 0, -1):
        if table[i][w] != table[i - 1][w]:
            chosen.append(i - 1)
            w -= trips[i - 1]["cost"]
    chosen.reverse()
    cells = (n + 1) * (capacity + 1)
    return table[n][capacity], chosen, cells, table


def greedy_by_ratio(trips, capacity):
    """Greedy baseline, to show that it is not always optimal."""
    order = sorted(range(len(trips)),
                   key=lambda i: trips[i]["value"] / trips[i]["cost"],
                   reverse=True)
    total, used, chosen = 0, 0, []
    for i in order:
        if used + trips[i]["cost"] <= capacity:
            used += trips[i]["cost"]
            total += trips[i]["value"]
            chosen.append(i)
    return total, sorted(chosen)


def show(label, trips, total, chosen):
    used = sum(trips[i]["cost"] for i in chosen)
    print(f"\n  {label}")
    print(f"    value   : Rs.{total:,}")
    print(f"    battery : {used}/{CAPACITY} units used")
    print(f"    trips   : {[trips[i]['id'] for i in chosen]}")


if __name__ == "__main__":
    trips = generate_trips()

    print(f"=== 15 candidate trips, battery capacity {CAPACITY} units ===")
    print(f"  {'trip':<6}{'battery':>9}{'value':>10}{'value/unit':>13}")
    for t in trips:
        print(f"  {t['id']:<6}{t['cost']:>9}{t['value']:>10,}"
              f"{t['value'] / t['cost']:>13.2f}")
    print(f"\n  flying every trip would need "
          f"{sum(t['cost'] for t in trips)} units "
          f"(only {CAPACITY} available), worth "
          f"Rs.{sum(t['value'] for t in trips):,}")

    t0 = time.perf_counter()
    td_total, td_chosen, td_calls, td_info = knapsack_topdown(trips, CAPACITY)
    td_ms = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    bu_total, bu_chosen, bu_cells, table = knapsack_bottomup(trips, CAPACITY)
    bu_ms = (time.perf_counter() - t0) * 1000

    g_total, g_chosen = greedy_by_ratio(trips, CAPACITY)

    print("\n=== optimal schedules ===")
    show("top-down (memoised recursion)", trips, td_total, td_chosen)
    show("bottom-up (tabulation)", trips, bu_total, bu_chosen)
    show("greedy by value/unit (baseline)", trips, g_total, g_chosen)

    print("\n=== comparison ===")
    print(f"  {'method':<30}{'value':>10}{'time (ms)':>12}{'states':>10}")
    print(f"  {'top-down memoised':<30}{td_total:>10,}{td_ms:>12.3f}"
          f"{td_info.currsize:>10}")
    print(f"  {'bottom-up tabulation':<30}{bu_total:>10,}{bu_ms:>12.3f}"
          f"{bu_cells:>10}")
    print(f"  {'greedy':<30}{g_total:>10,}{'-':>12}{'-':>10}")
    print(f"\n  both DP methods agree : {td_total == bu_total}")
    print(f"  same subset chosen    : {td_chosen == bu_chosen}")
    print(f"  greedy loses          : Rs.{bu_total - g_total:,} "
          f"({(bu_total - g_total) / bu_total * 100:.1f}% below optimal)")
    print(f"  cache statistics      : {td_info}")

    print("\n=== value as the battery grows (row n of the DP table) ===")
    for cap in range(0, CAPACITY + 1, 10):
        print(f"  capacity {cap:>3} units -> best value Rs.{table[TRIPS][cap]:>6,}")

    print("\n  Top-down only visits the states it needs; bottom-up fills all")
    print(f"  {bu_cells} cells but uses no recursion stack.")
