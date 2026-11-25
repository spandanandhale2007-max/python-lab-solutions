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
