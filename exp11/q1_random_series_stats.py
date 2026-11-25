"""
Experiment 11 - Question 1: Random Data Generation with Pandas

Scenario: A data analyst needs to simulate data for testing.

Task:
  1) Create a Pandas Series of 10 random integers between 1 and 100 and
     display the mean, median and standard deviation.

Rubrics covered:
  * Series creation using random numbers
  * use of statistical functions (mean, median, std)
  * output formatting

Requires: pandas, numpy
"""

import numpy as np
import pandas as pd


def main():
    rng = np.random.default_rng(seed=11)
    values = rng.integers(1, 101, size=10)
    labels = [f"sample_{i:02d}" for i in range(1, 11)]

    series = pd.Series(values, index=labels, name="random_value")

    print("=== the Series ===")
    print(series.to_string())
    print(f"\n  name   : {series.name}")
    print(f"  dtype  : {series.dtype}")
    print(f"  length : {len(series)}")
    print(f"  index  : {list(series.index)}")

    print("\n=== required statistics ===")
    print(f"  mean               : {series.mean():.4f}")
    print(f"  median             : {series.median():.4f}")
    print(f"  standard deviation : {series.std():.4f}  (sample, ddof=1)")
    print(f"  population std     : {series.std(ddof=0):.4f}  (ddof=0)")

    print("\n=== describe() gives all of it at once ===")
    print(series.describe().to_string())

    print("\n=== more statistics ===")
    print(f"  sum      : {series.sum()}")
    print(f"  min      : {series.min()}  at {series.idxmin()}")
    print(f"  max      : {series.max()}  at {series.idxmax()}")
    print(f"  range    : {series.max() - series.min()}")
    print(f"  variance : {series.var():.4f}")
    print(f"  skew     : {series.skew():.4f}")
    print(f"  mode     : {series.mode().tolist()}")

    print("\n=== quartiles ===")
    for q in (0.25, 0.50, 0.75):
        print(f"  quantile({q:.2f}) : {series.quantile(q):.2f}")
    iqr = series.quantile(0.75) - series.quantile(0.25)
    print(f"  IQR            : {iqr:.2f}")

    print("\n=== sorted view ===")
    print(series.sort_values(ascending=False).to_string())

    print("\n=== values above the mean (boolean indexing) ===")
    above = series[series > series.mean()]
    print(above.to_string())
    print(f"  {len(above)} of {len(series)} values are above "
          f"{series.mean():.2f}")

    print("\n=== deviation from the mean ===")
    frame = pd.DataFrame({
        "value": series,
        "deviation": (series - series.mean()).round(2),
        "z_score": ((series - series.mean()) / series.std()).round(3),
        "above_mean": series > series.mean(),
    })
    print(frame.to_string())

    print("\n=== binning with pd.cut ===")
    bins = pd.cut(series, bins=[0, 25, 50, 75, 100],
                  labels=["1-25", "26-50", "51-75", "76-100"])
    counts = bins.value_counts().sort_index()
    for label, count in counts.items():
        print(f"  {label:<8}{count:>3}  {'#' * count}")

    print("\n=== cumulative statistics ===")
    cumulative = pd.DataFrame({
        "value": series,
        "cumsum": series.cumsum(),
        "running_mean": series.expanding().mean().round(2),
        "rolling_mean_3": series.rolling(3).mean().round(2),
    })
    print(cumulative.to_string())

    print("\n=== vectorised transforms ===")
    print(f"  doubled      : {(series * 2).tolist()}")
    print(f"  as percentage: "
          f"{(series / series.sum() * 100).round(2).tolist()}")
    print(f"  square roots : {np.sqrt(series).round(3).tolist()}")
    print(f"  rank         : {series.rank(ascending=False).astype(int).tolist()}")

    print("\n=== reproducibility ===")
    again = pd.Series(np.random.default_rng(seed=11).integers(1, 101, size=10),
                      index=labels, name="random_value")
    print(f"  the same seed gives the same Series: "
          f"{series.equals(again)}")
    print("  this matters so the lab result can be checked later")


if __name__ == "__main__":
    main()
