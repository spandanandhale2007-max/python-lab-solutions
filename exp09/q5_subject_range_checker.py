"""
Experiment 9 - Question 5: Student Subject Range Checker

Scenario: A professor wants to find students who scored within a specific mark
range in any subject. The script accepts the marks and the desired range, then
displays the students who scored inside that range in any subject.

Usage:
  python q5_subject_range_checker.py --marks 78,85,69,90 91,88,95,84 \
                                     --low 60 --high 75
  python q5_subject_range_checker.py --low 40 --high 59
  python q5_subject_range_checker.py                  (demo data, 60-75)
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
        description="Find students scoring inside a mark range.")
    parser.add_argument("--marks", nargs="+", metavar="ROW", default=DEMO)
    parser.add_argument("--low", type=int, default=60, help="range lower bound")
    parser.add_argument("--high", type=int, default=75, help="range upper bound")
    parser.add_argument("--names", nargs="*", default=None)
    parser.add_argument("--all-subjects", action="store_true",
                        help="require EVERY subject in range instead of any")
    args = parser.parse_args()

    if args.low > args.high:
        raise SystemExit("error: --low cannot be greater than --high")

    marks = parse_marks(args.marks)
    rows, cols = len(marks), len(marks[0])
    if any(len(r) != cols for r in marks):
        raise SystemExit("error: all rows must have the same number of marks")

    names = args.names or [f"Student {i + 1}" for i in range(rows)]
    if len(names) < rows:
        names += [f"Student {i + 1}" for i in range(len(names), rows)]
    subjects = (SUBJECTS[:cols] +
                [f"Sub{i + 1}" for i in range(len(SUBJECTS), cols)])

    low, high = args.low, args.high
    in_range = lambda v: low <= v <= high

    print(f"=== marks table, range of interest {low}-{high} ===")
    print(f"  {'idx':<5}{'name':<14}" + "".join(f"{s:>10}" for s in subjects))
    print("  " + "-" * (19 + 10 * cols))
    for i, row in enumerate(marks):
        cells = []
        for v in row:
            cells.append(f"{f'*{v}*' if in_range(v) else v:>10}")
        print(f"  {i:<5}{names[i]:<14}" + "".join(cells))
    print(f"  (*n* marks a score inside {low}-{high})")

    print(f"\n=== students with ANY subject in {low}-{high} ===")
    any_hits = []
    for i, row in enumerate(marks):
        hits = [(subjects[j], row[j]) for j in range(cols) if in_range(row[j])]
        if hits:
            any_hits.append(i)
            detail = ", ".join(f"{s} {m}" for s, m in hits)
            print(f"  idx {i:<3}{names[i]:<14}{len(hits)} subject(s): {detail}")
    if not any_hits:
        print("  none")

    print(f"\n=== students with ALL subjects in {low}-{high} ===")
    all_hits = [i for i, row in enumerate(marks)
                if all(in_range(v) for v in row)]
    for i in all_hits:
        print(f"  idx {i:<3}{names[i]:<14}{marks[i]}")
    if not all_hits:
        print("  none")

    selected = all_hits if args.all_subjects else any_hits
    mode = "ALL subjects" if args.all_subjects else "ANY subject"
    print(f"\n=== selection ({mode}) ===")
    print(f"  matched {len(selected)} of {rows} student(s): "
          f"{[names[i] for i in selected]}")

    print(f"\n=== subject-wise count inside {low}-{high} ===")
    for j, subject in enumerate(subjects):
        column = [marks[i][j] for i in range(rows)]
        hits = [v for v in column if in_range(v)]
        print(f"  {subject:<10}{len(hits):>3} of {rows}  "
              f"{'#' * len(hits):<8} values {hits}")

    all_values = [v for row in marks for v in row]
    inside = [v for v in all_values if in_range(v)]
    print(f"\n=== overall ===")
    print(f"  total marks entered : {len(all_values)}")
    print(f"  inside the range    : {len(inside)} "
          f"({len(inside) / len(all_values) * 100:.1f}%)")
    if inside:
        print(f"  average inside      : {sum(inside) / len(inside):.2f}")
    print(f"  below {low:<13}: {sum(1 for v in all_values if v < low)}")
    print(f"  above {high:<13}: {sum(1 for v in all_values if v > high)}")

    print("\n=== common grade bands, for reference ===")
    for label, lo, hi in (("Distinction 75-100", 75, 100),
                          ("First class 60-74", 60, 74),
                          ("Second class 50-59", 50, 59),
                          ("Pass 35-49", 35, 49),
                          ("Fail 0-34", 0, 34)):
        n = sum(1 for v in all_values if lo <= v <= hi)
        students = sorted({names[i] for i in range(rows)
                           for j in range(cols) if lo <= marks[i][j] <= hi})
        print(f"  {label:<20}{n:>3} mark(s)  {len(students)} student(s)")
