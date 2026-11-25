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
