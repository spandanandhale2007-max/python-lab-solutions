"""
Experiment 10 - Question 8: Scientific Experiment Data

Scenario: 5 experiments were conducted, each with 4 trials, giving a 5x4 array
of readings.

Task:
  1) Find the average result of each experiment (row-wise).
  2) Find the trial that produced the maximum overall reading.

Rubrics covered:
  * 2D array creation
  * row-wise average (axis=1)
  * max value and its position (np.max, np.argmax)
  * output clarity

Requires: numpy
"""

import numpy as np

EXPERIMENTS = ["E1 Catalyst A", "E2 Catalyst B", "E3 Control",
               "E4 Catalyst C", "E5 Catalyst D"]
TRIALS = ["Trial 1", "Trial 2", "Trial 3", "Trial 4"]


def main():
    readings = np.array([
        [12.4, 13.1, 12.9, 13.6],     # E1
        [15.8, 16.2, 15.5, 17.1],     # E2
        [ 9.2,  9.0,  9.4,  8.8],     # E3 control
        [14.1, 13.8, 18.9, 14.4],     # E4, one outlier
        [16.0, 15.7, 16.4, 16.1],     # E5
    ])

    print("=== 5x4 reading array ===")
    print(f"  shape {readings.shape}, dtype {readings.dtype}, "
          f"{readings.size} readings")
    print(f"\n  {'experiment':<16}" + "".join(f"{t:>10}" for t in TRIALS))
    print("  " + "-" * 57)
    for name, row in zip(EXPERIMENTS, readings):
        print(f"  {name:<16}" + "".join(f"{v:>10.2f}" for v in row))

    # 1) row-wise average
    row_avg = readings.mean(axis=1)
    print("\n=== 1) average per experiment (axis=1) ===")
    print(f"  readings.mean(axis=1) -> {np.round(row_avg, 3)}")
    print(f"\n  {'experiment':<16}{'mean':>9}{'std':>8}{'min':>8}{'max':>8}"
          f"{'spread':>9}")
    for name, mean, std, lo, hi in zip(EXPERIMENTS, row_avg,
                                       readings.std(axis=1),
                                       readings.min(axis=1),
                                       readings.max(axis=1)):
        print(f"  {name:<16}{mean:>9.3f}{std:>8.3f}{lo:>8.2f}{hi:>8.2f}"
              f"{hi - lo:>9.2f}")

    print(f"\n  best experiment  : {EXPERIMENTS[row_avg.argmax()]} "
          f"(mean {row_avg.max():.3f})")
    print(f"  worst experiment : {EXPERIMENTS[row_avg.argmin()]} "
          f"(mean {row_avg.min():.3f})")

    # 2) the single maximum reading and where it came from
    peak = readings.max()
    flat = readings.argmax()
    row, col = np.unravel_index(flat, readings.shape)

    print("\n=== 2) maximum overall reading ===")
    print(f"  np.max(readings)      : {peak:.2f}")
    print(f"  np.argmax(readings)   : {flat}  (index into the flattened array)")
    print(f"  np.unravel_index      : row {row}, column {col}")
    print(f"  that is {EXPERIMENTS[row]}, {TRIALS[col]} -> "
          f"{readings[row, col]:.2f}")
    print(f"  flattened array       : {readings.ravel()}")
    print(f"  element {flat} of the flat array is {readings.ravel()[flat]:.2f}")

    print("\n=== best trial inside each experiment (argmax with axis=1) ===")
    best_cols = readings.argmax(axis=1)
    for name, c, value in zip(EXPERIMENTS, best_cols,
                              readings.max(axis=1)):
        print(f"  {name:<16}{TRIALS[c]:<9}{value:>8.2f}")

    print("\n=== column-wise view: which trial number performs best? ===")
    col_avg = readings.mean(axis=0)
    print(f"  readings.mean(axis=0) -> {np.round(col_avg, 3)}")
    for trial, avg in zip(TRIALS, col_avg):
        print(f"  {trial:<9}mean {avg:>8.3f}  {'#' * int(avg * 2)}")
    print(f"  strongest trial slot : {TRIALS[col_avg.argmax()]}")

    print("\n=== repeatability check (lower std is better) ===")
    stds = readings.std(axis=1)
    order = stds.argsort()
    for rank, i in enumerate(order, 1):
        verdict = ("highly repeatable" if stds[i] < 0.5 else
                   "acceptable" if stds[i] < 1.0 else
                   "poor, suspect an outlier")
        print(f"  {rank}. {EXPERIMENTS[i]:<16}std {stds[i]:>6.3f}  {verdict}")

    print("\n=== outlier detection (more than 2 std from its row mean) ===")
    centred = readings - row_avg[:, None]
    scaled = np.abs(centred) / readings.std(axis=1)[:, None]
    rows, cols = np.where(scaled > 1.6)
    if rows.size:
        for r, c in zip(rows, cols):
            print(f"  {EXPERIMENTS[r]:<16}{TRIALS[c]:<9}"
                  f"{readings[r, c]:>8.2f}  "
                  f"({scaled[r, c]:.2f} std from its row mean "
                  f"{row_avg[r]:.2f})")
    else:
        print("  no reading stands out")

    print("\n=== comparison against the control (E3) ===")
    control_mean = row_avg[2]
    for name, mean in zip(EXPERIMENTS, row_avg):
        if name.startswith("E3"):
            continue
        lift = (mean / control_mean - 1) * 100
        print(f"  {name:<16}{mean:>8.3f}  {lift:>+8.2f}% vs control "
              f"({control_mean:.3f})")

    print("\n=== whole-dataset summary ===")
    print(f"  grand mean   : {readings.mean():.3f}")
    print(f"  overall std  : {readings.std():.3f}")
    print(f"  minimum      : {readings.min():.2f} at "
          f"{np.unravel_index(readings.argmin(), readings.shape)}")
    print(f"  maximum      : {readings.max():.2f} at {(row, col)}")
    print(f"  range        : {np.ptp(readings):.2f}")


if __name__ == "__main__":
    main()
