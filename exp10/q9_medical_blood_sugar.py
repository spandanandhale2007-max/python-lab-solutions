"""
Experiment 10 - Question 9: Medical Data Analysis

Scenario: A hospital stores patients' blood sugar levels recorded at 4 times
of day (Morning, Noon, Evening, Night) for 5 patients in a 5x4 array.

Task:
  1) Calculate the daily average for each patient (row-wise).
  2) Find the time of day when the average blood sugar was highest
     (column-wise).

Rubrics covered:
  * correct 2D array representation
  * row-wise and column-wise computation
  * correct use of NumPy functions (mean, argmax)
  * clarity in output and labelling

Requires: numpy
"""

import numpy as np

PATIENTS = ["P-101 Sharma", "P-102 Andhale", "P-103 Kulkarni",
            "P-104 Deshmukh", "P-105 Patil"]
TIMES = ["Morning", "Noon", "Evening", "Night"]

NORMAL_FASTING = (70, 100)          # mg/dL
NORMAL_POST_MEAL = (70, 140)


def main():
    # rows = patients, columns = time of day, values in mg/dL
    sugar = np.array([
        [ 92, 148, 134, 110],      # P-101 borderline
        [ 86, 132, 121,  98],      # P-102 normal
        [128, 196, 178, 152],      # P-103 diabetic range
        [ 74, 118, 109,  88],      # P-104 healthy
        [112, 172, 160, 131],      # P-105 pre-diabetic
    ])

    print("=== 5x4 blood sugar array (mg/dL) ===")
    print(f"  shape {sugar.shape}, dtype {sugar.dtype}")
    print(f"\n  {'patient':<17}" + "".join(f"{t:>10}" for t in TIMES))
    print("  " + "-" * 58)
    for name, row in zip(PATIENTS, sugar):
        print(f"  {name:<17}" + "".join(f"{v:>10}" for v in row))

    # 1) row-wise average: daily average per patient
    patient_avg = sugar.mean(axis=1)

    print("\n=== 1) daily average per patient (axis=1) ===")
    print(f"  sugar.mean(axis=1) -> {np.round(patient_avg, 2)}")
    print(f"\n  {'patient':<17}{'daily avg':>11}{'min':>7}{'max':>7}"
          f"{'swing':>8}  status")
    for name, avg, lo, hi in zip(PATIENTS, patient_avg,
                                 sugar.min(axis=1), sugar.max(axis=1)):
        status = ("diabetic range" if avg >= 150 else
                  "pre-diabetic" if avg >= 125 else
                  "borderline" if avg >= 110 else "within range")
        print(f"  {name:<17}{avg:>11.2f}{lo:>7}{hi:>7}{hi - lo:>8}  {status}")

    print(f"\n  highest daily average : {PATIENTS[patient_avg.argmax()]} "
          f"({patient_avg.max():.2f} mg/dL)")
    print(f"  lowest daily average  : {PATIENTS[patient_avg.argmin()]} "
          f"({patient_avg.min():.2f} mg/dL)")

    # 2) column-wise average: which time of day runs highest
    time_avg = sugar.mean(axis=0)
    peak_time = time_avg.argmax()

    print("\n=== 2) average by time of day (axis=0) ===")
    print(f"  sugar.mean(axis=0) -> {np.round(time_avg, 2)}")
    print(f"\n  {'time':<10}{'average':>10}{'min':>7}{'max':>7}  bar")
    for time, avg, lo, hi in zip(TIMES, time_avg,
                                 sugar.min(axis=0), sugar.max(axis=0)):
        marker = "  <== highest" if time == TIMES[peak_time] else ""
        print(f"  {time:<10}{avg:>10.2f}{lo:>7}{hi:>7}  "
              f"{'#' * int(avg / 4)}{marker}")

    print(f"\n  np.argmax(sugar.mean(axis=0)) = {peak_time}")
    print(f"  the highest average blood sugar occurs at "
          f"{TIMES[peak_time]} ({time_avg[peak_time]:.2f} mg/dL)")
    print(f"  the lowest is at {TIMES[time_avg.argmin()]} "
          f"({time_avg.min():.2f} mg/dL)")
    print(f"  morning-to-noon rise: "
          f"{time_avg[1] - time_avg[0]:+.2f} mg/dL on average "
          f"(the post-meal spike)")

    print("\n=== axis recap ===")
    print(f"  sugar.mean()       : {sugar.mean():.2f}  (all 20 readings)")
    print(f"  sugar.mean(axis=0) : shape {time_avg.shape} -> one per time")
    print(f"  sugar.mean(axis=1) : shape {patient_avg.shape} -> one per patient")

    print("\n=== clinical flags ===")
    fasting = sugar[:, 0]
    print(f"  fasting (Morning) normal range {NORMAL_FASTING[0]}-"
          f"{NORMAL_FASTING[1]} mg/dL")
    for name, value in zip(PATIENTS, fasting):
        if value > NORMAL_FASTING[1]:
            print(f"    {name:<17}{value:>5} mg/dL  HIGH fasting "
                  f"({value - NORMAL_FASTING[1]:+} above normal)")
        elif value < NORMAL_FASTING[0]:
            print(f"    {name:<17}{value:>5} mg/dL  LOW fasting")
        else:
            print(f"    {name:<17}{value:>5} mg/dL  normal")

    print(f"\n  post-meal readings above {NORMAL_POST_MEAL[1]} mg/dL:")
    post_meal = sugar[:, 1:]
    rows, cols = np.where(post_meal > NORMAL_POST_MEAL[1])
    for r, c in zip(rows, cols):
        print(f"    {PATIENTS[r]:<17}{TIMES[c + 1]:<9}"
              f"{post_meal[r, c]:>5} mg/dL")
    print(f"  total out-of-range post-meal readings: {rows.size} of "
          f"{post_meal.size}")

    print("\n=== patients needing review (any reading above 180) ===")
    critical = (sugar > 180).any(axis=1)
    if critical.any():
        for name, row in zip(np.array(PATIENTS)[critical], sugar[critical]):
            print(f"  {name:<17}{row}  peak {row.max()} mg/dL")
    else:
        print("  none")

    print("\n=== ward-level summary ===")
    print(f"  patients monitored : {sugar.shape[0]}")
    print(f"  readings per day   : {sugar.shape[1]}")
    print(f"  ward average       : {sugar.mean():.2f} mg/dL")
    print(f"  ward median        : {np.median(sugar):.2f} mg/dL")
    print(f"  overall peak       : {sugar.max()} mg/dL "
          f"({PATIENTS[np.unravel_index(sugar.argmax(), sugar.shape)[0]]} at "
          f"{TIMES[np.unravel_index(sugar.argmax(), sugar.shape)[1]]})")
    print(f"  patients above 140 daily average: "
          f"{int((patient_avg > 140).sum())} of {sugar.shape[0]}")

    print("\n=== normalised per patient (how each reading compares to "
          "that patient's own average) ===")
    deviation = sugar - patient_avg[:, None]
    print(f"  {'patient':<17}" + "".join(f"{t:>10}" for t in TIMES))
    for name, row in zip(PATIENTS, deviation):
        print(f"  {name:<17}" + "".join(f"{v:>+10.1f}" for v in row))


if __name__ == "__main__":
    main()
