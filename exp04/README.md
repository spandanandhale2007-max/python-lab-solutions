# Experiment 4 - Unit II

Introduction to dynamic programming and list-based data analysis

10 scenario questions, each solved in its own section and its own file. Every program below was executed and the real output is included.

[Back to the index](../README.md)

---

## Questions in this experiment

- [Experiment 4 - Question 1: Climbing Stairs (naive recursion)](#experiment-4---question-1-climbing-stairs-naive-recursion)
- [Experiment 4 - Question 2: Climbing Stairs (memoised, top-down)](#experiment-4---question-2-climbing-stairs-memoised-top-down)
- [Experiment 4 - Question 3: Weather Station Daily Trend](#experiment-4---question-3-weather-station-daily-trend)
- [Experiment 4 - Question 4: Robotic Vacuum Efficiency](#experiment-4---question-4-robotic-vacuum-efficiency)
- [Experiment 4 - Question 5: Online Learning Quiz Progress](#experiment-4---question-5-online-learning-quiz-progress)
- [Experiment 4 - Question 6: Daily Expense Summary](#experiment-4---question-6-daily-expense-summary)
- [Experiment 4 - Question 7: Weather Sensor Anomaly Detection](#experiment-4---question-7-weather-sensor-anomaly-detection)
- [Experiment 4 - Question 8: Robot Vacuum Cleaning Efficiency (60 minutes)](#experiment-4---question-8-robot-vacuum-cleaning-efficiency-60-minutes)
- [Experiment 4 - Question 9: Diet Calorie Balance](#experiment-4---question-9-diet-calorie-balance)
- [Experiment 4 - Question 10: Traffic Flow Analysis](#experiment-4---question-10-traffic-flow-analysis)

---

## Experiment 4 - Question 1: Climbing Stairs (naive recursion)

Scenario: A fitness app tracks the different ways a user can climb a staircase.
A user climbs either 1 step or 2 steps at a time. Count the unique ways to
climb a staircase of n steps.

Rubrics covered:
  * demonstrates overlapping subproblems
  * correct logic
  * measures the inefficiency of plain recursion

**File:** [`q1_climbing_stairs_naive.py`](q1_climbing_stairs_naive.py) &nbsp;&middot;&nbsp; **Run:** `python q1_climbing_stairs_naive.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 4 - Question 1: Climbing Stairs (naive recursion)

Scenario: A fitness app tracks the different ways a user can climb a staircase.
A user climbs either 1 step or 2 steps at a time. Count the unique ways to
climb a staircase of n steps.

Rubrics covered:
  * demonstrates overlapping subproblems
  * correct logic
  * measures the inefficiency of plain recursion
"""

import sys
import time
from collections import Counter

call_counter = Counter()
total_calls = 0


def climb_naive(n):
    """Plain recursion: ways(n) = ways(n-1) + ways(n-2)."""
    global total_calls
    total_calls += 1
    call_counter[n] += 1
    if n < 0:
        return 0
    if n in (0, 1):
        return 1
    return climb_naive(n - 1) + climb_naive(n - 2)


def climb_iterative(n):
    """Correct answer in O(n) time and O(1) space, used as a reference."""
    if n < 0:
        return 0
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b if n >= 1 else 1


def call_tree(n, depth=0, lines=None):
    """Prints the first few levels of the recursion tree to show repeats."""
    if lines is None:
        lines = []
    if depth > 3:
        return lines
    lines.append("  " * depth + f"climb({n})")
    if n >= 2:
        call_tree(n - 1, depth + 1, lines)
        call_tree(n - 2, depth + 1, lines)
    return lines


if __name__ == "__main__":
    sys.setrecursionlimit(10000)

    print("=== correct logic check against the iterative formula ===")
    print(f"  {'n':>3} {'naive':>8} {'iterative':>10} {'match':>6}")
    for n in range(1, 11):
        total_calls = 0
        call_counter.clear()
        naive = climb_naive(n)
        ref = climb_iterative(n)
        print(f"  {n:>3} {naive:>8} {ref:>10} {str(naive == ref):>6}")

    print("\n=== overlapping subproblems: climb(10) call counts per value ===")
    total_calls = 0
    call_counter.clear()
    climb_naive(10)
    print(f"  total recursive calls for n=10 : {total_calls}")
    for value in sorted(call_counter, reverse=True):
        print(f"    climb({value:>2}) was computed {call_counter[value]:>3} time(s)")
    print("  the same subproblem is recomputed again and again")

    print("\n=== recursion tree for n=6, first four levels ===")
    for line in call_tree(6):
        print("   " + line)

    print("\n=== measuring the inefficiency ===")
    print(f"  {'n':>3} {'ways':>10} {'calls':>12} {'time (ms)':>12} "
          f"{'calls/answer':>13}")
    for n in (10, 15, 20, 25, 30):
        total_calls = 0
        call_counter.clear()
        start = time.perf_counter()
        ways = climb_naive(n)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"  {n:>3} {ways:>10} {total_calls:>12,} {elapsed:>12.2f} "
              f"{total_calls / ways:>13.2f}")

    print("\n  Calls grow like the answer itself, i.e. O(2^n) / golden-ratio^n.")
    print("  Each +5 steps multiplies the work by about 11x.")
    print("  n = 50 by plain recursion would need ~2.5e10 calls, hours of CPU.")
    print("  Fix: memoise the repeated subproblems (see question 2).")
```

</details>

<details>
<summary>Program output</summary>

```text
=== correct logic check against the iterative formula ===
    n    naive  iterative  match
    1        1          1   True
    2        2          2   True
    3        3          3   True
    4        5          5   True
    5        8          8   True
    6       13         13   True
    7       21         21   True
    8       34         34   True
    9       55         55   True
   10       89         89   True

=== overlapping subproblems: climb(10) call counts per value ===
  total recursive calls for n=10 : 177
    climb(10) was computed   1 time(s)
    climb( 9) was computed   1 time(s)
    climb( 8) was computed   2 time(s)
    climb( 7) was computed   3 time(s)
    climb( 6) was computed   5 time(s)
    climb( 5) was computed   8 time(s)
    climb( 4) was computed  13 time(s)
    climb( 3) was computed  21 time(s)
    climb( 2) was computed  34 time(s)
    climb( 1) was computed  55 time(s)
    climb( 0) was computed  34 time(s)
  the same subproblem is recomputed again and again

=== recursion tree for n=6, first four levels ===
   climb(6)
     climb(5)
       climb(4)
         climb(3)
         climb(2)
       climb(3)
         climb(2)
         climb(1)
     climb(4)
       climb(3)
         climb(2)
         climb(1)
       climb(2)
         climb(1)
         climb(0)

=== measuring the inefficiency ===
    n       ways        calls    time (ms)  calls/answer
   10         89          177         0.05          1.99
   15        987        1,973         0.59          2.00
   20      10946       21,891         4.57          2.00
   25     121393      242,785        49.61          2.00
   30    1346269    2,692,537       563.24          2.00

  Calls grow like the answer itself, i.e. O(2^n) / golden-ratio^n.
  Each +5 steps multiplies the work by about 11x.
  n = 50 by plain recursion would need ~2.5e10 calls, hours of CPU.
  Fix: memoise the repeated subproblems (see question 2).

```

</details>

---

## Experiment 4 - Question 2: Climbing Stairs (memoised, top-down)

Scenario: Climbing a staircase of n steps taking 1 or 2 steps at a time.
Count the unique ways to reach the top.

Rubrics covered:
  * correct memoization usage
  * performance improves measurably
  * top-down approach understood

**File:** [`q2_climbing_stairs_memo.py`](q2_climbing_stairs_memo.py) &nbsp;&middot;&nbsp; **Run:** `python q2_climbing_stairs_memo.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 4 - Question 2: Climbing Stairs (memoised, top-down)

Scenario: Climbing a staircase of n steps taking 1 or 2 steps at a time.
Count the unique ways to reach the top.

Rubrics covered:
  * correct memoization usage
  * performance improves measurably
  * top-down approach understood
"""

import sys
import time
from functools import lru_cache

calls_naive = 0
calls_memo = 0


def climb_naive(n):
    global calls_naive
    calls_naive += 1
    if n < 0:
        return 0
    if n in (0, 1):
        return 1
    return climb_naive(n - 1) + climb_naive(n - 2)


def climb_memo(n, memo=None):
    """Top-down: solve the big problem, cache every subproblem on the way."""
    global calls_memo
    calls_memo += 1
    if memo is None:
        memo = {}
    if n < 0:
        return 0
    if n in (0, 1):
        return 1
    if n in memo:                       # cache hit, no further recursion
        return memo[n]
    memo[n] = climb_memo(n - 1, memo) + climb_memo(n - 2, memo)
    return memo[n]


@lru_cache(maxsize=None)
def climb_lru(n):
    """Same thing using the standard library cache."""
    if n < 0:
        return 0
    if n in (0, 1):
        return 1
    return climb_lru(n - 1) + climb_lru(n - 2)


def climb_bottom_up(n):
    """Tabulation, for comparison with the top-down version."""
    if n < 0:
        return 0
    table = [0] * (max(n, 1) + 1)
    table[0] = 1
    table[1] = 1
    for i in range(2, n + 1):
        table[i] = table[i - 1] + table[i - 2]
    return table[n]


def climb_steps_variable(n, allowed=(1, 2, 3), memo=None):
    """Top-down generalisation: any set of allowed step sizes."""
    if memo is None:
        memo = {}
    if n == 0:
        return 1
    if n < 0:
        return 0
    if n in memo:
        return memo[n]
    memo[n] = sum(climb_steps_variable(n - s, allowed, memo) for s in allowed)
    return memo[n]


if __name__ == "__main__":
    sys.setrecursionlimit(20000)

    print("=== all four methods agree ===")
    print(f"  {'n':>3} {'memo':>10} {'lru_cache':>10} {'bottom-up':>10} {'match':>6}")
    for n in range(1, 16):
        a, b, c = climb_memo(n), climb_lru(n), climb_bottom_up(n)
        print(f"  {n:>3} {a:>10} {b:>10} {c:>10} {str(a == b == c):>6}")

    print("\n=== call count: naive vs memoised ===")
    print(f"  {'n':>3} {'naive calls':>14} {'memo calls':>12} {'saved':>12}")
    for n in (10, 20, 25, 30):
        calls_naive = calls_memo = 0
        climb_naive(n)
        climb_memo(n)
        print(f"  {n:>3} {calls_naive:>14,} {calls_memo:>12,} "
              f"{calls_naive / calls_memo:>11.0f}x")

    print("\n=== timing: memoisation turns exponential into linear ===")
    print(f"  {'n':>3} {'naive (ms)':>12} {'memo (ms)':>12} {'speed-up':>10}")
    for n in (20, 25, 30, 32):
        calls_naive = calls_memo = 0
        t0 = time.perf_counter()
        climb_naive(n)
        t_naive = (time.perf_counter() - t0) * 1000
        t0 = time.perf_counter()
        climb_memo(n)
        t_memo = (time.perf_counter() - t0) * 1000
        print(f"  {n:>3} {t_naive:>12.2f} {t_memo:>12.4f} "
              f"{t_naive / max(t_memo, 1e-6):>9.0f}x")

    print("\n=== sizes the naive version could never reach ===")
    for n in (100, 500, 1000):
        t0 = time.perf_counter()
        ways = climb_memo(n)
        ms = (time.perf_counter() - t0) * 1000
        print(f"  n={n:<5} ways has {len(str(ways))} digits, computed in {ms:.2f} ms")
    print("  climb(1000) starts:", str(climb_memo(1000))[:30], "...")

    print("\n=== lru_cache statistics (hits prove the cache is doing the work) ===")
    climb_lru.cache_clear()
    climb_lru(40)
    print("  ", climb_lru.cache_info())

    print("\n=== generalised: user may also climb 3 steps ===")
    for n in (3, 5, 10, 20):
        print(f"  n={n:<3} 1-or-2 steps: {climb_memo(n):>8}   "
              f"1-2-or-3 steps: {climb_steps_variable(n):>10}")

    print("\n  Top-down = recursion plus a cache: write the natural recurrence,")
    print("  store each result the first time it is computed, read it after that.")
```

</details>

<details>
<summary>Program output</summary>

```text
=== all four methods agree ===
    n       memo  lru_cache  bottom-up  match
    1          1          1          1   True
    2          2          2          2   True
    3          3          3          3   True
    4          5          5          5   True
    5          8          8          8   True
    6         13         13         13   True
    7         21         21         21   True
    8         34         34         34   True
    9         55         55         55   True
   10         89         89         89   True
   11        144        144        144   True
   12        233        233        233   True
   13        377        377        377   True
   14        610        610        610   True
   15        987        987        987   True

=== call count: naive vs memoised ===
    n    naive calls   memo calls        saved
   10            177           19           9x
   20         21,891           39         561x
   25        242,785           49        4955x
   30      2,692,537           59       45636x

=== timing: memoisation turns exponential into linear ===
    n   naive (ms)    memo (ms)   speed-up
   20         1.84       0.0077       239x
   25        20.83       0.0157      1327x
   30       235.84       0.0309      7632x
   32       614.73       0.0269     22853x

=== sizes the naive version could never reach ===
  n=100   ways has 21 digits, computed in 0.03 ms
  n=500   ways has 105 digits, computed in 0.23 ms
  n=1000  ways has 209 digits, computed in 0.42 ms
  climb(1000) starts: 703303677114228158218352548771 ...

=== lru_cache statistics (hits prove the cache is doing the work) ===
   CacheInfo(hits=38, misses=41, maxsize=None, currsize=41)

=== generalised: user may also climb 3 steps ===
  n=3   1-or-2 steps:        3   1-2-or-3 steps:          4
  n=5   1-or-2 steps:        8   1-2-or-3 steps:         13
  n=10  1-or-2 steps:       89   1-2-or-3 steps:        274
  n=20  1-or-2 steps:    10946   1-2-or-3 steps:     121415

  Top-down = recursion plus a cache: write the natural recurrence,
  store each result the first time it is computed, read it after that.

```

</details>

---

## Experiment 4 - Question 3: Weather Station Daily Trend

Scenario: A weather station records the temperature every hour for a day
(24 hours). Analyse the daily trend.

Rubrics covered:
  * temperature data generated
  * min, max and average computed

**File:** [`q3_weather_station_hourly.py`](q3_weather_station_hourly.py) &nbsp;&middot;&nbsp; **Run:** `python q3_weather_station_hourly.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 4 - Question 3: Weather Station Daily Trend

Scenario: A weather station records the temperature every hour for a day
(24 hours). Analyse the daily trend.

Rubrics covered:
  * temperature data generated
  * min, max and average computed
"""

import random

HOURS = 24


def generate_temperatures(seed=11):
    """Realistic daily curve: cool at dawn, hottest mid-afternoon."""
    random.seed(seed)
    base = [22, 21.5, 21, 20.5, 20, 20.5, 22, 24, 26.5, 29, 31, 33,
            34.5, 35.5, 35, 34, 32.5, 30.5, 28.5, 27, 26, 25, 24, 23]
    return [round(t + random.uniform(-1.2, 1.2), 1) for t in base]


def summarise(temps):
    return {
        "count": len(temps),
        "min": min(temps),
        "min_hour": temps.index(min(temps)),
        "max": max(temps),
        "max_hour": temps.index(max(temps)),
        "avg": sum(temps) / len(temps),
        "range": max(temps) - min(temps),
    }


def bar(value, lo, hi, width=40):
    filled = int((value - lo) / (hi - lo) * width) if hi > lo else 0
    return "#" * filled


if __name__ == "__main__":
    temps = generate_temperatures()

    print("=== hourly temperature log (24 readings, degrees C) ===")
    for hour, t in enumerate(temps):
        print(f"  {hour:02d}:00  {t:>5.1f} C")

    s = summarise(temps)
    print("\n=== daily summary ===")
    print(f"  readings        : {s['count']}")
    print(f"  minimum         : {s['min']:.1f} C at {s['min_hour']:02d}:00")
    print(f"  maximum         : {s['max']:.1f} C at {s['max_hour']:02d}:00")
    print(f"  average         : {s['avg']:.2f} C")
    print(f"  diurnal range   : {s['range']:.1f} C")

    print("\n=== shape of the day ===")
    lo, hi = s["min"], s["max"]
    for hour, t in enumerate(temps):
        mark = ""
        if t == hi:
            mark = "  <- hottest"
        elif t == lo:
            mark = "  <- coldest"
        print(f"  {hour:02d}:00 {t:>5.1f} |{bar(t, lo, hi):<40}|{mark}")

    print("\n=== above / below the daily average ===")
    above = [(h, t) for h, t in enumerate(temps) if t > s["avg"]]
    below = [(h, t) for h, t in enumerate(temps) if t <= s["avg"]]
    print(f"  {len(above)} hour(s) above {s['avg']:.2f} C: "
          f"{[f'{h:02d}:00' for h, _ in above]}")
    print(f"  {len(below)} hour(s) at or below average")

    print("\n=== hour-to-hour change ===")
    deltas = [round(temps[i] - temps[i - 1], 1) for i in range(1, len(temps))]
    steepest_rise = max(deltas)
    steepest_fall = min(deltas)
    print(f"  fastest warming : {steepest_rise:+.1f} C/h between "
          f"{deltas.index(steepest_rise):02d}:00 and "
          f"{deltas.index(steepest_rise) + 1:02d}:00")
    print(f"  fastest cooling : {steepest_fall:+.1f} C/h between "
          f"{deltas.index(steepest_fall):02d}:00 and "
          f"{deltas.index(steepest_fall) + 1:02d}:00")

    print("\n=== three-hour blocks ===")
    for start in range(0, HOURS, 3):
        block = temps[start:start + 3]
        print(f"  {start:02d}:00-{start + 2:02d}:59  "
              f"avg {sum(block) / len(block):>5.1f} C  "
              f"min {min(block):>5.1f}  max {max(block):>5.1f}")
```

</details>

<details>
<summary>Program output</summary>

```text
=== hourly temperature log (24 readings, degrees C) ===
  00:00   21.9 C
  01:00   21.6 C
  02:00   22.0 C
  03:00   20.4 C
  04:00   20.0 C
  05:00   20.7 C
  06:00   21.2 C
  07:00   24.0 C
  08:00   26.8 C
  09:00   29.7 C
  10:00   30.0 C
  11:00   32.5 C
  12:00   33.5 C
  13:00   36.2 C
  14:00   35.5 C
  15:00   32.9 C
  16:00   33.7 C
  17:00   31.6 C
  18:00   28.9 C
  19:00   27.3 C
  20:00   25.2 C
  21:00   23.8 C
  22:00   24.1 C
  23:00   21.9 C

=== daily summary ===
  readings        : 24
  minimum         : 20.0 C at 04:00
  maximum         : 36.2 C at 13:00
  average         : 26.89 C
  diurnal range   : 16.2 C

=== shape of the day ===
  00:00  21.9 |####                                    |
  01:00  21.6 |###                                     |
  02:00  22.0 |####                                    |
  03:00  20.4 |                                        |
  04:00  20.0 |                                        |  <- coldest
  05:00  20.7 |#                                       |
  06:00  21.2 |##                                      |
  07:00  24.0 |#########                               |
  08:00  26.8 |################                        |
  09:00  29.7 |#######################                 |
  10:00  30.0 |########################                |
  11:00  32.5 |##############################          |
  12:00  33.5 |#################################       |
  13:00  36.2 |########################################|  <- hottest
  14:00  35.5 |######################################  |
  15:00  32.9 |###############################         |
  16:00  33.7 |#################################       |
  17:00  31.6 |############################            |
  18:00  28.9 |#####################                   |
  19:00  27.3 |##################                      |
  20:00  25.2 |############                            |
  21:00  23.8 |#########                               |
  22:00  24.1 |##########                              |
  23:00  21.9 |####                                    |

=== above / below the daily average ===
  11 hour(s) above 26.89 C: ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00']
  13 hour(s) at or below average

=== hour-to-hour change ===
  fastest warming : +2.9 C/h between 08:00 and 09:00
  fastest cooling : -2.7 C/h between 17:00 and 18:00

=== three-hour blocks ===
  00:00-02:59  avg  21.8 C  min  21.6  max  22.0
  03:00-05:59  avg  20.4 C  min  20.0  max  20.7
  06:00-08:59  avg  24.0 C  min  21.2  max  26.8
  09:00-11:59  avg  30.7 C  min  29.7  max  32.5
  12:00-14:59  avg  35.1 C  min  33.5  max  36.2
  15:00-17:59  avg  32.7 C  min  31.6  max  33.7
  18:00-20:59  avg  27.1 C  min  25.2  max  28.9
  21:00-23:59  avg  23.3 C  min  21.9  max  24.1

```

</details>

---

## Experiment 4 - Question 4: Robotic Vacuum Efficiency

Scenario: A robotic vacuum logs the distance covered every minute during a
45-minute cleaning session. Evaluate its efficiency.

Rubrics covered:
  * distance data generated
  * total distance computed
  * idle minutes (0 movement) found
  * the 5-minute window with maximum movement identified

**File:** [`q4_robotic_vacuum_45min.py`](q4_robotic_vacuum_45min.py) &nbsp;&middot;&nbsp; **Run:** `python q4_robotic_vacuum_45min.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== per-minute distance log (metres) ===
  min 00-08      9.8   11.5   11.3    0.0   11.5   11.2    0.0    5.6    8.4
  min 09-17      0.0    5.9   10.0   10.3    0.0    4.6    0.0    5.3   11.9
  min 18-26      6.0    8.1    5.2    9.4   11.1    6.6    4.7    0.0    8.6
  min 27-35      0.0    6.4   10.5    6.2    9.5    0.0    3.7   10.7    0.0
  min 36-44      6.6    3.6    0.0   11.6    9.9   11.5    6.5   10.1    0.0

=== totals ===
  session length      : 45 minutes
  total distance      : 283.8 m
  average per minute  : 6.31 m
  average when moving : 8.35 m
  best single minute  : 11.9 m at minute 17

=== idle minutes (0 movement) ===
  count   : 11 of 45 (24.4% of the session)
  minutes : [3, 6, 9, 13, 15, 25, 27, 32, 35, 38, 44]
  streaks :
    minutes 03-03 (1 min)
    minutes 06-06 (1 min)
    minutes 09-09 (1 min)
    minutes 13-13 (1 min)
    minutes 15-15 (1 min)
    minutes 25-25 (1 min)
    minutes 27-27 (1 min)
    minutes 32-32 (1 min)
    minutes 35-35 (1 min)
    minutes 38-38 (1 min)
    minutes 44-44 (1 min)
  longest stall: minutes 03-03

=== best 5-minute window ===
  minutes 39-43: 49.6 m (avg 9.92 m/min)
  readings: [11.6, 9.9, 11.5, 6.5, 10.1]

=== every 5-minute window, for comparison ===
  min 00-04    44.1 m
  min 05-09    25.2 m
  min 10-14    30.8 m
  min 15-19    31.3 m
  min 20-24    37.0 m
  min 25-29    25.5 m
  min 30-34    30.1 m
  min 35-39    21.8 m
  min 40-44    38.0 m

=== efficiency verdict ===
  moving 75.6% of the time, 4.73 m per second of motion on average
  verdict: acceptable

```

</details>

---

## Experiment 4 - Question 5: Online Learning Quiz Progress

Scenario: An online learning platform records quiz scores across 20 sessions.
Track the user's progress.

Rubrics covered:
  * random score data generated
  * last 5 sessions sliced
  * min, max and average scores found
  * consistent improvement identified from the difference between sessions

**File:** [`q5_quiz_scores_progress.py`](q5_quiz_scores_progress.py) &nbsp;&middot;&nbsp; **Run:** `python q5_quiz_scores_progress.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 4 - Question 5: Online Learning Quiz Progress

Scenario: An online learning platform records quiz scores across 20 sessions.
Track the user's progress.

Rubrics covered:
  * random score data generated
  * last 5 sessions sliced
  * min, max and average scores found
  * consistent improvement identified from the difference between sessions
"""

import random

SESSIONS = 20


def generate_scores(seed=9):
    """Scores out of 100 with a mild upward trend plus noise."""
    random.seed(seed)
    scores = []
    for i in range(SESSIONS):
        trend = 45 + i * 1.8                     # learning curve
        scores.append(max(0, min(100, int(trend + random.gauss(0, 7)))))
    return scores


def longest_improving_run(scores):
    """Longest streak where each session beats the previous one.
    best[i] is the length of the improving run ending at i - a 1-D DP."""
    if not scores:
        return 0, 0, 0
    best = [1] * len(scores)
    for i in range(1, len(scores)):
        if scores[i] > scores[i - 1]:
            best[i] = best[i - 1] + 1
    length = max(best)
    end = best.index(length)
    return length, end - length + 1, end


if __name__ == "__main__":
    scores = generate_scores()

    print("=== 20 quiz sessions ===")
    for i, s in enumerate(scores, 1):
        bar = "#" * (s // 3)
        print(f"  session {i:>2}: {s:>3} |{bar}")

    print("\n=== whole-course statistics ===")
    print(f"  sessions  : {len(scores)}")
    print(f"  minimum   : {min(scores)} (session {scores.index(min(scores)) + 1})")
    print(f"  maximum   : {max(scores)} (session {scores.index(max(scores)) + 1})")
    print(f"  average   : {sum(scores) / len(scores):.2f}")
    print(f"  first vs last : {scores[0]} -> {scores[-1]} "
          f"({scores[-1] - scores[0]:+d})")

    last5 = scores[-5:]                      # slicing
    first5 = scores[:5]
    print("\n=== slices ===")
    print(f"  first 5 sessions : {first5}  avg {sum(first5) / 5:.2f}")
    print(f"  last 5 sessions  : {last5}  avg {sum(last5) / 5:.2f}")
    print(f"  improvement      : {sum(last5) / 5 - sum(first5) / 5:+.2f} marks")
    print(f"  best of last 5   : {max(last5)}   worst of last 5: {min(last5)}")
    print(f"  every 4th session: {scores[::4]}")

    print("\n=== session-to-session difference ===")
    deltas = [scores[i] - scores[i - 1] for i in range(1, len(scores))]
    for i, d in enumerate(deltas, 2):
        arrow = "up  " if d > 0 else "down" if d < 0 else "same"
        print(f"  session {i - 1:>2} -> {i:>2}: {d:>+4}  {arrow}")

    ups = sum(1 for d in deltas if d > 0)
    downs = sum(1 for d in deltas if d < 0)
    print(f"\n  improved in {ups} of {len(deltas)} transitions, "
          f"dropped in {downs}, flat in {len(deltas) - ups - downs}")

    length, start, end = longest_improving_run(scores)
    print("\n=== consistent improvement (DP on the difference array) ===")
    print(f"  longest improving streak : {length} session(s), "
          f"sessions {start + 1} to {end + 1}")
    print(f"  scores in that streak    : {scores[start:end + 1]}")
    print(f"  average gain per session : "
          f"{sum(deltas) / len(deltas):+.2f} marks")
    verdict = ("consistent improvement" if sum(deltas) > 10 and ups > downs
               else "flat progress" if abs(sum(deltas)) <= 10
               else "declining")
    print(f"  verdict                  : {verdict}")

    print("\n=== 3-session moving average (smoothed trend) ===")
    for i in range(2, len(scores)):
        window = scores[i - 2:i + 1]
        print(f"  sessions {i - 1}-{i + 1}: {sum(window) / 3:>6.2f}")
```

</details>

<details>
<summary>Program output</summary>

```text
=== 20 quiz sessions ===
  session  1:  38 |############
  session  2:  48 |################
  session  3:  57 |###################
  session  4:  61 |####################
  session  5:  60 |####################
  session  6:  54 |##################
  session  7:  58 |###################
  session  8:  55 |##################
  session  9:  50 |################
  session 10:  57 |###################
  session 11:  69 |#######################
  session 12:  66 |######################
  session 13:  64 |#####################
  session 14:  61 |####################
  session 15:  69 |#######################
  session 16:  67 |######################
  session 17:  74 |########################
  session 18:  78 |##########################
  session 19:  61 |####################
  session 20:  78 |##########################

=== whole-course statistics ===
  sessions  : 20
  minimum   : 38 (session 1)
  maximum   : 78 (session 18)
  average   : 61.25
  first vs last : 38 -> 78 (+40)

=== slices ===
  first 5 sessions : [38, 48, 57, 61, 60]  avg 52.80
  last 5 sessions  : [67, 74, 78, 61, 78]  avg 71.60
  improvement      : +18.80 marks
  best of last 5   : 78   worst of last 5: 61
  every 4th session: [38, 60, 50, 64, 74]

=== session-to-session difference ===
  session  1 ->  2:  +10  up  
  session  2 ->  3:   +9  up  
  session  3 ->  4:   +4  up  
  session  4 ->  5:   -1  down
  session  5 ->  6:   -6  down
  session  6 ->  7:   +4  up  
  session  7 ->  8:   -3  down
  session  8 ->  9:   -5  down
  session  9 -> 10:   +7  up  
  session 10 -> 11:  +12  up  
  session 11 -> 12:   -3  down
  session 12 -> 13:   -2  down
  session 13 -> 14:   -3  down
  session 14 -> 15:   +8  up  
  session 15 -> 16:   -2  down
  session 16 -> 17:   +7  up  
  session 17 -> 18:   +4  up  
  session 18 -> 19:  -17  down
  session 19 -> 20:  +17  up  

  improved in 10 of 19 transitions, dropped in 9, flat in 0

=== consistent improvement (DP on the difference array) ===
  longest improving streak : 4 session(s), sessions 1 to 4
  scores in that streak    : [38, 48, 57, 61]
  average gain per session : +2.11 marks
  verdict                  : consistent improvement

=== 3-session moving average (smoothed trend) ===
  sessions 1-3:  47.67
  sessions 2-4:  55.33
  sessions 3-5:  59.33
  sessions 4-6:  58.33
  sessions 5-7:  57.33
  sessions 6-8:  55.67
  sessions 7-9:  54.33
  sessions 8-10:  54.00
  sessions 9-11:  58.67
  sessions 10-12:  64.00
  sessions 11-13:  66.33
  sessions 12-14:  63.67
  sessions 13-15:  64.67
  sessions 14-16:  65.67
  sessions 15-17:  70.00
  sessions 16-18:  73.00
  sessions 17-19:  71.00
  sessions 18-20:  72.33

```

</details>

---

## Experiment 4 - Question 6: Daily Expense Summary

Scenario: A finance app logs daily expenses for 30 days. Summarise the
spending behaviour.

Rubrics covered:
  * random expense data generated
  * week 1 and week 4 sliced
  * weekly totals and averages calculated
  * no-spend days and streaks identified

**File:** [`q6_finance_expenses_30days.py`](q6_finance_expenses_30days.py) &nbsp;&middot;&nbsp; **Run:** `python q6_finance_expenses_30days.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 4 - Question 6: Daily Expense Summary

Scenario: A finance app logs daily expenses for 30 days. Summarise the
spending behaviour.

Rubrics covered:
  * random expense data generated
  * week 1 and week 4 sliced
  * weekly totals and averages calculated
  * no-spend days and streaks identified
"""

import random

DAYS = 30


def generate_expenses(seed=21):
    """Rupees spent per day; some days nothing is spent."""
    random.seed(seed)
    data = []
    for day in range(DAYS):
        if random.random() < 0.18:                  # no-spend day
            data.append(0)
        elif day % 7 in (5, 6):                     # weekends cost more
            data.append(random.randint(600, 2400))
        else:
            data.append(random.randint(80, 900))
    return data


def streaks_of_zero(data):
    runs, start = [], None
    for i, v in enumerate(data):
        if v == 0 and start is None:
            start = i
        elif v != 0 and start is not None:
            runs.append((start + 1, i))             # 1-based day numbers
            start = None
    if start is not None:
        runs.append((start + 1, len(data)))
    return runs


if __name__ == "__main__":
    expenses = generate_expenses()

    print("=== 30-day expense log (Rs.) ===")
    for week in range(4):
        row = expenses[week * 7:(week + 1) * 7]
        print(f"  week {week + 1}: " + " ".join(f"{v:>6}" for v in row))
    print("  extra  : " + " ".join(f"{v:>6}" for v in expenses[28:]))

    week1 = expenses[0:7]                           # slicing
    week4 = expenses[21:28]
    print("\n=== slices ===")
    print(f"  week 1 (days 1-7)   : {week1}")
    print(f"  week 4 (days 22-28) : {week4}")
    print(f"  week 1 total Rs.{sum(week1):>6,}   average Rs.{sum(week1) / 7:>8,.2f}")
    print(f"  week 4 total Rs.{sum(week4):>6,}   average Rs.{sum(week4) / 7:>8,.2f}")
    change = sum(week4) - sum(week1)
    print(f"  change week1 -> week4: Rs.{change:+,} "
          f"({change / max(sum(week1), 1) * 100:+.1f}%)")

    print("\n=== weekly totals and averages ===")
    print(f"  {'week':<8}{'days':<10}{'total':>10}{'average':>12}"
          f"{'max day':>10}{'no-spend':>10}")
    for week in range(5):
        chunk = expenses[week * 7:(week + 1) * 7]
        if not chunk:
            break
        zeros = sum(1 for v in chunk if v == 0)
        print(f"  {week + 1:<8}{f'{week * 7 + 1}-{week * 7 + len(chunk)}':<10}"
              f"{sum(chunk):>10,}{sum(chunk) / len(chunk):>12,.2f}"
              f"{max(chunk):>10,}{zeros:>10}")

    total = sum(expenses)
    print("\n=== month summary ===")
    print(f"  total spent        : Rs.{total:,}")
    print(f"  daily average      : Rs.{total / DAYS:,.2f}")
    print(f"  highest single day : Rs.{max(expenses):,} "
          f"(day {expenses.index(max(expenses)) + 1})")
    spent_days = [v for v in expenses if v > 0]
    print(f"  average spend day  : Rs.{sum(spent_days) / len(spent_days):,.2f}")

    zero_days = [i + 1 for i, v in enumerate(expenses) if v == 0]
    print("\n=== no-spend days ===")
    print(f"  count : {len(zero_days)} of {DAYS}")
    print(f"  days  : {zero_days}")
    runs = streaks_of_zero(expenses)
    print("  streaks:")
    for a, b in runs:
        print(f"    days {a}-{b} ({b - a + 1} day(s))")
    if runs:
        longest = max(runs, key=lambda r: r[1] - r[0])
        print(f"  longest no-spend streak: days {longest[0]}-{longest[1]} "
              f"({longest[1] - longest[0] + 1} days)")

    print("\n=== weekday vs weekend behaviour ===")
    weekend = [v for i, v in enumerate(expenses) if i % 7 in (5, 6)]
    weekday = [v for i, v in enumerate(expenses) if i % 7 not in (5, 6)]
    print(f"  weekdays: Rs.{sum(weekday):>7,} over {len(weekday)} days "
          f"(avg Rs.{sum(weekday) / len(weekday):,.2f})")
    print(f"  weekends: Rs.{sum(weekend):>7,} over {len(weekend)} days "
          f"(avg Rs.{sum(weekend) / len(weekend):,.2f})")

    print("\n=== days above the monthly average (overspending) ===")
    avg = total / DAYS
    for i, v in enumerate(expenses, 1):
        if v > avg * 2:
            print(f"  day {i:>2}: Rs.{v:,} ({v / avg:.1f}x the daily average)")
```

</details>

<details>
<summary>Program output</summary>

```text
=== 30-day expense log (Rs.) ===
  week 1:      0    730    301    566    604   1680    606
  week 2:      0    518      0    317    790      0   2112
  week 3:    496    114    633    198    457      0    781
  week 4:      0    544      0    490    271   1562   1081
  extra  :      0    769

=== slices ===
  week 1 (days 1-7)   : [0, 730, 301, 566, 604, 1680, 606]
  week 4 (days 22-28) : [0, 544, 0, 490, 271, 1562, 1081]
  week 1 total Rs. 4,487   average Rs.  641.00
  week 4 total Rs. 3,948   average Rs.  564.00
  change week1 -> week4: Rs.-539 (-12.0%)

=== weekly totals and averages ===
  week    days           total     average   max day  no-spend
  1       1-7            4,487      641.00     1,680         1
  2       8-14           3,737      533.86     2,112         3
  3       15-21          2,679      382.71       781         1
  4       22-28          3,948      564.00     1,562         2
  5       29-30            769      384.50       769         1

=== month summary ===
  total spent        : Rs.15,620
  daily average      : Rs.520.67
  highest single day : Rs.2,112 (day 14)
  average spend day  : Rs.710.00

=== no-spend days ===
  count : 8 of 30
  days  : [1, 8, 10, 13, 20, 22, 24, 29]
  streaks:
    days 1-1 (1 day(s))
    days 8-8 (1 day(s))
    days 10-10 (1 day(s))
    days 13-13 (1 day(s))
    days 20-20 (1 day(s))
    days 22-22 (1 day(s))
    days 24-24 (1 day(s))
    days 29-29 (1 day(s))
  longest no-spend streak: days 1-1 (1 days)

=== weekday vs weekend behaviour ===
  weekdays: Rs.  7,798 over 22 days (avg Rs.354.45)
  weekends: Rs.  7,822 over 8 days (avg Rs.977.75)

=== days above the monthly average (overspending) ===
  day  6: Rs.1,680 (3.2x the daily average)
  day 14: Rs.2,112 (4.1x the daily average)
  day 27: Rs.1,562 (3.0x the daily average)
  day 28: Rs.1,081 (2.1x the daily average)

```

</details>

---

## Experiment 4 - Question 7: Weather Sensor Anomaly Detection

Scenario: A weather sensor logs the temperature every hour over 24 hours.
Detect anomalies.

Rubrics covered:
  * hourly temperature readings generated
  * divided into morning / afternoon / evening
  * average computed for each time block
  * rapid temperature changes (more than 5 C per hour) filtered out

**File:** [`q7_weather_anomaly_blocks.py`](q7_weather_anomaly_blocks.py) &nbsp;&middot;&nbsp; **Run:** `python q7_weather_anomaly_blocks.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== 24 hourly readings (degrees C) ===
  00:00-05:00    21.1   20.7   20.5   19.1   19.7   20.6
  06:00-11:00    22.7   24.5   28.2   39.7   32.0   34.2
  12:00-17:00    35.0   35.9   36.2   34.2   31.7   29.7
  18:00-23:00    28.0   17.8   25.2   24.4   22.9   22.6

=== block averages ===
  night   (00-05)    avg  20.28 C   min  19.1   max  21.1
  morning (06-11)    avg  30.22 C   min  22.7   max  39.7
  afternoon (12-17)  avg  33.78 C   min  29.7   max  36.2
  evening (18-23)    avg  23.48 C   min  17.8   max  28.0

  hottest block : afternoon (12-17) (33.78 C)
  coolest block : night   (00-05) (20.28 C)

=== hour-to-hour change (flagging |delta| > 5.0 C/h) ===
  00:00 -> 01:00    21.1 ->   20.7    -0.4 C/h
  01:00 -> 02:00    20.7 ->   20.5    -0.2 C/h
  02:00 -> 03:00    20.5 ->   19.1    -1.4 C/h
  03:00 -> 04:00    19.1 ->   19.7    +0.6 C/h
  04:00 -> 05:00    19.7 ->   20.6    +0.9 C/h
  05:00 -> 06:00    20.6 ->   22.7    +2.1 C/h
  06:00 -> 07:00    22.7 ->   24.5    +1.8 C/h
  07:00 -> 08:00    24.5 ->   28.2    +3.7 C/h
  08:00 -> 09:00    28.2 ->   39.7   +11.5 C/h  <== ANOMALY
  09:00 -> 10:00    39.7 ->   32.0    -7.7 C/h  <== ANOMALY
  10:00 -> 11:00    32.0 ->   34.2    +2.2 C/h
  11:00 -> 12:00    34.2 ->   35.0    +0.8 C/h
  12:00 -> 13:00    35.0 ->   35.9    +0.9 C/h
  13:00 -> 14:00    35.9 ->   36.2    +0.3 C/h
  14:00 -> 15:00    36.2 ->   34.2    -2.0 C/h
  15:00 -> 16:00    34.2 ->   31.7    -2.5 C/h
  16:00 -> 17:00    31.7 ->   29.7    -2.0 C/h
  17:00 -> 18:00    29.7 ->   28.0    -1.7 C/h
  18:00 -> 19:00    28.0 ->   17.8   -10.2 C/h  <== ANOMALY
  19:00 -> 20:00    17.8 ->   25.2    +7.4 C/h  <== ANOMALY
  20:00 -> 21:00    25.2 ->   24.4    -0.8 C/h
  21:00 -> 22:00    24.4 ->   22.9    -1.5 C/h
  22:00 -> 23:00    22.9 ->   22.6    -0.3 C/h

=== 4 anomaly(ies) detected ===
  09:00  28.2 -> 39.7 C  (+11.5 C/h) sudden spike
  10:00  39.7 -> 32.0 C  (-7.7 C/h) sudden drop
  19:00  28.0 -> 17.8 C  (-10.2 C/h) sudden drop
  20:00  17.8 -> 25.2 C  (+7.4 C/h) sudden spike

=== cleaned series (anomalies replaced by the neighbour average) ===
  09:00 corrected 39.7 -> 30.1 C
  10:00 corrected 32.0 -> 37.0 C
  19:00 corrected 17.8 -> 26.6 C
  20:00 corrected 25.2 -> 21.1 C

  raw     daily average: 26.94 C (max 39.7)
  cleaned daily average: 26.95 C (max 37.0)
  the two spikes alone shifted the daily average by 0.00 C

```

</details>

---

## Experiment 4 - Question 8: Robot Vacuum Cleaning Efficiency (60 minutes)

Scenario: A robot vacuum tracks movement in metres every minute over 60
minutes. Analyse the cleaning efficiency.

Rubrics covered:
  * random movement data generated
  * first 20 minutes sliced
  * total and average movement computed
  * idle minutes (0 metres moved) filtered

**File:** [`q8_robot_vacuum_60min.py`](q8_robot_vacuum_60min.py) &nbsp;&middot;&nbsp; **Run:** `python q8_robot_vacuum_60min.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== per-minute movement (metres) ===
  min 00-09    9.6   6.0   8.8   4.7   0.0   8.9   7.2   9.5   6.4   4.2
  min 10-19    9.5   8.3   9.8   7.1   7.7   4.1   6.5   4.4   8.5   3.6
  min 20-29    3.8   5.6   5.7   8.5   6.6   6.4   4.9   4.4   6.4   4.0
  min 30-39    8.3   5.0   6.3   3.2   5.0   4.5   6.9   3.4   7.7   0.0
  min 40-49    6.5   6.6   5.9   3.8   3.6   0.0   6.9   6.6   6.6   0.0
  min 50-59    3.1   6.5   4.5   0.0   0.0   3.6   3.7   3.8   4.5   4.5

=== slices of 20 minutes each ===
  first 20 (00-19)     total   134.8 m   avg  6.74 m/min   idle  1 min
  middle 20 (20-39)    total   106.6 m   avg  5.33 m/min   idle  1 min
  last 20 (40-59)      total    80.7 m   avg  4.04 m/min   idle  4 min

=== whole session ===
  total distance      : 322.1 m
  average per minute  : 5.37 m
  best minute         : 9.8 m at minute 12

=== idle filter ===
  idle minutes        : 6 -> [4, 39, 45, 49, 53, 54]
  active minutes      : 54
  average while active: 5.96 m/min
  duty cycle          : 90.0%

=== slowest and fastest active minutes ===
  slowest active      : 3.1 m at minute 50
  5 slowest active    : [3.1, 3.2, 3.4, 3.6, 3.6]
  5 fastest           : [9.8, 9.6, 9.5, 9.5, 8.9]

=== battery fade check: 10-minute blocks ===
  min 00-09    65.3 m  |#############
  min 10-19    69.5 m  |#############
  min 20-29    56.3 m  |###########
  min 30-39    50.3 m  |##########
  min 40-49    46.5 m  |#########
  min 50-59    34.2 m  |######

  first half 191.1 m vs second half 131.0 m (-31.4%)

=== efficiency verdict ===
  coverage estimate   : 80.5 sq m (assuming a 25 cm brush width)
  verdict             : efficient run

```

</details>

---

## Experiment 4 - Question 9: Diet Calorie Balance

Scenario: A diet app tracks calorie intake per meal over a week
(3 meals per day). Review the diet balance.

Rubrics covered:
  * calorie data generated (21 values)
  * specific meals indexed (for example every breakfast)
  * average per meal type computed
  * high-calorie meals (above 700 calories) filtered

**File:** [`q9_diet_calorie_tracker.py`](q9_diet_calorie_tracker.py) &nbsp;&middot;&nbsp; **Run:** `python q9_diet_calorie_tracker.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 4 - Question 9: Diet Calorie Balance

Scenario: A diet app tracks calorie intake per meal over a week
(3 meals per day). Review the diet balance.

Rubrics covered:
  * calorie data generated (21 values)
  * specific meals indexed (for example every breakfast)
  * average per meal type computed
  * high-calorie meals (above 700 calories) filtered
"""

import random

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MEALS = ["Breakfast", "Lunch", "Dinner"]
HIGH_CAL = 700


def generate_calories(seed=42):
    """21 values: day 0 breakfast, lunch, dinner, day 1 breakfast, ..."""
    random.seed(seed)
    typical = {"Breakfast": (280, 520), "Lunch": (520, 880), "Dinner": (430, 760)}
    data = []
    for day in DAYS:
        for meal in MEALS:
            lo, hi = typical[meal]
            bump = 180 if day in ("Sat", "Sun") else 0     # weekend treats
            data.append(random.randint(lo, hi) + bump)
    return data


def meal_index(day_i, meal_i):
    """Flat index for a (day, meal) pair in the 21-value list."""
    return day_i * len(MEALS) + meal_i


if __name__ == "__main__":
    calories = generate_calories()
    assert len(calories) == 21

    print("=== weekly calorie log (21 meals) ===")
    print(f"  {'Day':<6}" + "".join(f"{m:>12}" for m in MEALS) +
          f"{'TOTAL':>10}")
    for d, day in enumerate(DAYS):
        row = calories[d * 3:d * 3 + 3]
        print(f"  {day:<6}" + "".join(f"{v:>12}" for v in row) +
              f"{sum(row):>10}")

    print("\n=== indexing specific meals (slicing with a step) ===")
    breakfasts = calories[0::3]
    lunches = calories[1::3]
    dinners = calories[2::3]
    print(f"  every Breakfast (index 0::3) : {breakfasts}")
    print(f"  every Lunch     (index 1::3) : {lunches}")
    print(f"  every Dinner    (index 2::3) : {dinners}")
    print(f"  Wednesday lunch (index {meal_index(2, 1)})      : "
          f"{calories[meal_index(2, 1)]} kcal")
    print(f"  Sunday dinner   (index {meal_index(6, 2)})      : "
          f"{calories[meal_index(6, 2)]} kcal")

    print("\n=== average per meal type ===")
    for name, series in (("Breakfast", breakfasts), ("Lunch", lunches),
                         ("Dinner", dinners)):
        print(f"  {name:<10} avg {sum(series) / len(series):>7.1f} kcal   "
              f"min {min(series):>4}   max {max(series):>4}   "
              f"share {sum(series) / sum(calories) * 100:>5.1f}%")

    print("\n=== daily totals against a 2000 kcal target ===")
    for d, day in enumerate(DAYS):
        total = sum(calories[d * 3:d * 3 + 3])
        verdict = "over " if total > 2000 else "under"
        bar = "#" * (total // 60)
        print(f"  {day:<4} {total:>5} kcal  {verdict}  |{bar}")

    weekly = sum(calories)
    print(f"\n  weekly intake   : {weekly:,} kcal")
    print(f"  daily average   : {weekly / 7:.1f} kcal")
    print(f"  per-meal average: {weekly / 21:.1f} kcal")

    heavy = [(DAYS[i // 3], MEALS[i % 3], c)
             for i, c in enumerate(calories) if c > HIGH_CAL]
    print(f"\n=== high-calorie meals (above {HIGH_CAL} kcal): {len(heavy)} ===")
    for day, meal, c in heavy:
        print(f"  {day:<4} {meal:<10} {c:>5} kcal  "
              f"({c - HIGH_CAL:+} over the limit)")
    if heavy:
        print(f"  heaviest meal: {max(heavy, key=lambda t: t[2])}")

    print("\n=== balance check ===")
    weekend = sum(calories[15:])              # Sat + Sun
    weekdays = sum(calories[:15])
    print(f"  weekdays (Mon-Fri): {weekdays:,} kcal, "
          f"{weekdays / 5:.1f} per day")
    print(f"  weekend  (Sat-Sun): {weekend:,} kcal, "
          f"{weekend / 2:.1f} per day")
    print(f"  weekend excess    : {weekend / 2 - weekdays / 5:+.1f} kcal/day")
    print("  balance verdict   : " +
          ("well balanced across meal types"
           if max(sum(breakfasts), sum(lunches), sum(dinners)) /
           min(sum(breakfasts), sum(lunches), sum(dinners)) < 1.6
           else "intake is skewed towards one meal of the day"))
```

</details>

<details>
<summary>Program output</summary>

```text
=== weekly calorie log (21 meals) ===
  Day      Breakfast       Lunch      Dinner     TOTAL
  Mon            443         577         442      1462
  Tue            469         660         555      1684
  Wed            337         591         482      1410
  Thu            453         799         474      1726
  Fri            431         736         446      1613
  Sat            467         747         721      1935
  Sun            519         958         918      2395

=== indexing specific meals (slicing with a step) ===
  every Breakfast (index 0::3) : [443, 469, 337, 453, 431, 467, 519]
  every Lunch     (index 1::3) : [577, 660, 591, 799, 736, 747, 958]
  every Dinner    (index 2::3) : [442, 555, 482, 474, 446, 721, 918]
  Wednesday lunch (index 7)      : 591 kcal
  Sunday dinner   (index 20)      : 918 kcal

=== average per meal type ===
  Breakfast  avg   445.6 kcal   min  337   max  519   share  25.5%
  Lunch      avg   724.0 kcal   min  577   max  958   share  41.5%
  Dinner     avg   576.9 kcal   min  442   max  918   share  33.0%

=== daily totals against a 2000 kcal target ===
  Mon   1462 kcal  under  |########################
  Tue   1684 kcal  under  |############################
  Wed   1410 kcal  under  |#######################
  Thu   1726 kcal  under  |############################
  Fri   1613 kcal  under  |##########################
  Sat   1935 kcal  under  |################################
  Sun   2395 kcal  over   |#######################################

  weekly intake   : 12,225 kcal
  daily average   : 1746.4 kcal
  per-meal average: 582.1 kcal

=== high-calorie meals (above 700 kcal): 6 ===
  Thu  Lunch        799 kcal  (+99 over the limit)
  Fri  Lunch        736 kcal  (+36 over the limit)
  Sat  Lunch        747 kcal  (+47 over the limit)
  Sat  Dinner       721 kcal  (+21 over the limit)
  Sun  Lunch        958 kcal  (+258 over the limit)
  Sun  Dinner       918 kcal  (+218 over the limit)
  heaviest meal: ('Sun', 'Lunch', 958)

=== balance check ===
  weekdays (Mon-Fri): 7,895 kcal, 1579.0 per day
  weekend  (Sat-Sun): 4,330 kcal, 2165.0 per day
  weekend excess    : +586.0 kcal/day
  balance verdict   : intake is skewed towards one meal of the day

```

</details>

---

## Experiment 4 - Question 10: Traffic Flow Analysis

Scenario: A traffic monitoring system logs the vehicle count per hour at a
junction over 48 hours. Analyse the traffic flow.

Rubrics covered:
  * vehicle count data generated
  * day period compared with night period
  * moving averages computed using the DP running-sum idea
  * congestion hours (more than 150 vehicles per hour) filtered

**File:** [`q10_traffic_flow_48h.py`](q10_traffic_flow_48h.py) &nbsp;&middot;&nbsp; **Run:** `python q10_traffic_flow_48h.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== hourly vehicle counts over 48 hours ===
  day 1:
    00:00-11:00    22   42   22   21   21   39   86  141  179  154  106  112
    12:00-23:00   123  131  111  122  157  183  173  174  107   78   42   63
  day 2:
    00:00-11:00    29   16    0   18    1   43   45  113  163  122   98   89
    12:00-23:00   105   83   93  121  101  136  163  121   74   78   48   36

=== day vs night ===
  day   (06-21): 32 hours, total  3,842, avg   120.1 veh/h, peak 183
  night (22-05): 16 hours, total    463, avg    28.9 veh/h, peak 63
  the junction carries 8.3x more traffic by day

=== day 1 vs day 2 ===
  day 1: total  2,409  avg  100.4  peak  183 at 17:00
  day 2: total  1,896  avg   79.0  peak  163 at 08:00

=== 3-hour moving average (DP running sum) ===
  hours 00-02:   28.67 veh/h  |####
  hours 04-06:   48.67 veh/h  |########
  hours 08-10:  146.33 veh/h  |########################
  hours 12-14:  121.67 veh/h  |####################
  hours 16-18:  171.00 veh/h  |############################
  hours 20-22:   75.67 veh/h  |############
  hours 24-26:   15.00 veh/h  |##
  hours 28-30:   29.67 veh/h  |####
  hours 32-34:  127.67 veh/h  |#####################
  hours 36-38:   93.67 veh/h  |###############
  hours 40-42:  133.33 veh/h  |######################
  hours 44-46:   66.67 veh/h  |###########

=== 6-hour moving average, smoothest view of the trend ===
  computed 43 windows; peak smoothed flow 153.33 veh/h starting at hour 14:00
  quietest 6-hour stretch: 17.83 veh/h starting at hour 24:00

=== busiest 4-hour window ===
  hours 16:00-19:59 carried 687 vehicles (171.8 veh/h)
  readings: [157, 183, 173, 174]

=== congestion hours (above 150 veh/h): 8 of 48 ===
  day 1 08:00   179 veh/h  (+29 over the threshold)
  day 1 09:00   154 veh/h  (+4 over the threshold)
  day 1 16:00   157 veh/h  (+7 over the threshold)
  day 1 17:00   183 veh/h  (+33 over the threshold)
  day 1 18:00   173 veh/h  (+23 over the threshold)
  day 1 19:00   174 veh/h  (+24 over the threshold)
  day 2 08:00   163 veh/h  (+13 over the threshold)
  day 2 18:00   163 veh/h  (+13 over the threshold)

  worst hour: day 1 17:00 with 183 vehicles
  congestion share: 16.7% of all hours

```

</details>

---
