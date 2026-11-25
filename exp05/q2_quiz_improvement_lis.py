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
