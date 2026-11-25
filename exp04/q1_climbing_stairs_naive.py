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
