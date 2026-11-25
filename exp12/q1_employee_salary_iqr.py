"""
Experiment 12 - Question 1: Employee Salary Analysis

Scenario: Analyse salary data from a startup to understand patterns and detect
anomalies in compensation.

Rubrics covered:
  * create a DataFrame with employee salary data
  * compute summary statistics and the IQR
  * filter outliers using the IQR method
  * visualise with a boxplot and a histogram

Requires: pandas, numpy, matplotlib
Charts are written to exp12/plots/ (no window is opened).
"""

import numpy as np
import pandas as pd

from chart_style import (CATEGORICAL, CRITICAL, INK_MUTED, apply_style, save)
import matplotlib.pyplot as plt


def build_frame():
    rng = np.random.default_rng(seed=12)
    names = ["Spandan", "Riya", "Aman", "Neha", "Omkar", "Sana", "Rohit",
             "Pooja", "Kiran", "Tanvi", "Harsh", "Kavita", "Sameer", "Isha",
             "Vikram", "Meera", "Nikhil", "Aarti", "Dev", "Sneha"]
    departments = rng.choice(["Engineering", "Design", "Sales", "Operations"],
                             size=len(names), p=[0.45, 0.15, 0.25, 0.15])
    # a normal band plus three deliberate anomalies
    salaries = np.round(rng.normal(68000, 14000, size=len(names)), -2)
    salaries[0] = 29000         # underpaid intern-level salary
    salaries[5] = 245000        # founder-level outlier
    salaries[11] = 198000       # second high outlier
    return pd.DataFrame({"name": names, "department": departments,
                         "salary": salaries.astype(int)})


def main():
    apply_style()
    df = build_frame()

    print("=== employee salary DataFrame ===")
    print(df.to_string(index=False))
    print(f"\n  rows {len(df)}, columns {list(df.columns)}")

    print("\n=== summary statistics ===")
    print(df["salary"].describe().round(2).to_string())

    q1 = df["salary"].quantile(0.25)
    q3 = df["salary"].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    print("\n=== IQR calculation ===")
    print(f"  Q1 (25th percentile) : Rs.{q1:>12,.2f}")
    print(f"  Q3 (75th percentile) : Rs.{q3:>12,.2f}")
    print(f"  IQR = Q3 - Q1        : Rs.{iqr:>12,.2f}")
    print(f"  lower fence Q1-1.5*IQR: Rs.{lower:>11,.2f}")
    print(f"  upper fence Q3+1.5*IQR: Rs.{upper:>11,.2f}")
    print(f"  median               : Rs.{df['salary'].median():>12,.2f}")
    print(f"  mean                 : Rs.{df['salary'].mean():>12,.2f}")
    print(f"  the mean sits "
          f"Rs.{df['salary'].mean() - df['salary'].median():,.2f} above the "
          f"median, which already hints at high outliers")

    df["is_outlier"] = (df["salary"] < lower) | (df["salary"] > upper)
    df["side"] = np.where(df["salary"] > upper, "high",
                          np.where(df["salary"] < lower, "low", "normal"))

    outliers = df[df["is_outlier"]].sort_values("salary")
    clean = df[~df["is_outlier"]]

    print(f"\n=== outliers detected: {len(outliers)} ===")
    if len(outliers):
        print(outliers[["name", "department", "salary", "side"]]
              .to_string(index=False))
    else:
        print("  none")

    print("\n=== effect of removing the outliers ===")
    comparison = pd.DataFrame({
        "with_outliers": df["salary"].describe().round(2),
        "without_outliers": clean["salary"].describe().round(2),
    })
    print(comparison.to_string())
    print(f"\n  mean falls from Rs.{df['salary'].mean():,.0f} to "
          f"Rs.{clean['salary'].mean():,.0f}")
    print(f"  std dev falls from Rs.{df['salary'].std():,.0f} to "
          f"Rs.{clean['salary'].std():,.0f}")
    print(f"  the median barely moves: Rs.{df['salary'].median():,.0f} -> "
          f"Rs.{clean['salary'].median():,.0f} (medians resist outliers)")

    print("\n=== by department (outliers excluded) ===")
    by_dept = clean.groupby("department")["salary"].agg(
        ["count", "mean", "median", "min", "max"]).round(0).astype(int)
    print(by_dept.to_string())

    # ---------------- charts ----------------
    fig, (ax_box, ax_hist) = plt.subplots(1, 2, figsize=(12, 5))

    # boxplot: shows the quartiles and the fences the IQR method uses
    bp = ax_box.boxplot(df["salary"], vert=True, widths=0.45,
                        patch_artist=True, showfliers=True,
                        medianprops=dict(color="#FFFFFF", linewidth=2),
                        boxprops=dict(facecolor=CATEGORICAL[0],
                                      edgecolor=CATEGORICAL[0], linewidth=1.5),
                        whiskerprops=dict(color=INK_MUTED, linewidth=1.5),
                        capprops=dict(color=INK_MUTED, linewidth=1.5),
                        flierprops=dict(marker="o", markersize=8,
                                        markerfacecolor=CRITICAL,
                                        markeredgecolor="#FFFFFF",
                                        markeredgewidth=1.5))
    ax_box.set_title("Salary spread with IQR fences")
    ax_box.set_ylabel("Annual salary (Rs.)")
    ax_box.set_xticks([1])
    ax_box.set_xticklabels([f"All staff (n={len(df)})"])
    ax_box.axhline(upper, color=CRITICAL, linestyle="--", linewidth=1.2)
    ax_box.text(1.32, upper, f"upper fence\nRs.{upper:,.0f}",
                color=CRITICAL, fontsize=8, va="center")
    ax_box.axhline(lower, color=CRITICAL, linestyle="--", linewidth=1.2)
    ax_box.text(1.32, lower, f"lower fence\nRs.{lower:,.0f}",
                color=CRITICAL, fontsize=8, va="center")
    ax_box.axhline(df["salary"].median(), color=CATEGORICAL[2],
                   linestyle=":", linewidth=1.2)
    for _, row in outliers.iterrows():
        ax_box.annotate(f"{row['name']} Rs.{row['salary']:,}",
                        xy=(1, row["salary"]), xytext=(0.52, row["salary"]),
                        fontsize=8, color=CRITICAL, va="center", ha="right")
    ax_box.set_ylim(0, df["salary"].max() * 1.12)

    # histogram: shows the shape of the distribution
    ax_hist.hist(clean["salary"], bins=8, color=CATEGORICAL[0],
                 edgecolor="#FCFCFB", linewidth=1.5, label="within fences")
    if len(outliers):
        ax_hist.hist(outliers["salary"], bins=8, color=CRITICAL,
                     edgecolor="#FCFCFB", linewidth=1.5, label="outlier")
    ax_hist.axvline(df["salary"].median(), color=CATEGORICAL[2],
                    linestyle="--", linewidth=1.5)
    ax_hist.text(df["salary"].median(), ax_hist.get_ylim()[1] * 0.95,
                 f" median Rs.{df['salary'].median():,.0f}",
                 color=CATEGORICAL[2], fontsize=8, va="top")
    ax_hist.set_title("Salary distribution")
    ax_hist.set_xlabel("Annual salary (Rs.)")
    ax_hist.set_ylabel("Employees")
    ax_hist.legend(loc="upper right")

    fig.suptitle("Startup compensation: spread and anomalies "
                 f"({len(outliers)} outliers by the 1.5 x IQR rule)")
    save(fig, "q1_salary_box_hist.png")

    print("\n=== reading the charts ===")
    print("  The boxplot answers 'is anyone paid out of band?' - the three red")
    print("  points sit outside the dashed 1.5 x IQR fences.")
    print("  The histogram answers 'what does normal look like?' - a single")
    print(f"  cluster around Rs.{clean['salary'].median():,.0f} with a long "
          f"right tail.")
    print("  Both charts carry direct value labels, so colour is never the")
    print("  only encoding.")


if __name__ == "__main__":
    main()
