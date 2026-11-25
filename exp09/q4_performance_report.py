"""
Experiment 9 - Question 4: Student Performance Report

Scenario: A school admin wants a report of all students whose average is above
a threshold. The script accepts the marks of all students and a threshold value
from the command line, calculates each student's average and displays those
above the threshold.

Usage:
  python q4_performance_report.py --marks 78,85,69,90 91,88,95,84 55,61,48,70 \
                                  --threshold 75
  python q4_performance_report.py --threshold 60
  python q4_performance_report.py                     (demo data, threshold 70)
"""

import argparse

SUBJECTS = ["Python", "DSA", "DBMS", "OS"]
DEMO = ["78,85,69,90", "91,88,95,84", "55,61,48,70", "66,72,80,75",
        "40,52,38,61", "88,79,91,83"]


def parse_marks(rows):
    grid = []
    for i, row in enumerate(rows):
        try:
            grid.append([int(v.strip()) for v in row.split(",") if v.strip()])
        except ValueError:
            raise SystemExit(f"error: row {i + 1} contains a non-numeric mark")
    return grid


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Report students above an average threshold.")
    parser.add_argument("--marks", nargs="+", metavar="ROW", default=DEMO)
    parser.add_argument("--threshold", type=float, default=70.0,
                        help="minimum average to appear in the report")
    parser.add_argument("--names", nargs="*", default=None)
    parser.add_argument("--weak-mark", type=int, default=50,
                        help="a subject below this is flagged as weak")
    args = parser.parse_args()

    marks = parse_marks(args.marks)
    rows = len(marks)
    cols = len(marks[0])
    if any(len(r) != cols for r in marks):
        raise SystemExit("error: all rows must have the same number of marks")

    names = args.names or [f"Student {i + 1}" for i in range(rows)]
    if len(names) < rows:
        names += [f"Student {i + 1}" for i in range(len(names), rows)]
    subjects = (SUBJECTS[:cols] +
                [f"Sub{i + 1}" for i in range(len(SUBJECTS), cols)])

    averages = [sum(r) / len(r) for r in marks]

    print(f"=== input: {rows} student(s) x {cols} subject(s), "
          f"threshold {args.threshold} ===")
    print(f"  {'idx':<5}{'name':<14}" + "".join(f"{s:>9}" for s in subjects) +
          f"{'average':>10}  status")
    print("  " + "-" * (29 + 9 * cols + 18))
    for i, row in enumerate(marks):
        status = "ABOVE" if averages[i] > args.threshold else "below"
        print(f"  {i:<5}{names[i]:<14}" + "".join(f"{v:>9}" for v in row) +
              f"{averages[i]:>10.2f}  {status}")

    above = [(i, averages[i]) for i in range(rows)
             if averages[i] > args.threshold]
    below = [(i, averages[i]) for i in range(rows)
             if averages[i] <= args.threshold]

    print(f"\n=== students above {args.threshold} ===")
    if above:
        print(f"  {'rank':<6}{'idx':<5}{'name':<14}{'average':>10}"
              f"{'margin':>10}")
        for rank, (i, avg) in enumerate(
                sorted(above, key=lambda p: -p[1]), 1):
            print(f"  {rank:<6}{i:<5}{names[i]:<14}{avg:>10.2f}"
                  f"{avg - args.threshold:>+10.2f}")
    else:
        print("  none met the threshold")

    print(f"\n=== summary ===")
    print(f"  total students      : {rows}")
    print(f"  above the threshold : {len(above)} "
          f"({len(above) / rows * 100:.1f}%)")
    print(f"  at or below         : {len(below)}")
    print(f"  class average       : {sum(averages) / rows:.2f}")
    if above:
        print(f"  average of those above: "
              f"{sum(a for _, a in above) / len(above):.2f}")

    print(f"\n=== students needing support (at or below {args.threshold}) ===")
    for i, avg in sorted(below, key=lambda p: p[1]):
        weak = [subjects[j] for j in range(cols)
                if marks[i][j] < args.weak_mark]
        gap = args.threshold - avg
        print(f"  {names[i]:<14}avg {avg:>6.2f}  short by {gap:>5.2f}  "
              f"needs {gap * cols:.0f} more total marks")
        if weak:
            print(f"  {'':<14}weak in: {', '.join(weak)}")
    if not below:
        print("  none, every student is above the threshold")

    print("\n=== how the count changes with the threshold ===")
    for t in (40, 50, 60, 70, 80, 90):
        n = sum(1 for a in averages if a > t)
        print(f"  threshold {t:>3}: {n:>2} of {rows} student(s) qualify  "
              f"{'#' * n}")

    print("\n=== distinction and merit lists ===")
    for label, cut in (("Distinction (75+)", 75), ("First class (60+)", 60),
                       ("Pass (40+)", 40)):
        qualifying = [names[i] for i in range(rows) if averages[i] >= cut]
        print(f"  {label:<20}{len(qualifying):>2}  {qualifying}")
