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
