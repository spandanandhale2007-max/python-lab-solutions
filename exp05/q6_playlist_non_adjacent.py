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
