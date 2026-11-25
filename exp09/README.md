# Experiment 9 - Unit III

Command-line arguments, 2D arrays and CSV to JSON conversion

10 scenario questions, each solved in its own section and its own file. Every program below was executed and the real output is included.

[Back to the index](../README.md)

---

## Questions in this experiment

- [Experiment 9 - Question 1: Marks Analyzer](#experiment-9---question-1-marks-analyzer)
- [Experiment 9 - Question 2: Subject-wise Performance](#experiment-9---question-2-subject-wise-performance)
- [Experiment 9 - Question 3: Topper Identification](#experiment-9---question-3-topper-identification)
- [Experiment 9 - Question 4: Student Performance Report](#experiment-9---question-4-student-performance-report)
- [Experiment 9 - Question 5: Student Subject Range Checker](#experiment-9---question-5-student-subject-range-checker)
- [Experiment 9 - Question 6: Student Marks Uploader](#experiment-9---question-6-student-marks-uploader)
- [Experiment 9 - Question 7: Employee Directory Export](#experiment-9---question-7-employee-directory-export)
- [Experiment 9 - Question 8: Survey Results Dashboard](#experiment-9---question-8-survey-results-dashboard)
- [Experiment 9 - Question 9: Student Records Management System](#experiment-9---question-9-student-records-management-system)
- [Experiment 9 - Question 10: E-commerce Product Catalog Converter](#experiment-9---question-10-e-commerce-product-catalog-converter)

---

## Experiment 9 - Question 1: Marks Analyzer

Scenario: A professor analyses the marks of 5 students across 4 subjects. The
script accepts marks from the command line, stores them in a 2D array, slices
one student's subject marks and displays that student's average.

Usage:
  python q1_marks_analyzer.py --marks 78,85,69,90 91,88,95,84 55,61,48,70                                       66,72,80,75 40,52,38,61 --student 2
  python q1_marks_analyzer.py                 (runs with the built-in demo data)

**File:** [`q1_marks_analyzer.py`](q1_marks_analyzer.py) &nbsp;&middot;&nbsp; **Run:** `python q1_marks_analyzer.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
[info] no --marks given, using the built-in demo data

=== 2D marks array: 5 student(s) x 4 subject(s) ===
  index  student         Python       DSA      DBMS        OS   total   average
  ---------------------------------------------------------------------------------------
  0      Student 1           78        85        69        90     322     80.50
  1      Student 2           91        88        95        84     358     89.50
  2      Student 3           55        61        48        70     234     58.50
  3      Student 4           66        72        80        75     293     73.25
  4      Student 5           40        52        38        61     191     47.75

=== raw 2D array as Python sees it ===
  [[78, 85, 69, 90], [91, 88, 95, 84], [55, 61, 48, 70], [66, 72, 80, 75], [40, 52, 38, 61]]

=== slicing student index 0 ===
  marks[0]        = [78, 85, 69, 90]
  marks[0][0:2]   = [78, 85]  (first two subjects)
  marks[0][-2:]   = [69, 90]  (last two subjects)
  marks[0][::2]   = [78, 69]  (every other subject)

=== report for student index 0 ===
  Python      78  |###############
  DSA         85  |#################
  DBMS        69  |#############
  OS          90  |##################
  total      322
  average     80.50
  grade           A
  best        90 in OS
  weakest     69 in DBMS
  result       PASS

=== how this student compares with the class ===
  class average   : 69.90
  student average : 80.50 (+10.60 vs the class)
  rank            : 2 of 5

=== column slices (subject-wise), for reference ===
  Python    [78, 91, 55, 66, 40]  avg  66.00
  DSA       [85, 88, 61, 72, 52]  avg  71.60
  DBMS      [69, 95, 48, 80, 38]  avg  66.00
  OS        [90, 84, 70, 75, 61]  avg  76.00

```

</details>

---

## Experiment 9 - Question 2: Subject-wise Performance

Scenario: The academic head evaluates how students performed in a specific
subject. The script takes marks in a 2D array format and a subject index
(0 to 3), extracts the marks for that subject and calculates the class average.

Usage:
  python q2_subject_performance.py --marks 78,85,69,90 91,88,95,84 55,61,48,70                                    --subject 1
  python q2_subject_performance.py --subject 2
  python q2_subject_performance.py                (demo data, subject 0)

**File:** [`q2_subject_performance.py`](q2_subject_performance.py) &nbsp;&middot;&nbsp; **Run:** `python q2_subject_performance.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== 2D marks array (5 students x 4 subjects) ===
  student         Python       DSA      DBMS        OS
  Student 1         [78]        85        69        90
  Student 2         [91]        88        95        84
  Student 3         [55]        61        48        70
  Student 4         [66]        72        80        75
  Student 5         [40]        52        38        61
  (the selected column, Python, is marked in brackets)

=== extracting subject index 0: Python ===
  column slice [row[0] for row in marks] = [78, 91, 55, 66, 40]

=== Python class report ===
  students      : 5
  class average : 66.00
  highest       : 91 (Student 2)
  lowest        : 40 (Student 5)
  range         : 51
  median        : 66
  pass rate     : 5/5 (100.0%)

=== each student in Python ===
  Student 1    78  |###################      | +12.00 (above average)
  Student 2    91  |######################   | +25.00 (above average)
  Student 3    55  |#############            | -11.00 (below average)
  Student 4    66  |################         |  +0.00 (at average)
  Student 5    40  |##########               | -26.00 (below average)

=== grade distribution for this subject ===
  90-100 A+     1  #
  80-89  A      0  
  70-79  B      1  #
  60-69  C      1  #
  40-59  D      2  ##
  0-39   F      0  

=== all subjects, for comparison ===
  subject      average   high    low   pass %
  Python         66.00     91     40   100.0%  <- selected
  DSA            71.60     88     52   100.0%
  DBMS           66.00     95     38   100.0%
  OS             76.00     90     61   100.0%

  strongest subject : OS (76.00)
  weakest subject   : Python (66.00)
  Python ranks 3 of 4 by class average

```

</details>

---

## Experiment 9 - Question 3: Topper Identification

Scenario: A department head wants the student with the highest average marks.
The script accepts marks for multiple students and displays the index of the
topper.

Usage:
  python q3_topper_identification.py --marks 78,85,69,90 91,88,95,84 55,61,48,70
  python q3_topper_identification.py --marks 60,70,80,90 95,95,95,95 --names Riya Aman
  python q3_topper_identification.py                      (demo data)

**File:** [`q3_topper_identification.py`](q3_topper_identification.py) &nbsp;&middot;&nbsp; **Run:** `python q3_topper_identification.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== marks table (5 students x 4 subjects) ===
  idx  name             Python      DSA     DBMS       OS   total   average
  ---------------------------------------------------------------------------------
  0    Student 1            78       85       69       90     322     80.50
  1    Student 2            91       88       95       84     358     89.50
  2    Student 3            55       61       48       70     234     58.50
  3    Student 4            66       72       80       75     293     73.25
  4    Student 5            40       52       38       61     191     47.75

=== topper ===
  topper index   : 1
  topper name    : Student 2
  marks          : [91, 88, 95, 84]
  total          : 358
  average        : 89.50

=== full merit list ===
  rank  idx  name             average   gap to #1
  1     1    Student 2          89.50        0.00
  2     0    Student 1          80.50       -9.00
  3     3    Student 4          73.25      -16.25
  4     2    Student 3          58.50      -31.00
  5     4    Student 5          47.75      -41.75

=== class statistics ===
  class average      : 69.90
  highest average    : 89.50 (Student 2)
  lowest average     : 47.75 (Student 5)
  spread             : 41.75
  above class average: 3 of 5

=== subject toppers ===
  Python      91  Student 2
  DSA         88  Student 2
  DBMS        95  Student 2
  OS          90  Student 1

=== consistency check (lowest spread across subjects) ===
  Student 2     avg  89.50  spread  11  consistent
  Student 1     avg  80.50  spread  21  uneven
  Student 4     avg  73.25  spread  14  consistent

```

</details>

---

## Experiment 9 - Question 4: Student Performance Report

Scenario: A school admin wants a report of all students whose average is above
a threshold. The script accepts the marks of all students and a threshold value
from the command line, calculates each student's average and displays those
above the threshold.

Usage:
  python q4_performance_report.py --marks 78,85,69,90 91,88,95,84 55,61,48,70                                   --threshold 75
  python q4_performance_report.py --threshold 60
  python q4_performance_report.py                     (demo data, threshold 70)

**File:** [`q4_performance_report.py`](q4_performance_report.py) &nbsp;&middot;&nbsp; **Run:** `python q4_performance_report.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== input: 6 student(s) x 4 subject(s), threshold 70.0 ===
  idx  name             Python      DSA     DBMS       OS   average  status
  -----------------------------------------------------------------------------------
  0    Student 1            78       85       69       90     80.50  ABOVE
  1    Student 2            91       88       95       84     89.50  ABOVE
  2    Student 3            55       61       48       70     58.50  below
  3    Student 4            66       72       80       75     73.25  ABOVE
  4    Student 5            40       52       38       61     47.75  below
  5    Student 6            88       79       91       83     85.25  ABOVE

=== students above 70.0 ===
  rank  idx  name             average    margin
  1     1    Student 2          89.50    +19.50
  2     5    Student 6          85.25    +15.25
  3     0    Student 1          80.50    +10.50
  4     3    Student 4          73.25     +3.25

=== summary ===
  total students      : 6
  above the threshold : 4 (66.7%)
  at or below         : 2
  class average       : 72.46
  average of those above: 82.12

=== students needing support (at or below 70.0) ===
  Student 5     avg  47.75  short by 22.25  needs 89 more total marks
                weak in: Python, DBMS
  Student 3     avg  58.50  short by 11.50  needs 46 more total marks
                weak in: DBMS

=== how the count changes with the threshold ===
  threshold  40:  6 of 6 student(s) qualify  ######
  threshold  50:  5 of 6 student(s) qualify  #####
  threshold  60:  4 of 6 student(s) qualify  ####
  threshold  70:  4 of 6 student(s) qualify  ####
  threshold  80:  3 of 6 student(s) qualify  ###
  threshold  90:  0 of 6 student(s) qualify  

=== distinction and merit lists ===
  Distinction (75+)    3  ['Student 1', 'Student 2', 'Student 6']
  First class (60+)    4  ['Student 1', 'Student 2', 'Student 4', 'Student 6']
  Pass (40+)           6  ['Student 1', 'Student 2', 'Student 3', 'Student 4', 'Student 5', 'Student 6']

```

</details>

---

## Experiment 9 - Question 5: Student Subject Range Checker

Scenario: A professor wants to find students who scored within a specific mark
range in any subject. The script accepts the marks and the desired range, then
displays the students who scored inside that range in any subject.

Usage:
  python q5_subject_range_checker.py --marks 78,85,69,90 91,88,95,84                                      --low 60 --high 75
  python q5_subject_range_checker.py --low 40 --high 59
  python q5_subject_range_checker.py                  (demo data, 60-75)

**File:** [`q5_subject_range_checker.py`](q5_subject_range_checker.py) &nbsp;&middot;&nbsp; **Run:** `python q5_subject_range_checker.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== marks table, range of interest 60-75 ===
  idx  name              Python       DSA      DBMS        OS
  -----------------------------------------------------------
  0    Student 1             78        85      *69*        90
  1    Student 2             91        88        95        84
  2    Student 3             55      *61*        48      *70*
  3    Student 4           *66*      *72*        80      *75*
  4    Student 5             40        52        38      *61*
  5    Student 6             88        79        91        83
  (*n* marks a score inside 60-75)

=== students with ANY subject in 60-75 ===
  idx 0  Student 1     1 subject(s): DBMS 69
  idx 2  Student 3     2 subject(s): DSA 61, OS 70
  idx 3  Student 4     3 subject(s): Python 66, DSA 72, OS 75
  idx 4  Student 5     1 subject(s): OS 61

=== students with ALL subjects in 60-75 ===
  none

=== selection (ANY subject) ===
  matched 4 of 6 student(s): ['Student 1', 'Student 3', 'Student 4', 'Student 5']

=== subject-wise count inside 60-75 ===
  Python      1 of 6  #        values [66]
  DSA         2 of 6  ##       values [61, 72]
  DBMS        1 of 6  #        values [69]
  OS          3 of 6  ###      values [70, 75, 61]

=== overall ===
  total marks entered : 24
  inside the range    : 7 (29.2%)
  average inside      : 67.71
  below 60           : 5
  above 75           : 12

=== common grade bands, for reference ===
  Distinction 75-100   13 mark(s)  4 student(s)
  First class 60-74     6 mark(s)  4 student(s)
  Second class 50-59    2 mark(s)  2 student(s)
  Pass 35-49            3 mark(s)  2 student(s)
  Fail 0-34             0 mark(s)  0 student(s)

```

</details>

---

## Experiment 9 - Question 6: Student Marks Uploader

Scenario: A teacher wants to enter marks for 5 students in 4 subjects, but
subject-wise rather than all at once. The script accepts four separate lists
with --s1 ... --s4 and builds a 2D array where each row is a student.

Usage:
  python q6_marks_uploader.py --s1 78,91,55,66,40 --s2 85,88,61,72,52                               --s3 69,95,48,80,38 --s4 90,84,70,75,61
  python q6_marks_uploader.py                       (demo data)

**File:** [`q6_marks_uploader.py`](q6_marks_uploader.py) &nbsp;&middot;&nbsp; **Run:** `python q6_marks_uploader.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
[info] no subject lists given, using the built-in demo data

=== uploaded subject-wise lists (column view) ===
  --s1 Python  [78, 91, 55, 66, 40]  avg  66.00  high  91  low  40
  --s2 DSA     [85, 88, 61, 72, 52]  avg  71.60  high  88  low  52
  --s3 DBMS    [69, 95, 48, 80, 38]  avg  66.00  high  95  low  38
  --s4 OS      [90, 84, 70, 75, 61]  avg  76.00  high  90  low  61

=== assembled 2D array: 5 rows x 4 columns ===
  [[78, 85, 69, 90], [91, 88, 95, 84], [55, 61, 48, 70], [66, 72, 80, 75], [40, 52, 38, 61]]

=== row view: one row per student ===
  idx  name             Python      DSA     DBMS       OS   total   average
  ------------------------------------------------------------------------
  0    Student 1            78       85       69       90     322     80.50
  1    Student 2            91       88       95       84     358     89.50
  2    Student 3            55       61       48       70     234     58.50
  3    Student 4            66       72       80       75     293     73.25
  4    Student 5            40       52       38       61     191     47.75

=== verification: the transpose round-trips ===
  transpose(transpose(columns)) == columns : True
  column 0 (Python  ) rebuilt from rows: [78, 91, 55, 66, 40]  matches input: True
  column 1 (DSA     ) rebuilt from rows: [85, 88, 61, 72, 52]  matches input: True
  column 2 (DBMS    ) rebuilt from rows: [69, 95, 48, 80, 38]  matches input: True
  column 3 (OS      ) rebuilt from rows: [90, 84, 70, 75, 61]  matches input: True

=== per-student slices ===
  marks[0] = [78, 85, 69, 90]   first two [78, 85]   last two [69, 90]
  marks[1] = [91, 88, 95, 84]   first two [91, 88]   last two [95, 84]
  marks[2] = [55, 61, 48, 70]   first two [55, 61]   last two [48, 70]
  marks[3] = [66, 72, 80, 75]   first two [66, 72]   last two [80, 75]
  marks[4] = [40, 52, 38, 61]   first two [40, 52]   last two [38, 61]

=== subject-wise statistics ===
  subject      average   high    low   spread
  Python         66.00     91     40       51
  DSA            71.60     88     52       36
  DBMS           66.00     95     38       57
  OS             76.00     90     61       29

=== class summary ===
  students          : 5
  marks entered     : 20
  class average     : 69.90
  topper            : Student 2 (index 1, total 358)
  lowest total      : Student 5 (191)

=== why subject-wise entry is convenient ===
  A teacher marks one answer sheet pile at a time, so the natural
  input order is by subject. The script transposes that into the
  student-wise 2D array the rest of the report needs.

```

</details>

---

## Experiment 9 - Question 7: Employee Directory Export

Scenario: An HR system exports employee details (name, ID, department, email)
to employees.csv. Read that file and convert the data to JSON
(employees.json) for an internal company directory app.

Usage:
  python q7_employee_csv_to_json.py
  python q7_employee_csv_to_json.py --input other.csv --output other.json

**File:** [`q7_employee_csv_to_json.py`](q7_employee_csv_to_json.py) &nbsp;&middot;&nbsp; **Run:** `python q7_employee_csv_to_json.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 9 - Question 7: Employee Directory Export

Scenario: An HR system exports employee details (name, ID, department, email)
to employees.csv. Read that file and convert the data to JSON
(employees.json) for an internal company directory app.

Usage:
  python q7_employee_csv_to_json.py
  python q7_employee_csv_to_json.py --input other.csv --output other.json
"""

import argparse
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
DEFAULT_CSV = os.path.join(DATA, "employees.csv")
DEFAULT_JSON = os.path.join(DATA, "employees.json")

SAMPLE_CSV = """employee_id,name,department,email,designation,joined
EMP-1001,Spandan Andhale,Engineering,spandan.andhale@company.in,Software Intern,2026-06-01
EMP-1002,Riya Sharma,Design,riya.sharma@company.in,UX Designer,2025-07-14
EMP-1003,Aman Kulkarni,Engineering,aman.kulkarni@company.in,Backend Engineer,2024-01-08
EMP-1004,Neha Deshmukh,Quality,neha.deshmukh@company.in,QA Engineer,2024-09-23
EMP-1005,Omkar Patil,Engineering,omkar.patil@company.in,DevOps Engineer,2023-03-15
EMP-1006,Sana Shaikh,Operations,sana.shaikh@company.in,Operations Lead,2022-11-02
EMP-1007,Kavita Rao,Research,kavita.rao@company.in,Principal Scientist,2021-05-19
EMP-1008,Harsh Mehta,Design,harsh.mehta@company.in,Visual Designer,2025-02-10
"""


def ensure_sample(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(SAMPLE_CSV)
        print(f"[setup] created sample input {path}")


def read_csv(path):
    with open(path, "r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = [dict(row) for row in reader]
        return rows, reader.fieldnames


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert an employee CSV export into JSON.")
    parser.add_argument("--input", default=DEFAULT_CSV)
    parser.add_argument("--output", default=DEFAULT_JSON)
    parser.add_argument("--indent", type=int, default=2)
    parser.add_argument("--group-by-department", action="store_true")
    args = parser.parse_args()

    ensure_sample(args.input)
    rows, headers = read_csv(args.input)

    print(f"=== read {os.path.basename(args.input)} ===")
    print(f"  columns : {headers}")
    print(f"  records : {len(rows)}")
    print(f"  size    : {os.path.getsize(args.input)} bytes")

    print("\n=== CSV as a table ===")
    widths = {h: max(len(h), max((len(r[h]) for r in rows), default=0))
              for h in headers}
    print("  " + "  ".join(f"{h:<{widths[h]}}" for h in headers))
    print("  " + "-" * (sum(widths.values()) + 2 * len(headers)))
    for r in rows:
        print("  " + "  ".join(f"{r[h]:<{widths[h]}}" for h in headers))

    # --- validation before export ---
    print("\n=== validation ===")
    problems = []
    seen_ids, seen_emails = set(), set()
    for n, r in enumerate(rows, 2):           # line 2 is the first data row
        if not r.get("email") or "@" not in r["email"]:
            problems.append((n, r.get("employee_id"), "invalid email"))
        if r["employee_id"] in seen_ids:
            problems.append((n, r["employee_id"], "duplicate employee id"))
        if r["email"].lower() in seen_emails:
            problems.append((n, r["employee_id"], "duplicate email"))
        seen_ids.add(r["employee_id"])
        seen_emails.add(r["email"].lower())
    if problems:
        for line, emp, why in problems:
            print(f"  line {line}: {emp} -> {why}")
    else:
        print(f"  all {len(rows)} record(s) valid, "
              f"{len(seen_ids)} unique id(s)")

    # --- build the JSON payload the directory app wants ---
    employees = []
    for r in rows:
        employees.append({
            "employeeId": r["employee_id"],
            "name": r["name"],
            "department": r["department"],
            "email": r["email"].lower(),
            "designation": r.get("designation", ""),
            "joined": r.get("joined", ""),
        })

    payload = (employees if not args.group_by_department else
               {"departments": {}})
    if args.group_by_department:
        for e in employees:
            payload["departments"].setdefault(e["department"], []).append(e)

    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=args.indent, ensure_ascii=False)

    print(f"\n=== wrote {os.path.basename(args.output)} ===")
    print(f"  size   : {os.path.getsize(args.output)} bytes")
    print(f"  records: {len(employees)}")

    print("\n=== first two JSON records ===")
    print(json.dumps(employees[:2], indent=2))

    print("\n=== round-trip check ===")
    with open(args.output, "r", encoding="utf-8") as fh:
        reloaded = json.load(fh)
    count = (len(reloaded) if isinstance(reloaded, list)
             else sum(len(v) for v in reloaded["departments"].values()))
    print(f"  reloaded {count} record(s) from JSON, matches CSV: "
          f"{count == len(rows)}")

    print("\n=== directory summary ===")
    departments = {}
    for e in employees:
        departments.setdefault(e["department"], []).append(e["name"])
    for dept, members in sorted(departments.items()):
        print(f"  {dept:<14}{len(members):>3}  {', '.join(members)}")

    print("\n=== JSON vs CSV size ===")
    csv_size = os.path.getsize(args.input)
    json_size = os.path.getsize(args.output)
    print(f"  CSV  : {csv_size:>6} bytes")
    print(f"  JSON : {json_size:>6} bytes "
          f"({json_size / csv_size:.1f}x larger, the cost of key names)")
    print("  JSON is still the right choice here: the frontend can consume it")
    print("  directly with fetch().then(r => r.json()) and no parsing code.")
```

</details>

<details>
<summary>Program output</summary>

```text
=== read employees.csv ===
  columns : ['employee_id', 'name', 'department', 'email', 'designation', 'joined']
  records : 8
  size    : 710 bytes

=== CSV as a table ===
  employee_id  name             department   email                       designation          joined    
  --------------------------------------------------------------------------------------------------------
  EMP-1001     Spandan Andhale  Engineering  spandan.andhale@company.in  Software Intern      2026-06-01
  EMP-1002     Riya Sharma      Design       riya.sharma@company.in      UX Designer          2025-07-14
  EMP-1003     Aman Kulkarni    Engineering  aman.kulkarni@company.in    Backend Engineer     2024-01-08
  EMP-1004     Neha Deshmukh    Quality      neha.deshmukh@company.in    QA Engineer          2024-09-23
  EMP-1005     Omkar Patil      Engineering  omkar.patil@company.in      DevOps Engineer      2023-03-15
  EMP-1006     Sana Shaikh      Operations   sana.shaikh@company.in      Operations Lead      2022-11-02
  EMP-1007     Kavita Rao       Research     kavita.rao@company.in       Principal Scientist  2021-05-19
  EMP-1008     Harsh Mehta      Design       harsh.mehta@company.in      Visual Designer      2025-02-10

=== validation ===
  all 8 record(s) valid, 8 unique id(s)

=== wrote employees.json ===
  size   : 1684 bytes
  records: 8

=== first two JSON records ===
[
  {
    "employeeId": "EMP-1001",
    "name": "Spandan Andhale",
    "department": "Engineering",
    "email": "spandan.andhale@company.in",
    "designation": "Software Intern",
    "joined": "2026-06-01"
  },
  {
    "employeeId": "EMP-1002",
    "name": "Riya Sharma",
    "department": "Design",
    "email": "riya.sharma@company.in",
    "designation": "UX Designer",
    "joined": "2025-07-14"
  }
]

=== round-trip check ===
  reloaded 8 record(s) from JSON, matches CSV: True

=== directory summary ===
  Design          2  Riya Sharma, Harsh Mehta
  Engineering     3  Spandan Andhale, Aman Kulkarni, Omkar Patil
  Operations      1  Sana Shaikh
  Quality         1  Neha Deshmukh
  Research        1  Kavita Rao

=== JSON vs CSV size ===
  CSV  :    710 bytes
  JSON :   1684 bytes (2.4x larger, the cost of key names)
  JSON is still the right choice here: the frontend can consume it
  directly with fetch().then(r => r.json()) and no parsing code.

```

</details>

---

## Experiment 9 - Question 8: Survey Results Dashboard

Scenario: Survey results are stored in survey_results.csv. Convert the data to
JSON (survey_results.json) so a web dashboard can consume it in JavaScript.

Usage:
  python q8_survey_csv_to_json.py
  python q8_survey_csv_to_json.py --input other.csv --output other.json

**File:** [`q8_survey_csv_to_json.py`](q8_survey_csv_to_json.py) &nbsp;&middot;&nbsp; **Run:** `python q8_survey_csv_to_json.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 9 - Question 8: Survey Results Dashboard

Scenario: Survey results are stored in survey_results.csv. Convert the data to
JSON (survey_results.json) so a web dashboard can consume it in JavaScript.

Usage:
  python q8_survey_csv_to_json.py
  python q8_survey_csv_to_json.py --input other.csv --output other.json
"""

import argparse
import csv
import json
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
DEFAULT_CSV = os.path.join(DATA, "survey_results.csv")
DEFAULT_JSON = os.path.join(DATA, "survey_results.json")

SAMPLE_CSV = """response_id,timestamp,age_group,city,rating,recommend,comment
R001,2026-11-18 09:14,18-24,Pune,9,yes,Bed availability page saves us phone calls
R002,2026-11-18 10:02,25-34,Mumbai,8,yes,Useful but the data looked stale once
R003,2026-11-18 11:40,35-44,Nashik,10,yes,Exactly what a district hospital needs
R004,2026-11-19 08:21,18-24,Pune,6,no,Mobile layout squeezes the ward names
R005,2026-11-19 09:55,45-54,Nagpur,7,yes,Please add a paediatric bed filter
R006,2026-11-19 12:30,25-34,Mumbai,3,no,Showed a bed as free that was taken
R007,2026-11-20 10:05,35-44,Pune,9,yes,Refresh is fast and colour coding is clear
R008,2026-11-20 14:18,55+,Nashik,10,yes,Front desk answers bed queries without calling
R009,2026-11-21 09:02,25-34,Nagpur,5,no,Fine for one hospital we need a multi view
R010,2026-11-21 16:44,18-24,Pune,8,yes,An SMS alert on low ICU capacity would help
R011,2026-11-22 11:11,45-54,Mumbai,2,no,Could not log in for two days
R012,2026-11-22 13:27,35-44,Pune,9,yes,Clean interface no training needed
"""


def ensure_sample(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(SAMPLE_CSV)
        print(f"[setup] created sample input {path}")


def typed(row):
    """CSV gives everything as strings; the dashboard wants real types."""
    return {
        "responseId": row["response_id"],
        "timestamp": row["timestamp"],
        "ageGroup": row["age_group"],
        "city": row["city"],
        "rating": int(row["rating"]),
        "recommend": row["recommend"].strip().lower() == "yes",
        "comment": row["comment"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert survey CSV results into dashboard-ready JSON.")
    parser.add_argument("--input", default=DEFAULT_CSV)
    parser.add_argument("--output", default=DEFAULT_JSON)
    parser.add_argument("--indent", type=int, default=2)
    args = parser.parse_args()

    ensure_sample(args.input)

    with open(args.input, "r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        raw_rows = list(reader)
        headers = reader.fieldnames

    print(f"=== read {os.path.basename(args.input)} ===")
    print(f"  columns   : {headers}")
    print(f"  responses : {len(raw_rows)}")
    print(f"  size      : {os.path.getsize(args.input)} bytes")

    responses = [typed(r) for r in raw_rows]

    print("\n=== type conversion ===")
    sample = raw_rows[0]
    print(f"  CSV  : rating={sample['rating']!r} "
          f"recommend={sample['recommend']!r}  (both strings)")
    print(f"  JSON : rating={responses[0]['rating']!r} "
          f"recommend={responses[0]['recommend']!r}  (int and bool)")

    ratings = [r["rating"] for r in responses]
    promoters = sum(1 for r in ratings if r >= 9)
    detractors = sum(1 for r in ratings if r <= 6)
    nps = (promoters - detractors) / len(ratings) * 100

    by_city = Counter(r["city"] for r in responses)
    by_age = Counter(r["ageGroup"] for r in responses)

    # the aggregates the dashboard needs, computed once here
    summary = {
        "totalResponses": len(responses),
        "averageRating": round(sum(ratings) / len(ratings), 2),
        "minRating": min(ratings),
        "maxRating": max(ratings),
        "recommendCount": sum(1 for r in responses if r["recommend"]),
        "recommendPercent": round(
            sum(1 for r in responses if r["recommend"]) / len(responses) * 100, 1),
        "nps": round(nps, 1),
        "ratingDistribution": {str(k): v for k, v in
                               sorted(Counter(ratings).items())},
        "byCity": dict(by_city),
        "byAgeGroup": dict(sorted(by_age.items())),
    }

    payload = {"summary": summary, "responses": responses}

    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=args.indent, ensure_ascii=False)

    print(f"\n=== wrote {os.path.basename(args.output)} ===")
    print(f"  size : {os.path.getsize(args.output)} bytes")
    print(f"  shape: {{ summary: {{...}}, responses: [{len(responses)}] }}")

    print("\n=== summary block (what the dashboard tiles read) ===")
    print(json.dumps(summary, indent=2))

    print("\n=== first two response objects ===")
    print(json.dumps(responses[:2], indent=2))

    print("\n=== rating distribution ===")
    for rating, count in sorted(Counter(ratings).items()):
        print(f"  {rating:>2} : {'#' * count} ({count})")

    print("\n=== by city ===")
    for city, count in by_city.most_common():
        city_ratings = [r["rating"] for r in responses if r["city"] == city]
        print(f"  {city:<10}{count:>3} response(s)  "
              f"avg {sum(city_ratings) / len(city_ratings):>5.2f}")

    print("\n=== by age group ===")
    for group, count in sorted(by_age.items()):
        group_ratings = [r["rating"] for r in responses
                         if r["ageGroup"] == group]
        print(f"  {group:<8}{count:>3} response(s)  "
              f"avg {sum(group_ratings) / len(group_ratings):>5.2f}")

    print("\n=== round-trip check ===")
    with open(args.output, "r", encoding="utf-8") as fh:
        reloaded = json.load(fh)
    print(f"  responses reloaded : {len(reloaded['responses'])}")
    print(f"  matches CSV rows   : "
          f"{len(reloaded['responses']) == len(raw_rows)}")
    print(f"  rating is a number : "
          f"{isinstance(reloaded['responses'][0]['rating'], int)}")

    print("\n=== how the frontend consumes it ===")
    print("  fetch('survey_results.json')")
    print("    .then(r => r.json())")
    print("    .then(d => renderTiles(d.summary, d.responses));")
```

</details>

<details>
<summary>Program output</summary>

```text
=== read survey_results.csv ===
  columns   : ['response_id', 'timestamp', 'age_group', 'city', 'rating', 'recommend', 'comment']
  responses : 12
  size      : 1011 bytes

=== type conversion ===
  CSV  : rating='9' recommend='yes'  (both strings)
  JSON : rating=9 recommend=True  (int and bool)

=== wrote survey_results.json ===
  size : 3500 bytes
  shape: { summary: {...}, responses: [12] }

=== summary block (what the dashboard tiles read) ===
{
  "totalResponses": 12,
  "averageRating": 7.17,
  "minRating": 2,
  "maxRating": 10,
  "recommendCount": 8,
  "recommendPercent": 66.7,
  "nps": 8.3,
  "ratingDistribution": {
    "2": 1,
    "3": 1,
    "5": 1,
    "6": 1,
    "7": 1,
    "8": 2,
    "9": 3,
    "10": 2
  },
  "byCity": {
    "Pune": 5,
    "Mumbai": 3,
    "Nashik": 2,
    "Nagpur": 2
  },
  "byAgeGroup": {
    "18-24": 3,
    "25-34": 3,
    "35-44": 3,
    "45-54": 2,
    "55+": 1
  }
}

=== first two response objects ===
[
  {
    "responseId": "R001",
    "timestamp": "2026-11-18 09:14",
    "ageGroup": "18-24",
    "city": "Pune",
    "rating": 9,
    "recommend": true,
    "comment": "Bed availability page saves us phone calls"
  },
  {
    "responseId": "R002",
    "timestamp": "2026-11-18 10:02",
    "ageGroup": "25-34",
    "city": "Mumbai",
    "rating": 8,
    "recommend": true,
    "comment": "Useful but the data looked stale once"
  }
]

=== rating distribution ===
   2 : # (1)
   3 : # (1)
   5 : # (1)
   6 : # (1)
   7 : # (1)
   8 : ## (2)
   9 : ### (3)
  10 : ## (2)

=== by city ===
  Pune        5 response(s)  avg  8.20
  Mumbai      3 response(s)  avg  4.33
  Nashik      2 response(s)  avg 10.00
  Nagpur      2 response(s)  avg  6.00

=== by age group ===
  18-24     3 response(s)  avg  7.67
  25-34     3 response(s)  avg  5.33
  35-44     3 response(s)  avg  9.33
  45-54     2 response(s)  avg  4.50
  55+       1 response(s)  avg 10.00

=== round-trip check ===
  responses reloaded : 12
  matches CSV rows   : True
  rating is a number : True

=== how the frontend consumes it ===
  fetch('survey_results.json')
    .then(r => r.json())
    .then(d => renderTiles(d.summary, d.responses));

```

</details>

---

## Experiment 9 - Question 9: Student Records Management System

Scenario: A school stores student details in students.csv with fields such as
student_id, name, grade and email. Convert the CSV into students.json to
integrate with a web-based student portal.

Usage:
  python q9_students_csv_to_json.py
  python q9_students_csv_to_json.py --group-by-grade

**File:** [`q9_students_csv_to_json.py`](q9_students_csv_to_json.py) &nbsp;&middot;&nbsp; **Run:** `python q9_students_csv_to_json.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 9 - Question 9: Student Records Management System

Scenario: A school stores student details in students.csv with fields such as
student_id, name, grade and email. Convert the CSV into students.json to
integrate with a web-based student portal.

Usage:
  python q9_students_csv_to_json.py
  python q9_students_csv_to_json.py --group-by-grade
"""

import argparse
import csv
import json
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
DEFAULT_CSV = os.path.join(DATA, "students.csv")
DEFAULT_JSON = os.path.join(DATA, "students.json")

SAMPLE_CSV = """student_id,name,grade,email,section,attendance_percent
STU-2301,Spandan Andhale,SY-CSE,spandan.andhale@school.edu.in,A,92.5
STU-2302,Riya Sharma,SY-CSE,riya.sharma@school.edu.in,A,88.0
STU-2303,Aman Kulkarni,SY-CSE,aman.kulkarni@school.edu.in,B,74.5
STU-2304,Neha Deshmukh,TY-CSE,neha.deshmukh@school.edu.in,A,96.0
STU-2305,Omkar Patil,TY-CSE,omkar.patil@school.edu.in,B,61.5
STU-2306,Sana Shaikh,FY-CSE,sana.shaikh@school.edu.in,A,85.0
STU-2307,Rohit Jadhav,FY-CSE,rohit.jadhav@school.edu.in,B,79.0
STU-2308,Pooja Nair,SY-CSE,pooja.nair@school.edu.in,B,58.0
STU-2309,Kiran Rao,TY-CSE,kiran.rao@school.edu.in,A,90.5
STU-2310,Tanvi Gokhale,FY-CSE,tanvi.gokhale@school.edu.in,A,99.0
"""

ATTENDANCE_CUTOFF = 75.0


def ensure_sample(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(SAMPLE_CSV)
        print(f"[setup] created sample input {path}")


def to_record(row):
    attendance = float(row["attendance_percent"])
    return {
        "studentId": row["student_id"],
        "name": row["name"],
        "grade": row["grade"],
        "email": row["email"].lower(),
        "section": row["section"],
        "attendancePercent": attendance,
        "attendanceOk": attendance >= ATTENDANCE_CUTOFF,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a student records CSV into portal-ready JSON.")
    parser.add_argument("--input", default=DEFAULT_CSV)
    parser.add_argument("--output", default=DEFAULT_JSON)
    parser.add_argument("--indent", type=int, default=2)
    parser.add_argument("--group-by-grade", action="store_true",
                        help="nest the records under each grade")
    args = parser.parse_args()

    ensure_sample(args.input)

    with open(args.input, "r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        headers = reader.fieldnames

    print(f"=== read {os.path.basename(args.input)} ===")
    print(f"  columns  : {headers}")
    print(f"  students : {len(rows)}")
    print(f"  size     : {os.path.getsize(args.input)} bytes")

    print("\n=== CSV contents ===")
    print(f"  {'id':<10}{'name':<18}{'grade':<9}{'sec':<5}"
          f"{'attendance':>11}  email")
    print("  " + "-" * 92)
    for r in rows:
        print(f"  {r['student_id']:<10}{r['name']:<18}{r['grade']:<9}"
              f"{r['section']:<5}{r['attendance_percent']:>10}%  {r['email']}")

    print("\n=== validation ===")
    issues = []
    ids = Counter(r["student_id"] for r in rows)
    emails = Counter(r["email"].lower() for r in rows)
    for r in rows:
        if ids[r["student_id"]] > 1:
            issues.append(f"{r['student_id']}: duplicate student id")
        if emails[r["email"].lower()] > 1:
            issues.append(f"{r['student_id']}: duplicate email")
        if "@" not in r["email"]:
            issues.append(f"{r['student_id']}: malformed email")
        try:
            value = float(r["attendance_percent"])
            if not 0 <= value <= 100:
                issues.append(f"{r['student_id']}: attendance out of range")
        except ValueError:
            issues.append(f"{r['student_id']}: attendance is not a number")
    for issue in sorted(set(issues)):
        print("  ", issue)
    if not issues:
        print(f"  all {len(rows)} record(s) passed")

    records = [to_record(r) for r in rows]

    if args.group_by_grade:
        grouped = defaultdict(list)
        for rec in records:
            grouped[rec["grade"]].append(rec)
        payload = {"generatedFor": "student portal",
                   "cutoff": ATTENDANCE_CUTOFF,
                   "grades": dict(sorted(grouped.items()))}
    else:
        payload = {"generatedFor": "student portal",
                   "cutoff": ATTENDANCE_CUTOFF,
                   "count": len(records),
                   "students": records}

    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=args.indent, ensure_ascii=False)

    print(f"\n=== wrote {os.path.basename(args.output)} ===")
    print(f"  size : {os.path.getsize(args.output)} bytes")
    print(f"  shape: {'grouped by grade' if args.group_by_grade else 'flat list'}")

    print("\n=== first two JSON records ===")
    print(json.dumps(records[:2], indent=2))

    print("\n=== grade-wise summary ===")
    by_grade = defaultdict(list)
    for rec in records:
        by_grade[rec["grade"]].append(rec)
    print(f"  {'grade':<9}{'students':>9}{'avg attendance':>17}"
          f"{'below cutoff':>14}")
    for grade in sorted(by_grade):
        group = by_grade[grade]
        avg = sum(s["attendancePercent"] for s in group) / len(group)
        short = sum(1 for s in group if not s["attendanceOk"])
        print(f"  {grade:<9}{len(group):>9}{avg:>16.2f}%{short:>14}")

    print(f"\n=== students below the {ATTENDANCE_CUTOFF}% cutoff ===")
    for rec in sorted(records, key=lambda s: s["attendancePercent"]):
        if not rec["attendanceOk"]:
            short = ATTENDANCE_CUTOFF - rec["attendancePercent"]
            print(f"  {rec['name']:<18}{rec['grade']:<9}"
                  f"{rec['attendancePercent']:>6.1f}%  short by {short:.1f} points")

    print("\n=== section split ===")
    for section, count in Counter(r["section"] for r in records).most_common():
        print(f"  section {section}: {count} student(s)")

    print("\n=== round-trip check ===")
    with open(args.output, "r", encoding="utf-8") as fh:
        reloaded = json.load(fh)
    count = (sum(len(v) for v in reloaded["grades"].values())
             if args.group_by_grade else len(reloaded["students"]))
    print(f"  records reloaded : {count}")
    print(f"  matches CSV      : {count == len(rows)}")
    print(f"  attendance typed as float: "
          f"{isinstance(records[0]['attendancePercent'], float)}")
```

</details>

<details>
<summary>Program output</summary>

```text
=== read students.csv ===
  columns  : ['student_id', 'name', 'grade', 'email', 'section', 'attendance_percent']
  students : 10
  size     : 681 bytes

=== CSV contents ===
  id        name              grade    sec   attendance  email
  --------------------------------------------------------------------------------------------
  STU-2301  Spandan Andhale   SY-CSE   A          92.5%  spandan.andhale@school.edu.in
  STU-2302  Riya Sharma       SY-CSE   A          88.0%  riya.sharma@school.edu.in
  STU-2303  Aman Kulkarni     SY-CSE   B          74.5%  aman.kulkarni@school.edu.in
  STU-2304  Neha Deshmukh     TY-CSE   A          96.0%  neha.deshmukh@school.edu.in
  STU-2305  Omkar Patil       TY-CSE   B          61.5%  omkar.patil@school.edu.in
  STU-2306  Sana Shaikh       FY-CSE   A          85.0%  sana.shaikh@school.edu.in
  STU-2307  Rohit Jadhav      FY-CSE   B          79.0%  rohit.jadhav@school.edu.in
  STU-2308  Pooja Nair        SY-CSE   B          58.0%  pooja.nair@school.edu.in
  STU-2309  Kiran Rao         TY-CSE   A          90.5%  kiran.rao@school.edu.in
  STU-2310  Tanvi Gokhale     FY-CSE   A          99.0%  tanvi.gokhale@school.edu.in

=== validation ===
  all 10 record(s) passed

=== wrote students.json ===
  size : 2446 bytes
  shape: flat list

=== first two JSON records ===
[
  {
    "studentId": "STU-2301",
    "name": "Spandan Andhale",
    "grade": "SY-CSE",
    "email": "spandan.andhale@school.edu.in",
    "section": "A",
    "attendancePercent": 92.5,
    "attendanceOk": true
  },
  {
    "studentId": "STU-2302",
    "name": "Riya Sharma",
    "grade": "SY-CSE",
    "email": "riya.sharma@school.edu.in",
    "section": "A",
    "attendancePercent": 88.0,
    "attendanceOk": true
  }
]

=== grade-wise summary ===
  grade     students   avg attendance  below cutoff
  FY-CSE           3           87.67%             0
  SY-CSE           4           78.25%             2
  TY-CSE           3           82.67%             1

=== students below the 75.0% cutoff ===
  Pooja Nair        SY-CSE     58.0%  short by 17.0 points
  Omkar Patil       TY-CSE     61.5%  short by 13.5 points
  Aman Kulkarni     SY-CSE     74.5%  short by 0.5 points

=== section split ===
  section A: 6 student(s)
  section B: 4 student(s)

=== round-trip check ===
  records reloaded : 10
  matches CSV      : True
  attendance typed as float: True

```

</details>

---

## Experiment 9 - Question 10: E-commerce Product Catalog Converter

Scenario: An e-commerce platform keeps its inventory in products.csv with
columns such as product_id, name, price and stock. Convert the CSV into JSON
(products.json) for a frontend that displays products dynamically.

Usage:
  python q10_products_csv_to_json.py
  python q10_products_csv_to_json.py --in-stock-only --indent 4

**File:** [`q10_products_csv_to_json.py`](q10_products_csv_to_json.py) &nbsp;&middot;&nbsp; **Run:** `python q10_products_csv_to_json.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 9 - Question 10: E-commerce Product Catalog Converter

Scenario: An e-commerce platform keeps its inventory in products.csv with
columns such as product_id, name, price and stock. Convert the CSV into JSON
(products.json) for a frontend that displays products dynamically.

Usage:
  python q10_products_csv_to_json.py
  python q10_products_csv_to_json.py --in-stock-only --indent 4
"""

import argparse
import csv
import json
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
DEFAULT_CSV = os.path.join(DATA, "products.csv")
DEFAULT_JSON = os.path.join(DATA, "products.json")

LOW_STOCK = 10

SAMPLE_CSV = """product_id,name,category,price,stock,rating
P-1001,Digital Thermometer,Diagnostics,349.00,120,4.4
P-1002,Pulse Oximeter,Diagnostics,1299.00,45,4.6
P-1003,BP Monitor,Diagnostics,2199.00,8,4.3
P-1004,N95 Mask (pack of 10),Protective,499.00,0,4.1
P-1005,Surgical Gloves (box),Protective,650.00,210,4.5
P-1006,Nebulizer,Respiratory,1850.00,6,4.2
P-1007,Wheelchair Foldable,Mobility,7499.00,3,4.0
P-1008,Walking Stick,Mobility,899.00,64,3.9
P-1009,Glucometer Kit,Diagnostics,1099.00,0,4.4
P-1010,First Aid Box,General,1299.00,32,4.7
P-1011,Hot Water Bag,General,299.00,88,3.8
P-1012,Oxygen Concentrator,Respiratory,38999.00,2,4.8
"""


def ensure_sample(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(SAMPLE_CSV)
        print(f"[setup] created sample input {path}")


def to_product(row):
    price = float(row["price"])
    stock = int(row["stock"])
    return {
        "productId": row["product_id"],
        "name": row["name"],
        "category": row["category"],
        "price": price,
        "priceDisplay": f"Rs.{price:,.2f}",
        "stock": stock,
        "inStock": stock > 0,
        "lowStock": 0 < stock <= LOW_STOCK,
        "rating": float(row["rating"]),
        "inventoryValue": round(price * stock, 2),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a product catalogue CSV into frontend JSON.")
    parser.add_argument("--input", default=DEFAULT_CSV)
    parser.add_argument("--output", default=DEFAULT_JSON)
    parser.add_argument("--indent", type=int, default=2)
    parser.add_argument("--in-stock-only", action="store_true",
                        help="export only products with stock above zero")
    args = parser.parse_args()

    ensure_sample(args.input)

    with open(args.input, "r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        headers = reader.fieldnames

    print(f"=== read {os.path.basename(args.input)} ===")
    print(f"  columns  : {headers}")
    print(f"  products : {len(rows)}")
    print(f"  size     : {os.path.getsize(args.input)} bytes")

    print("\n=== catalogue ===")
    print(f"  {'id':<9}{'name':<26}{'category':<14}{'price':>11}"
          f"{'stock':>7}{'rating':>8}")
    print("  " + "-" * 76)
    for r in rows:
        print(f"  {r['product_id']:<9}{r['name']:<26}{r['category']:<14}"
              f"{float(r['price']):>11,.2f}{int(r['stock']):>7}"
              f"{float(r['rating']):>8.1f}")

    products = [to_product(r) for r in rows]
    exported = [p for p in products if p["inStock"]] \
        if args.in_stock_only else products

    print("\n=== derived fields added for the frontend ===")
    print(json.dumps(products[0], indent=2))

    categories = defaultdict(list)
    for p in products:
        categories[p["category"]].append(p)

    summary = {
        "totalProducts": len(products),
        "exported": len(exported),
        "inStock": sum(1 for p in products if p["inStock"]),
        "outOfStock": sum(1 for p in products if not p["inStock"]),
        "lowStock": sum(1 for p in products if p["lowStock"]),
        "categories": sorted(categories),
        "priceRange": {"min": min(p["price"] for p in products),
                       "max": max(p["price"] for p in products)},
        "averagePrice": round(sum(p["price"] for p in products) /
                              len(products), 2),
        "inventoryValue": round(sum(p["inventoryValue"] for p in products), 2),
        "averageRating": round(sum(p["rating"] for p in products) /
                               len(products), 2),
    }

    payload = {"summary": summary, "products": exported}

    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=args.indent, ensure_ascii=False)

    print(f"\n=== wrote {os.path.basename(args.output)} ===")
    print(f"  size     : {os.path.getsize(args.output)} bytes")
    print(f"  exported : {len(exported)} of {len(products)} product(s)")

    print("\n=== summary block ===")
    print(json.dumps(summary, indent=2))

    print("\n=== category breakdown ===")
    print(f"  {'category':<14}{'items':>6}{'in stock':>10}"
          f"{'avg price':>12}{'inventory value':>18}")
    for cat in sorted(categories):
        group = categories[cat]
        avg = sum(p["price"] for p in group) / len(group)
        value = sum(p["inventoryValue"] for p in group)
        print(f"  {cat:<14}{len(group):>6}"
              f"{sum(1 for p in group if p['inStock']):>10}"
              f"{avg:>12,.2f}{value:>18,.2f}")

    print("\n=== out of stock, hide or mark on the storefront ===")
    for p in products:
        if not p["inStock"]:
            print(f"  {p['productId']}  {p['name']:<26}"
                  f"{p['priceDisplay']:>14}")

    print(f"\n=== low stock (1 to {LOW_STOCK} units), reorder soon ===")
    for p in sorted((p for p in products if p["lowStock"]),
                    key=lambda x: x["stock"]):
        print(f"  {p['productId']}  {p['name']:<26}{p['stock']:>3} left")

    print("\n=== top rated and most valuable stock ===")
    for p in sorted(products, key=lambda x: -x["rating"])[:3]:
        print(f"  rating {p['rating']:.1f}  {p['name']}")
    print()
    for p in sorted(products, key=lambda x: -x["inventoryValue"])[:3]:
        print(f"  Rs.{p['inventoryValue']:>12,.2f} tied up in {p['name']}")

    print("\n=== round-trip check ===")
    with open(args.output, "r", encoding="utf-8") as fh:
        reloaded = json.load(fh)
    print(f"  products reloaded   : {len(reloaded['products'])}")
    print(f"  price is a number   : "
          f"{isinstance(reloaded['products'][0]['price'], float)}")
    print(f"  inStock is a boolean: "
          f"{isinstance(reloaded['products'][0]['inStock'], bool)}")
    print(f"  matches export      : "
          f"{len(reloaded['products']) == len(exported)}")
```

</details>

<details>
<summary>Program output</summary>

```text
=== read products.csv ===
  columns  : ['product_id', 'name', 'category', 'price', 'stock', 'rating']
  products : 12
  size     : 625 bytes

=== catalogue ===
  id       name                      category            price  stock  rating
  ----------------------------------------------------------------------------
  P-1001   Digital Thermometer       Diagnostics        349.00    120     4.4
  P-1002   Pulse Oximeter            Diagnostics      1,299.00     45     4.6
  P-1003   BP Monitor                Diagnostics      2,199.00      8     4.3
  P-1004   N95 Mask (pack of 10)     Protective         499.00      0     4.1
  P-1005   Surgical Gloves (box)     Protective         650.00    210     4.5
  P-1006   Nebulizer                 Respiratory      1,850.00      6     4.2
  P-1007   Wheelchair Foldable       Mobility         7,499.00      3     4.0
  P-1008   Walking Stick             Mobility           899.00     64     3.9
  P-1009   Glucometer Kit            Diagnostics      1,099.00      0     4.4
  P-1010   First Aid Box             General          1,299.00     32     4.7
  P-1011   Hot Water Bag             General            299.00     88     3.8
  P-1012   Oxygen Concentrator       Respiratory     38,999.00      2     4.8

=== derived fields added for the frontend ===
{
  "productId": "P-1001",
  "name": "Digital Thermometer",
  "category": "Diagnostics",
  "price": 349.0,
  "priceDisplay": "Rs.349.00",
  "stock": 120,
  "inStock": true,
  "lowStock": false,
  "rating": 4.4,
  "inventoryValue": 41880.0
}

=== wrote products.json ===
  size     : 4010 bytes
  exported : 12 of 12 product(s)

=== summary block ===
{
  "totalProducts": 12,
  "exported": 12,
  "inStock": 10,
  "outOfStock": 2,
  "lowStock": 4,
  "categories": [
    "Diagnostics",
    "General",
    "Mobility",
    "Protective",
    "Respiratory"
  ],
  "priceRange": {
    "min": 299.0,
    "max": 38999.0
  },
  "averagePrice": 4745.0,
  "inventoryValue": 491438.0,
  "averageRating": 4.31
}

=== category breakdown ===
  category       items  in stock   avg price   inventory value
  Diagnostics        4         3    1,236.50        117,927.00
  General            2         2      799.00         67,880.00
  Mobility           2         2    4,199.00         80,033.00
  Protective         2         1      574.50        136,500.00
  Respiratory        2         2   20,424.50         89,098.00

=== out of stock, hide or mark on the storefront ===
  P-1004  N95 Mask (pack of 10)          Rs.499.00
  P-1009  Glucometer Kit               Rs.1,099.00

=== low stock (1 to 10 units), reorder soon ===
  P-1012  Oxygen Concentrator         2 left
  P-1007  Wheelchair Foldable         3 left
  P-1006  Nebulizer                   6 left
  P-1003  BP Monitor                  8 left

=== top rated and most valuable stock ===
  rating 4.8  Oxygen Concentrator
  rating 4.7  First Aid Box
  rating 4.6  Pulse Oximeter

  Rs.  136,500.00 tied up in Surgical Gloves (box)
  Rs.   77,998.00 tied up in Oxygen Concentrator
  Rs.   58,455.00 tied up in Pulse Oximeter

=== round-trip check ===
  products reloaded   : 12
  price is a number   : True
  inStock is a boolean: True
  matches export      : True

```

</details>

---
