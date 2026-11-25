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
