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
