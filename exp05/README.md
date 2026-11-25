# Experiment 5 - Unit II

Dynamic programming: knapsack, LIS/LCS, house robber, memoisation

10 scenario questions, each solved in its own section and its own file. Every program below was executed and the real output is included.

[Back to the index](../README.md)

---

## Questions in this experiment

- [Experiment 5 - Question 1: Fitness Band Heart Rate](#experiment-5---question-1-fitness-band-heart-rate)
- [Experiment 5 - Question 2: Longest Improvement Streak (LIS / LCS style)](#experiment-5---question-2-longest-improvement-streak-lis--lcs-style)
- [Experiment 5 - Question 3: Delivery Drone Battery Knapsack](#experiment-5---question-3-delivery-drone-battery-knapsack)
- [Experiment 5 - Question 4: Optimal Study Plan (Knapsack)](#experiment-5---question-4-optimal-study-plan-knapsack)
- [Experiment 5 - Question 5: Longest Stable Traffic Flow](#experiment-5---question-5-longest-stable-traffic-flow)
- [Experiment 5 - Question 6: Playlist Optimisation (non-adjacent selection)](#experiment-5---question-6-playlist-optimisation-non-adjacent-selection)
- [Experiment 5 - Question 7: Longest Decreasing Spending Pattern](#experiment-5---question-7-longest-decreasing-spending-pattern)
- [Experiment 5 - Question 8: Robot Vacuum Area Coverage (Knapsack)](#experiment-5---question-8-robot-vacuum-area-coverage-knapsack)
- [Experiment 5 - Question 9: Stock Growth Prediction (Fibonacci-style recurrence)](#experiment-5---question-9-stock-growth-prediction-fibonacci-style-recurrence)
- [Experiment 5 - Question 10: Road Trip Rewards (House Robber pattern)](#experiment-5---question-10-road-trip-rewards-house-robber-pattern)

---

## Experiment 5 - Question 1: Fitness Band Heart Rate

Scenario: A fitness band records the heart rate every minute for 10 minutes.
Analyse this data.

Rubrics covered:
  * random heart rate data generated
  * first 5 minutes indexed
  * min, max and average computed
  * high heart rate values (above 120 bpm) filtered

**File:** [`q1_fitness_band_heart_rate.py`](q1_fitness_band_heart_rate.py) &nbsp;&middot;&nbsp; **Run:** `python q1_fitness_band_heart_rate.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== 10-minute heart rate log ===
  min  1:  72 bpm  resting     |##################
  min  2:  80 bpm  resting     |####################
  min  3:  85 bpm  resting     |#####################
  min  4: 105 bpm  very light  |##########################
  min  5: 122 bpm  light       |##############################  HIGH
  min  6: 133 bpm  light       |#################################  HIGH
  min  7: 145 bpm  moderate    |####################################  HIGH
  min  8: 121 bpm  light       |##############################  HIGH
  min  9: 108 bpm  very light  |###########################
  min 10:  90 bpm  resting     |######################

=== slices ===
  first 5 minutes : [72, 80, 85, 105, 122]  avg 92.8 bpm
  last 5 minutes  : [133, 145, 121, 108, 90]  avg 119.4 bpm
  minute 1 (bpm[0]) : 72 bpm
  minute 10 (bpm[-1]): 90 bpm
  every 2nd minute   : [72, 85, 122, 145, 108]

=== statistics ===
  readings : 10
  minimum  : 72 bpm at minute 1
  maximum  : 145 bpm at minute 7
  average  : 106.10 bpm
  range    : 73 bpm
  median   : 106.5 bpm

=== high heart rate filter (above 120 bpm) ===
  4 of 10 minutes exceeded the threshold
    minute  5: 122 bpm (+2 over)
    minute  6: 133 bpm (+13 over)
    minute  7: 145 bpm (+25 over)
    minute  8: 121 bpm (+1 over)
  time in the high zone: 4 minute(s) (40% of the session)
  average while high   : 130.2 bpm

=== recovery check ===
  peak 145 bpm -> final 90 bpm, dropped 55 bpm
  recovery: excellent

=== time in each zone ===
  resting      4 minute(s)
  very light   2 minute(s)
  light        3 minute(s)
  moderate     1 minute(s)

```

</details>

---

## Experiment 5 - Question 2: Longest Improvement Streak (LIS / LCS style)

Scenario: A language learning app tracks correct answers in each of 20 quiz
sessions. Identify the longest improvement streak.

Rubrics covered:
  * random correct-answer counts generated
  * compared with a sorted version for pattern detection
  * dynamic programming used to find the longest increasing subsequence
  * streaks of improvement tracked

**File:** [`q2_quiz_improvement_lis.py`](q2_quiz_improvement_lis.py) &nbsp;&middot;&nbsp; **Run:** `python q2_quiz_improvement_lis.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 5 - Question 2: Longest Improvement Streak (LIS / LCS style)

Scenario: A language learning app tracks correct answers in each of 20 quiz
sessions. Identify the longest improvement streak.

Rubrics covered:
  * random correct-answer counts generated
  * compared with a sorted version for pattern detection
  * dynamic programming used to find the longest increasing subsequence
  * streaks of improvement tracked
"""

import random

SESSIONS = 20


def generate_scores(seed=14):
    random.seed(seed)
    return [random.randint(4, 20) for _ in range(SESSIONS)]


def lis_dp(a):
    """Longest strictly increasing SUBSEQUENCE (gaps allowed).
    dp[i] = length of the best subsequence ending at i. O(n^2)."""
    n = len(a)
    if n == 0:
        return 0, [], []
    dp = [1] * n
    parent = [-1] * n
    for i in range(1, n):
        for j in range(i):
            if a[j] < a[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                parent[i] = j
    best_len = max(dp)
    idx = dp.index(best_len)
    path = []
    while idx != -1:
        path.append(idx)
        idx = parent[idx]
    path.reverse()
    return best_len, path, dp


def longest_consecutive_run(a):
    """Longest streak of consecutive sessions that each improve. O(n)."""
    if not a:
        return 0, 0
    dp = [1] * len(a)
    for i in range(1, len(a)):
        if a[i] > a[i - 1]:
            dp[i] = dp[i - 1] + 1
    length = max(dp)
    end = dp.index(length)
    return length, end - length + 1


def lcs_dp(a, b):
    """Classic LCS table: length of the longest common subsequence."""
    n, m = len(a), len(b)
    table = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])
    # reconstruct
    i, j, seq = n, m, []
    while i and j:
        if a[i - 1] == b[j - 1]:
            seq.append(a[i - 1])
            i -= 1
            j -= 1
        elif table[i - 1][j] >= table[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return table[n][m], list(reversed(seq)), table


if __name__ == "__main__":
    scores = generate_scores()

    print("=== correct answers per session (out of 20) ===")
    for i, s in enumerate(scores, 1):
        print(f"  session {i:>2}: {s:>2} |{'#' * s}")

    print(f"\n  average {sum(scores) / len(scores):.2f}   "
          f"best {max(scores)} (session {scores.index(max(scores)) + 1})   "
          f"worst {min(scores)} (session {scores.index(min(scores)) + 1})")

    print("\n=== comparison with the sorted version ===")
    ordered = sorted(scores)
    print(f"  actual : {scores}")
    print(f"  sorted : {ordered}")
    matches = sum(1 for x, y in zip(scores, ordered) if x == y)
    print(f"  positions already in sorted order: {matches}/{SESSIONS}")

    lcs_len, lcs_seq, lcs_table = lcs_dp(scores, ordered)
    print(f"\n  LCS(actual, sorted) length = {lcs_len}")
    print(f"  common subsequence         = {lcs_seq}")
    print("  (the LCS with the sorted list is exactly the longest "
          "non-decreasing run of progress)")

    best_len, path, dp = lis_dp(scores)
    print("\n=== longest increasing subsequence (DP, gaps allowed) ===")
    print(f"  dp table : {dp}")
    print(f"  length   : {best_len}")
    print(f"  sessions : {[i + 1 for i in path]}")
    print(f"  values   : {[scores[i] for i in path]}")

    run_len, run_start = longest_consecutive_run(scores)
    print("\n=== longest consecutive improvement streak ===")
    print(f"  length   : {run_len} session(s)")
    print(f"  sessions : {run_start + 1} to {run_start + run_len}")
    print(f"  values   : {scores[run_start:run_start + run_len]}")

    print("\n=== all improvement streaks ===")
    streak, start = 1, 0
    for i in range(1, len(scores)):
        if scores[i] > scores[i - 1]:
            streak += 1
        else:
            if streak >= 2:
                print(f"  sessions {start + 1}-{i}: "
                      f"{scores[start:i]} ({streak} long)")
            streak, start = 1, i
    if streak >= 2:
        print(f"  sessions {start + 1}-{len(scores)}: "
              f"{scores[start:]} ({streak} long)")

    print("\n=== verdict ===")
    ups = sum(1 for i in range(1, SESSIONS) if scores[i] > scores[i - 1])
    print(f"  improved in {ups} of {SESSIONS - 1} transitions")
    print(f"  overall trend: {scores[-1] - scores[0]:+d} answers from first "
          f"to last session")
    print(f"  the learner's best sustained progress covered {best_len} "
          f"sessions out of {SESSIONS}")
```

</details>

<details>
<summary>Program output</summary>

```text
=== correct answers per session (out of 20) ===
  session  1:  7 |#######
  session  2: 20 |####################
  session  3: 11 |###########
  session  4: 12 |############
  session  5: 12 |############
  session  6: 13 |#############
  session  7:  6 |######
  session  8: 18 |##################
  session  9: 13 |#############
  session 10: 18 |##################
  session 11: 16 |################
  session 12: 16 |################
  session 13:  7 |#######
  session 14: 12 |############
  session 15: 11 |###########
  session 16: 14 |##############
  session 17: 15 |###############
  session 18: 12 |############
  session 19: 15 |###############
  session 20: 20 |####################

  average 13.40   best 20 (session 2)   worst 6 (session 7)

=== comparison with the sorted version ===
  actual : [7, 20, 11, 12, 12, 13, 6, 18, 13, 18, 16, 16, 7, 12, 11, 14, 15, 12, 15, 20]
  sorted : [6, 7, 7, 11, 11, 12, 12, 12, 12, 13, 13, 14, 15, 15, 16, 16, 18, 18, 20, 20]
  positions already in sorted order: 1/20

  LCS(actual, sorted) length = 10
  common subsequence         = [7, 11, 12, 12, 13, 13, 14, 15, 15, 20]
  (the LCS with the sorted list is exactly the longest non-decreasing run of progress)

=== longest increasing subsequence (DP, gaps allowed) ===
  dp table : [1, 2, 2, 3, 3, 4, 1, 5, 4, 5, 5, 5, 2, 3, 3, 5, 6, 4, 6, 7]
  length   : 7
  sessions : [1, 3, 4, 6, 16, 17, 20]
  values   : [7, 11, 12, 13, 14, 15, 20]

=== longest consecutive improvement streak ===
  length   : 3 session(s)
  sessions : 15 to 17
  values   : [11, 14, 15]

=== all improvement streaks ===
  sessions 1-2: [7, 20] (2 long)
  sessions 3-4: [11, 12] (2 long)
  sessions 5-6: [12, 13] (2 long)
  sessions 7-8: [6, 18] (2 long)
  sessions 9-10: [13, 18] (2 long)
  sessions 13-14: [7, 12] (2 long)
  sessions 15-17: [11, 14, 15] (3 long)
  sessions 18-20: [12, 15, 20] (3 long)

=== verdict ===
  improved in 10 of 19 transitions
  overall trend: +13 answers from first to last session
  the learner's best sustained progress covered 7 sessions out of 20

```

</details>

---

## Experiment 5 - Question 3: Delivery Drone Battery Knapsack

Scenario: A delivery drone logs battery consumption for 15 trips. Maximise the
delivery value under a limited battery.

Rubrics covered:
  * trip values and battery costs generated
  * a maximum battery capacity set
  * optimal subset of trips selected
  * top-down and bottom-up results compared

**File:** [`q3_drone_knapsack.py`](q3_drone_knapsack.py) &nbsp;&middot;&nbsp; **Run:** `python q3_drone_knapsack.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== 15 candidate trips, battery capacity 100 units ===
  trip    battery     value   value/unit
  T01          26       202         7.77
  T02          23       900        39.13
  T03          16       157         9.81
  T04           8       269        33.62
  T05          29       720        24.83
  T06          23       897        39.00
  T07          31       502        16.19
  T08          18       142         7.89
  T09          16       620        38.75
  T10          14       867        61.93
  T11          21       671        31.95
  T12          25       818        32.72
  T13          11       317        28.82
  T14          26       686        26.38
  T15          30       866        28.87

  flying every trip would need 317 units (only 100 available), worth Rs.8,634

=== optimal schedules ===

  top-down (memoised recursion)
    value   : Rs.3,955
    battery : 97/100 units used
    trips   : ['T02', 'T06', 'T09', 'T10', 'T11']

  bottom-up (tabulation)
    value   : Rs.3,955
    battery : 97/100 units used
    trips   : ['T02', 'T06', 'T09', 'T10', 'T11']

  greedy by value/unit (baseline)
    value   : Rs.3,870
    battery : 95/100 units used
    trips   : ['T02', 'T04', 'T06', 'T09', 'T10', 'T13']

=== comparison ===
  method                             value   time (ms)    states
  top-down memoised                  3,955       0.381       776
  bottom-up tabulation               3,955       0.229      1616
  greedy                             3,870           -         -

  both DP methods agree : True
  same subset chosen    : True
  greedy loses          : Rs.85 (2.1% below optimal)
  cache statistics      : CacheInfo(hits=450, misses=776, maxsize=None, currsize=776)

=== value as the battery grows (row n of the DP table) ===
  capacity   0 units -> best value Rs.     0
  capacity  10 units -> best value Rs.   269
  capacity  20 units -> best value Rs.   867
  capacity  30 units -> best value Rs. 1,487
  capacity  40 units -> best value Rs. 1,767
  capacity  50 units -> best value Rs. 2,084
  capacity  60 units -> best value Rs. 2,664
  capacity  70 units -> best value Rs. 2,933
  capacity  80 units -> best value Rs. 3,284
  capacity  90 units -> best value Rs. 3,604
  capacity 100 units -> best value Rs. 3,955

  Top-down only visits the states it needs; bottom-up fills all
  1616 cells but uses no recursion stack.

```

</details>

---

## Experiment 5 - Question 4: Optimal Study Plan (Knapsack)

Scenario: A student revision tracker logs the time spent per subject each day
for 7 days. Find the optimal study plan.

Rubrics covered:
  * study hours and an effectiveness score generated per subject
  * total hours per day limited
  * total effectiveness maximised
  * solved with bottom-up dynamic programming

**File:** [`q4_study_plan_knapsack.py`](q4_study_plan_knapsack.py) &nbsp;&middot;&nbsp; **Run:** `python q4_study_plan_knapsack.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 5 - Question 4: Optimal Study Plan (Knapsack)

Scenario: A student revision tracker logs the time spent per subject each day
for 7 days. Find the optimal study plan.

Rubrics covered:
  * study hours and an effectiveness score generated per subject
  * total hours per day limited
  * total effectiveness maximised
  * solved with bottom-up dynamic programming
"""

import random

DAILY_LIMIT = 8          # hours a student can realistically study in a day
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
SUBJECTS = ["Python", "DSA", "DBMS", "OS", "Maths", "CN", "Soft Skills"]


def generate_plan(seed=12):
    """Each subject needs a whole number of hours and yields an
    effectiveness score (marks expected to be gained)."""
    random.seed(seed)
    return [{"subject": s,
             "hours": random.randint(1, 5),
             "effectiveness": random.randint(10, 60)}
            for s in SUBJECTS]


def knapsack_bottom_up(items, limit):
    """dp[i][h] = best effectiveness using the first i subjects in h hours."""
    n = len(items)
    dp = [[0] * (limit + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        hours, score = items[i - 1]["hours"], items[i - 1]["effectiveness"]
        for h in range(limit + 1):
            dp[i][h] = dp[i - 1][h]                    # skip this subject
            if hours <= h:
                dp[i][h] = max(dp[i][h], score + dp[i - 1][h - hours])
    # trace back which subjects were taken
    chosen, h = [], limit
    for i in range(n, 0, -1):
        if dp[i][h] != dp[i - 1][h]:
            chosen.append(i - 1)
            h -= items[i - 1]["hours"]
    chosen.reverse()
    return dp[n][limit], chosen, dp


def knapsack_1d(items, limit):
    """Space-optimised tabulation: one row instead of n+1 rows."""
    dp = [0] * (limit + 1)
    for item in items:
        for h in range(limit, item["hours"] - 1, -1):   # iterate backwards
            dp[h] = max(dp[h], item["effectiveness"] + dp[h - item["hours"]])
    return dp[limit]


if __name__ == "__main__":
    plan = generate_plan()

    print(f"=== subjects available (daily limit {DAILY_LIMIT} hours) ===")
    print(f"  {'subject':<14}{'hours':>7}{'effectiveness':>15}{'per hour':>11}")
    for item in plan:
        print(f"  {item['subject']:<14}{item['hours']:>7}"
              f"{item['effectiveness']:>15}"
              f"{item['effectiveness'] / item['hours']:>11.2f}")
    print(f"\n  studying everything would take "
          f"{sum(i['hours'] for i in plan)} hours, worth "
          f"{sum(i['effectiveness'] for i in plan)} points")

    best, chosen, dp = knapsack_bottom_up(plan, DAILY_LIMIT)
    print(f"\n=== optimal single-day plan (bottom-up DP) ===")
    used = sum(plan[i]["hours"] for i in chosen)
    for i in chosen:
        print(f"  {plan[i]['subject']:<14} {plan[i]['hours']} h  "
              f"-> {plan[i]['effectiveness']} points")
    print(f"  total: {used}/{DAILY_LIMIT} hours, {best} effectiveness points")
    print(f"  1-D space-optimised answer matches: "
          f"{knapsack_1d(plan, DAILY_LIMIT) == best}")

    print("\n=== DP table (rows = subjects considered, columns = hours) ===")
    print("        " + "".join(f"{h:>5}" for h in range(DAILY_LIMIT + 1)))
    for i, row in enumerate(dp):
        label = "none" if i == 0 else plan[i - 1]["subject"][:7]
        print(f"  {label:<7}" + "".join(f"{v:>5}" for v in row))

    print("\n=== marginal value of each extra hour ===")
    for h in range(1, DAILY_LIMIT + 1):
        gain = dp[len(plan)][h] - dp[len(plan)][h - 1]
        print(f"  hour {h}: total {dp[len(plan)][h]:>3} points "
              f"({gain:+} from the previous hour)")

    print(f"\n=== weekly plan: each day gets its own limit ===")
    random.seed(99)
    weekly_total = 0
    print(f"  {'day':<5}{'limit':>7}{'points':>9}  subjects")
    for day in DAYS:
        limit = random.randint(4, DAILY_LIMIT)
        score, picks, _ = knapsack_bottom_up(plan, limit)
        weekly_total += score
        names = ", ".join(plan[i]["subject"] for i in picks)
        print(f"  {day:<5}{limit:>7}{score:>9}  {names}")
    print(f"\n  expected effectiveness for the week: {weekly_total} points")

    print("\n=== why greedy fails here ===")
    greedy_order = sorted(plan, key=lambda i: i["effectiveness"] / i["hours"],
                          reverse=True)
    g_hours, g_score, g_names = 0, 0, []
    for item in greedy_order:
        if g_hours + item["hours"] <= DAILY_LIMIT:
            g_hours += item["hours"]
            g_score += item["effectiveness"]
            g_names.append(item["subject"])
    print(f"  greedy picks {g_names} -> {g_score} points in {g_hours} h")
    print(f"  DP achieves {best} points, a difference of {best - g_score}")
```

</details>

<details>
<summary>Program output</summary>

```text
=== subjects available (daily limit 8 hours) ===
  subject         hours  effectiveness   per hour
  Python              4             27       6.75
  DSA                 5             52      10.40
  DBMS                3             19       6.33
  OS                  4             10       2.50
  Maths               3             40      13.33
  CN                  3             51      17.00
  Soft Skills         4             54      13.50

  studying everything would take 26 hours, worth 253 points

=== optimal single-day plan (bottom-up DP) ===
  CN             3 h  -> 51 points
  Soft Skills    4 h  -> 54 points
  total: 7/8 hours, 105 effectiveness points
  1-D space-optimised answer matches: True

=== DP table (rows = subjects considered, columns = hours) ===
            0    1    2    3    4    5    6    7    8
  none       0    0    0    0    0    0    0    0    0
  Python     0    0    0    0   27   27   27   27   27
  DSA        0    0    0    0   27   52   52   52   52
  DBMS       0    0    0   19   27   52   52   52   71
  OS         0    0    0   19   27   52   52   52   71
  Maths      0    0    0   40   40   52   59   67   92
  CN         0    0    0   51   51   52   91   91  103
  Soft Sk    0    0    0   51   54   54   91  105  105

=== marginal value of each extra hour ===
  hour 1: total   0 points (+0 from the previous hour)
  hour 2: total   0 points (+0 from the previous hour)
  hour 3: total  51 points (+51 from the previous hour)
  hour 4: total  54 points (+3 from the previous hour)
  hour 5: total  54 points (+0 from the previous hour)
  hour 6: total  91 points (+37 from the previous hour)
  hour 7: total 105 points (+14 from the previous hour)
  hour 8: total 105 points (+0 from the previous hour)

=== weekly plan: each day gets its own limit ===
  day    limit   points  subjects
  Mon        7      105  CN, Soft Skills
  Tue        7      105  CN, Soft Skills
  Wed        5       54  Soft Skills
  Thu        8      105  CN, Soft Skills
  Fri        5       54  Soft Skills
  Sat        5       54  Soft Skills
  Sun        5       54  Soft Skills

  expected effectiveness for the week: 531 points

=== why greedy fails here ===
  greedy picks ['CN', 'Soft Skills'] -> 105 points in 7 h
  DP achieves 105 points, a difference of 0

```

</details>

---

## Experiment 5 - Question 5: Longest Stable Traffic Flow

Scenario: A traffic monitoring system counts cars each minute at a junction.
Find the longest stable flow.

Rubrics covered:
  * minute-wise traffic counts generated
  * a stable flow range defined (40-60 cars)
  * the longest sequence within that range identified
  * DP used to track stable streaks

**File:** [`q5_traffic_stable_flow.py`](q5_traffic_stable_flow.py) &nbsp;&middot;&nbsp; **Run:** `python q5_traffic_stable_flow.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== car counts per minute (stable band 40-60) ===
  min  0:  40 cars  stable |#############
  min  1:  39 cars  lull   |#############
  min  2:  55 cars  stable |##################
  min  3:  77 cars  SURGE  |#########################
  min  4:  88 cars  SURGE  |#############################
  min  5:  68 cars  SURGE  |######################
  min  6:  46 cars  stable |###############
  min  7:  59 cars  stable |###################
  min  8:  45 cars  stable |###############
  min  9:  56 cars  stable |##################
  min 10:  43 cars  stable |##############
  min 11:  60 cars  stable |####################
  min 12:  59 cars  stable |###################
  min 13:  53 cars  stable |#################
  min 14:  45 cars  stable |###############
  min 15:  42 cars  stable |##############
  min 16:  65 cars  SURGE  |#####################
  min 17:  44 cars  stable |##############
  min 18:  41 cars  stable |#############
  min 19:  42 cars  stable |##############
  min 20:  47 cars  stable |###############
  min 21:  57 cars  stable |###################
  min 22:  55 cars  stable |##################
  min 23:  60 cars  stable |####################
  min 24:  41 cars  stable |#############
  min 25:  55 cars  stable |##################
  min 26:  13 cars  lull   |####
  min 27:  52 cars  stable |#################
  min 28:  54 cars  stable |##################
  min 29:  75 cars  SURGE  |#########################
  min 30:  58 cars  stable |###################
  min 31:  42 cars  stable |##############
  min 32:  43 cars  stable |##############
  min 33:  72 cars  SURGE  |########################
  min 34:  44 cars  stable |##############
  min 35:  16 cars  lull   |#####
  min 36:  51 cars  stable |#################
  min 37:  32 cars  lull   |##########
  min 38:  59 cars  stable |###################
  min 39:  56 cars  stable |##################

=== overall ===
  minutes monitored : 40
  average flow      : 51.23 cars/min
  minutes in band   : 30 (75.0%)
  surges (> 60)    : 6
  lulls  (< 40)    : 4

=== DP streak table ===
  minutes  0- 9 counts:  40  39  55  77  88  68  46  59  45  56
                   dp    :   1   0   1   0   0   0   1   2   3   4
  minutes 10-19 counts:  43  60  59  53  45  42  65  44  41  42
                   dp    :   5   6   7   8   9  10   0   1   2   3
  minutes 20-29 counts:  47  57  55  60  41  55  13  52  54  75
                   dp    :   4   5   6   7   8   9   0   1   2   0
  minutes 30-39 counts:  58  42  43  72  44  16  51  32  59  56
                   dp    :   1   2   3   0   1   0   1   0   1   2

=== longest stable flow ===
  length   : 10 minute(s)
  minutes  : 6 to 15
  counts   : [46, 59, 45, 56, 43, 60, 59, 53, 45, 42]
  average  : 50.80 cars/min

=== every stable run ===
  minutes  0- 0 (1 min): [40]
  minutes  2- 2 (1 min): [55]
  minutes  6-15 (10 min): [46, 59, 45, 56, 43, 60, 59, 53, 45, 42]  <- longest
  minutes 17-25 (9 min): [44, 41, 42, 47, 57, 55, 60, 41, 55]
  minutes 27-28 (2 min): [52, 54]
  minutes 30-32 (3 min): [58, 42, 43]
  minutes 34-34 (1 min): [44]
  minutes 36-36 (1 min): [51]
  minutes 38-39 (2 min): [59, 56]

=== LCS-style match against an ideal stable pattern ===
  longest common stable subsequence: 30 of 40 minutes (75.0% similarity to steady flow)

=== verdict ===
  flow quality: steady, signal timing is fine

```

</details>

---

## Experiment 5 - Question 6: Playlist Optimisation (non-adjacent selection)

Scenario: A music streaming app records listening durations for 50 tracks.
Optimise the playlist length.

Rubrics covered:
  * track durations generated
  * a time constraint set (60 minutes)
  * maximum number of non-adjacent tracks that fit found
  * memoisation stores the results of subproblems

**File:** [`q6_playlist_non_adjacent.py`](q6_playlist_non_adjacent.py) &nbsp;&middot;&nbsp; **Run:** `python q6_playlist_non_adjacent.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 5 - Question 6: Playlist Optimisation (non-adjacent selection)

Scenario: A music streaming app records listening durations for 50 tracks.
Optimise the playlist length.

Rubrics covered:
  * track durations generated
  * a time constraint set (60 minutes)
  * maximum number of non-adjacent tracks that fit found
  * memoisation stores the results of subproblems
"""

import random
import sys
from functools import lru_cache

TRACKS = 50
TIME_LIMIT = 60 * 60          # 60 minutes in seconds


def generate_durations(seed=31):
    """Track lengths in seconds, 1:30 to 6:30."""
    random.seed(seed)
    return [random.randint(90, 390) for _ in range(TRACKS)]


def max_tracks_memo(durations, limit):
    """Maximum COUNT of non-adjacent tracks fitting inside the limit.
    State = (index, time left). Memoised top-down recursion."""
    calls = {"n": 0}

    @lru_cache(maxsize=None)
    def best(i, remaining):
        calls["n"] += 1
        if i >= len(durations):
            return 0
        # skip track i
        answer = best(i + 1, remaining)
        # take track i, then skip i+1 (non-adjacent rule)
        if durations[i] <= remaining:
            answer = max(answer, 1 + best(i + 2, remaining - durations[i]))
        return answer

    total = best(0, limit)

    chosen, i, remaining = [], 0, limit
    while i < len(durations):
        if durations[i] <= remaining and \
                1 + best(i + 2, remaining - durations[i]) >= best(i, remaining):
            chosen.append(i)
            remaining -= durations[i]
            i += 2
        else:
            i += 1
    return total, chosen, calls["n"], best.cache_info()


def max_duration_house_robber(durations):
    """Classic non-adjacent maximum SUM (no time limit), bottom-up.
    dp[i] = max(dp[i-1], dp[i-2] + durations[i])"""
    n = len(durations)
    if n == 0:
        return 0, []
    dp = [0] * (n + 1)
    dp[1] = durations[0]
    for i in range(2, n + 1):
        dp[i] = max(dp[i - 1], dp[i - 2] + durations[i - 1])
    chosen, i = [], n
    while i > 0:
        if i == 1 or dp[i] != dp[i - 1]:
            chosen.append(i - 1)
            i -= 2
        else:
            i -= 1
    return dp[n], sorted(chosen)


def fmt(seconds):
    return f"{seconds // 60}:{seconds % 60:02d}"


if __name__ == "__main__":
    sys.setrecursionlimit(5000)
    durations = generate_durations()

    print(f"=== {TRACKS} tracks, time budget {fmt(TIME_LIMIT)} ===")
    for i in range(0, TRACKS, 10):
        row = durations[i:i + 10]
        print(f"  tracks {i:>2}-{i + len(row) - 1:>2}: " +
              " ".join(fmt(d) for d in row))
    print(f"\n  total catalogue length : {fmt(sum(durations))}")
    print(f"  average track          : {fmt(sum(durations) // TRACKS)}")
    print(f"  shortest / longest     : {fmt(min(durations))} / "
          f"{fmt(max(durations))}")

    count, chosen, calls, info = max_tracks_memo(durations, TIME_LIMIT)
    used = sum(durations[i] for i in chosen)

    print("\n=== maximum number of non-adjacent tracks inside the budget ===")
    print(f"  tracks selected : {count}")
    print(f"  indices         : {chosen}")
    print(f"  playlist time   : {fmt(used)} of {fmt(TIME_LIMIT)} "
          f"({used / TIME_LIMIT * 100:.1f}% used)")
    print(f"  adjacency check : no two indices differ by 1 -> "
          f"{all(chosen[i + 1] - chosen[i] >= 2 for i in range(len(chosen) - 1))}")

    print("\n=== the playlist ===")
    for n, i in enumerate(chosen, 1):
        print(f"  {n:>2}. track {i:>2}  {fmt(durations[i])}")

    print("\n=== memoisation statistics ===")
    print(f"  recursive calls made : {calls:,}")
    print(f"  distinct states cached: {info.currsize:,}")
    print(f"  cache hits / misses   : {info.hits:,} / {info.misses:,}")
    print(f"  without the cache this would branch 2^{TRACKS} times "
          f"(~{2 ** 20:,}x more work even at 20 tracks)")

    total_sum, robber_choice = max_duration_house_robber(durations)
    print("\n=== related DP: maximum non-adjacent TOTAL time (no budget) ===")
    print(f"  best total      : {fmt(total_sum)}")
    print(f"  tracks used     : {len(robber_choice)}")
    print(f"  indices         : {robber_choice[:12]}"
          f"{' ...' if len(robber_choice) > 12 else ''}")

    print("\n=== how the answer scales with the budget ===")
    for minutes in (10, 20, 30, 45, 60, 90):
        c, picks, _, _ = max_tracks_memo(durations, minutes * 60)
        print(f"  {minutes:>3} min budget -> {c:>2} tracks, "
              f"{fmt(sum(durations[i] for i in picks))} used")
```

</details>

<details>
<summary>Program output</summary>

```text
=== 50 tracks, time budget 60:00 ===
  tracks  0- 9: 1:36 5:30 2:27 4:51 2:42 1:52 2:41 2:27 6:04 3:28
  tracks 10-19: 2:41 2:45 1:46 2:01 2:39 3:28 6:04 5:19 5:59 5:01
  tracks 20-29: 3:14 2:17 2:30 1:40 4:56 4:24 3:11 3:15 4:19 4:50
  tracks 30-39: 4:36 3:36 3:17 3:21 5:03 6:29 6:10 2:00 1:56 3:02
  tracks 40-49: 4:32 2:38 3:14 2:45 4:42 1:45 2:14 6:01 5:14 3:21

  total catalogue length : 181:53
  average track          : 3:38
  shortest / longest     : 1:36 / 6:29

=== maximum number of non-adjacent tracks inside the budget ===
  tracks selected : 21
  indices         : [0, 2, 4, 7, 9, 11, 13, 15, 19, 21, 23, 25, 27, 31, 33, 37, 39, 41, 43, 45, 49]
  playlist time   : 59:59 of 60:00 (100.0% used)
  adjacency check : no two indices differ by 1 -> True

=== the playlist ===
   1. track  0  1:36
   2. track  2  2:27
   3. track  4  2:42
   4. track  7  2:27
   5. track  9  3:28
   6. track 11  2:45
   7. track 13  2:01
   8. track 15  3:28
   9. track 19  5:01
  10. track 21  2:17
  11. track 23  1:40
  12. track 25  4:24
  13. track 27  3:15
  14. track 31  3:36
  15. track 33  3:21
  16. track 37  2:00
  17. track 39  3:02
  18. track 41  2:38
  19. track 43  2:45
  20. track 45  1:45
  21. track 49  3:21

=== memoisation statistics ===
  recursive calls made : 100,051
  distinct states cached: 100,051
  cache hits / misses   : 83,130 / 100,051
  without the cache this would branch 2^50 times (~1,048,576x more work even at 20 tracks)

=== related DP: maximum non-adjacent TOTAL time (no budget) ===
  best total      : 99:17
  tracks used     : 24
  indices         : [1, 3, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24] ...

=== how the answer scales with the budget ===
   10 min budget ->  5 tracks, 9:58 used
   20 min budget ->  9 tracks, 19:57 used
   30 min budget -> 13 tracks, 29:59 used
   45 min budget -> 17 tracks, 44:59 used
   60 min budget -> 21 tracks, 59:59 used
   90 min budget -> 25 tracks, 87:17 used

```

</details>

---

## Experiment 5 - Question 7: Longest Decreasing Spending Pattern

Scenario: A finance tracker logs daily expenses for 30 days. Find the longest
decreasing spending pattern.

Rubrics covered:
  * daily expense values generated
  * compared with a decreasing sequence
  * DP used to find the longest match
  * savings behaviour analysed

**File:** [`q7_expense_decreasing_lcs.py`](q7_expense_decreasing_lcs.py) &nbsp;&middot;&nbsp; **Run:** `python q7_expense_decreasing_lcs.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 5 - Question 7: Longest Decreasing Spending Pattern

Scenario: A finance tracker logs daily expenses for 30 days. Find the longest
decreasing spending pattern.

Rubrics covered:
  * daily expense values generated
  * compared with a decreasing sequence
  * DP used to find the longest match
  * savings behaviour analysed
"""

import random

DAYS = 30


def generate_expenses(seed=18):
    """Spending that drifts downwards as the month goes on."""
    random.seed(seed)
    data = []
    for day in range(DAYS):
        trend = 1200 - day * 22                   # the user is cutting back
        data.append(max(50, int(trend + random.gauss(0, 220))))
    return data


def longest_decreasing_subsequence(a):
    """dp[i] = longest strictly decreasing subsequence ending at i. O(n^2)."""
    n = len(a)
    dp = [1] * n
    parent = [-1] * n
    for i in range(1, n):
        for j in range(i):
            if a[j] > a[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                parent[i] = j
    best = max(dp)
    idx = dp.index(best)
    path = []
    while idx != -1:
        path.append(idx)
        idx = parent[idx]
    return best, list(reversed(path)), dp


def longest_consecutive_decrease(a):
    """Longest run of consecutive days where each day spends less. O(n)."""
    dp = [1] * len(a)
    for i in range(1, len(a)):
        if a[i] < a[i - 1]:
            dp[i] = dp[i - 1] + 1
    best = max(dp)
    end = dp.index(best)
    return best, end - best + 1, dp


def lcs_against_decreasing(a):
    """LCS between the real series and a sorted-descending copy of it:
    this is exactly the longest non-increasing subsequence."""
    b = sorted(a, reverse=True)
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    i, j, seq = n, m, []
    while i and j:
        if a[i - 1] == b[j - 1]:
            seq.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return dp[n][m], list(reversed(seq))


if __name__ == "__main__":
    expenses = generate_expenses()

    print("=== 30 days of expenses (Rs.) ===")
    for i in range(0, DAYS, 6):
        row = expenses[i:i + 6]
        print(f"  days {i + 1:>2}-{i + len(row):>2}: " +
              " ".join(f"{v:>6,}" for v in row))

    print("\n=== month statistics ===")
    print(f"  total   : Rs.{sum(expenses):,}")
    print(f"  average : Rs.{sum(expenses) / DAYS:,.2f}")
    print(f"  highest : Rs.{max(expenses):,} (day {expenses.index(max(expenses)) + 1})")
    print(f"  lowest  : Rs.{min(expenses):,} (day {expenses.index(min(expenses)) + 1})")

    print("\n=== comparison with a strictly decreasing reference ===")
    reference = sorted(expenses, reverse=True)
    print(f"  actual (first 10)  : {expenses[:10]}")
    print(f"  sorted descending  : {reference[:10]}")
    aligned = sum(1 for x, y in zip(expenses, reference) if x == y)
    print(f"  positions matching the ideal decline: {aligned}/{DAYS}")

    lcs_len, lcs_seq = lcs_against_decreasing(expenses)
    print(f"\n  LCS with the descending copy = {lcs_len} days")
    print(f"  that subsequence : {lcs_seq}")

    best, path, dp = longest_decreasing_subsequence(expenses)
    print("\n=== longest decreasing subsequence (DP, gaps allowed) ===")
    print(f"  length : {best} days of {DAYS}")
    print(f"  days   : {[i + 1 for i in path]}")
    print(f"  amounts: {[expenses[i] for i in path]}")
    print(f"  dp row : {dp}")

    run, start, run_dp = longest_consecutive_decrease(expenses)
    print("\n=== longest run of consecutive cut-backs ===")
    print(f"  length : {run} day(s)")
    print(f"  days   : {start + 1} to {start + run}")
    print(f"  amounts: {expenses[start:start + run]}")

    print("\n=== all decreasing runs of 3+ days ===")
    length, begin = 1, 0
    for i in range(1, DAYS):
        if expenses[i] < expenses[i - 1]:
            length += 1
        else:
            if length >= 3:
                print(f"  days {begin + 1:>2}-{i:>2} ({length} days): "
                      f"{expenses[begin:i]}")
            length, begin = 1, i
    if length >= 3:
        print(f"  days {begin + 1:>2}-{DAYS:>2} ({length} days): "
              f"{expenses[begin:]}")

    print("\n=== savings behaviour ===")
    week1 = sum(expenses[:7])
    week4 = sum(expenses[21:28])
    drops = sum(1 for i in range(1, DAYS) if expenses[i] < expenses[i - 1])
    print(f"  week 1 total : Rs.{week1:,}")
    print(f"  week 4 total : Rs.{week4:,}")
    print(f"  change       : Rs.{week4 - week1:+,} "
          f"({(week4 - week1) / week1 * 100:+.1f}%)")
    print(f"  days spending less than the day before: {drops}/{DAYS - 1}")
    print(f"  verdict      : " +
          ("clear savings discipline, spending is trending down"
           if week4 < week1 and best >= DAYS // 3 else
           "spending is mostly flat" if abs(week4 - week1) < week1 * 0.1 else
           "spending is creeping up, review the budget"))
```

</details>

<details>
<summary>Program output</summary>

```text
=== 30 days of expenses (Rs.) ===
  days  1- 6:  1,335  1,472  1,081  1,259    855  1,106
  days  7-12:    826  1,076  1,008  1,169    910    775
  days 13-18:    759    569  1,243    475    863    987
  days 19-24:    776    495    858  1,054  1,008    395
  days 25-30:    711    831  1,227    631    649    910

=== month statistics ===
  total   : Rs.27,313
  average : Rs.910.43
  highest : Rs.1,472 (day 2)
  lowest  : Rs.395 (day 24)

=== comparison with a strictly decreasing reference ===
  actual (first 10)  : [1335, 1472, 1081, 1259, 855, 1106, 826, 1076, 1008, 1169]
  sorted descending  : [1472, 1335, 1259, 1243, 1227, 1169, 1106, 1081, 1076, 1054]
  positions matching the ideal decline: 0/30

  LCS with the descending copy = 11 days
  that subsequence : [1335, 1259, 1106, 1076, 1008, 910, 775, 759, 569, 475, 395]

=== longest decreasing subsequence (DP, gaps allowed) ===
  length : 11 days of 30
  days   : [1, 4, 6, 8, 9, 11, 12, 13, 14, 16, 24]
  amounts: [1335, 1259, 1106, 1076, 1008, 910, 775, 759, 569, 475, 395]
  dp row : [1, 1, 2, 2, 3, 3, 4, 4, 5, 3, 6, 7, 8, 9, 3, 10, 7, 6, 8, 10, 8, 5, 6, 11, 9, 9, 4, 10, 10, 7]

=== longest run of consecutive cut-backs ===
  length : 5 day(s)
  days   : 10 to 14
  amounts: [1169, 910, 775, 759, 569]

=== all decreasing runs of 3+ days ===
  days 10-14 (5 days): [1169, 910, 775, 759, 569]
  days 18-20 (3 days): [987, 776, 495]
  days 22-24 (3 days): [1054, 1008, 395]

=== savings behaviour ===
  week 1 total : Rs.7,934
  week 4 total : Rs.5,857
  change       : Rs.-2,077 (-26.2%)
  days spending less than the day before: 14/29
  verdict      : clear savings discipline, spending is trending down

```

</details>

---

## Experiment 5 - Question 8: Robot Vacuum Area Coverage (Knapsack)

Scenario: A robot vacuum must cover sections of a room with different energy
costs. Maximise the area cleaned under a battery limit.

Rubrics covered:
  * cost and area generated for each section
  * total energy budget set
  * optimal subset of sections chosen
  * tabulation used to optimise memory use

**File:** [`q8_vacuum_area_knapsack.py`](q8_vacuum_area_knapsack.py) &nbsp;&middot;&nbsp; **Run:** `python q8_vacuum_area_knapsack.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== room sections, battery budget 70 units ===
  section       energy  area (m2)  m2 per unit
  Hall              14          6         0.43
  Kitchen            5         22         4.40
  Bedroom 1         14         17         1.21
  Bedroom 2         17         20         1.18
  Study             16          8         0.50
  Balcony           11         12         1.09
  Corridor          19          4         0.21
  Bathroom          12         23         1.92
  Dining            19          4         0.21
  Store              8          6         0.75
  Puja Room         20         17         0.85
  Lobby              5         20         4.00

  cleaning the whole flat needs 160 units for 159 m2 (only 70 units available)

=== optimal cleaning plan ===
  Kitchen        5 units ->  22 m2
  Bedroom 1     14 units ->  17 m2
  Bedroom 2     17 units ->  20 m2
  Balcony       11 units ->  12 m2
  Bathroom      12 units ->  23 m2
  Lobby          5 units ->  20 m2
  total: 64/70 units, 114 m2 cleaned
  skipped: Hall, Study, Corridor, Dining, Store, Puja Room

=== 2-D table vs 1-D tabulation ===
  2-D: 114 m2, 923 cells stored (13 rows x 71 cols)
  1-D: 114 m2, 71 cells stored (one row)
  same answer        : True
  same sections      : True
  memory saved       : 92.3%

=== how much can be cleaned as the battery grows ===
    0 units ->   0 m2 in 0 section(s)
    7 units ->  22 m2 in 1 section(s)
   14 units ->  42 m2 in 2 section(s)
   21 units ->  54 m2 in 3 section(s)
   28 units ->  65 m2 in 3 section(s)
   35 units ->  77 m2 in 4 section(s)
   42 units ->  85 m2 in 4 section(s)
   49 units ->  94 m2 in 5 section(s)
   56 units -> 102 m2 in 5 section(s)
   63 units -> 108 m2 in 6 section(s)
   70 units -> 114 m2 in 6 section(s)

=== greedy by area-per-unit, for comparison ===
  greedy cleans 114 m2 using 64 units
  DP cleans     114 m2 using 64 units (+0 m2 better)

```

</details>

---

## Experiment 5 - Question 9: Stock Growth Prediction (Fibonacci-style recurrence)

Scenario: A stock app tracks price changes hourly. Predict future growth using
previous trends.

Rubrics covered:
  * hourly price changes generated
  * price growth modelled with a recurrence relation
  * next value predicted using DP
  * computed values stored to avoid repetition

**File:** [`q9_stock_growth_recurrence.py`](q9_stock_growth_recurrence.py) &nbsp;&middot;&nbsp; **Run:** `python q9_stock_growth_recurrence.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 5 - Question 9: Stock Growth Prediction (Fibonacci-style recurrence)

Scenario: A stock app tracks price changes hourly. Predict future growth using
previous trends.

Rubrics covered:
  * hourly price changes generated
  * price growth modelled with a recurrence relation
  * next value predicted using DP
  * computed values stored to avoid repetition
"""

import random
import time
from functools import lru_cache

HOURS = 24


def generate_changes(seed=27):
    """Hourly percentage change in the stock price."""
    random.seed(seed)
    return [round(random.gauss(0.18, 1.1), 2) for _ in range(HOURS)]


def rebuild_prices(start, changes):
    prices = [start]
    for pct in changes:
        prices.append(round(prices[-1] * (1 + pct / 100), 2))
    return prices


# ---------- recurrence 1: momentum model, m(t) = a*m(t-1) + b*m(t-2) ----------
def momentum_naive(t, seed_values, a=0.6, b=0.3, counter=None):
    """Plain recursion: every call recomputes the same subproblems."""
    if counter is not None:
        counter["n"] += 1
    if t < len(seed_values):
        return seed_values[t]
    return (a * momentum_naive(t - 1, seed_values, a, b, counter) +
            b * momentum_naive(t - 2, seed_values, a, b, counter))


def momentum_memo(t, seed_values, a=0.6, b=0.3, memo=None, counter=None):
    """Top-down DP: each t is computed once and stored."""
    if memo is None:
        memo = {}
    if counter is not None:
        counter["n"] += 1
    if t < len(seed_values):
        return seed_values[t]
    if t in memo:
        return memo[t]
    memo[t] = (a * momentum_memo(t - 1, seed_values, a, b, memo, counter) +
               b * momentum_memo(t - 2, seed_values, a, b, memo, counter))
    return memo[t]


def momentum_bottom_up(n, seed_values, a=0.6, b=0.3):
    """Tabulation: fill the table forwards, no recursion at all."""
    table = list(seed_values)
    for t in range(len(seed_values), n + 1):
        table.append(a * table[t - 1] + b * table[t - 2])
    return table


# ---------- recurrence 2: Fibonacci-weighted forecast ----------
@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def fib_weighted_forecast(history, horizon=5, window=5):
    """Weight the last `window` observations by Fibonacci numbers, so the
    most recent hours matter most, then roll the forecast forward."""
    series = list(history)
    for _ in range(horizon):
        recent = series[-window:]
        weights = [fib(i + 2) for i in range(len(recent))]
        nxt = sum(v * w for v, w in zip(recent, weights)) / sum(weights)
        series.append(round(nxt, 3))
    return series[len(history):]


if __name__ == "__main__":
    changes = generate_changes()
    prices = rebuild_prices(1500.0, changes)

    print("=== hourly price changes and the resulting price ===")
    print(f"  {'hour':<6}{'change %':>10}{'price':>12}")
    for h, (pct, price) in enumerate(zip(changes, prices[1:])):
        arrow = "up" if pct > 0 else "down" if pct < 0 else "flat"
        print(f"  {h:<6}{pct:>+10.2f}{price:>12,.2f}  {arrow}")

    print(f"\n  opening price : Rs.{prices[0]:,.2f}")
    print(f"  closing price : Rs.{prices[-1]:,.2f}")
    print(f"  net move      : {(prices[-1] / prices[0] - 1) * 100:+.2f}%")
    print(f"  best hour     : {max(changes):+.2f}% at hour "
          f"{changes.index(max(changes))}")
    print(f"  worst hour    : {min(changes):+.2f}% at hour "
          f"{changes.index(min(changes))}")

    seed_values = changes[:2]
    print("\n=== momentum recurrence  m(t) = 0.6*m(t-1) + 0.3*m(t-2) ===")
    print(f"  seed: m(0)={seed_values[0]:+.2f}%, m(1)={seed_values[1]:+.2f}%")

    naive_counter = {"n": 0}
    memo_counter = {"n": 0}
    t = 22
    t0 = time.perf_counter()
    naive_val = momentum_naive(t, seed_values, counter=naive_counter)
    naive_ms = (time.perf_counter() - t0) * 1000
    t0 = time.perf_counter()
    memo_val = momentum_memo(t, seed_values, counter=memo_counter)
    memo_ms = (time.perf_counter() - t0) * 1000

    print(f"\n  m({t}) naive  = {naive_val:+.6f}%  "
          f"({naive_counter['n']:,} calls, {naive_ms:.2f} ms)")
    print(f"  m({t}) memo   = {memo_val:+.6f}%  "
          f"({memo_counter['n']:,} calls, {memo_ms:.3f} ms)")
    print(f"  identical            : {abs(naive_val - memo_val) < 1e-9}")
    print(f"  calls avoided        : "
          f"{naive_counter['n'] - memo_counter['n']:,} "
          f"({naive_counter['n'] / memo_counter['n']:.0f}x fewer)")

    table = momentum_bottom_up(t, seed_values)
    print(f"  bottom-up table[{t}] = {table[t]:+.6f}%  (matches: "
          f"{abs(table[t] - memo_val) < 1e-9})")

    print("\n=== stored subproblem table (bottom-up) ===")
    for h in range(0, len(table), 4):
        row = table[h:h + 4]
        print(f"  t={h:>2}-{h + len(row) - 1:<2} " +
              " ".join(f"{v:>+9.4f}" for v in row))

    print("\n=== Fibonacci-weighted forecast for the next 5 hours ===")
    forecast = fib_weighted_forecast(changes, horizon=5)
    future_price = prices[-1]
    print(f"  weights used (Fibonacci): "
          f"{[fib(i + 2) for i in range(5)]} - the latest hour weighs most")
    for i, pct in enumerate(forecast, 1):
        future_price = round(future_price * (1 + pct / 100), 2)
        print(f"  hour +{i}: predicted change {pct:+.3f}%  "
              f"-> price Rs.{future_price:,.2f}")
    print(f"\n  fib() cache after the run: {fib.cache_info()}")
    print(f"  predicted move over 5 hours: "
          f"{(future_price / prices[-1] - 1) * 100:+.2f}%")

    print("\n  Note: this is a lab exercise in recurrences and memoisation,")
    print("  not a trading model. Real prices are not Fibonacci-generated.")
```

</details>

<details>
<summary>Program output</summary>

```text
=== hourly price changes and the resulting price ===
  hour    change %       price
  0          -0.84    1,487.40  down
  1          -1.19    1,469.70  down
  2          +0.88    1,482.63  up
  3          -0.01    1,482.48  down
  4          +2.06    1,513.02  up
  5          +1.00    1,528.15  up
  6          -0.35    1,522.80  down
  7          +1.10    1,539.55  up
  8          +0.46    1,546.63  up
  9          -0.46    1,539.52  down
  10         +1.26    1,558.92  up
  11         -0.51    1,550.97  down
  12         +2.40    1,588.19  up
  13         +1.25    1,608.04  up
  14         -0.22    1,604.50  down
  15         -0.02    1,604.18  down
  16         +1.18    1,623.11  up
  17         -1.43    1,599.90  down
  18         +0.08    1,601.18  up
  19         -1.43    1,578.28  down
  20         +0.35    1,583.80  up
  21         +0.17    1,586.49  up
  22         +1.74    1,614.09  up
  23         -0.07    1,612.96  down

  opening price : Rs.1,500.00
  closing price : Rs.1,612.96
  net move      : +7.53%
  best hour     : +2.40% at hour 12
  worst hour    : -1.43% at hour 17

=== momentum recurrence  m(t) = 0.6*m(t-1) + 0.3*m(t-2) ===
  seed: m(0)=-0.84%, m(1)=-1.19%

  m(22) naive  = -0.208213%  (57,313 calls, 6.45 ms)
  m(22) memo   = -0.208213%  (43 calls, 0.023 ms)
  identical            : True
  calls avoided        : 57,270 (1333x fewer)
  bottom-up table[22] = -0.208213%  (matches: True)

=== stored subproblem table (bottom-up) ===
  t= 0-3    -0.8400   -1.1900   -0.9660   -0.9366
  t= 4-7    -0.8518   -0.7920   -0.7307   -0.6761
  t= 8-11   -0.6249   -0.5777   -0.5341   -0.4938
  t=12-15   -0.4565   -0.4220   -0.3902   -0.3607
  t=16-19   -0.3335   -0.3083   -0.2850   -0.2635
  t=20-22   -0.2436   -0.2252   -0.2082

=== Fibonacci-weighted forecast for the next 5 hours ===
  weights used (Fibonacci): [1, 2, 3, 5, 8] - the latest hour weighs most
  hour +1: predicted change +0.417%  -> price Rs.1,619.69
  hour +2: predicted change +0.468%  -> price Rs.1,627.27
  hour +3: predicted change +0.488%  -> price Rs.1,635.21
  hour +4: predicted change +0.479%  -> price Rs.1,643.04
  hour +5: predicted change +0.444%  -> price Rs.1,650.34

  fib() cache after the run: CacheInfo(hits=33, misses=7, maxsize=None, currsize=7)
  predicted move over 5 hours: +2.32%

  Note: this is a lab exercise in recurrences and memoisation,
  not a trading model. Real prices are not Fibonacci-generated.

```

</details>

---

## Experiment 5 - Question 10: Road Trip Rewards (House Robber pattern)

Scenario: A travel app plans a road trip through cities with a reward at each
stop. Maximise the total reward without visiting adjacent cities.

Rubrics covered:
  * reward values generated per city
  * adjacent city selection avoided
  * bottom-up DP used to calculate the maximum reward
  * iterative and recursive approaches compared

**File:** [`q10_road_trip_house_robber.py`](q10_road_trip_house_robber.py) &nbsp;&middot;&nbsp; **Run:** `python q10_road_trip_house_robber.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 5 - Question 10: Road Trip Rewards (House Robber pattern)

Scenario: A travel app plans a road trip through cities with a reward at each
stop. Maximise the total reward without visiting adjacent cities.

Rubrics covered:
  * reward values generated per city
  * adjacent city selection avoided
  * bottom-up DP used to calculate the maximum reward
  * iterative and recursive approaches compared
"""

import random
import time
from functools import lru_cache

CITIES = ["Pune", "Nashik", "Shirdi", "Aurangabad", "Jalgaon", "Dhule",
          "Nagpur", "Amravati", "Akola", "Nanded", "Latur", "Solapur",
          "Kolhapur", "Satara", "Ratnagiri"]


def generate_rewards(seed=37):
    random.seed(seed)
    return [random.randint(20, 160) for _ in CITIES]


# ---------------- bottom-up tabulation ----------------
def rob_bottom_up(rewards):
    """dp[i] = best reward using the first i cities.
    dp[i] = max(dp[i-1], dp[i-2] + rewards[i-1])"""
    n = len(rewards)
    if n == 0:
        return 0, [], []
    dp = [0] * (n + 1)
    dp[1] = rewards[0]
    for i in range(2, n + 1):
        dp[i] = max(dp[i - 1], dp[i - 2] + rewards[i - 1])

    chosen, i = [], n
    while i > 0:
        if i == 1:
            if dp[1] > 0:
                chosen.append(0)
            break
        if dp[i] == dp[i - 1]:
            i -= 1
        else:
            chosen.append(i - 1)
            i -= 2
    return dp[n], sorted(chosen), dp


# ---------------- O(1) space version ----------------
def rob_two_variables(rewards):
    take, skip = 0, 0
    for r in rewards:
        take, skip = skip + r, max(skip, take)
    return max(take, skip)


# ---------------- recursive versions ----------------
def rob_naive(rewards, i=0, counter=None):
    if counter is not None:
        counter["n"] += 1
    if i >= len(rewards):
        return 0
    return max(rob_naive(rewards, i + 1, counter),
               rewards[i] + rob_naive(rewards, i + 2, counter))


def rob_memo(rewards, counter=None):
    rewards = tuple(rewards)

    @lru_cache(maxsize=None)
    def best(i):
        if counter is not None:
            counter["n"] += 1
        if i >= len(rewards):
            return 0
        return max(best(i + 1), rewards[i] + best(i + 2))

    return best(0), best.cache_info()


if __name__ == "__main__":
    rewards = generate_rewards()

    print("=== candidate stops and their rewards ===")
    for i, (city, r) in enumerate(zip(CITIES, rewards)):
        print(f"  {i:>2} {city:<12} {r:>4} points |{'#' * (r // 6)}")
    print(f"\n  {len(CITIES)} cities, total reward if adjacency were allowed: "
          f"{sum(rewards)}")

    best, chosen, dp = rob_bottom_up(rewards)

    print("\n=== optimal itinerary (bottom-up DP) ===")
    for i in chosen:
        print(f"  stop at {CITIES[i]:<12} (+{rewards[i]} points)")
    print(f"  total reward : {best} points from {len(chosen)} stop(s)")
    skipped = [CITIES[i] for i in range(len(CITIES)) if i not in chosen]
    print(f"  skipped      : {', '.join(skipped)}")
    print(f"  no two stops adjacent: "
          f"{all(chosen[i + 1] - chosen[i] >= 2 for i in range(len(chosen) - 1))}")

    print("\n=== DP table ===")
    print(f"  {'i':>3} {'city':<12}{'reward':>8}{'dp[i]':>8}  decision")
    print(f"  {0:>3} {'(start)':<12}{'-':>8}{dp[0]:>8}")
    for i in range(1, len(dp)):
        decision = "skip" if i >= 2 and dp[i] == dp[i - 1] else "take"
        print(f"  {i:>3} {CITIES[i - 1]:<12}{rewards[i - 1]:>8}{dp[i]:>8}  "
              f"{decision}")

    print("\n=== iterative vs recursive ===")
    naive_counter = {"n": 0}
    memo_counter = {"n": 0}

    t0 = time.perf_counter()
    naive = rob_naive(rewards, counter=naive_counter)
    naive_ms = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    memo, info = rob_memo(rewards, memo_counter)
    memo_ms = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    iterative = rob_two_variables(rewards)
    iter_ms = (time.perf_counter() - t0) * 1000

    print(f"  {'method':<28}{'reward':>8}{'calls':>10}{'time (ms)':>12}"
          f"{'memory':>12}")
    print(f"  {'naive recursion':<28}{naive:>8}{naive_counter['n']:>10,}"
          f"{naive_ms:>12.3f}{'O(n) stack':>12}")
    print(f"  {'memoised recursion':<28}{memo:>8}{memo_counter['n']:>10,}"
          f"{memo_ms:>12.3f}{'O(n) cache':>12}")
    print(f"  {'bottom-up table':<28}{best:>8}{'-':>10}"
          f"{'-':>12}{'O(n) table':>12}")
    print(f"  {'two variables':<28}{iterative:>8}{'-':>10}"
          f"{iter_ms:>12.3f}{'O(1)':>12}")
    print(f"\n  all four agree  : "
          f"{naive == memo == best == iterative}")
    print(f"  cache info      : {info}")
    print(f"  recursion saved : "
          f"{naive_counter['n'] - memo_counter['n']:,} calls")

    print("\n=== scaling: naive recursion becomes unusable ===")
    for n in (10, 15, 20, 25):
        sub = rewards[:n] * (n // len(rewards) + 1)
        sub = sub[:n]
        c = {"n": 0}
        t0 = time.perf_counter()
        rob_naive(sub, counter=c)
        ms = (time.perf_counter() - t0) * 1000
        print(f"  n={n:<3} naive {c['n']:>9,} calls in {ms:>8.2f} ms   "
              f"bottom-up: {n} steps")
```

</details>

<details>
<summary>Program output</summary>

```text
=== candidate stops and their rewards ===
   0 Pune           43 points |#######
   1 Nashik        151 points |#########################
   2 Shirdi         29 points |####
   3 Aurangabad    114 points |###################
   4 Jalgaon       132 points |######################
   5 Dhule         155 points |#########################
   6 Nagpur         47 points |#######
   7 Amravati      136 points |######################
   8 Akola          92 points |###############
   9 Nanded        116 points |###################
  10 Latur         128 points |#####################
  11 Solapur       133 points |######################
  12 Kolhapur       56 points |#########
  13 Satara         32 points |#####
  14 Ratnagiri      43 points |#######

  15 cities, total reward if adjacency were allowed: 1407

=== optimal itinerary (bottom-up DP) ===
  stop at Nashik       (+151 points)
  stop at Aurangabad   (+114 points)
  stop at Dhule        (+155 points)
  stop at Amravati     (+136 points)
  stop at Nanded       (+116 points)
  stop at Solapur      (+133 points)
  stop at Ratnagiri    (+43 points)
  total reward : 848 points from 7 stop(s)
  skipped      : Pune, Shirdi, Jalgaon, Nagpur, Akola, Latur, Kolhapur, Satara
  no two stops adjacent: True

=== DP table ===
    i city          reward   dp[i]  decision
    0 (start)            -       0
    1 Pune              43      43  take
    2 Nashik           151     151  take
    3 Shirdi            29     151  skip
    4 Aurangabad       114     265  take
    5 Jalgaon          132     283  take
    6 Dhule            155     420  take
    7 Nagpur            47     420  skip
    8 Amravati         136     556  take
    9 Akola             92     556  skip
   10 Nanded           116     672  take
   11 Latur            128     684  take
   12 Solapur          133     805  take
   13 Kolhapur          56     805  skip
   14 Satara            32     837  take
   15 Ratnagiri         43     848  take

=== iterative vs recursive ===
  method                        reward     calls   time (ms)      memory
  naive recursion                  848     3,193       0.453  O(n) stack
  memoised recursion               848        17       0.027  O(n) cache
  bottom-up table                  848         -           -  O(n) table
  two variables                    848         -       0.004        O(1)

  all four agree  : True
  cache info      : CacheInfo(hits=14, misses=17, maxsize=None, currsize=17)
  recursion saved : 3,176 calls

=== scaling: naive recursion becomes unusable ===
  n=10  naive       287 calls in     0.04 ms   bottom-up: 10 steps
  n=15  naive     3,193 calls in     0.44 ms   bottom-up: 15 steps
  n=20  naive    35,421 calls in     4.89 ms   bottom-up: 20 steps
  n=25  naive   392,835 calls in    53.52 ms   bottom-up: 25 steps

```

</details>

---
