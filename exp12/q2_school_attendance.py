"""
Experiment 12 - Question 2: School Attendance Data

Scenario: A school management system has incomplete attendance records. Fill in
the missing data and compute attendance percentages.

Rubrics covered:
  * create a DataFrame with attendance and total days
  * fill missing attendance using the mean
  * calculate the attendance percentage
  * visualise with a bar chart

Requires: pandas, numpy, matplotlib
"""

import numpy as np
import pandas as pd

from chart_style import (CATEGORICAL, CRITICAL, GOOD, WARNING, apply_style,
                         label_bars, save)
import matplotlib.pyplot as plt

CUTOFF = 75.0


def build_frame():
    return pd.DataFrame({
        "student": ["Spandan", "Riya", "Aman", "Neha", "Omkar", "Sana",
                    "Rohit", "Pooja", "Kiran", "Tanvi", "Harsh", "Isha"],
        "class": ["SY-A", "SY-A", "SY-B", "SY-A", "SY-B", "SY-A",
                  "SY-B", "SY-A", "SY-B", "SY-A", "SY-B", "SY-B"],
        "days_attended": [112, np.nan, 86, 118, 64, 101,
                          np.nan, 71, 95, 121, np.nan, 108],
        "total_days": [124] * 12,
    })


def main():
    apply_style()
    df = build_frame()

    print("=== raw attendance records ===")
    print(df.to_string(index=False))

    print("\n=== missing data check ===")
    print(df.isna().sum().to_string())
    missing = df[df["days_attended"].isna()]
    print(f"\n  {len(missing)} record(s) incomplete: "
          f"{missing['student'].tolist()}")
    print(f"  completeness: "
          f"{df['days_attended'].notna().mean() * 100:.1f}%")

    mean_attended = df["days_attended"].mean()
    print("\n=== filling the gaps with the column mean ===")
    print(f"  mean of the known values : {mean_attended:.2f} days")
    print(f"  (computed from {int(df['days_attended'].notna().sum())} "
          f"known record(s), NaN is skipped automatically)")

    df["was_missing"] = df["days_attended"].isna()
    df["days_attended"] = df["days_attended"].fillna(round(mean_attended))
    df["days_attended"] = df["days_attended"].astype(int)

    print("\n=== after fillna ===")
    print(df.to_string(index=False))
    print(f"\n  remaining nulls: {int(df.isna().sum().sum())}")

    df["attendance_percent"] = (
        df["days_attended"] / df["total_days"] * 100).round(2)
    df["days_absent"] = df["total_days"] - df["days_attended"]
    df["meets_cutoff"] = df["attendance_percent"] >= CUTOFF
    df["status"] = np.where(df["attendance_percent"] >= 90, "excellent",
                            np.where(df["attendance_percent"] >= CUTOFF,
                                     "adequate", "detained"))

    print("\n=== attendance percentages ===")
    print(df[["student", "class", "days_attended", "total_days",
              "attendance_percent", "days_absent", "status",
              "was_missing"]].to_string(index=False))

    print(f"\n=== summary (cutoff {CUTOFF}%) ===")
    print(f"  students              : {len(df)}")
    print(f"  average attendance    : "
          f"{df['attendance_percent'].mean():.2f}%")
    print(f"  median attendance     : "
          f"{df['attendance_percent'].median():.2f}%")
    print(f"  highest               : {df['attendance_percent'].max():.2f}% "
          f"({df.loc[df['attendance_percent'].idxmax(), 'student']})")
    print(f"  lowest                : {df['attendance_percent'].min():.2f}% "
          f"({df.loc[df['attendance_percent'].idxmin(), 'student']})")
    print(f"  meeting the cutoff    : {int(df['meets_cutoff'].sum())} "
          f"of {len(df)} ({df['meets_cutoff'].mean() * 100:.1f}%)")

    print("\n=== students below the cutoff (detention list) ===")
    short = df[~df["meets_cutoff"]].sort_values("attendance_percent")
    if len(short):
        for _, row in short.iterrows():
            needed = int(np.ceil(
                (CUTOFF / 100 * row["total_days"]) - row["days_attended"]))
            print(f"  {row['student']:<10}{row['attendance_percent']:>7.2f}%  "
                  f"needs {needed} more day(s) to reach {CUTOFF:.0f}%")
    else:
        print("  none")

    print("\n=== by class ===")
    print(df.groupby("class")["attendance_percent"].agg(
        ["count", "mean", "min", "max"]).round(2).to_string())

    print("\n=== status counts ===")
    print(df["status"].value_counts().to_string())

    # ---------------- chart ----------------
    ordered = df.sort_values("attendance_percent", ascending=False)
    colour_for = {"excellent": GOOD, "adequate": CATEGORICAL[0],
                  "detained": CRITICAL}
    colours = [colour_for[s] for s in ordered["status"]]

    fig, ax = plt.subplots(figsize=(11, 5.5))
    bars = ax.bar(ordered["student"], ordered["attendance_percent"],
                  color=colours, edgecolor="#FCFCFB", linewidth=2, width=0.72)
    label_bars(ax, bars, ordered["attendance_percent"].tolist(),
               fmt="{:.1f}%", offset=0.015)

    ax.axhline(CUTOFF, color=WARNING, linestyle="--", linewidth=1.5)
    ax.text(len(ordered) - 0.4, CUTOFF + 1.2,
            f"{CUTOFF:.0f}% cutoff", color=WARNING, fontsize=9, ha="right")
    ax.axhline(df["attendance_percent"].mean(), color="#8A8A82",
               linestyle=":", linewidth=1.2)
    ax.text(0, df["attendance_percent"].mean() + 1.2,
            f"class average {df['attendance_percent'].mean():.1f}%",
            color="#6B6B64", fontsize=8)

    # mark the three imputed bars, so the chart does not hide the gap-filling
    for bar, flag in zip(bars, ordered["was_missing"]):
        if flag:
            ax.text(bar.get_x() + bar.get_width() / 2, 2,
                    "imputed", rotation=90, fontsize=7.5, color="#FCFCFB",
                    ha="center", va="bottom")

    ax.set_title("Attendance percentage by student "
                 f"({int(df['was_missing'].sum())} records filled with the "
                 f"mean)")
    ax.set_ylabel("Attendance (%)")
    ax.set_ylim(0, 112)
    ax.set_xlabel("")

    handles = [plt.Rectangle((0, 0), 1, 1, color=colour_for[k])
               for k in ("excellent", "adequate", "detained")]
    ax.legend(handles, ["90% and above", f"{CUTOFF:.0f}-89%",
                        f"below {CUTOFF:.0f}% (detained)"],
              loc="lower left", ncol=3)

    save(fig, "q2_attendance_bar.png")

    print("\n=== note on imputation ===")
    print("  Filling with the column mean keeps the row usable but invents a")
    print("  value, so the three affected bars are labelled 'imputed' on the")
    print("  chart. For a real detention decision those records should be")
    print("  corrected from the register, not estimated.")


if __name__ == "__main__":
    main()
