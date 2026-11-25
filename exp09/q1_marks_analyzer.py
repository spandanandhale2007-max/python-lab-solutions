"""
Experiment 9 - Question 1: Marks Analyzer

Scenario: A professor analyses the marks of 5 students across 4 subjects. The
script accepts marks from the command line, stores them in a 2D array, slices
one student's subject marks and displays that student's average.

Usage:
  python q1_marks_analyzer.py --marks 78,85,69,90 91,88,95,84 55,61,48,70 \
                                      66,72,80,75 40,52,38,61 --student 2
  python q1_marks_analyzer.py                 (runs with the built-in demo data)
"""

import argparse

SUBJECTS = ["Python", "DSA", "DBMS", "OS"]
DEMO = ["78,85,69,90", "91,88,95,84", "55,61,48,70", "66,72,80,75",
        "40,52,38,61"]


def parse_marks(rows):
    """Turns ['78,85,69,90', ...] into a 2D list of integers."""
    grid = []
    for i, row in enumerate(rows):
        try:
            values = [int(v.strip()) for v in row.split(",") if v.strip()]
        except ValueError:
            raise SystemExit(f"error: row {i + 1} has a non-numeric mark: {row!r}")
        if len(values) != len(SUBJECTS):
            raise SystemExit(f"error: row {i + 1} has {len(values)} mark(s), "
                             f"expected {len(SUBJECTS)}")
        if any(not 0 <= v <= 100 for v in values):
            raise SystemExit(f"error: row {i + 1} has a mark outside 0-100")
        grid.append(values)
    return grid


def build_parser():
    p = argparse.ArgumentParser(
        description="Analyse student marks supplied on the command line.")
    p.add_argument("--marks", nargs="+", metavar="ROW", default=DEMO,
                   help="one comma-separated row of 4 subject marks per student")
    p.add_argument("--student", type=int, default=0,
                   help="zero-based index of the student to analyse")
    p.add_argument("--subjects", nargs="+", default=SUBJECTS,
                   help="subject names (must match the number of columns)")
    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    subjects = args.subjects
    marks = parse_marks(args.marks)
    rows, cols = len(marks), len(marks[0])

    if args.marks is DEMO:
        print("[info] no --marks given, using the built-in demo data\n")

    print(f"=== 2D marks array: {rows} student(s) x {cols} subject(s) ===")
    print(f"  {'index':<7}{'student':<12}" +
          "".join(f"{s:>10}" for s in subjects) +
          f"{'total':>8}{'average':>10}")
    print("  " + "-" * (29 + 10 * cols + 18))
    for i, row in enumerate(marks):
        total = sum(row)
        print(f"  {i:<7}{f'Student {i + 1}':<12}" +
              "".join(f"{v:>10}" for v in row) +
              f"{total:>8}{total / cols:>10.2f}")

    print("\n=== raw 2D array as Python sees it ===")
    print(f"  {marks}")

    index = args.student
    if not 0 <= index < rows:
        raise SystemExit(f"error: --student {index} is out of range "
                         f"(0 to {rows - 1})")

    sliced = marks[index]                      # row slice for one student
    print(f"\n=== slicing student index {index} ===")
    print(f"  marks[{index}]        = {sliced}")
    print(f"  marks[{index}][0:2]   = {sliced[0:2]}  (first two subjects)")
    print(f"  marks[{index}][-2:]   = {sliced[-2:]}  (last two subjects)")
    print(f"  marks[{index}][::2]   = {sliced[::2]}  (every other subject)")

    average = sum(sliced) / len(sliced)
    print(f"\n=== report for student index {index} ===")
    for subject, mark in zip(subjects, sliced):
        bar = "#" * (mark // 5)
        print(f"  {subject:<10}{mark:>4}  |{bar}")
    print(f"  {'total':<10}{sum(sliced):>4}")
    print(f"  {'average':<10}{average:>7.2f}")
    grade = ("A+" if average >= 90 else "A" if average >= 80 else
             "B" if average >= 70 else "C" if average >= 60 else
             "D" if average >= 40 else "F")
    print(f"  {'grade':<10}{grade:>7}")
    print(f"  {'best':<10}{max(sliced):>4} in "
          f"{subjects[sliced.index(max(sliced))]}")
    print(f"  {'weakest':<10}{min(sliced):>4} in "
          f"{subjects[sliced.index(min(sliced))]}")
    print(f"  {'result':<10}{'PASS' if min(sliced) >= 35 else 'FAIL':>7}")

    print("\n=== how this student compares with the class ===")
    class_avg = sum(sum(r) for r in marks) / (rows * cols)
    print(f"  class average   : {class_avg:.2f}")
    print(f"  student average : {average:.2f} "
          f"({average - class_avg:+.2f} vs the class)")
    ranking = sorted(range(rows), key=lambda i: -sum(marks[i]))
    print(f"  rank            : {ranking.index(index) + 1} of {rows}")

    print("\n=== column slices (subject-wise), for reference ===")
    for j, subject in enumerate(subjects):
        column = [marks[i][j] for i in range(rows)]
        print(f"  {subject:<10}{column}  avg {sum(column) / rows:>6.2f}")
