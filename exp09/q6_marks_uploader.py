"""
Experiment 9 - Question 6: Student Marks Uploader

Scenario: A teacher wants to enter marks for 5 students in 4 subjects, but
subject-wise rather than all at once. The script accepts four separate lists
with --s1 ... --s4 and builds a 2D array where each row is a student.

Usage:
  python q6_marks_uploader.py --s1 78,91,55,66,40 --s2 85,88,61,72,52 \
                              --s3 69,95,48,80,38 --s4 90,84,70,75,61
  python q6_marks_uploader.py                       (demo data)
"""

import argparse

SUBJECT_NAMES = ["Python", "DSA", "DBMS", "OS"]
DEMO = {
    "s1": "78,91,55,66,40",
    "s2": "85,88,61,72,52",
    "s3": "69,95,48,80,38",
    "s4": "90,84,70,75,61",
}


def parse_list(text, flag):
    try:
        return [int(v.strip()) for v in text.split(",") if v.strip()]
    except ValueError:
        raise SystemExit(f"error: --{flag} contains a non-numeric mark: {text!r}")


def transpose(columns):
    """columns is subject-wise; return it student-wise (one row per student)."""
    return [list(row) for row in zip(*columns)]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Upload marks subject by subject and build a 2D array.")
    for flag, name in zip(("s1", "s2", "s3", "s4"), SUBJECT_NAMES):
        parser.add_argument(f"--{flag}", default=DEMO[flag],
                            help=f"comma-separated {name} marks, one per student")
    parser.add_argument("--names", nargs="*", default=None,
                        help="optional student names")
    args = parser.parse_args()

    used_demo = all(getattr(args, f) == DEMO[f] for f in ("s1", "s2", "s3", "s4"))
    if used_demo:
        print("[info] no subject lists given, using the built-in demo data\n")

    columns = [parse_list(getattr(args, f), f)
               for f in ("s1", "s2", "s3", "s4")]

    lengths = {len(c) for c in columns}
    if len(lengths) != 1:
        print("error: every subject list must have the same number of marks")
        for flag, col in zip(("s1", "s2", "s3", "s4"), columns):
            print(f"  --{flag}: {len(col)} mark(s)")
        raise SystemExit(1)

    students = lengths.pop()

    print("=== uploaded subject-wise lists (column view) ===")
    for flag, name, col in zip(("s1", "s2", "s3", "s4"), SUBJECT_NAMES, columns):
        print(f"  --{flag} {name:<8}{col}  "
              f"avg {sum(col) / len(col):>6.2f}  "
              f"high {max(col):>3}  low {min(col):>3}")

    marks = transpose(columns)              # the required 2D array

    names = args.names or [f"Student {i + 1}" for i in range(students)]
    if len(names) < students:
        names += [f"Student {i + 1}" for i in range(len(names), students)]

    print(f"\n=== assembled 2D array: {students} rows x "
          f"{len(SUBJECT_NAMES)} columns ===")
    print(f"  {marks}")

    print("\n=== row view: one row per student ===")
    print(f"  {'idx':<5}{'name':<14}" +
          "".join(f"{s:>9}" for s in SUBJECT_NAMES) +
          f"{'total':>8}{'average':>10}")
    print("  " + "-" * 72)
    for i, row in enumerate(marks):
        print(f"  {i:<5}{names[i]:<14}" + "".join(f"{v:>9}" for v in row) +
              f"{sum(row):>8}{sum(row) / len(row):>10.2f}")

    print("\n=== verification: the transpose round-trips ===")
    back = transpose(marks)
    print(f"  transpose(transpose(columns)) == columns : {back == columns}")
    for j, name in enumerate(SUBJECT_NAMES):
        column = [marks[i][j] for i in range(students)]
        print(f"  column {j} ({name:<8}) rebuilt from rows: {column}  "
              f"matches input: {column == columns[j]}")

    print("\n=== per-student slices ===")
    for i in range(students):
        print(f"  marks[{i}] = {marks[i]}   first two {marks[i][:2]}   "
              f"last two {marks[i][-2:]}")

    print("\n=== subject-wise statistics ===")
    print(f"  {'subject':<10}{'average':>10}{'high':>7}{'low':>7}{'spread':>9}")
    for j, name in enumerate(SUBJECT_NAMES):
        col = columns[j]
        print(f"  {name:<10}{sum(col) / len(col):>10.2f}{max(col):>7}"
              f"{min(col):>7}{max(col) - min(col):>9}")

    print("\n=== class summary ===")
    totals = [sum(r) for r in marks]
    print(f"  students          : {students}")
    print(f"  marks entered     : {students * len(SUBJECT_NAMES)}")
    print(f"  class average     : "
          f"{sum(totals) / (students * len(SUBJECT_NAMES)):.2f}")
    topper = totals.index(max(totals))
    print(f"  topper            : {names[topper]} (index {topper}, "
          f"total {max(totals)})")
    print(f"  lowest total      : {names[totals.index(min(totals))]} "
          f"({min(totals)})")

    print("\n=== why subject-wise entry is convenient ===")
    print("  A teacher marks one answer sheet pile at a time, so the natural")
    print("  input order is by subject. The script transposes that into the")
    print("  student-wise 2D array the rest of the report needs.")
