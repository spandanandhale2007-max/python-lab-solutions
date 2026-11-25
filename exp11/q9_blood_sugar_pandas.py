"""
Experiment 11 - Question 9: Medical Data Analysis with Pandas

Scenario: A hospital stores patients' blood sugar levels recorded at 4 times
of day (Morning, Noon, Evening, Night) for 5 patients.

Task:
  1) Calculate the daily average for each patient (row-wise).
  2) Find the time of day when the average blood sugar was highest
     (column-wise).

Note: the sheet repeats Experiment 10 Question 9 here; this version answers it
with Pandas, the topic of Experiment 11.

Rubrics covered:
  * correct DataFrame representation
  * row-wise and column-wise computation
  * correct use of mean and idxmax
  * clarity in output and labelling

Requires: pandas, numpy
"""

import numpy as np
import pandas as pd

PATIENTS = ["P-101 Sharma", "P-102 Andhale", "P-103 Kulkarni",
            "P-104 Deshmukh", "P-105 Patil"]
TIMES = ["Morning", "Noon", "Evening", "Night"]
NORMAL_FASTING_MAX = 100
NORMAL_POST_MEAL_MAX = 140


def classify(avg):
    if avg >= 150:
        return "diabetic range"
    if avg >= 125:
        return "pre-diabetic"
    if avg >= 110:
        return "borderline"
    return "within range"


def main():
    df = pd.DataFrame(
        [[92, 148, 134, 110],
         [86, 132, 121, 98],
         [128, 196, 178, 152],
         [74, 118, 109, 88],
         [112, 172, 160, 131]],
        index=PATIENTS, columns=TIMES)
    df.index.name = "patient"
    df.columns.name = "time_of_day"

    print("=== blood sugar table (mg/dL) ===")
    print(df.to_string())
    print(f"\n  shape {df.shape}, {df.size} readings")

    # 1) row-wise average
    patient_avg = df.mean(axis=1)
    print("\n=== 1) daily average per patient (axis=1) ===")
    print(patient_avg.round(2).to_string())

    report = pd.DataFrame({
        "daily_avg": patient_avg.round(2),
        "min": df.min(axis=1),
        "max": df.max(axis=1),
        "swing": df.max(axis=1) - df.min(axis=1),
        "peak_time": df.idxmax(axis=1),
    })
    report["status"] = report["daily_avg"].apply(classify)
    print("\n" + report.to_string())
    print(f"\n  highest daily average : {patient_avg.idxmax()} "
          f"({patient_avg.max():.2f} mg/dL)")
    print(f"  lowest daily average  : {patient_avg.idxmin()} "
          f"({patient_avg.min():.2f} mg/dL)")

    # 2) column-wise average
    time_avg = df.mean(axis=0)
    print("\n=== 2) average by time of day (axis=0) ===")
    print(time_avg.round(2).to_string())
    print(f"\n  time_avg.idxmax() -> {time_avg.idxmax()}")
    print(f"  the highest average blood sugar occurs at "
          f"{time_avg.idxmax()} ({time_avg.max():.2f} mg/dL)")
    print(f"  the lowest is at {time_avg.idxmin()} "
          f"({time_avg.min():.2f} mg/dL)")
    print(f"  morning to noon rise  : "
          f"{time_avg['Noon'] - time_avg['Morning']:+.2f} mg/dL "
          f"(the post-meal spike)")

    time_report = pd.DataFrame({
        "average": time_avg.round(2),
        "min": df.min(axis=0),
        "max": df.max(axis=0),
        "highest_patient": df.idxmax(axis=0),
    })
    print("\n" + time_report.to_string())

    print("\n=== text chart by time of day ===")
    for time, value in time_avg.items():
        marker = "  <== highest" if time == time_avg.idxmax() else ""
        print(f"  {time:<9}{value:>8.2f}  {'#' * int(value / 4)}{marker}")

    print("\n=== describe() per time of day ===")
    print(df.describe().round(2).to_string())

    print("\n=== fasting (Morning) check ===")
    fasting = df["Morning"]
    fasting_report = pd.DataFrame({
        "morning_mg_dl": fasting,
        "above_normal": fasting > NORMAL_FASTING_MAX,
        "excess": (fasting - NORMAL_FASTING_MAX).clip(lower=0),
    })
    print(fasting_report.to_string())
    print(f"\n  {int(fasting_report['above_normal'].sum())} of {len(df)} "
          f"patient(s) have a high fasting reading "
          f"(normal up to {NORMAL_FASTING_MAX} mg/dL)")

    print(f"\n=== post-meal readings above {NORMAL_POST_MEAL_MAX} mg/dL ===")
    post_meal = df[["Noon", "Evening", "Night"]]
    flagged = post_meal.stack()
    flagged = flagged[flagged > NORMAL_POST_MEAL_MAX]
    print(flagged.to_string())
    print(f"\n  {len(flagged)} of {post_meal.size} post-meal readings are "
          f"out of range")

    print("\n=== patients needing review (any reading above 180) ===")
    critical = df[(df > 180).any(axis=1)]
    if len(critical):
        print(critical.to_string())
        print(f"\n  {len(critical)} patient(s) flagged")
    else:
        print("  none")

    print("\n=== deviation from each patient's own daily average ===")
    deviation = df.sub(patient_avg, axis=0).round(1)
    print(deviation.to_string())

    print("\n=== long format and groupby ===")
    long = df.reset_index().melt(id_vars="patient", var_name="time_of_day",
                                 value_name="mg_dl")
    print(long.head(6).to_string(index=False))
    print("\n  groupby time_of_day:")
    print(long.groupby("time_of_day", sort=False)["mg_dl"].agg(
        ["mean", "min", "max"]).round(2).to_string())
    print("\n  groupby patient:")
    print(long.groupby("patient")["mg_dl"].agg(
        ["mean", "max"]).round(2).to_string())

    print("\n=== reading bands (pd.cut) ===")
    long["band"] = pd.cut(long["mg_dl"],
                          bins=[0, 100, 140, 180, np.inf],
                          labels=["normal", "elevated", "high", "very high"])
    print(long["band"].value_counts().sort_index().to_string())

    print("\n=== ward-level summary ===")
    values = df.to_numpy()
    print(f"  patients monitored  : {df.shape[0]}")
    print(f"  readings per day    : {df.shape[1]}")
    print(f"  ward average        : {values.mean():.2f} mg/dL")
    print(f"  ward median         : {np.median(values):.2f} mg/dL")
    peak = df.stack().idxmax()
    print(f"  overall peak        : {df.stack().max()} mg/dL "
          f"({peak[0]} at {peak[1]})")
    print(f"  patients above a 140 daily average : "
          f"{int((patient_avg > 140).sum())} of {df.shape[0]}")


if __name__ == "__main__":
    main()
