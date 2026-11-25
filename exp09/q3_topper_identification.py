"""
Experiment 9 - Question 3: Topper Identification

Scenario: A department head wants the student with the highest average marks.
The script accepts marks for multiple students and displays the index of the
topper.

Usage:
  python q3_topper_identification.py --marks 78,85,69,90 91,88,95,84 55,61,48,70
  python q3_topper_identification.py --marks 60,70,80,90 95,95,95,95 --names Riya Aman
  python q3_topper_identification.py                      (demo data)
"""

import argparse

SUBJECTS = ["Python", "DSA", "DBMS", "OS"]
DEMO = ["78,85,69,90", "91,88,95,84", "55,61,48,70", "66,72,80,75",
        "40,52,38,61"]


def parse_marks(rows):
    grid = []
    for i, row in enumerate(rows):
        try:
            values = [int(v.strip()) for v in row.split(",") if v.strip()]
        except ValueError:
            raise SystemExit(f"error: row {i + 1} contains a non-numeric mark")
        if not values:
            raise SystemExit(f"error: row {i + 1} is empty")
        grid.append(values)
    return grid


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find the student with the highest average.")
    parser.add_argument("--marks", nargs="+", metavar="ROW", default=DEMO,
                        help="comma-separated marks, one row per student")
    parser.add_argument("--names", nargs="*", default=None,
                        help="optional student names, in the same order")
    args = parser.parse_args()

    marks = parse_marks(args.marks)
    rows = len(marks)
    cols = len(marks[0])
    if any(len(r) != cols for r in marks):
        raise SystemExit("error: every student must have the same number of marks")

    names = args.names or [f"Student {i + 1}" for i in range(rows)]
    if len(names) < rows:
        names += [f"Student {i + 1}" for i in range(len(names), rows)]

    subjects = SUBJECTS[:cols] + [f"Sub{i + 1}" for i in range(len(SUBJECTS), cols)]

    averages = [sum(r) / len(r) for r in marks]

    print(f"=== marks table ({rows} students x {cols} subjects) ===")
    print(f"  {'idx':<5}{'name':<14}" + "".join(f"{s:>9}" for s in subjects) +
          f"{'total':>8}{'average':>10}")
    print("  " + "-" * (27 + 9 * cols + 18))
    for i, row in enumerate(marks):
        print(f"  {i:<5}{names[i]:<14}" + "".join(f"{v:>9}" for v in row) +
              f"{sum(row):>8}{averages[i]:>10.2f}")

    best_average = max(averages)
    topper_index = averages.index(best_average)
    tied = [i for i, a in enumerate(averages) if a == best_average]

    print("\n=== topper ===")
    print(f"  topper index   : {topper_index}")
    print(f"  topper name    : {names[topper_index]}")
    print(f"  marks          : {marks[topper_index]}")
    print(f"  total          : {sum(marks[topper_index])}")
    print(f"  average        : {best_average:.2f}")
    if len(tied) > 1:
        print(f"  NOTE: {len(tied)} students tie at {best_average:.2f} -> "
              f"indices {tied}")
        print("  tie broken by the highest single subject mark:")
        winner = max(tied, key=lambda i: max(marks[i]))
        print(f"    index {winner} ({names[winner]}) with a top mark of "
              f"{max(marks[winner])}")

    print("\n=== full merit list ===")
    order = sorted(range(rows), key=lambda i: -averages[i])
    print(f"  {'rank':<6}{'idx':<5}{'name':<14}{'average':>10}{'gap to #1':>12}")
    for rank, i in enumerate(order, 1):
        gap = averages[i] - best_average
        print(f"  {rank:<6}{i:<5}{names[i]:<14}{averages[i]:>10.2f}"
              f"{gap:>12.2f}")

    print("\n=== class statistics ===")
    print(f"  class average      : {sum(averages) / rows:.2f}")
    print(f"  highest average    : {best_average:.2f} ({names[topper_index]})")
    print(f"  lowest average     : {min(averages):.2f} "
          f"({names[averages.index(min(averages))]})")
    print(f"  spread             : {best_average - min(averages):.2f}")
    above = sum(1 for a in averages if a > sum(averages) / rows)
    print(f"  above class average: {above} of {rows}")

    print("\n=== subject toppers ===")
    for j, subject in enumerate(subjects):
        column = [marks[i][j] for i in range(rows)]
        best = max(column)
        winners = [names[i] for i in range(rows) if column[i] == best]
        print(f"  {subject:<10}{best:>4}  {', '.join(winners)}")

    print("\n=== consistency check (lowest spread across subjects) ===")
    for i in order[:3]:
        spread = max(marks[i]) - min(marks[i])
        print(f"  {names[i]:<14}avg {averages[i]:>6.2f}  spread {spread:>3}  "
              f"{'consistent' if spread <= 15 else 'uneven'}")
