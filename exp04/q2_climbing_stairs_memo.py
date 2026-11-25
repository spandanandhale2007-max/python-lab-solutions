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
