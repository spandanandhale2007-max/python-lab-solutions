"""
Experiment 10 - Question 1: Marks Analysis with NumPy

Scenario: The marks of 10 students are given in a NumPy array.

Task:
  1) Find the average, highest and lowest marks.
  2) Display the marks of students who scored above average.

Rubrics covered:
  * correct array creation
  * correct use of NumPy functions (mean, max, min)
  * logical filtering (above average)
  * clear, correct output

Requires: numpy   (pip install numpy)
"""

import numpy as np

STUDENTS = ["Spandan", "Riya", "Aman", "Neha", "Omkar",
            "Sana", "Rohit", "Pooja", "Kiran", "Tanvi"]


def main():
    # 1) array creation
    marks = np.array([78, 92, 55, 88, 64, 71, 45, 83, 96, 59])

    print("=== the array ===")
    print(f"  marks  : {marks}")
    print(f"  names  : {STUDENTS}")
    print(f"  dtype  : {marks.dtype}")
    print(f"  shape  : {marks.shape}")
    print(f"  ndim   : {marks.ndim}")
    print(f"  size   : {marks.size}")
    print(f"  memory : {marks.nbytes} bytes")

    # 2) aggregation with NumPy functions
    average = marks.mean()
    highest = marks.max()
    lowest = marks.min()

    print("\n=== statistics with NumPy ===")
    print(f"  np.mean  -> average : {average:.2f}")
    print(f"  np.max   -> highest : {highest}")
    print(f"  np.min   -> lowest  : {lowest}")
    print(f"  np.argmax-> topper  : index {marks.argmax()} "
          f"({STUDENTS[marks.argmax()]})")
    print(f"  np.argmin-> lowest  : index {marks.argmin()} "
          f"({STUDENTS[marks.argmin()]})")
    print(f"  np.sum   -> total   : {marks.sum()}")
    print(f"  np.median           : {np.median(marks):.2f}")
    print(f"  np.std              : {marks.std():.2f}")
    print(f"  np.ptp   -> range   : {np.ptp(marks)}")

    # 3) boolean filtering
    mask = marks > average
    above = marks[mask]

    print(f"\n=== students above the average of {average:.2f} ===")
    print(f"  boolean mask : {mask}")
    print(f"  filtered     : {above}")
    print(f"  count        : {above.size} of {marks.size}")
    print(f"  their average: {above.mean():.2f}")
    print(f"  indices      : {np.where(mask)[0]}")

    print("\n  name-wise:")
    for name, mark in zip(np.array(STUDENTS)[mask], above):
        print(f"    {name:<10}{mark:>4}  ({mark - average:+.2f} vs average)")

    below = marks[~mask]
    print(f"\n=== at or below average ({below.size} student(s)) ===")
    for name, mark in zip(np.array(STUDENTS)[~mask], below):
        print(f"    {name:<10}{mark:>4}  ({mark - average:+.2f})")

    print("\n=== full class table ===")
    print(f"  {'name':<10}{'marks':>7}{'vs avg':>9}  bar")
    for name, mark in zip(STUDENTS, marks):
        flag = "above" if mark > average else "below"
        print(f"  {name:<10}{mark:>7}{mark - average:>+9.2f}  "
              f"{'#' * (mark // 4)} {flag}")

    print("\n=== vectorised operations, no Python loop ===")
    print(f"  5 grace marks added  : {marks + 5}")
    print(f"  scaled to 50 marks   : {np.round(marks / 2, 1)}")
    print(f"  percentage of total  : "
          f"{np.round(marks / marks.sum() * 100, 2)}")
    print(f"  clipped at 90        : {np.clip(marks, None, 90)}")
    print(f"  sorted ascending     : {np.sort(marks)}")
    print(f"  merit order (indices): {np.argsort(-marks)}")

    print("\n=== grade bands with np.select ===")
    grades = np.select(
        [marks >= 90, marks >= 80, marks >= 70, marks >= 60, marks >= 40],
        ["A+", "A", "B", "C", "D"], default="F")
    for name, mark, grade in zip(STUDENTS, marks, grades):
        print(f"  {name:<10}{mark:>4}  {grade}")

    print("\n=== pass / fail (cut-off 40) ===")
    passed = marks >= 40
    print(f"  passed : {passed.sum()} of {marks.size} "
          f"({passed.mean() * 100:.1f}%)")
    print(f"  failed : {(~passed).sum()} -> "
          f"{np.array(STUDENTS)[~passed].tolist() or 'none'}")


if __name__ == "__main__":
    main()
