"""
Experiment 11 - Question 8: Scientific Experiment Data with Pandas

Scenario: 5 experiments, each with 4 trials, giving a 5x4 table of readings.

Task:
  1) Find the average result of each experiment (row-wise).
  2) Find the trial that produced the maximum overall reading.

Note: the sheet repeats Experiment 10 Question 8 here; this version answers it
with Pandas, the topic of Experiment 11.

Rubrics covered:
  * DataFrame creation
  * row-wise average (axis=1)
  * max value and its position (max, idxmax, stack().idxmax())
  * output clarity

Requires: pandas, numpy
"""

import numpy as np
import pandas as pd

EXPERIMENTS = ["E1 Catalyst A", "E2 Catalyst B", "E3 Control",
               "E4 Catalyst C", "E5 Catalyst D"]
TRIALS = ["Trial 1", "Trial 2", "Trial 3", "Trial 4"]


def main():
    df = pd.DataFrame(
        [[12.4, 13.1, 12.9, 13.6],
         [15.8, 16.2, 15.5, 17.1],
         [9.2, 9.0, 9.4, 8.8],
         [14.1, 13.8, 18.9, 14.4],
         [16.0, 15.7, 16.4, 16.1]],
        index=EXPERIMENTS, columns=TRIALS)
    df.index.name = "experiment"
    df.columns.name = "trial"

    print("=== the readings table ===")
    print(df.to_string())
    print(f"\n  shape {df.shape}, {df.size} readings")

    # 1) row-wise average
    row_avg = df.mean(axis=1)
    print("\n=== 1) average per experiment (axis=1) ===")
    print(row_avg.round(3).to_string())

    summary = pd.DataFrame({
        "mean": df.mean(axis=1).round(3),
        "std": df.std(axis=1).round(3),
        "min": df.min(axis=1),
        "max": df.max(axis=1),
        "spread": (df.max(axis=1) - df.min(axis=1)).round(2),
        "best_trial": df.idxmax(axis=1),
    })
    print("\n" + summary.to_string())
    print(f"\n  best experiment  : {row_avg.idxmax()} "
          f"(mean {row_avg.max():.3f})")
    print(f"  worst experiment : {row_avg.idxmin()} "
          f"(mean {row_avg.min():.3f})")

    # 2) the single maximum reading, with its row and column labels
    stacked = df.stack()
    peak_label = stacked.idxmax()
    peak_value = stacked.max()

    print("\n=== 2) maximum overall reading ===")
    print(f"  df.stack().max()    : {peak_value:.2f}")
    print(f"  df.stack().idxmax() : {peak_label}")
    print(f"  experiment          : {peak_label[0]}")
    print(f"  trial               : {peak_label[1]}")
    print(f"  df.max().max()      : {df.max().max():.2f}  (same value)")
    print(f"  df.max()            :")
    print(df.max().round(2).to_string())
    print(f"\n  the column holding the peak : {df.max().idxmax()}")

    print("\n=== column-wise view: which trial slot performs best? ===")
    col_summary = pd.DataFrame({
        "mean": df.mean(axis=0).round(3),
        "min": df.min(axis=0),
        "max": df.max(axis=0),
        "best_experiment": df.idxmax(axis=0),
    })
    print(col_summary.to_string())
    print(f"\n  strongest trial slot : {df.mean(axis=0).idxmax()}")

    print("\n=== describe() per trial ===")
    print(df.describe().round(3).to_string())

    print("\n=== repeatability ranking (lower std is better) ===")
    stds = df.std(axis=1).sort_values()
    for rank, (name, value) in enumerate(stds.items(), 1):
        verdict = ("highly repeatable" if value < 0.5 else
                   "acceptable" if value < 1.0 else
                   "poor, suspect an outlier")
        print(f"  {rank}. {name:<16}std {value:>6.3f}  {verdict}")

    print("\n=== outlier detection with z-scores per row ===")
    z = df.sub(row_avg, axis=0).div(df.std(axis=1), axis=0).abs().round(2)
    print(z.to_string())
    flagged = z.stack()
    flagged = flagged[flagged > 1.6]
    if len(flagged):
        for (exp, trial), score in flagged.items():
            print(f"\n  {exp} / {trial}: reading {df.loc[exp, trial]:.2f} "
                  f"is {score:.2f} std from its row mean "
                  f"({row_avg[exp]:.2f})")
    else:
        print("\n  no reading stands out")

    print("\n=== comparison against the control row ===")
    control = row_avg["E3 Control"]
    comparison = pd.DataFrame({
        "mean": row_avg.round(3),
        "lift_vs_control_percent": ((row_avg / control - 1) * 100).round(2),
    }).drop(index="E3 Control")
    print(comparison.to_string())
    print(f"\n  control mean : {control:.3f}")

    print("\n=== long format and groupby ===")
    long = df.reset_index().melt(id_vars="experiment", var_name="trial",
                                 value_name="reading")
    print(long.head(6).to_string(index=False))
    print(f"\n  rows: {len(long)}")
    print("\n  groupby experiment:")
    print(long.groupby("experiment")["reading"].agg(
        ["mean", "std", "max"]).round(3).to_string())
    print("\n  groupby trial:")
    print(long.groupby("trial")["reading"].agg(
        ["mean", "max"]).round(3).to_string())

    print("\n=== top 5 individual readings ===")
    print(long.nlargest(5, "reading").to_string(index=False))

    print("\n=== whole-dataset summary ===")
    values = df.to_numpy()
    print(f"  grand mean : {values.mean():.3f}")
    print(f"  overall std: {values.std():.3f}")
    print(f"  minimum    : {stacked.min():.2f} at {stacked.idxmin()}")
    print(f"  maximum    : {peak_value:.2f} at {peak_label}")
    print(f"  range      : {np.ptp(values):.2f}")


if __name__ == "__main__":
    main()
