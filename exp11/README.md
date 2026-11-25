# Experiment 11 - Unit IV

Pandas: Series, DataFrames, groupby, pivot tables, time series

10 scenario questions, each solved in its own section and its own file. Every program below was executed and the real output is included.

[Back to the index](../README.md)

---

## Questions in this experiment

- [Experiment 11 - Question 1: Random Data Generation with Pandas](#experiment-11---question-1-random-data-generation-with-pandas)
- [Experiment 11 - Question 2: Daily Sales Analysis with Pandas](#experiment-11---question-2-daily-sales-analysis-with-pandas)
- [Experiment 11 - Question 3: Stock Price Analysis with Pandas](#experiment-11---question-3-stock-price-analysis-with-pandas)
- [Experiment 11 - Question 4: Matrix Operations with Pandas](#experiment-11---question-4-matrix-operations-with-pandas)
- [Experiment 11 - Question 5: Product Inventory Check with Pandas](#experiment-11---question-5-product-inventory-check-with-pandas)
- [Experiment 11 - Question 6: Weather Dataset Operations with Pandas](#experiment-11---question-6-weather-dataset-operations-with-pandas)
- [Experiment 11 - Question 7: E-commerce Order Analysis with Pandas](#experiment-11---question-7-e-commerce-order-analysis-with-pandas)
- [Experiment 11 - Question 8: Scientific Experiment Data with Pandas](#experiment-11---question-8-scientific-experiment-data-with-pandas)
- [Experiment 11 - Question 9: Medical Data Analysis with Pandas](#experiment-11---question-9-medical-data-analysis-with-pandas)
- [Experiment 11 - Question 10: Electricity Consumption Analysis with Pandas](#experiment-11---question-10-electricity-consumption-analysis-with-pandas)

---

## Experiment 11 - Question 1: Random Data Generation with Pandas

Scenario: A data analyst needs to simulate data for testing.

Task:
  1) Create a Pandas Series of 10 random integers between 1 and 100 and
     display the mean, median and standard deviation.

Rubrics covered:
  * Series creation using random numbers
  * use of statistical functions (mean, median, std)
  * output formatting

Requires: pandas, numpy

**File:** [`q1_random_series_stats.py`](q1_random_series_stats.py) &nbsp;&middot;&nbsp; **Run:** `python q1_random_series_stats.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== the Series ===
sample_01    14
sample_02    13
sample_03    80
sample_04    50
sample_05    60
sample_06    61
sample_07    72
sample_08     3
sample_09    49
sample_10    15

  name   : random_value
  dtype  : int64
  length : 10
  index  : ['sample_01', 'sample_02', 'sample_03', 'sample_04', 'sample_05', 'sample_06', 'sample_07', 'sample_08', 'sample_09', 'sample_10']

=== required statistics ===
  mean               : 41.7000
  median             : 49.5000
  standard deviation : 27.9207  (sample, ddof=1)
  population std     : 26.4879  (ddof=0)

=== describe() gives all of it at once ===
count    10.000000
mean     41.700000
std      27.920721
min       3.000000
25%      14.250000
50%      49.500000
75%      60.750000
max      80.000000

=== more statistics ===
  sum      : 417
  min      : 3  at sample_08
  max      : 80  at sample_03
  range    : 77
  variance : 779.5667
  skew     : -0.1507
  mode     : [3, 13, 14, 15, 49, 50, 60, 61, 72, 80]

=== quartiles ===
  quantile(0.25) : 14.25
  quantile(0.50) : 49.50
  quantile(0.75) : 60.75
  IQR            : 46.50

=== sorted view ===
sample_03    80
sample_07    72
sample_06    61
sample_05    60
sample_04    50
sample_09    49
sample_10    15
sample_01    14
sample_02    13
sample_08     3

=== values above the mean (boolean indexing) ===
sample_03    80
sample_04    50
sample_05    60
sample_06    61
sample_07    72
sample_09    49
  6 of 10 values are above 41.70

=== deviation from the mean ===
           value  deviation  z_score  above_mean
sample_01     14      -27.7   -0.992       False
sample_02     13      -28.7   -1.028       False
sample_03     80       38.3    1.372        True
sample_04     50        8.3    0.297        True
sample_05     60       18.3    0.655        True
sample_06     61       19.3    0.691        True
sample_07     72       30.3    1.085        True
sample_08      3      -38.7   -1.386       False
sample_09     49        7.3    0.261        True
sample_10     15      -26.7   -0.956       False

=== binning with pd.cut ===
  1-25      4  ####
  26-50     2  ##
  51-75     3  ###
  76-100    1  #

=== cumulative statistics ===
           value  cumsum  running_mean  rolling_mean_3
sample_01     14      14         14.00             NaN
sample_02     13      27         13.50             NaN
sample_03     80     107         35.67           35.67
sample_04     50     157         39.25           47.67
sample_05     60     217         43.40           63.33
sample_06     61     278         46.33           57.00
sample_07     72     350         50.00           64.33
sample_08      3     353         44.12           45.33
sample_09     49     402         44.67           41.33
sample_10     15     417         41.70           22.33

=== vectorised transforms ===
  doubled      : [28, 26, 160, 100, 120, 122, 144, 6, 98, 30]
  as percentage: [3.36, 3.12, 19.18, 11.99, 14.39, 14.63, 17.27, 0.72, 11.75, 3.6]
  square roots : [3.742, 3.606, 8.944, 7.071, 7.746, 7.81, 8.485, 1.732, 7.0, 3.873]
  rank         : [8, 9, 1, 5, 4, 3, 2, 10, 6, 7]

=== reproducibility ===
  the same seed gives the same Series: True
  this matters so the lab result can be checked later

```

</details>

---

## Experiment 11 - Question 2: Daily Sales Analysis with Pandas

Scenario: A store records daily sales (in Rs.) for 7 days:
[1200, 1500, 900, 1800, 2100, 1600, 1900].

Task:
  1) Load this into a Pandas Series indexed by weekday.
  2) Find the total sales, average sales and the day with maximum sales.

Note: the question sheet repeats Experiment 10 Question 2 here. Since
Experiment 11 is the Pandas experiment, this solution answers the same
scenario with pandas rather than plain NumPy.

Rubrics covered:
  * Series creation
  * correct use of aggregation functions (sum, mean, idxmax)
  * display of results
  * correct logic

Requires: pandas, numpy

**File:** [`q2_daily_sales_pandas.py`](q2_daily_sales_pandas.py) &nbsp;&middot;&nbsp; **Run:** `python q2_daily_sales_pandas.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 11 - Question 2: Daily Sales Analysis with Pandas

Scenario: A store records daily sales (in Rs.) for 7 days:
[1200, 1500, 900, 1800, 2100, 1600, 1900].

Task:
  1) Load this into a Pandas Series indexed by weekday.
  2) Find the total sales, average sales and the day with maximum sales.

Note: the question sheet repeats Experiment 10 Question 2 here. Since
Experiment 11 is the Pandas experiment, this solution answers the same
scenario with pandas rather than plain NumPy.

Rubrics covered:
  * Series creation
  * correct use of aggregation functions (sum, mean, idxmax)
  * display of results
  * correct logic

Requires: pandas, numpy
"""

import numpy as np
import pandas as pd

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
        "Saturday", "Sunday"]
RAW = [1200, 1500, 900, 1800, 2100, 1600, 1900]


def main():
    sales = pd.Series(RAW, index=DAYS, name="sales_rupees")

    print("=== the Series ===")
    print(sales.to_string())
    print(f"\n  dtype {sales.dtype}, length {len(sales)}")

    total = sales.sum()
    average = sales.mean()
    best_day = sales.idxmax()

    print("\n=== required answers ===")
    print(f"  total sales       : Rs.{total:,}")
    print(f"  average sales     : Rs.{average:,.2f} per day")
    print(f"  maximum sales day : {best_day} (Rs.{sales.max():,})")
    print(f"  idxmax() returns the LABEL, argmax() the position "
          f"({sales.argmax()})")

    print("\n=== describe() ===")
    print(sales.describe().round(2).to_string())

    print("\n=== a DataFrame with derived columns ===")
    frame = pd.DataFrame({"sales": sales})
    frame["share_percent"] = (frame["sales"] / total * 100).round(2)
    frame["vs_average"] = (frame["sales"] - average).round(2)
    frame["cumulative"] = frame["sales"].cumsum()
    frame["change"] = frame["sales"].diff()
    frame["change_percent"] = (frame["sales"].pct_change() * 100).round(1)
    frame["is_weekend"] = frame.index.isin(["Saturday", "Sunday"])
    print(frame.to_string())

    print("\n=== days above the weekly average ===")
    above = sales[sales > average]
    print(above.to_string())
    print(f"  {len(above)} day(s), contributing Rs.{above.sum():,} "
          f"({above.sum() / total * 100:.1f}% of the week)")

    print("\n=== weekday vs weekend (groupby) ===")
    grouped = frame.groupby("is_weekend")["sales"].agg(
        ["count", "sum", "mean", "max"])
    grouped.index = ["Weekday", "Weekend"]
    print(grouped.round(2).to_string())
    uplift = (grouped.loc["Weekend", "mean"] /
              grouped.loc["Weekday", "mean"] - 1) * 100
    print(f"\n  weekend days average {uplift:+.1f}% versus weekdays")

    print("\n=== sorted, ranked ===")
    ranked = pd.DataFrame({
        "sales": sales.sort_values(ascending=False),
    })
    ranked["rank"] = range(1, len(ranked) + 1)
    ranked["gap_to_best"] = ranked["sales"] - ranked["sales"].max()
    print(ranked.to_string())

    print("\n=== rolling 3-day average ===")
    rolling = sales.rolling(window=3).mean().round(2)
    print(rolling.to_string())
    print(f"  best 3-day stretch ends on {rolling.idxmax()} "
          f"(Rs.{rolling.max():,.2f} per day)")

    print("\n=== text bar chart ===")
    for day, amount in sales.items():
        marker = "  <== best" if day == best_day else ""
        print(f"  {day:<11}Rs.{amount:>6,}  "
              f"{'#' * (amount // 100)}{marker}")

    print("\n=== what-if scenarios (vectorised) ===")
    scenarios = pd.DataFrame({
        "actual": sales,
        "plus_10pct": (sales * 1.10).round(0).astype(int),
        "gst_18pct": (sales * 0.18).round(2),
        "after_fixed_cost_300": sales - 300,
    })
    print(scenarios.to_string())
    print(f"\n  profit after Rs.300 daily cost: "
          f"Rs.{scenarios['after_fixed_cost_300'].sum():,}")

    target = 1500
    met = sales >= target
    print(f"\n=== Rs.{target:,} daily target ===")
    print(f"  days met : {int(met.sum())} of 7 "
          f"({met.mean() * 100:.1f}%)")
    print(f"  which    : {sales[met].index.tolist()}")
    print(f"  shortfall on the rest: "
          f"Rs.{int((target - sales[~met]).sum()):,}")

    print("\n=== resampling as a time series ===")
    dated = pd.Series(
        RAW, index=pd.date_range("2026-11-16", periods=7, freq="D"),
        name="sales_rupees")
    print(dated.to_string())
    print(f"\n  weekly total via resample('W'): "
          f"Rs.{int(dated.resample('W').sum().iloc[-1]):,}")
    print(f"  day-of-week labels: "
          f"{dated.index.day_name().tolist()}")


if __name__ == "__main__":
    main()
```

</details>

<details>
<summary>Program output</summary>

```text
=== the Series ===
Monday       1200
Tuesday      1500
Wednesday     900
Thursday     1800
Friday       2100
Saturday     1600
Sunday       1900

  dtype int64, length 7

=== required answers ===
  total sales       : Rs.11,000
  average sales     : Rs.1,571.43 per day
  maximum sales day : Friday (Rs.2,100)
  idxmax() returns the LABEL, argmax() the position (4)

=== describe() ===
count       7.00
mean     1571.43
std       415.19
min       900.00
25%      1350.00
50%      1600.00
75%      1850.00
max      2100.00

=== a DataFrame with derived columns ===
           sales  share_percent  vs_average  cumulative  change  change_percent  is_weekend
Monday      1200          10.91     -371.43        1200     NaN             NaN       False
Tuesday     1500          13.64      -71.43        2700   300.0            25.0       False
Wednesday    900           8.18     -671.43        3600  -600.0           -40.0       False
Thursday    1800          16.36      228.57        5400   900.0           100.0       False
Friday      2100          19.09      528.57        7500   300.0            16.7       False
Saturday    1600          14.55       28.57        9100  -500.0           -23.8        True
Sunday      1900          17.27      328.57       11000   300.0            18.8        True

=== days above the weekly average ===
Thursday    1800
Friday      2100
Saturday    1600
Sunday      1900
  4 day(s), contributing Rs.7,400 (67.3% of the week)

=== weekday vs weekend (groupby) ===
         count   sum    mean   max
Weekday      5  7500  1500.0  2100
Weekend      2  3500  1750.0  1900

  weekend days average +16.7% versus weekdays

=== sorted, ranked ===
           sales  rank  gap_to_best
Friday      2100     1            0
Sunday      1900     2         -200
Thursday    1800     3         -300
Saturday    1600     4         -500
Tuesday     1500     5         -600
Monday      1200     6         -900
Wednesday    900     7        -1200

=== rolling 3-day average ===
Monday           NaN
Tuesday          NaN
Wednesday    1200.00
Thursday     1400.00
Friday       1600.00
Saturday     1833.33
Sunday       1866.67
  best 3-day stretch ends on Sunday (Rs.1,866.67 per day)

=== text bar chart ===
  Monday     Rs. 1,200  ############
  Tuesday    Rs. 1,500  ###############
  Wednesday  Rs.   900  #########
  Thursday   Rs. 1,800  ##################
  Friday     Rs. 2,100  #####################  <== best
  Saturday   Rs. 1,600  ################
  Sunday     Rs. 1,900  ###################

=== what-if scenarios (vectorised) ===
           actual  plus_10pct  gst_18pct  after_fixed_cost_300
Monday       1200        1320      216.0                   900
Tuesday      1500        1650      270.0                  1200
Wednesday     900         990      162.0                   600
Thursday     1800        1980      324.0                  1500
Friday       2100        2310      378.0                  1800
Saturday     1600        1760      288.0                  1300
Sunday       1900        2090      342.0                  1600

  profit after Rs.300 daily cost: Rs.8,900

=== Rs.1,500 daily target ===
  days met : 5 of 7 (71.4%)
  which    : ['Tuesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  shortfall on the rest: Rs.900

=== resampling as a time series ===
2026-11-16    1200
2026-11-17    1500
2026-11-18     900
2026-11-19    1800
2026-11-20    2100
2026-11-21    1600
2026-11-22    1900
Freq: D

  weekly total via resample('W'): Rs.11,000
  day-of-week labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

```

</details>

---

## Experiment 11 - Question 3: Stock Price Analysis with Pandas

Scenario: Closing stock prices for 5 companies over 5 trading days.

Task:
  1) Find the average stock price of each company (row-wise).
  2) Find the day with the highest overall stock price.

Note: the sheet repeats Experiment 10 Question 3 here; this version answers it
with a Pandas DataFrame, which is the topic of Experiment 11.

Rubrics covered:
  * DataFrame handling
  * correct row-wise average (axis=1)
  * highest price logic
  * result display

Requires: pandas, numpy

**File:** [`q3_stock_prices_dataframe.py`](q3_stock_prices_dataframe.py) &nbsp;&middot;&nbsp; **Run:** `python q3_stock_prices_dataframe.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 11 - Question 3: Stock Price Analysis with Pandas

Scenario: Closing stock prices for 5 companies over 5 trading days.

Task:
  1) Find the average stock price of each company (row-wise).
  2) Find the day with the highest overall stock price.

Note: the sheet repeats Experiment 10 Question 3 here; this version answers it
with a Pandas DataFrame, which is the topic of Experiment 11.

Rubrics covered:
  * DataFrame handling
  * correct row-wise average (axis=1)
  * highest price logic
  * result display

Requires: pandas, numpy
"""

import numpy as np
import pandas as pd

COMPANIES = ["TCS", "INFY", "RELIANCE", "HDFCBANK", "WIPRO"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]


def main():
    data = [
        [3850.00, 3920.50, 3870.25, 3990.00, 4015.75],
        [1480.00, 1495.25, 1460.50, 1510.00, 1525.50],
        [2890.50, 2935.00, 2910.75, 2880.25, 2955.00],
        [1620.00, 1605.50, 1640.00, 1655.75, 1648.25],
        [452.00, 448.75, 455.50, 461.00, 458.25],
    ]
    df = pd.DataFrame(data, index=COMPANIES, columns=DAYS)
    df.index.name = "company"
    df.columns.name = "day"

    print("=== the DataFrame ===")
    print(df.to_string())
    print(f"\n  shape {df.shape}, "
          f"{df.size} values, dtypes {df.dtypes.unique().tolist()}")

    print("\n=== info and describe ===")
    print(df.describe().round(2).to_string())

    # 1) row-wise average
    row_avg = df.mean(axis=1)
    print("\n=== 1) average price per company (axis=1) ===")
    print(row_avg.round(2).to_string())

    summary = pd.DataFrame({
        "average": df.mean(axis=1).round(2),
        "low": df.min(axis=1),
        "high": df.max(axis=1),
        "swing": (df.max(axis=1) - df.min(axis=1)).round(2),
        "volatility": df.std(axis=1).round(2),
    })
    print("\n" + summary.to_string())
    print(f"\n  costliest on average : {row_avg.idxmax()} "
          f"(Rs.{row_avg.max():,.2f})")
    print(f"  cheapest on average  : {row_avg.idxmin()} "
          f"(Rs.{row_avg.min():,.2f})")

    # 2) the single highest price anywhere in the frame
    peak_value = df.max().max()
    peak_day = df.max().idxmax()
    peak_company = df[peak_day].idxmax()

    print("\n=== 2) highest overall stock price ===")
    print(f"  df.max()          (per column):")
    print(df.max().round(2).to_string())
    print(f"\n  highest value     : Rs.{peak_value:,.2f}")
    print(f"  company           : {peak_company}")
    print(f"  day               : {peak_day}")
    print(f"  via df.stack().idxmax() : {df.stack().idxmax()}")

    col_total = df.sum(axis=0)
    print("\n=== the day with the highest total market value (axis=0) ===")
    print(col_total.round(2).to_string())
    print(f"\n  strongest day : {col_total.idxmax()} "
          f"(Rs.{col_total.max():,.2f})")
    print(f"  weakest day   : {col_total.idxmin()} "
          f"(Rs.{col_total.min():,.2f})")

    print("\n=== column-wise average (axis=0) ===")
    print(df.mean(axis=0).round(2).to_string())

    print("\n=== weekly return per company ===")
    returns = pd.DataFrame({
        "open": df["Mon"],
        "close": df["Fri"],
        "change": (df["Fri"] - df["Mon"]).round(2),
        "return_percent": ((df["Fri"] / df["Mon"] - 1) * 100).round(2),
    })
    returns["direction"] = np.where(returns["return_percent"] > 0,
                                    "up", "down")
    print(returns.to_string())
    print(f"\n  best performer  : {returns['return_percent'].idxmax()} "
          f"({returns['return_percent'].max():+.2f}%)")
    print(f"  worst performer : {returns['return_percent'].idxmin()} "
          f"({returns['return_percent'].min():+.2f}%)")

    print("\n=== daily percentage change (pct_change across columns) ===")
    daily = (df.pct_change(axis=1) * 100).round(2)
    print(daily.to_string())

    print("\n=== selection and slicing ===")
    print(f"  df.loc['TCS']        :\n{df.loc['TCS'].to_string()}")
    print(f"\n  df['Wed']            :\n{df['Wed'].to_string()}")
    print(f"\n  df.loc['INFY':'RELIANCE', 'Tue':'Thu'] :")
    print(df.loc["INFY":"RELIANCE", "Tue":"Thu"].to_string())
    print(f"\n  df.iloc[0:2, 0:2]    :")
    print(df.iloc[0:2, 0:2].to_string())

    print("\n=== prices above Rs.2,000 (boolean mask) ===")
    mask = df > 2000
    print(mask.to_string())
    stacked = df[mask].stack()
    print(f"\n  {len(stacked)} value(s) above Rs.2,000:")
    print(stacked.round(2).to_string())

    print("\n=== long format with melt, ready for grouping ===")
    long = df.reset_index().melt(id_vars="company", var_name="day",
                                 value_name="price")
    print(long.head(8).to_string(index=False))
    print(f"\n  rows in long format: {len(long)}")

    print("\n=== groupby on the long format ===")
    print(long.groupby("company")["price"].agg(
        ["mean", "min", "max"]).round(2).to_string())
    print()
    print(long.groupby("day")["price"].agg(
        ["sum", "mean"]).round(2).to_string())

    print("\n=== ranking companies by average price ===")
    ranking = row_avg.rank(ascending=False).astype(int).sort_values()
    for company, rank in ranking.items():
        print(f"  {rank}. {company:<10}Rs.{row_avg[company]:>10,.2f}")


if __name__ == "__main__":
    main()
```

</details>

<details>
<summary>Program output</summary>

```text
=== the DataFrame ===
day          Mon      Tue      Wed      Thu      Fri
company                                             
TCS       3850.0  3920.50  3870.25  3990.00  4015.75
INFY      1480.0  1495.25  1460.50  1510.00  1525.50
RELIANCE  2890.5  2935.00  2910.75  2880.25  2955.00
HDFCBANK  1620.0  1605.50  1640.00  1655.75  1648.25
WIPRO      452.0   448.75   455.50   461.00   458.25

  shape (5, 5), 25 values, dtypes [dtype('float64')]

=== info and describe ===
day        Mon      Tue      Wed      Thu      Fri
count     5.00     5.00     5.00     5.00     5.00
mean   2058.50  2081.00  2067.40  2099.40  2120.55
std    1323.77  1355.22  1333.30  1361.31  1380.99
min     452.00   448.75   455.50   461.00   458.25
25%    1480.00  1495.25  1460.50  1510.00  1525.50
50%    1620.00  1605.50  1640.00  1655.75  1648.25
75%    2890.50  2935.00  2910.75  2880.25  2955.00
max    3850.00  3920.50  3870.25  3990.00  4015.75

=== 1) average price per company (axis=1) ===
company
TCS         3929.30
INFY        1494.25
RELIANCE    2914.30
HDFCBANK    1633.90
WIPRO        455.10

          average      low     high   swing  volatility
company                                                
TCS       3929.30  3850.00  4015.75  165.75       72.48
INFY      1494.25  1460.50  1525.50   65.00       25.34
RELIANCE  2914.30  2880.25  2955.00   74.75       30.92
HDFCBANK  1633.90  1605.50  1655.75   50.25       20.74
WIPRO      455.10   448.75   461.00   12.25        4.87

  costliest on average : TCS (Rs.3,929.30)
  cheapest on average  : WIPRO (Rs.455.10)

=== 2) highest overall stock price ===
  df.max()          (per column):
day
Mon    3850.00
Tue    3920.50
Wed    3870.25
Thu    3990.00
Fri    4015.75

  highest value     : Rs.4,015.75
  company           : TCS
  day               : Fri
  via df.stack().idxmax() : ('TCS', 'Fri')

=== the day with the highest total market value (axis=0) ===
day
Mon    10292.50
Tue    10405.00
Wed    10337.00
Thu    10497.00
Fri    10602.75

  strongest day : Fri (Rs.10,602.75)
  weakest day   : Mon (Rs.10,292.50)

=== column-wise average (axis=0) ===
day
Mon    2058.50
Tue    2081.00
Wed    2067.40
Thu    2099.40
Fri    2120.55

=== weekly return per company ===
            open    close  change  return_percent direction
company                                                    
TCS       3850.0  4015.75  165.75            4.31        up
INFY      1480.0  1525.50   45.50            3.07        up
RELIANCE  2890.5  2955.00   64.50            2.23        up
HDFCBANK  1620.0  1648.25   28.25            1.74        up
WIPRO      452.0   458.25    6.25            1.38        up

  best performer  : TCS (+4.31%)
  worst performer : WIPRO (+1.38%)

=== daily percentage change (pct_change across columns) ===
day       Mon   Tue   Wed   Thu   Fri
company                              
TCS       NaN  1.83 -1.28  3.09  0.65
INFY      NaN  1.03 -2.32  3.39  1.03
RELIANCE  NaN  1.54 -0.83 -1.05  2.60
HDFCBANK  NaN -0.90  2.15  0.96 -0.45
WIPRO     NaN -0.72  1.50  1.21 -0.60

=== selection and slicing ===
  df.loc['TCS']        :
day
Mon    3850.00
Tue    3920.50
Wed    3870.25
Thu    3990.00
Fri    4015.75

  df['Wed']            :
company
TCS         3870.25
INFY        1460.50
RELIANCE    2910.75
HDFCBANK    1640.00
WIPRO        455.50

  df.loc['INFY':'RELIANCE', 'Tue':'Thu'] :
day           Tue      Wed      Thu
company                            
INFY      1495.25  1460.50  1510.00
RELIANCE  2935.00  2910.75  2880.25

  df.iloc[0:2, 0:2]    :
day         Mon      Tue
company                 
TCS      3850.0  3920.50
INFY     1480.0  1495.25

=== prices above Rs.2,000 (boolean mask) ===
day         Mon    Tue    Wed    Thu    Fri
company                                    
TCS        True   True   True   True   True
INFY      False  False  False  False  False
RELIANCE   True   True   True   True   True
HDFCBANK  False  False  False  False  False
WIPRO     False  False  False  False  False

  25 value(s) above Rs.2,000:
company   day
TCS       Mon    3850.00
          Tue    3920.50
          Wed    3870.25
          Thu    3990.00
          Fri    4015.75
INFY      Mon        NaN
          Tue        NaN
          Wed        NaN
          Thu        NaN
          Fri        NaN
RELIANCE  Mon    2890.50
          Tue    2935.00
          Wed    2910.75
          Thu    2880.25
          Fri    2955.00
HDFCBANK  Mon        NaN
          Tue        NaN
          Wed        NaN
          Thu        NaN
          Fri        NaN
WIPRO     Mon        NaN
          Tue        NaN
          Wed        NaN
          Thu        NaN
          Fri        NaN

... output truncated, run the file to see the rest.
```

</details>

---

## Experiment 11 - Question 4: Matrix Operations with Pandas

Scenario: Two 3x3 matrices represent transformations.

Task:
  1) Perform addition, subtraction and matrix multiplication between them.

Note: the sheet repeats Experiment 10 Question 4 here; this version uses
Pandas DataFrames, which is the topic of Experiment 11. It also shows where
Pandas aligns on labels and NumPy does not.

Rubrics covered:
  * DataFrame creation
  * element-wise operations
  * matrix multiplication (DataFrame.dot / @)
  * correct results

Requires: pandas, numpy

**File:** [`q4_matrix_dataframe_ops.py`](q4_matrix_dataframe_ops.py) &nbsp;&middot;&nbsp; **Run:** `python q4_matrix_dataframe_ops.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 11 - Question 4: Matrix Operations with Pandas

Scenario: Two 3x3 matrices represent transformations.

Task:
  1) Perform addition, subtraction and matrix multiplication between them.

Note: the sheet repeats Experiment 10 Question 4 here; this version uses
Pandas DataFrames, which is the topic of Experiment 11. It also shows where
Pandas aligns on labels and NumPy does not.

Rubrics covered:
  * DataFrame creation
  * element-wise operations
  * matrix multiplication (DataFrame.dot / @)
  * correct results

Requires: pandas, numpy
"""

import numpy as np
import pandas as pd

LABELS = ["r0", "r1", "r2"]
COLS = ["c0", "c1", "c2"]


def main():
    A = pd.DataFrame([[2, 0, 1],
                      [1, 3, 2],
                      [4, 1, 0]], index=LABELS, columns=COLS)

    B = pd.DataFrame([[1, 2, 0],
                      [0, 1, 3],
                      [2, 1, 1]], index=LABELS, columns=COLS)

    print("=== matrix A ===")
    print(A.to_string())
    print("\n=== matrix B ===")
    print(B.to_string())
    print(f"\n  shapes {A.shape} and {B.shape}, dtype {A.dtypes.iloc[0]}")

    print("\n=== 1) addition (element-wise, label aligned) ===")
    print((A + B).to_string())
    print(f"\n  A.add(B) gives the same: "
          f"{(A + B).equals(A.add(B))}")

    print("\n=== 2) subtraction ===")
    print("A - B")
    print((A - B).to_string())
    print("\nB - A")
    print((B - A).to_string())
    print(f"\n  not commutative: {not (A - B).equals(B - A)}")

    print("\n=== 3) matrix multiplication ===")
    # dot() needs A's columns to line up with B's index
    B_aligned = B.copy()
    B_aligned.index = COLS                 # c0, c1, c2 so A.columns match
    product = A.dot(B_aligned)
    print("A.dot(B)  (B re-indexed so A.columns match B.index)")
    print(product.to_string())
    print(f"\n  the @ operator does the same: "
          f"{(A @ B_aligned).equals(product)}")
    print(f"  NumPy agrees: "
          f"{np.array_equal(product.to_numpy(), A.to_numpy() @ B.to_numpy())}")

    print("\n  how one cell is computed:")
    row, col = A.iloc[0], B_aligned.iloc[:, 0]
    terms = " + ".join(f"{a}*{b}" for a, b in zip(row, col))
    print(f"    A.loc['r0'] . B[:, 'c0'] = {terms} = {product.iloc[0, 0]}")

    print("\n=== element-wise multiplication is different ===")
    print((A * B).to_string())
    print(f"\n  A * B equals A.dot(B): "
          f"{(A * B).to_numpy().tolist() == product.to_numpy().tolist()}")

    print("\n=== transpose ===")
    print(A.T.to_string())

    print("\n=== linear algebra via NumPy on the underlying values ===")
    a_np = A.to_numpy()
    print(f"  trace       : {np.trace(a_np)}")
    print(f"  determinant : {np.linalg.det(a_np):.4f}")
    print(f"  rank        : {np.linalg.matrix_rank(a_np)}")
    if abs(np.linalg.det(a_np)) > 1e-9:
        inv = pd.DataFrame(np.linalg.inv(a_np), index=LABELS, columns=COLS)
        print("\n  inverse of A:")
        print(inv.round(4).to_string())
        identity = A.dot(pd.DataFrame(np.linalg.inv(a_np),
                                      index=COLS, columns=COLS))
        print("\n  A @ inv(A):")
        print(identity.round(10).to_string())
        print(f"  is the identity: "
              f"{np.allclose(identity.to_numpy(), np.eye(3))}")

    print("\n=== scalar operations ===")
    print("A * 3")
    print((A * 3).to_string())
    print("\nA ** 2 (element-wise)")
    print((A ** 2).to_string())

    print("\n=== Pandas aggregations the raw array does not label ===")
    print(f"  column sums  :\n{A.sum(axis=0).to_string()}")
    print(f"\n  row sums     :\n{A.sum(axis=1).to_string()}")
    print(f"\n  column means :\n{A.mean(axis=0).round(4).to_string()}")
    print(f"\n  describe():")
    print(A.describe().round(3).to_string())

    print("\n=== label alignment: the real difference from NumPy ===")
    C = pd.DataFrame([[1, 1], [1, 1]], index=["r0", "r9"],
                     columns=["c0", "c9"])
    print("  C (different labels):")
    print(C.to_string())
    print("\n  A + C aligns on labels and fills the gaps with NaN:")
    print((A + C).to_string())
    print("\n  A.add(C, fill_value=0) treats the missing entries as zero:")
    print(A.add(C, fill_value=0).to_string())
    print("\n  NumPy would simply refuse: shapes (3,3) and (2,2) do not"
          " broadcast.")

    print("\n=== applying the transformation to a vector ===")
    v = pd.Series([1, 2, 3], index=COLS, name="v")
    print(f"  v        :\n{v.to_string()}")
    print(f"\n  A.dot(v) :\n{A.dot(v).to_string()}")


if __name__ == "__main__":
    main()
```

</details>

<details>
<summary>Program output</summary>

```text
=== matrix A ===
    c0  c1  c2
r0   2   0   1
r1   1   3   2
r2   4   1   0

=== matrix B ===
    c0  c1  c2
r0   1   2   0
r1   0   1   3
r2   2   1   1

  shapes (3, 3) and (3, 3), dtype int64

=== 1) addition (element-wise, label aligned) ===
    c0  c1  c2
r0   3   2   1
r1   1   4   5
r2   6   2   1

  A.add(B) gives the same: True

=== 2) subtraction ===
A - B
    c0  c1  c2
r0   1  -2   1
r1   1   2  -1
r2   2   0  -1

B - A
    c0  c1  c2
r0  -1   2  -1
r1  -1  -2   1
r2  -2   0   1

  not commutative: True

=== 3) matrix multiplication ===
A.dot(B)  (B re-indexed so A.columns match B.index)
    c0  c1  c2
r0   4   5   1
r1   5   7  11
r2   4   9   3

  the @ operator does the same: True
  NumPy agrees: True

  how one cell is computed:
    A.loc['r0'] . B[:, 'c0'] = 2*1 + 0*0 + 1*2 = 4

=== element-wise multiplication is different ===
    c0  c1  c2
r0   2   0   0
r1   0   3   6
r2   8   1   0

  A * B equals A.dot(B): False

=== transpose ===
    r0  r1  r2
c0   2   1   4
c1   0   3   1
c2   1   2   0

=== linear algebra via NumPy on the underlying values ===
  trace       : 5
  determinant : -15.0000
  rank        : 3

  inverse of A:
        c0      c1   c2
r0  0.1333 -0.0667  0.2
r1 -0.5333  0.2667  0.2
r2  0.7333  0.1333 -0.4

  A @ inv(A):
     c0   c1   c2
r0  1.0 -0.0  0.0
r1  0.0  1.0  0.0
r2  0.0  0.0  1.0
  is the identity: True

=== scalar operations ===
A * 3
    c0  c1  c2
r0   6   0   3
r1   3   9   6
r2  12   3   0

A ** 2 (element-wise)
    c0  c1  c2
r0   4   0   1
r1   1   9   4
r2  16   1   0

=== Pandas aggregations the raw array does not label ===
  column sums  :
c0    7
c1    4
c2    3

  row sums     :
r0    3
r1    6
r2    5

  column means :
c0    2.3333
c1    1.3333
c2    1.0000

  describe():
          c0     c1   c2
count  3.000  3.000  3.0
mean   2.333  1.333  1.0
std    1.528  1.528  1.0
min    1.000  0.000  0.0
25%    1.500  0.500  0.5
50%    2.000  1.000  1.0
75%    3.000  2.000  1.5
max    4.000  3.000  2.0

=== label alignment: the real difference from NumPy ===
  C (different labels):
    c0  c9
r0   1   1
r9   1   1

  A + C aligns on labels and fills the gaps with NaN:
     c0  c1  c2  c9
r0  3.0 NaN NaN NaN
r1  NaN NaN NaN NaN
r2  NaN NaN NaN NaN
r9  NaN NaN NaN NaN

  A.add(C, fill_value=0) treats the missing entries as zero:
     c0   c1   c2   c9
r0  3.0  0.0  1.0  1.0
r1  1.0  3.0  2.0  NaN
r2  4.0  1.0  0.0  NaN
r9  1.0  NaN  NaN  1.0

  NumPy would simply refuse: shapes (3,3) and (2,2) do not broadcast.

=== applying the transformation to a vector ===
  v        :
c0    1
c1    2
c2    3

  A.dot(v) :
r0     5
r1    13
r2     6

```

</details>

---

## Experiment 11 - Question 5: Product Inventory Check with Pandas

Scenario: A shop records the number of products sold in 4 categories across
5 days.

Task:
  1) Represent this as a DataFrame.
  2) Find the total items sold per category and per day.

Note: the sheet repeats Experiment 10 Question 5 here; this version answers it
with Pandas, the topic of Experiment 11.

Rubrics covered:
  * DataFrame creation
  * row-wise and column-wise sum (axis=1, axis=0)
  * clear display of both results
  * accuracy

Requires: pandas, numpy

**File:** [`q5_inventory_dataframe.py`](q5_inventory_dataframe.py) &nbsp;&middot;&nbsp; **Run:** `python q5_inventory_dataframe.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 11 - Question 5: Product Inventory Check with Pandas

Scenario: A shop records the number of products sold in 4 categories across
5 days.

Task:
  1) Represent this as a DataFrame.
  2) Find the total items sold per category and per day.

Note: the sheet repeats Experiment 10 Question 5 here; this version answers it
with Pandas, the topic of Experiment 11.

Rubrics covered:
  * DataFrame creation
  * row-wise and column-wise sum (axis=1, axis=0)
  * clear display of both results
  * accuracy

Requires: pandas, numpy
"""

import pandas as pd

CATEGORIES = ["Medicines", "Devices", "Protective", "Supplements"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]


def main():
    sold = pd.DataFrame(
        [[142, 158, 131, 177, 190],
         [18, 22, 15, 27, 31],
         [64, 71, 58, 83, 92],
         [35, 41, 29, 46, 52]],
        index=CATEGORIES, columns=DAYS)
    sold.index.name = "category"
    sold.columns.name = "day"

    print("=== the DataFrame ===")
    print(sold.to_string())
    print(f"\n  shape {sold.shape}, {sold.size} values")

    per_category = sold.sum(axis=1)     # collapse days
    per_day = sold.sum(axis=0)          # collapse categories
    grand_total = sold.to_numpy().sum()

    print("\n=== 1) total per category (axis=1) ===")
    print(per_category.to_string())

    cat_summary = pd.DataFrame({
        "total": per_category,
        "daily_avg": sold.mean(axis=1).round(1),
        "best_day": sold.idxmax(axis=1),
        "peak": sold.max(axis=1),
        "share_percent": (per_category / grand_total * 100).round(1),
    })
    print("\n" + cat_summary.to_string())

    print("\n=== 2) total per day (axis=0) ===")
    print(per_day.to_string())

    day_summary = pd.DataFrame({
        "total": per_day,
        "category_avg": sold.mean(axis=0).round(1),
        "top_category": sold.idxmax(axis=0),
        "share_percent": (per_day / grand_total * 100).round(1),
    })
    print("\n" + day_summary.to_string())

    print("\n=== cross-check ===")
    print(f"  grand total              : {grand_total:,}")
    print(f"  sum of category totals   : {per_category.sum():,}")
    print(f"  sum of day totals        : {per_day.sum():,}")
    print(f"  all three agree          : "
          f"{grand_total == per_category.sum() == per_day.sum()}")

    print("\n=== table with margins (the Pandas way) ===")
    with_margins = sold.copy()
    with_margins["TOTAL"] = per_category
    with_margins.loc["TOTAL"] = with_margins.sum(axis=0)
    print(with_margins.to_string())

    print("\n=== highlights ===")
    print(f"  best-selling category : {per_category.idxmax()} "
          f"({per_category.max():,} units)")
    print(f"  slowest category      : {per_category.idxmin()} "
          f"({per_category.min():,} units)")
    print(f"  busiest day           : {per_day.idxmax()} "
          f"({per_day.max():,} units)")
    print(f"  quietest day          : {per_day.idxmin()} "
          f"({per_day.min():,} units)")
    peak = sold.stack().idxmax()
    print(f"  single biggest cell   : {peak[0]} on {peak[1]} "
          f"({sold.stack().max()} units)")

    print("\n=== percentage of each day's sales, by category ===")
    share = (sold / per_day * 100).round(1)
    print(share.to_string())

    print("\n=== day-on-day change, whole shop ===")
    change = pd.DataFrame({
        "total": per_day,
        "change": per_day.diff(),
        "change_percent": (per_day.pct_change() * 100).round(1),
    })
    print(change.to_string())

    print("\n=== cumulative sales through the week ===")
    print(sold.cumsum(axis=1).to_string())

    print("\n=== long format and groupby ===")
    long = sold.reset_index().melt(id_vars="category", var_name="day",
                                   value_name="units")
    print(long.head(6).to_string(index=False))
    print(f"\n  rows: {len(long)}")
    print("\n  groupby category:")
    print(long.groupby("category")["units"].agg(
        ["sum", "mean", "max"]).round(1).to_string())
    print("\n  groupby day:")
    print(long.groupby("day", sort=False)["units"].agg(
        ["sum", "mean"]).round(1).to_string())

    print("\n=== pivot_table reproduces the original layout ===")
    pivot = long.pivot_table(index="category", columns="day",
                             values="units", aggfunc="sum")
    pivot = pivot[DAYS]
    print(pivot.to_string())
    print(f"  identical to the source frame: "
          f"{pivot.equals(sold)}")

    print("\n=== restocking signal: categories averaging over 50 a day ===")
    avg = sold.mean(axis=1)
    for name, value in avg[avg > 50].items():
        print(f"  {name:<13}{value:>6.1f} units/day -> order "
              f"{int(round(value * 7))} for next week")

    print("\n=== text bar chart of category totals ===")
    for name, total in per_category.sort_values(ascending=False).items():
        print(f"  {name:<13}{total:>6,}  {'#' * (total // 25)}")


if __name__ == "__main__":
    main()
```

</details>

<details>
<summary>Program output</summary>

```text
=== the DataFrame ===
day          Mon  Tue  Wed  Thu  Fri
category                            
Medicines    142  158  131  177  190
Devices       18   22   15   27   31
Protective    64   71   58   83   92
Supplements   35   41   29   46   52

  shape (4, 5), 20 values

=== 1) total per category (axis=1) ===
category
Medicines      798
Devices        113
Protective     368
Supplements    203

             total  daily_avg best_day  peak  share_percent
category                                                   
Medicines      798      159.6      Fri   190           53.8
Devices        113       22.6      Fri    31            7.6
Protective     368       73.6      Fri    92           24.8
Supplements    203       40.6      Fri    52           13.7

=== 2) total per day (axis=0) ===
day
Mon    259
Tue    292
Wed    233
Thu    333
Fri    365

     total  category_avg top_category  share_percent
day                                                 
Mon    259          64.8    Medicines           17.5
Tue    292          73.0    Medicines           19.7
Wed    233          58.2    Medicines           15.7
Thu    333          83.2    Medicines           22.5
Fri    365          91.2    Medicines           24.6

=== cross-check ===
  grand total              : 1,482
  sum of category totals   : 1,482
  sum of day totals        : 1,482
  all three agree          : True

=== table with margins (the Pandas way) ===
day          Mon  Tue  Wed  Thu  Fri  TOTAL
category                                   
Medicines    142  158  131  177  190    798
Devices       18   22   15   27   31    113
Protective    64   71   58   83   92    368
Supplements   35   41   29   46   52    203
TOTAL        259  292  233  333  365   1482

=== highlights ===
  best-selling category : Medicines (798 units)
  slowest category      : Devices (113 units)
  busiest day           : Fri (365 units)
  quietest day          : Wed (233 units)
  single biggest cell   : Medicines on Fri (190 units)

=== percentage of each day's sales, by category ===
day           Mon   Tue   Wed   Thu   Fri
category                                 
Medicines    54.8  54.1  56.2  53.2  52.1
Devices       6.9   7.5   6.4   8.1   8.5
Protective   24.7  24.3  24.9  24.9  25.2
Supplements  13.5  14.0  12.4  13.8  14.2

=== day-on-day change, whole shop ===
     total  change  change_percent
day                               
Mon    259     NaN             NaN
Tue    292    33.0            12.7
Wed    233   -59.0           -20.2
Thu    333   100.0            42.9
Fri    365    32.0             9.6

=== cumulative sales through the week ===
day          Mon  Tue  Wed  Thu  Fri
category                            
Medicines    142  300  431  608  798
Devices       18   40   55   82  113
Protective    64  135  193  276  368
Supplements   35   76  105  151  203

=== long format and groupby ===
   category day  units
  Medicines Mon    142
    Devices Mon     18
 Protective Mon     64
Supplements Mon     35
  Medicines Tue    158
    Devices Tue     22

  rows: 20

  groupby category:
             sum   mean  max
category                    
Devices      113   22.6   31
Medicines    798  159.6  190
Protective   368   73.6   92
Supplements  203   40.6   52

  groupby day:
     sum  mean
day           
Mon  259  64.8
Tue  292  73.0
Wed  233  58.2
Thu  333  83.2
Fri  365  91.2

=== pivot_table reproduces the original layout ===
day          Mon  Tue  Wed  Thu  Fri
category                            
Devices       18   22   15   27   31
Medicines    142  158  131  177  190
Protective    64   71   58   83   92
Supplements   35   41   29   46   52
  identical to the source frame: False

=== restocking signal: categories averaging over 50 a day ===
  Medicines     159.6 units/day -> order 1117 for next week
  Protective     73.6 units/day -> order 515 for next week

=== text bar chart of category totals ===
  Medicines       798  ###############################
  Protective      368  ##############
  Supplements     203  ########
  Devices         113  ####

```

</details>

---

## Experiment 11 - Question 6: Weather Dataset Operations with Pandas

Scenario: Rainfall data (in mm) for 12 months.

Task:
  1) Compute the total and average annual rainfall.
  2) Identify the months with rainfall above 100 mm.

Note: the sheet repeats Experiment 10 Question 6 here; this version answers it
with Pandas, the topic of Experiment 11.

Rubrics covered:
  * Series handling
  * use of aggregation functions (sum, mean)
  * boolean indexing (> 100)
  * correct output

Requires: pandas, numpy

**File:** [`q6_rainfall_pandas.py`](q6_rainfall_pandas.py) &nbsp;&middot;&nbsp; **Run:** `python q6_rainfall_pandas.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 11 - Question 6: Weather Dataset Operations with Pandas

Scenario: Rainfall data (in mm) for 12 months.

Task:
  1) Compute the total and average annual rainfall.
  2) Identify the months with rainfall above 100 mm.

Note: the sheet repeats Experiment 10 Question 6 here; this version answers it
with Pandas, the topic of Experiment 11.

Rubrics covered:
  * Series handling
  * use of aggregation functions (sum, mean)
  * boolean indexing (> 100)
  * correct output

Requires: pandas, numpy
"""

import numpy as np
import pandas as pd

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
THRESHOLD = 100.0


def main():
    rainfall = pd.Series(
        [2.5, 1.0, 3.5, 12.0, 38.5, 142.0, 187.5, 164.0, 128.5, 74.0,
         21.5, 6.0],
        index=MONTHS, name="rainfall_mm")
    rainfall.index.name = "month"

    print("=== the Series ===")
    print(rainfall.to_string())
    print(f"\n  dtype {rainfall.dtype}, {len(rainfall)} months")

    total = rainfall.sum()
    average = rainfall.mean()

    print("\n=== 1) annual totals ===")
    print(f"  total annual rainfall    : {total:,.1f} mm")
    print(f"  average monthly rainfall : {average:,.2f} mm")
    print(f"  median                   : {rainfall.median():,.2f} mm")
    print(f"  standard deviation       : {rainfall.std():,.2f} mm")
    print(f"  wettest month            : {rainfall.idxmax()} "
          f"({rainfall.max():,.1f} mm)")
    print(f"  driest month             : {rainfall.idxmin()} "
          f"({rainfall.min():,.1f} mm)")

    print("\n=== describe() ===")
    print(rainfall.describe().round(2).to_string())

    print("\n=== monthly frame with derived columns ===")
    frame = pd.DataFrame({"rainfall_mm": rainfall})
    frame["share_percent"] = (frame["rainfall_mm"] / total * 100).round(1)
    frame["cumulative_mm"] = frame["rainfall_mm"].cumsum()
    frame["change"] = frame["rainfall_mm"].diff()
    frame["above_threshold"] = frame["rainfall_mm"] > THRESHOLD
    frame["category"] = pd.cut(
        frame["rainfall_mm"],
        bins=[-0.01, 10, 50, 100, 150, np.inf],
        labels=["negligible", "light", "moderate", "heavy", "very heavy"])
    print(frame.to_string())

    # 2) boolean indexing
    heavy = rainfall[rainfall > THRESHOLD]

    print(f"\n=== 2) months above {THRESHOLD:.0f} mm ===")
    print(heavy.to_string())
    print(f"\n  count          : {len(heavy)} of {len(rainfall)}")
    print(f"  months         : {heavy.index.tolist()}")
    print(f"  combined total : {heavy.sum():,.1f} mm "
          f"({heavy.sum() / total * 100:.1f}% of the annual rainfall)")
    print(f"  their average  : {heavy.mean():,.2f} mm")
    for month, mm in heavy.items():
        print(f"    {month:<5}{mm:>8.1f} mm  "
              f"({mm - THRESHOLD:+.1f} mm above the threshold)")

    print("\n=== how the count changes with the threshold ===")
    for t in (50, 75, 100, 125, 150, 175):
        picked = rainfall[rainfall > t]
        print(f"  above {t:>3} mm : {len(picked)} month(s)  "
              f"{picked.index.tolist()}")

    print("\n=== quarterly split (groupby) ===")
    quarter_map = {m: f"Q{i // 3 + 1}" for i, m in enumerate(MONTHS)}
    by_quarter = rainfall.groupby(rainfall.index.map(quarter_map)).agg(
        ["sum", "mean", "max"]).round(2)
    by_quarter["share_percent"] = (by_quarter["sum"] / total * 100).round(1)
    print(by_quarter.to_string())
    print(f"\n  wettest quarter : {by_quarter['sum'].idxmax()} "
          f"({by_quarter['sum'].max():,.1f} mm)")

    print("\n=== monsoon (Jun-Sep) vs the rest of the year ===")
    is_monsoon = rainfall.index.isin(["Jun", "Jul", "Aug", "Sep"])
    monsoon = rainfall[is_monsoon]
    rest = rainfall[~is_monsoon]
    season = pd.DataFrame({
        "months": [len(monsoon), len(rest)],
        "total_mm": [monsoon.sum(), rest.sum()],
        "avg_mm": [monsoon.mean().round(2), rest.mean().round(2)],
        "share_percent": [round(monsoon.sum() / total * 100, 1),
                          round(rest.sum() / total * 100, 1)],
    }, index=["Monsoon Jun-Sep", "Rest of year"])
    print(season.to_string())

    print("\n=== 3-month rolling average ===")
    rolling = rainfall.rolling(window=3).mean().round(2)
    print(rolling.to_string())
    print(f"\n  wettest 3-month window ends in {rolling.idxmax()} "
          f"({rolling.max():.2f} mm/month)")

    print("\n=== category counts ===")
    counts = frame["category"].value_counts().sort_index()
    for label, n in counts.items():
        print(f"  {str(label):<12}{n:>3} month(s)  {'#' * n}")

    print("\n=== rank and sort ===")
    ranked = pd.DataFrame({
        "rainfall_mm": rainfall.sort_values(ascending=False),
    })
    ranked["rank"] = range(1, len(ranked) + 1)
    print(ranked.to_string())

    print("\n=== text chart ===")
    for month, mm in rainfall.items():
        flag = "  <== above 100 mm" if mm > THRESHOLD else ""
        print(f"  {month:<5}{mm:>8.1f}  {'#' * int(mm / 4)}{flag}")

    print("\n=== as a proper time series ===")
    dated = pd.Series(
        rainfall.to_numpy(),
        index=pd.date_range("2026-01-31", periods=12, freq="ME"),
        name="rainfall_mm")
    print(f"  quarterly resample:")
    print(dated.resample("QE").sum().round(1).to_string())


if __name__ == "__main__":
    main()
```

</details>

<details>
<summary>Program output</summary>

```text
=== the Series ===
month
Jan      2.5
Feb      1.0
Mar      3.5
Apr     12.0
May     38.5
Jun    142.0
Jul    187.5
Aug    164.0
Sep    128.5
Oct     74.0
Nov     21.5
Dec      6.0

  dtype float64, 12 months

=== 1) annual totals ===
  total annual rainfall    : 781.0 mm
  average monthly rainfall : 65.08 mm
  median                   : 30.00 mm
  standard deviation       : 71.04 mm
  wettest month            : Jul (187.5 mm)
  driest month             : Feb (1.0 mm)

=== describe() ===
count     12.00
mean      65.08
std       71.04
min        1.00
25%        5.38
50%       30.00
75%      131.88
max      187.50

=== monthly frame with derived columns ===
       rainfall_mm  share_percent  cumulative_mm  change  above_threshold    category
month                                                                                
Jan            2.5            0.3            2.5     NaN            False  negligible
Feb            1.0            0.1            3.5    -1.5            False  negligible
Mar            3.5            0.4            7.0     2.5            False  negligible
Apr           12.0            1.5           19.0     8.5            False       light
May           38.5            4.9           57.5    26.5            False       light
Jun          142.0           18.2          199.5   103.5             True       heavy
Jul          187.5           24.0          387.0    45.5             True  very heavy
Aug          164.0           21.0          551.0   -23.5             True  very heavy
Sep          128.5           16.5          679.5   -35.5             True       heavy
Oct           74.0            9.5          753.5   -54.5            False    moderate
Nov           21.5            2.8          775.0   -52.5            False       light
Dec            6.0            0.8          781.0   -15.5            False  negligible

=== 2) months above 100 mm ===
month
Jun    142.0
Jul    187.5
Aug    164.0
Sep    128.5

  count          : 4 of 12
  months         : ['Jun', 'Jul', 'Aug', 'Sep']
  combined total : 622.0 mm (79.6% of the annual rainfall)
  their average  : 155.50 mm
    Jun     142.0 mm  (+42.0 mm above the threshold)
    Jul     187.5 mm  (+87.5 mm above the threshold)
    Aug     164.0 mm  (+64.0 mm above the threshold)
    Sep     128.5 mm  (+28.5 mm above the threshold)

=== how the count changes with the threshold ===
  above  50 mm : 5 month(s)  ['Jun', 'Jul', 'Aug', 'Sep', 'Oct']
  above  75 mm : 4 month(s)  ['Jun', 'Jul', 'Aug', 'Sep']
  above 100 mm : 4 month(s)  ['Jun', 'Jul', 'Aug', 'Sep']
  above 125 mm : 4 month(s)  ['Jun', 'Jul', 'Aug', 'Sep']
  above 150 mm : 2 month(s)  ['Jul', 'Aug']
  above 175 mm : 1 month(s)  ['Jul']

=== quarterly split (groupby) ===
         sum    mean    max  share_percent
month                                     
Q1       7.0    2.33    3.5            0.9
Q2     192.5   64.17  142.0           24.6
Q3     480.0  160.00  187.5           61.5
Q4     101.5   33.83   74.0           13.0

  wettest quarter : Q3 (480.0 mm)

=== monsoon (Jun-Sep) vs the rest of the year ===
                 months  total_mm  avg_mm  share_percent
Monsoon Jun-Sep       4     622.0  155.50           79.6
Rest of year          8     159.0   19.88           20.4

=== 3-month rolling average ===
month
Jan       NaN
Feb       NaN
Mar      2.33
Apr      5.50
May     18.00
Jun     64.17
Jul    122.67
Aug    164.50
Sep    160.00
Oct    122.17
Nov     74.67
Dec     33.83

  wettest 3-month window ends in Aug (164.50 mm/month)

=== category counts ===
  negligible    4 month(s)  ####
  light         3 month(s)  ###
  moderate      1 month(s)  #
  heavy         2 month(s)  ##
  very heavy    2 month(s)  ##

=== rank and sort ===
       rainfall_mm  rank
month                   
Jul          187.5     1
Aug          164.0     2
Jun          142.0     3
Sep          128.5     4
Oct           74.0     5
May           38.5     6
Nov           21.5     7
Apr           12.0     8
Dec            6.0     9
Mar            3.5    10
Jan            2.5    11
Feb            1.0    12

=== text chart ===
  Jan       2.5  
  Feb       1.0  
  Mar       3.5  
  Apr      12.0  ###
  May      38.5  #########
  Jun     142.0  ###################################  <== above 100 mm
  Jul     187.5  ##############################################  <== above 100 mm
  Aug     164.0  #########################################  <== above 100 mm
  Sep     128.5  ################################  <== above 100 mm
  Oct      74.0  ##################
  Nov      21.5  #####
  Dec       6.0  #

=== as a proper time series ===
  quarterly resample:
2026-03-31      7.0
2026-06-30    192.5
2026-09-30    480.0
2026-12-31    101.5
Freq: QE-DEC

```

</details>

---

## Experiment 11 - Question 7: E-commerce Order Analysis with Pandas

Scenario: An e-commerce company stores order amounts.

Task:
  1) Find how many orders are above Rs.1000.
  2) Calculate the percentage of such orders.

Note: the sheet repeats Experiment 10 Question 7 here; this version answers it
with Pandas, the topic of Experiment 11.

Rubrics covered:
  * Series / DataFrame creation
  * boolean condition (> 1000)
  * percentage calculation
  * correct output

Requires: pandas, numpy

**File:** [`q7_orders_pandas.py`](q7_orders_pandas.py) &nbsp;&middot;&nbsp; **Run:** `python q7_orders_pandas.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 11 - Question 7: E-commerce Order Analysis with Pandas

Scenario: An e-commerce company stores order amounts.

Task:
  1) Find how many orders are above Rs.1000.
  2) Calculate the percentage of such orders.

Note: the sheet repeats Experiment 10 Question 7 here; this version answers it
with Pandas, the topic of Experiment 11.

Rubrics covered:
  * Series / DataFrame creation
  * boolean condition (> 1000)
  * percentage calculation
  * correct output

Requires: pandas, numpy
"""

import numpy as np
import pandas as pd

THRESHOLD = 1000
CITIES = ["Pune", "Mumbai", "Nashik", "Nagpur"]
CHANNELS = ["app", "web"]


def main():
    rng = np.random.default_rng(seed=2026)
    n = 40
    orders = pd.DataFrame({
        "order_id": [f"ORD-{i:04d}" for i in range(1, n + 1)],
        "amount": np.round(rng.lognormal(mean=6.4, sigma=0.9, size=n), 2),
        "city": rng.choice(CITIES, size=n),
        "channel": rng.choice(CHANNELS, size=n, p=[0.65, 0.35]),
    }).set_index("order_id")

    print("=== the DataFrame (first 10 rows) ===")
    print(orders.head(10).to_string())
    print(f"\n  rows {len(orders)}, columns {list(orders.columns)}")
    print(f"  dtypes:\n{orders.dtypes.to_string()}")

    amount = orders["amount"]

    # 1) count with a boolean mask
    mask = amount > THRESHOLD
    count = int(mask.sum())
    # 2) percentage
    percent = mask.mean() * 100

    print(f"\n=== 1) orders above Rs.{THRESHOLD:,} ===")
    print(f"  condition : orders['amount'] > {THRESHOLD}")
    print(f"  count     : {count}")
    print(f"  order ids : {amount[mask].index.tolist()}")

    print(f"\n=== 2) percentage of such orders ===")
    print(f"  {count} / {len(orders)} x 100 = {percent:.2f}%")
    print(f"  mask.mean() * 100 gives the same : {mask.mean() * 100:.2f}%")

    high_value = amount[mask]
    print("\n=== revenue contribution ===")
    print(f"  total revenue           : Rs.{amount.sum():,.2f}")
    print(f"  revenue above Rs.{THRESHOLD:,}  : Rs.{high_value.sum():,.2f}")
    print(f"  share of revenue        : "
          f"{high_value.sum() / amount.sum() * 100:.2f}%")
    print(f"  so {percent:.1f}% of orders bring "
          f"{high_value.sum() / amount.sum() * 100:.1f}% of the money")

    print("\n=== the high-value orders ===")
    print(orders[mask].sort_values("amount", ascending=False).to_string())

    print("\n=== describe() ===")
    print(amount.describe().round(2).to_string())
    print(f"\n  the mean (Rs.{amount.mean():,.2f}) sits above the median "
          f"(Rs.{amount.median():,.2f}):")
    print("  the long tail of large orders pulls the mean up")

    print("\n=== percentiles ===")
    for p in (0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99):
        print(f"  p{int(p * 100):<3} : Rs.{amount.quantile(p):>11,.2f}")

    print("\n=== how the answer moves with the threshold ===")
    rows = []
    for t in (250, 500, 750, 1000, 1500, 2000, 3000):
        m = amount > t
        rows.append({
            "threshold": t,
            "orders": int(m.sum()),
            "percent_orders": round(m.mean() * 100, 2),
            "percent_revenue": round(
                amount[m].sum() / amount.sum() * 100, 2) if m.any() else 0.0,
        })
    print(pd.DataFrame(rows).set_index("threshold").to_string())

    print("\n=== order size bands (pd.cut) ===")
    bands = pd.cut(amount,
                   bins=[0, 250, 500, 1000, 2000, 5000, np.inf],
                   labels=["0-250", "250-500", "500-1000", "1000-2000",
                           "2000-5000", "5000+"])
    band_summary = pd.DataFrame({
        "orders": bands.value_counts().sort_index(),
        "revenue": amount.groupby(bands, observed=False).sum().round(2),
    })
    band_summary["percent_orders"] = (
        band_summary["orders"] / len(orders) * 100).round(1)
    print(band_summary.to_string())

    print("\n=== by city (groupby) ===")
    by_city = orders.groupby("city")["amount"].agg(
        ["count", "sum", "mean", "max"]).round(2)
    by_city["high_value_orders"] = orders[mask].groupby("city")["amount"]\
        .count().reindex(by_city.index).fillna(0).astype(int)
    by_city["percent_high"] = (
        by_city["high_value_orders"] / by_city["count"] * 100).round(1)
    print(by_city.to_string())

    print("\n=== by channel ===")
    by_channel = orders.groupby("channel")["amount"].agg(
        ["count", "sum", "mean"]).round(2)
    print(by_channel.to_string())

    print("\n=== pivot: average order value by city and channel ===")
    pivot = orders.pivot_table(index="city", columns="channel",
                               values="amount", aggfunc="mean").round(2)
    print(pivot.to_string())

    print("\n=== combined conditions ===")
    mid = amount.between(500, 1000, inclusive="right")
    print(f"  between Rs.500 and Rs.1,000  : {int(mid.sum())} "
          f"({mid.mean() * 100:.2f}%)")
    big_app = (amount > THRESHOLD) & (orders["channel"] == "app")
    print(f"  high value AND on the app    : {int(big_app.sum())} "
          f"({big_app.mean() * 100:.2f}%)")

    print("\n=== tagging every order ===")
    orders["tier"] = np.where(amount > THRESHOLD, "HIGH", "normal")
    print(orders["tier"].value_counts().to_string())

    print("\n=== business summary ===")
    print(f"  {len(orders)} orders worth Rs.{amount.sum():,.2f}")
    print(f"  {count} order(s) above Rs.{THRESHOLD:,} ({percent:.2f}%)")
    print(f"  average order value Rs.{amount.mean():,.2f}")
    print(f"  top city by revenue : {by_city['sum'].idxmax()} "
          f"(Rs.{by_city['sum'].max():,.2f})")


if __name__ == "__main__":
    main()
```

</details>

<details>
<summary>Program output</summary>

```text
=== the DataFrame (first 10 rows) ===
           amount    city channel
order_id                         
ORD-0001   294.77    Pune     app
ORD-0002   747.34  Mumbai     app
ORD-0003   109.21    Pune     web
ORD-0004  2113.70  Nashik     web
ORD-0005  1068.99  Mumbai     app
ORD-0006   462.74    Pune     app
ORD-0007   454.52  Nashik     web
ORD-0008   791.12  Mumbai     app
ORD-0009   473.00  Mumbai     app
ORD-0010   491.12  Nashik     app

  rows 40, columns ['amount', 'city', 'channel']
  dtypes:
amount     float64
city           str
channel        str

=== 1) orders above Rs.1,000 ===
  condition : orders['amount'] > 1000
  count     : 12
  order ids : ['ORD-0004', 'ORD-0005', 'ORD-0011', 'ORD-0022', 'ORD-0025', 'ORD-0026', 'ORD-0028', 'ORD-0032', 'ORD-0033', 'ORD-0034', 'ORD-0036', 'ORD-0040']

=== 2) percentage of such orders ===
  12 / 40 x 100 = 30.00%
  mask.mean() * 100 gives the same : 30.00%

=== revenue contribution ===
  total revenue           : Rs.32,942.73
  revenue above Rs.1,000  : Rs.19,047.63
  share of revenue        : 57.82%
  so 30.0% of orders bring 57.8% of the money

=== the high-value orders ===
           amount    city channel
order_id                         
ORD-0026  3109.29  Mumbai     app
ORD-0004  2113.70  Nashik     web
ORD-0032  2031.06  Mumbai     web
ORD-0028  2025.12  Nashik     web
ORD-0034  1675.63    Pune     web
ORD-0040  1324.84  Mumbai     app
ORD-0033  1274.78  Nagpur     app
ORD-0011  1150.63  Nashik     web
ORD-0036  1114.43  Nagpur     web
ORD-0022  1086.76  Mumbai     app
ORD-0025  1072.40  Nagpur     app
ORD-0005  1068.99  Mumbai     app

=== describe() ===
count      40.00
mean      823.57
std       637.89
min       109.21
25%       396.99
50%       562.68
75%      1075.99
max      3109.29

  the mean (Rs.823.57) sits above the median (Rs.562.68):
  the long tail of large orders pulls the mean up

=== percentiles ===
  p10  : Rs.     265.12
  p25  : Rs.     396.99
  p50  : Rs.     562.68
  p75  : Rs.   1,075.99
  p90  : Rs.   1,710.58
  p95  : Rs.   2,035.19
  p99  : Rs.   2,721.01

=== how the answer moves with the threshold ===
           orders  percent_orders  percent_revenue
threshold                                         
250            36            90.0            97.90
500            23            57.5            82.16
750            16            40.0            69.00
1000           12            30.0            57.82
1500            5            12.5            33.25
2000            4            10.0            28.17
3000            1             2.5             9.44

=== order size bands (pd.cut) ===
           orders  revenue  percent_orders
amount                                    
0-250           4   692.91            10.0
250-500        13  5184.95            32.5
500-1000       11  8017.24            27.5
1000-2000       8  9768.46            20.0
2000-5000       4  9279.17            10.0
5000+           0     0.00             0.0

=== by city (groupby) ===
        count       sum     mean      max  high_value_orders  percent_high
city                                                                      
Mumbai     12  12143.69  1011.97  3109.29                  5          41.7
Nagpur      8   5892.94   736.62  1274.78                  3          37.5
Nashik     11   9716.04   883.28  2113.70                  3          27.3
Pune        9   5190.06   576.67  1675.63                  1          11.1

=== by channel ===
         count       sum    mean
channel                         
app         25  18864.40  754.58
web         15  14078.33  938.56

=== pivot: average order value by city and channel ===
channel     app      web
city                    
Mumbai   993.79  1102.88
Nagpur   855.01   618.22
Nashik   604.29  1218.06
Pune     376.13   827.35

=== combined conditions ===
  between Rs.500 and Rs.1,000  : 11 (27.50%)
  high value AND on the app    : 6 (15.00%)

=== tagging every order ===
tier
normal    28
HIGH      12

=== business summary ===
  40 orders worth Rs.32,942.73
  12 order(s) above Rs.1,000 (30.00%)
  average order value Rs.823.57
  top city by revenue : Mumbai (Rs.12,143.69)

```

</details>

---

## Experiment 11 - Question 8: Scientific Experiment Data with Pandas

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

**File:** [`q8_experiment_trials_pandas.py`](q8_experiment_trials_pandas.py) &nbsp;&middot;&nbsp; **Run:** `python q8_experiment_trials_pandas.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== the readings table ===
trial          Trial 1  Trial 2  Trial 3  Trial 4
experiment                                       
E1 Catalyst A     12.4     13.1     12.9     13.6
E2 Catalyst B     15.8     16.2     15.5     17.1
E3 Control         9.2      9.0      9.4      8.8
E4 Catalyst C     14.1     13.8     18.9     14.4
E5 Catalyst D     16.0     15.7     16.4     16.1

  shape (5, 4), 20 readings

=== 1) average per experiment (axis=1) ===
experiment
E1 Catalyst A    13.00
E2 Catalyst B    16.15
E3 Control        9.10
E4 Catalyst C    15.30
E5 Catalyst D    16.05

                mean    std   min   max  spread best_trial
experiment                                                
E1 Catalyst A  13.00  0.497  12.4  13.6     1.2    Trial 4
E2 Catalyst B  16.15  0.695  15.5  17.1     1.6    Trial 4
E3 Control      9.10  0.258   8.8   9.4     0.6    Trial 3
E4 Catalyst C  15.30  2.412  13.8  18.9     5.1    Trial 3
E5 Catalyst D  16.05  0.289  15.7  16.4     0.7    Trial 3

  best experiment  : E2 Catalyst B (mean 16.150)
  worst experiment : E3 Control (mean 9.100)

=== 2) maximum overall reading ===
  df.stack().max()    : 18.90
  df.stack().idxmax() : ('E4 Catalyst C', 'Trial 3')
  experiment          : E4 Catalyst C
  trial               : Trial 3
  df.max().max()      : 18.90  (same value)
  df.max()            :
trial
Trial 1    16.0
Trial 2    16.2
Trial 3    18.9
Trial 4    17.1

  the column holding the peak : Trial 3

=== column-wise view: which trial slot performs best? ===
          mean  min   max best_experiment
trial                                    
Trial 1  13.50  9.2  16.0   E5 Catalyst D
Trial 2  13.56  9.0  16.2   E2 Catalyst B
Trial 3  14.62  9.4  18.9   E4 Catalyst C
Trial 4  14.00  8.8  17.1   E2 Catalyst B

  strongest trial slot : Trial 3

=== describe() per trial ===
trial  Trial 1  Trial 2  Trial 3  Trial 4
count    5.000    5.000    5.000    5.000
mean    13.500   13.560   14.620   14.000
std      2.811    2.855    3.622    3.216
min      9.200    9.000    9.400    8.800
25%     12.400   13.100   12.900   13.600
50%     14.100   13.800   15.500   14.400
75%     15.800   15.700   16.400   16.100
max     16.000   16.200   18.900   17.100

=== repeatability ranking (lower std is better) ===
  1. E3 Control      std  0.258  highly repeatable
  2. E5 Catalyst D   std  0.289  highly repeatable
  3. E1 Catalyst A   std  0.497  highly repeatable
  4. E2 Catalyst B   std  0.695  acceptable
  5. E4 Catalyst C   std  2.412  poor, suspect an outlier

=== outlier detection with z-scores per row ===
trial          Trial 1  Trial 2  Trial 3  Trial 4
experiment                                       
E1 Catalyst A     1.21     0.20     0.20     1.21
E2 Catalyst B     0.50     0.07     0.93     1.37
E3 Control        0.39     0.39     1.16     1.16
E4 Catalyst C     0.50     0.62     1.49     0.37
E5 Catalyst D     0.17     1.21     1.21     0.17

  no reading stands out

=== comparison against the control row ===
                mean  lift_vs_control_percent
experiment                                   
E1 Catalyst A  13.00                    42.86
E2 Catalyst B  16.15                    77.47
E4 Catalyst C  15.30                    68.13
E5 Catalyst D  16.05                    76.37

  control mean : 9.100

=== long format and groupby ===
   experiment   trial  reading
E1 Catalyst A Trial 1     12.4
E2 Catalyst B Trial 1     15.8
   E3 Control Trial 1      9.2
E4 Catalyst C Trial 1     14.1
E5 Catalyst D Trial 1     16.0
E1 Catalyst A Trial 2     13.1

  rows: 20

  groupby experiment:
                mean    std   max
experiment                       
E1 Catalyst A  13.00  0.497  13.6
E2 Catalyst B  16.15  0.695  17.1
E3 Control      9.10  0.258   9.4
E4 Catalyst C  15.30  2.412  18.9
E5 Catalyst D  16.05  0.289  16.4

  groupby trial:
          mean   max
trial               
Trial 1  13.50  16.0
Trial 2  13.56  16.2
Trial 3  14.62  18.9
Trial 4  14.00  17.1

=== top 5 individual readings ===
   experiment   trial  reading
E4 Catalyst C Trial 3     18.9
E2 Catalyst B Trial 4     17.1
E5 Catalyst D Trial 3     16.4
E2 Catalyst B Trial 2     16.2
E5 Catalyst D Trial 4     16.1

=== whole-dataset summary ===
  grand mean : 13.920
  overall std: 2.847
  minimum    : 8.80 at ('E3 Control', 'Trial 4')
  maximum    : 18.90 at ('E4 Catalyst C', 'Trial 3')
  range      : 10.10

```

</details>

---

## Experiment 11 - Question 9: Medical Data Analysis with Pandas

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

**File:** [`q9_blood_sugar_pandas.py`](q9_blood_sugar_pandas.py) &nbsp;&middot;&nbsp; **Run:** `python q9_blood_sugar_pandas.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== blood sugar table (mg/dL) ===
time_of_day     Morning  Noon  Evening  Night
patient                                      
P-101 Sharma         92   148      134    110
P-102 Andhale        86   132      121     98
P-103 Kulkarni      128   196      178    152
P-104 Deshmukh       74   118      109     88
P-105 Patil         112   172      160    131

  shape (5, 4), 20 readings

=== 1) daily average per patient (axis=1) ===
patient
P-101 Sharma      121.00
P-102 Andhale     109.25
P-103 Kulkarni    163.50
P-104 Deshmukh     97.25
P-105 Patil       143.75

                daily_avg  min  max  swing peak_time          status
patient                                                             
P-101 Sharma       121.00   92  148     56      Noon      borderline
P-102 Andhale      109.25   86  132     46      Noon    within range
P-103 Kulkarni     163.50  128  196     68      Noon  diabetic range
P-104 Deshmukh      97.25   74  118     44      Noon    within range
P-105 Patil        143.75  112  172     60      Noon    pre-diabetic

  highest daily average : P-103 Kulkarni (163.50 mg/dL)
  lowest daily average  : P-104 Deshmukh (97.25 mg/dL)

=== 2) average by time of day (axis=0) ===
time_of_day
Morning     98.4
Noon       153.2
Evening    140.4
Night      115.8

  time_avg.idxmax() -> Noon
  the highest average blood sugar occurs at Noon (153.20 mg/dL)
  the lowest is at Morning (98.40 mg/dL)
  morning to noon rise  : +54.80 mg/dL (the post-meal spike)

             average  min  max highest_patient
time_of_day                                   
Morning         98.4   74  128  P-103 Kulkarni
Noon           153.2  118  196  P-103 Kulkarni
Evening        140.4  109  178  P-103 Kulkarni
Night          115.8   88  152  P-103 Kulkarni

=== text chart by time of day ===
  Morning     98.40  ########################
  Noon       153.20  ######################################  <== highest
  Evening    140.40  ###################################
  Night      115.80  ############################

=== describe() per time of day ===
time_of_day  Morning    Noon  Evening   Night
count           5.00    5.00     5.00    5.00
mean           98.40  153.20   140.40  115.80
std            21.51   31.23    28.29   25.81
min            74.00  118.00   109.00   88.00
25%            86.00  132.00   121.00   98.00
50%            92.00  148.00   134.00  110.00
75%           112.00  172.00   160.00  131.00
max           128.00  196.00   178.00  152.00

=== fasting (Morning) check ===
                morning_mg_dl  above_normal  excess
patient                                            
P-101 Sharma               92         False       0
P-102 Andhale              86         False       0
P-103 Kulkarni            128          True      28
P-104 Deshmukh             74         False       0
P-105 Patil               112          True      12

  2 of 5 patient(s) have a high fasting reading (normal up to 100 mg/dL)

=== post-meal readings above 140 mg/dL ===
patient         time_of_day
P-101 Sharma    Noon           148
P-103 Kulkarni  Noon           196
                Evening        178
                Night          152
P-105 Patil     Noon           172
                Evening        160

  6 of 15 post-meal readings are out of range

=== patients needing review (any reading above 180) ===
time_of_day     Morning  Noon  Evening  Night
patient                                      
P-103 Kulkarni      128   196      178    152

  1 patient(s) flagged

=== deviation from each patient's own daily average ===
time_of_day     Morning  Noon  Evening  Night
patient                                      
P-101 Sharma      -29.0  27.0     13.0  -11.0
P-102 Andhale     -23.2  22.8     11.8  -11.2
P-103 Kulkarni    -35.5  32.5     14.5  -11.5
P-104 Deshmukh    -23.2  20.8     11.8   -9.2
P-105 Patil       -31.8  28.2     16.2  -12.8

=== long format and groupby ===
       patient time_of_day  mg_dl
  P-101 Sharma     Morning     92
 P-102 Andhale     Morning     86
P-103 Kulkarni     Morning    128
P-104 Deshmukh     Morning     74
   P-105 Patil     Morning    112
  P-101 Sharma        Noon    148

  groupby time_of_day:
              mean  min  max
time_of_day                 
Morning       98.4   74  128
Noon         153.2  118  196
Evening      140.4  109  178
Night        115.8   88  152

  groupby patient:
                  mean  max
patient                    
P-101 Sharma    121.00  148
P-102 Andhale   109.25  132
P-103 Kulkarni  163.50  196
P-104 Deshmukh   97.25  118
P-105 Patil     143.75  172

=== reading bands (pd.cut) ===
band
normal       5
elevated     9
high         5
very high    1

=== ward-level summary ===
  patients monitored  : 5
  readings per day    : 4
  ward average        : 126.95 mg/dL
  ward median         : 124.50 mg/dL
  overall peak        : 196 mg/dL (P-103 Kulkarni at Noon)
  patients above a 140 daily average : 2 of 5

```

</details>

---

## Experiment 11 - Question 10: Electricity Consumption Analysis with Pandas

Scenario: A housing society records electricity consumption (in kWh) for
6 apartments over 7 days.

Task:
  1) Find the total consumption for each apartment (row-wise).
  2) Identify the apartment with the highest total consumption.

Note: the sheet repeats Experiment 10 Question 10 here; this version answers it
with Pandas, the topic of Experiment 11.

Rubrics covered:
  * correct DataFrame representation
  * row-wise operation using axis
  * correct identification of the highest consumer
  * output clarity

Requires: pandas, numpy

**File:** [`q10_electricity_pandas.py`](q10_electricity_pandas.py) &nbsp;&middot;&nbsp; **Run:** `python q10_electricity_pandas.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 11 - Question 10: Electricity Consumption Analysis with Pandas

Scenario: A housing society records electricity consumption (in kWh) for
6 apartments over 7 days.

Task:
  1) Find the total consumption for each apartment (row-wise).
  2) Identify the apartment with the highest total consumption.

Note: the sheet repeats Experiment 10 Question 10 here; this version answers it
with Pandas, the topic of Experiment 11.

Rubrics covered:
  * correct DataFrame representation
  * row-wise operation using axis
  * correct identification of the highest consumer
  * output clarity

Requires: pandas, numpy
"""

import pandas as pd

FLATS = ["A-101", "A-102", "B-201", "B-202", "C-301", "C-302"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
TARIFF = 8.40          # Rs. per kWh


def main():
    df = pd.DataFrame(
        [[12.4, 11.8, 13.1, 12.0, 14.2, 18.5, 17.9],
         [8.2, 7.9, 8.6, 8.1, 9.0, 11.4, 10.8],
         [21.5, 22.8, 20.9, 23.4, 24.1, 27.6, 26.2],
         [5.1, 4.8, 5.4, 5.0, 5.6, 7.2, 6.9],
         [15.8, 16.4, 15.2, 16.9, 17.5, 20.3, 19.1],
         [10.2, 10.8, 9.9, 11.1, 11.8, 14.0, 13.2]],
        index=FLATS, columns=DAYS)
    df.index.name = "flat"
    df.columns.name = "day"

    print("=== consumption table (kWh) ===")
    print(df.to_string())
    print(f"\n  shape {df.shape}, {df.size} readings, tariff "
          f"Rs.{TARIFF:.2f}/kWh")

    # 1) row-wise total
    per_flat = df.sum(axis=1)
    print("\n=== 1) weekly total per apartment (axis=1) ===")
    print(per_flat.round(1).to_string())

    bills = pd.DataFrame({
        "total_kwh": per_flat.round(1),
        "daily_avg": df.mean(axis=1).round(2),
        "peak_day": df.idxmax(axis=1),
        "peak_kwh": df.max(axis=1),
        "weekly_bill": (per_flat * TARIFF).round(2),
        "share_percent": (per_flat / per_flat.sum() * 100).round(1),
    })
    print("\n" + bills.to_string())

    # 2) highest consumer
    top = per_flat.idxmax()
    print("\n=== 2) highest consumer ===")
    print(f"  per_flat.idxmax() -> {top}")
    print(f"  weekly total   : {per_flat.max():.1f} kWh")
    print(f"  daily average  : {df.loc[top].mean():.2f} kWh")
    print(f"  weekly bill    : Rs.{per_flat.max() * TARIFF:,.2f}")
    print(f"  readings       : {df.loc[top].tolist()}")
    print(f"  it used {per_flat.max() / per_flat.mean():.2f}x the society "
          f"average and {per_flat.max() / per_flat.min():.2f}x the lowest flat")
    print(f"\n  lowest consumer: {per_flat.idxmin()} "
          f"({per_flat.min():.1f} kWh, "
          f"Rs.{per_flat.min() * TARIFF:,.2f})")

    print("\n=== ranking ===")
    ranking = bills.sort_values("total_kwh", ascending=False).copy()
    ranking.insert(0, "rank", range(1, len(ranking) + 1))
    print(ranking[["rank", "total_kwh", "share_percent",
                   "weekly_bill"]].to_string())

    print("\n=== daily totals for the whole society (axis=0) ===")
    per_day = df.sum(axis=0)
    day_frame = pd.DataFrame({
        "total_kwh": per_day.round(1),
        "flat_avg": df.mean(axis=0).round(2),
        "top_flat": df.idxmax(axis=0),
    })
    print(day_frame.to_string())
    print(f"\n  busiest day : {per_day.idxmax()} ({per_day.max():.1f} kWh)")
    print(f"  quietest day: {per_day.idxmin()} ({per_day.min():.1f} kWh)")

    print("\n=== table with margins ===")
    with_margins = df.copy()
    with_margins["TOTAL"] = per_flat
    with_margins.loc["TOTAL"] = with_margins.sum(axis=0)
    print(with_margins.round(1).to_string())

    print("\n=== weekday vs weekend ===")
    weekday = df[["Mon", "Tue", "Wed", "Thu", "Fri"]]
    weekend = df[["Sat", "Sun"]]
    split = pd.DataFrame({
        "total_kwh": [weekday.to_numpy().sum().round(1),
                      weekend.to_numpy().sum().round(1)],
        "days": [5, 2],
        "per_day": [round(weekday.to_numpy().sum() / 5, 1),
                    round(weekend.to_numpy().sum() / 2, 1)],
    }, index=["Weekday", "Weekend"])
    print(split.to_string())
    uplift = split.loc["Weekend", "per_day"] / split.loc["Weekday", "per_day"]
    print(f"\n  weekend days use {(uplift - 1) * 100:+.1f}% more than weekdays")

    print("\n=== wing-level summary (groupby on the flat prefix) ===")
    wings = df.groupby(df.index.str[0]).sum()
    wing_summary = pd.DataFrame({
        "total_kwh": wings.sum(axis=1).round(1),
        "flats": df.groupby(df.index.str[0]).size(),
    })
    wing_summary["avg_per_flat"] = (
        wing_summary["total_kwh"] / wing_summary["flats"]).round(1)
    wing_summary["bill"] = (wing_summary["total_kwh"] * TARIFF).round(2)
    wing_summary.index.name = "wing"
    print(wing_summary.to_string())

    print("\n=== society billing summary ===")
    total = df.to_numpy().sum()
    print(f"  total units consumed : {total:.1f} kWh")
    print(f"  total bill           : Rs.{total * TARIFF:,.2f}")
    print(f"  average per flat     : {per_flat.mean():.2f} kWh "
          f"(Rs.{per_flat.mean() * TARIFF:,.2f})")
    print(f"  median per flat      : {per_flat.median():.2f} kWh")
    print(f"  standard deviation   : {per_flat.std():.2f} kWh")

    print("\n=== flats above the society average ===")
    above = per_flat[per_flat > per_flat.mean()]
    for flat, value in above.items():
        excess = value - per_flat.mean()
        print(f"  {flat:<8}{value:>8.1f} kWh  {excess:+.1f} above average "
              f"(Rs.{excess * TARIFF:,.2f} extra)")

    print("\n=== monthly slab projection ===")
    projection = pd.DataFrame({
        "weekly_kwh": per_flat.round(1),
        "projected_monthly": (per_flat / 7 * 30).round(1),
    })
    projection["slab"] = pd.cut(
        projection["projected_monthly"],
        bins=[0, 100, 150, float("inf")],
        labels=["low slab", "mid slab", "high slab"])
    print(projection.to_string())

    print("\n=== text chart of weekly totals ===")
    for flat, value in per_flat.sort_values(ascending=False).items():
        marker = "  <== highest" if flat == top else ""
        print(f"  {flat:<8}{value:>7.1f} kWh  "
              f"{'#' * int(value / 4)}{marker}")


if __name__ == "__main__":
    main()
```

</details>

<details>
<summary>Program output</summary>

```text
=== consumption table (kWh) ===
day     Mon   Tue   Wed   Thu   Fri   Sat   Sun
flat                                           
A-101  12.4  11.8  13.1  12.0  14.2  18.5  17.9
A-102   8.2   7.9   8.6   8.1   9.0  11.4  10.8
B-201  21.5  22.8  20.9  23.4  24.1  27.6  26.2
B-202   5.1   4.8   5.4   5.0   5.6   7.2   6.9
C-301  15.8  16.4  15.2  16.9  17.5  20.3  19.1
C-302  10.2  10.8   9.9  11.1  11.8  14.0  13.2

  shape (6, 7), 42 readings, tariff Rs.8.40/kWh

=== 1) weekly total per apartment (axis=1) ===
flat
A-101     99.9
A-102     64.0
B-201    166.5
B-202     40.0
C-301    121.2
C-302     81.0

       total_kwh  daily_avg peak_day  peak_kwh  weekly_bill  share_percent
flat                                                                      
A-101       99.9      14.27      Sat      18.5       839.16           17.4
A-102       64.0       9.14      Sat      11.4       537.60           11.2
B-201      166.5      23.79      Sat      27.6      1398.60           29.1
B-202       40.0       5.71      Sat       7.2       336.00            7.0
C-301      121.2      17.31      Sat      20.3      1018.08           21.2
C-302       81.0      11.57      Sat      14.0       680.40           14.1

=== 2) highest consumer ===
  per_flat.idxmax() -> B-201
  weekly total   : 166.5 kWh
  daily average  : 23.79 kWh
  weekly bill    : Rs.1,398.60
  readings       : [21.5, 22.8, 20.9, 23.4, 24.1, 27.6, 26.2]
  it used 1.74x the society average and 4.16x the lowest flat

  lowest consumer: B-202 (40.0 kWh, Rs.336.00)

=== ranking ===
       rank  total_kwh  share_percent  weekly_bill
flat                                              
B-201     1      166.5           29.1      1398.60
C-301     2      121.2           21.2      1018.08
A-101     3       99.9           17.4       839.16
C-302     4       81.0           14.1       680.40
A-102     5       64.0           11.2       537.60
B-202     6       40.0            7.0       336.00

=== daily totals for the whole society (axis=0) ===
     total_kwh  flat_avg top_flat
day                              
Mon       73.2     12.20    B-201
Tue       74.5     12.42    B-201
Wed       73.1     12.18    B-201
Thu       76.5     12.75    B-201
Fri       82.2     13.70    B-201
Sat       99.0     16.50    B-201
Sun       94.1     15.68    B-201

  busiest day : Sat (99.0 kWh)
  quietest day: Wed (73.1 kWh)

=== table with margins ===
day     Mon   Tue   Wed   Thu   Fri   Sat   Sun  TOTAL
flat                                                  
A-101  12.4  11.8  13.1  12.0  14.2  18.5  17.9   99.9
A-102   8.2   7.9   8.6   8.1   9.0  11.4  10.8   64.0
B-201  21.5  22.8  20.9  23.4  24.1  27.6  26.2  166.5
B-202   5.1   4.8   5.4   5.0   5.6   7.2   6.9   40.0
C-301  15.8  16.4  15.2  16.9  17.5  20.3  19.1  121.2
C-302  10.2  10.8   9.9  11.1  11.8  14.0  13.2   81.0
TOTAL  73.2  74.5  73.1  76.5  82.2  99.0  94.1  572.6

=== weekday vs weekend ===
         total_kwh  days  per_day
Weekday      379.5     5     75.9
Weekend      193.1     2     96.6

  weekend days use +27.3% more than weekdays

=== wing-level summary (groupby on the flat prefix) ===
      total_kwh  flats  avg_per_flat     bill
wing                                         
A         163.9      2          82.0  1376.76
B         206.5      2         103.2  1734.60
C         202.2      2         101.1  1698.48

=== society billing summary ===
  total units consumed : 572.6 kWh
  total bill           : Rs.4,809.84
  average per flat     : 95.43 kWh (Rs.801.64)
  median per flat      : 90.45 kWh
  standard deviation   : 44.73 kWh

=== flats above the society average ===
  A-101       99.9 kWh  +4.5 above average (Rs.37.52 extra)
  B-201      166.5 kWh  +71.1 above average (Rs.596.96 extra)
  C-301      121.2 kWh  +25.8 above average (Rs.216.44 extra)

=== monthly slab projection ===
       weekly_kwh  projected_monthly       slab
flat                                           
A-101        99.9              428.1  high slab
A-102        64.0              274.3  high slab
B-201       166.5              713.6  high slab
B-202        40.0              171.4  high slab
C-301       121.2              519.4  high slab
C-302        81.0              347.1  high slab

=== text chart of weekly totals ===
  B-201     166.5 kWh  #########################################  <== highest
  C-301     121.2 kWh  ##############################
  A-101      99.9 kWh  ########################
  C-302      81.0 kWh  ####################
  A-102      64.0 kWh  ################
  B-202      40.0 kWh  ##########

```

</details>

---
