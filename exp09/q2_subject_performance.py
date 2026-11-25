"""
Experiment 9 - Question 2: Subject-wise Performance

Scenario: The academic head evaluates how students performed in a specific
subject. The script takes marks in a 2D array format and a subject index
(0 to 3), extracts the marks for that subject and calculates the class average.

Usage:
  python q2_subject_performance.py --marks 78,85,69,90 91,88,95,84 55,61,48,70 \
                                   --subject 1
  python q2_subject_performance.py --subject 2
  python q2_subject_performance.py                (demo data, subject 0)
"""

import argparse

SUBJECTS = ["Python", "DSA", "DBMS", "OS"]
DEMO = ["78,85,69,90", "91,88,95,84", "55,61,48,70", "66,72,80,75",
        "40,52,38,61"]


def parse_marks(rows, expected_cols):
    grid = []
    for i, row in enumerate(rows):
        try:
            values = [int(v.strip()) for v in row.split(",") if v.strip()]
        except ValueError:
            raise SystemExit(f"error: row {i + 1} contains a non-numeric mark")
        if len(values) != expected_cols:
            raise SystemExit(f"error: row {i + 1} has {len(values)} mark(s), "
                             f"expected {expected_cols}")
        grid.append(values)
    return grid


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Class performance in one subject.")
    parser.add_argument("--marks", nargs="+", metavar="ROW", default=DEMO,
                        help="comma-separated marks, one row per student")
    parser.add_argument("--subject", type=int, default=0,
                        help=f"subject index, 0 to {len(SUBJECTS) - 1}")
    parser.add_argument("--pass-mark", type=int, default=35,
                        help="minimum mark to pass (default 35)")
    args = parser.parse_args()

    marks = parse_marks(args.marks, len(SUBJECTS))
    rows = len(marks)
    j = args.subject

    if not 0 <= j < len(SUBJECTS):
        raise SystemExit(f"error: --subject {j} is out of range "
                         f"(0 to {len(SUBJECTS) - 1})")

    print(f"=== 2D marks array ({rows} students x {len(SUBJECTS)} subjects) ===")
    print(f"  {'student':<12}" + "".join(f"{s:>10}" for s in SUBJECTS))
    for i, row in enumerate(marks):
        cells = []
        for col, v in enumerate(row):
            cells.append(f"{f'[{v}]' if col == j else v:>10}")
        print(f"  {f'Student {i + 1}':<12}" + "".join(cells))
    print(f"  (the selected column, {SUBJECTS[j]}, is marked in brackets)")

    # extract the column
    column = [marks[i][j] for i in range(rows)]
    print(f"\n=== extracting subject index {j}: {SUBJECTS[j]} ===")
    print(f"  column slice [row[{j}] for row in marks] = {column}")

    class_average = sum(column) / len(column)
    passed = [m for m in column if m >= args.pass_mark]
    failed = [m for m in column if m < args.pass_mark]

    print(f"\n=== {SUBJECTS[j]} class report ===")
    print(f"  students      : {rows}")
    print(f"  class average : {class_average:.2f}")
    print(f"  highest       : {max(column)} (Student "
          f"{column.index(max(column)) + 1})")
    print(f"  lowest        : {min(column)} (Student "
          f"{column.index(min(column)) + 1})")
    print(f"  range         : {max(column) - min(column)}")
    srt = sorted(column)
    mid = rows // 2
    median = srt[mid] if rows % 2 else (srt[mid - 1] + srt[mid]) / 2
    print(f"  median        : {median}")
    print(f"  pass rate     : {len(passed)}/{rows} "
          f"({len(passed) / rows * 100:.1f}%)")
    if failed:
        print(f"  failures      : {failed}")

    print(f"\n=== each student in {SUBJECTS[j]} ===")
    for i, mark in enumerate(column):
        bar = "#" * (mark // 4)
        vs = mark - class_average
        flag = "above" if vs > 0 else "below" if vs < 0 else "at"
        print(f"  Student {i + 1:<3}{mark:>4}  |{bar:<25}| "
              f"{vs:+6.2f} ({flag} average)")

    print("\n=== grade distribution for this subject ===")
    bands = [("90-100 A+", 90, 100), ("80-89  A", 80, 89), ("70-79  B", 70, 79),
             ("60-69  C", 60, 69), ("40-59  D", 40, 59), ("0-39   F", 0, 39)]
    for label, lo, hi in bands:
        n = sum(1 for m in column if lo <= m <= hi)
        print(f"  {label:<12}{n:>3}  {'#' * n}")

    print("\n=== all subjects, for comparison ===")
    print(f"  {'subject':<10}{'average':>10}{'high':>7}{'low':>7}"
          f"{'pass %':>9}")
    for col, name in enumerate(SUBJECTS):
        values = [marks[i][col] for i in range(rows)]
        p = sum(1 for v in values if v >= args.pass_mark) / rows * 100
        marker = "  <- selected" if col == j else ""
        print(f"  {name:<10}{sum(values) / rows:>10.2f}{max(values):>7}"
              f"{min(values):>7}{p:>8.1f}%{marker}")

    averages = {name: sum(marks[i][c] for i in range(rows)) / rows
                for c, name in enumerate(SUBJECTS)}
    best = max(averages, key=averages.get)
    worst = min(averages, key=averages.get)
    print(f"\n  strongest subject : {best} ({averages[best]:.2f})")
    print(f"  weakest subject   : {worst} ({averages[worst]:.2f})")
    print(f"  {SUBJECTS[j]} ranks "
          f"{sorted(averages, key=averages.get, reverse=True).index(SUBJECTS[j]) + 1}"
          f" of {len(SUBJECTS)} by class average")
