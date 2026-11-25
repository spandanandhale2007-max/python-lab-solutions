# Experiment 10 - Unit IV

NumPy: arrays, aggregation, axis operations, boolean filtering, matrix algebra

10 scenario questions, each solved in its own section and its own file. Every program below was executed and the real output is included.

[Back to the index](../README.md)

---

## Questions in this experiment

- [Experiment 10 - Question 1: Marks Analysis with NumPy](#experiment-10---question-1-marks-analysis-with-numpy)
- [Experiment 10 - Question 2: Daily Sales Analysis](#experiment-10---question-2-daily-sales-analysis)
- [Experiment 10 - Question 3: Stock Price Analysis](#experiment-10---question-3-stock-price-analysis)
- [Experiment 10 - Question 4: Matrix Operations](#experiment-10---question-4-matrix-operations)
- [Experiment 10 - Question 5: Product Inventory Check](#experiment-10---question-5-product-inventory-check)
- [Experiment 10 - Question 6: Weather Dataset Operations](#experiment-10---question-6-weather-dataset-operations)
- [Experiment 10 - Question 7: E-commerce Order Analysis](#experiment-10---question-7-e-commerce-order-analysis)
- [Experiment 10 - Question 8: Scientific Experiment Data](#experiment-10---question-8-scientific-experiment-data)
- [Experiment 10 - Question 9: Medical Data Analysis](#experiment-10---question-9-medical-data-analysis)
- [Experiment 10 - Question 10: Electricity Consumption Analysis](#experiment-10---question-10-electricity-consumption-analysis)

---

## Experiment 10 - Question 1: Marks Analysis with NumPy

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

**File:** [`q1_marks_numpy.py`](q1_marks_numpy.py) &nbsp;&middot;&nbsp; **Run:** `python q1_marks_numpy.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== the array ===
  marks  : [78 92 55 88 64 71 45 83 96 59]
  names  : ['Spandan', 'Riya', 'Aman', 'Neha', 'Omkar', 'Sana', 'Rohit', 'Pooja', 'Kiran', 'Tanvi']
  dtype  : int64
  shape  : (10,)
  ndim   : 1
  size   : 10
  memory : 80 bytes

=== statistics with NumPy ===
  np.mean  -> average : 73.10
  np.max   -> highest : 96
  np.min   -> lowest  : 45
  np.argmax-> topper  : index 8 (Kiran)
  np.argmin-> lowest  : index 6 (Rohit)
  np.sum   -> total   : 731
  np.median           : 74.50
  np.std              : 16.21
  np.ptp   -> range   : 51

=== students above the average of 73.10 ===
  boolean mask : [ True  True False  True False False False  True  True False]
  filtered     : [78 92 88 83 96]
  count        : 5 of 10
  their average: 87.40
  indices      : [0 1 3 7 8]

  name-wise:
    Spandan     78  (+4.90 vs average)
    Riya        92  (+18.90 vs average)
    Neha        88  (+14.90 vs average)
    Pooja       83  (+9.90 vs average)
    Kiran       96  (+22.90 vs average)

=== at or below average (5 student(s)) ===
    Aman        55  (-18.10)
    Omkar       64  (-9.10)
    Sana        71  (-2.10)
    Rohit       45  (-28.10)
    Tanvi       59  (-14.10)

=== full class table ===
  name        marks   vs avg  bar
  Spandan        78    +4.90  ################### above
  Riya           92   +18.90  ####################### above
  Aman           55   -18.10  ############# below
  Neha           88   +14.90  ###################### above
  Omkar          64    -9.10  ################ below
  Sana           71    -2.10  ################# below
  Rohit          45   -28.10  ########### below
  Pooja          83    +9.90  #################### above
  Kiran          96   +22.90  ######################## above
  Tanvi          59   -14.10  ############## below

=== vectorised operations, no Python loop ===
  5 grace marks added  : [ 83  97  60  93  69  76  50  88 101  64]
  scaled to 50 marks   : [39.  46.  27.5 44.  32.  35.5 22.5 41.5 48.  29.5]
  percentage of total  : [10.67 12.59  7.52 12.04  8.76  9.71  6.16 11.35 13.13  8.07]
  clipped at 90        : [78 90 55 88 64 71 45 83 90 59]
  sorted ascending     : [45 55 59 64 71 78 83 88 92 96]
  merit order (indices): [8 1 3 7 0 5 4 9 2 6]

=== grade bands with np.select ===
  Spandan     78  B
  Riya        92  A+
  Aman        55  D
  Neha        88  A
  Omkar       64  C
  Sana        71  B
  Rohit       45  D
  Pooja       83  A
  Kiran       96  A+
  Tanvi       59  D

=== pass / fail (cut-off 40) ===
  passed : 10 of 10 (100.0%)
  failed : 0 -> none

```

</details>

---

## Experiment 10 - Question 2: Daily Sales Analysis

Scenario: A store records daily sales (in Rs.) for 7 days:
[1200, 1500, 900, 1800, 2100, 1600, 1900].

Task:
  1) Convert this into a NumPy array.
  2) Find the total sales, average sales and the day with maximum sales.

Rubrics covered:
  * array creation
  * correct use of NumPy functions (sum, mean, argmax)
  * display of results
  * correct logic

Requires: numpy

**File:** [`q2_daily_sales_numpy.py`](q2_daily_sales_numpy.py) &nbsp;&middot;&nbsp; **Run:** `python q2_daily_sales_numpy.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 10 - Question 2: Daily Sales Analysis

Scenario: A store records daily sales (in Rs.) for 7 days:
[1200, 1500, 900, 1800, 2100, 1600, 1900].

Task:
  1) Convert this into a NumPy array.
  2) Find the total sales, average sales and the day with maximum sales.

Rubrics covered:
  * array creation
  * correct use of NumPy functions (sum, mean, argmax)
  * display of results
  * correct logic

Requires: numpy
"""

import numpy as np

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
        "Saturday", "Sunday"]
RAW = [1200, 1500, 900, 1800, 2100, 1600, 1900]


def main():
    # 1) convert the Python list into a NumPy array
    sales = np.array(RAW)

    print("=== conversion ===")
    print(f"  python list : {RAW}  (type {type(RAW).__name__})")
    print(f"  numpy array : {sales}  (type {type(sales).__name__})")
    print(f"  dtype {sales.dtype}, shape {sales.shape}, "
          f"{sales.nbytes} bytes")

    # 2) aggregation
    total = sales.sum()
    average = sales.mean()
    best_index = sales.argmax()
    worst_index = sales.argmin()

    print("\n=== required answers ===")
    print(f"  total sales        : Rs.{total:,}")
    print(f"  average sales      : Rs.{average:,.2f} per day")
    print(f"  maximum sales day  : {DAYS[best_index]} "
          f"(index {best_index}) with Rs.{sales[best_index]:,}")

    print("\n=== extra statistics ===")
    print(f"  minimum sales day  : {DAYS[worst_index]} "
          f"with Rs.{sales[worst_index]:,}")
    print(f"  median             : Rs.{np.median(sales):,.2f}")
    print(f"  standard deviation : Rs.{sales.std():,.2f}")
    print(f"  range (np.ptp)     : Rs.{np.ptp(sales):,}")
    print(f"  cumulative total   : {np.cumsum(sales)}")

    print("\n=== day-by-day ===")
    print(f"  {'day':<11}{'sales':>10}{'vs average':>13}{'share':>9}  bar")
    for day, amount in zip(DAYS, sales):
        share = amount / total * 100
        print(f"  {day:<11}{amount:>10,}{amount - average:>+13,.2f}"
              f"{share:>8.1f}%  {'#' * (amount // 100)}")

    print("\n=== days above the weekly average ===")
    mask = sales > average
    print(f"  mask    : {mask}")
    print(f"  days    : {np.array(DAYS)[mask].tolist()}")
    print(f"  amounts : {sales[mask]}")
    print(f"  they contributed Rs.{sales[mask].sum():,} "
          f"({sales[mask].sum() / total * 100:.1f}% of the week)")

    print("\n=== weekday vs weekend ===")
    weekday = sales[:5]
    weekend = sales[5:]
    print(f"  weekdays (Mon-Fri) : Rs.{weekday.sum():,}  "
          f"avg Rs.{weekday.mean():,.2f}")
    print(f"  weekend  (Sat-Sun) : Rs.{weekend.sum():,}  "
          f"avg Rs.{weekend.mean():,.2f}")
    print(f"  weekend uplift     : "
          f"{(weekend.mean() / weekday.mean() - 1) * 100:+.1f}%")

    print("\n=== day-on-day change ===")
    change = np.diff(sales)
    percent = np.round(change / sales[:-1] * 100, 1)
    for i, (delta, pct) in enumerate(zip(change, percent)):
        print(f"  {DAYS[i]:<11}-> {DAYS[i + 1]:<11}"
              f"{delta:>+8,}  {pct:>+7.1f}%")
    print(f"  biggest jump : {DAYS[change.argmax() + 1]} "
          f"({change.max():+,})")
    print(f"  biggest drop : {DAYS[change.argmin() + 1]} "
          f"({change.min():+,})")

    print("\n=== vectorised what-if scenarios ===")
    print(f"  10% growth next week  : {np.round(sales * 1.10).astype(int)} "
          f"-> Rs.{int(round(sales.sum() * 1.10)):,}")
    print(f"  GST at 18% collected  : "
          f"{np.round(sales * 0.18, 2)}")
    print(f"  Rs.300 fixed cost/day : {sales - 300} "
          f"-> profit Rs.{(sales - 300).sum():,}")
    target = 1500
    print(f"  days meeting the Rs.{target:,} target: "
          f"{int((sales >= target).sum())} of 7 -> "
          f"{np.array(DAYS)[sales >= target].tolist()}")

    print("\n=== 3-day moving average (np.convolve) ===")
    window = np.convolve(sales, np.ones(3) / 3, mode="valid")
    for i, value in enumerate(window):
        print(f"  {DAYS[i][:3]}-{DAYS[i + 2][:3]} : Rs.{value:,.2f}")


if __name__ == "__main__":
    main()
```

</details>

<details>
<summary>Program output</summary>

```text
=== conversion ===
  python list : [1200, 1500, 900, 1800, 2100, 1600, 1900]  (type list)
  numpy array : [1200 1500  900 1800 2100 1600 1900]  (type ndarray)
  dtype int64, shape (7,), 56 bytes

=== required answers ===
  total sales        : Rs.11,000
  average sales      : Rs.1,571.43 per day
  maximum sales day  : Friday (index 4) with Rs.2,100

=== extra statistics ===
  minimum sales day  : Wednesday with Rs.900
  median             : Rs.1,600.00
  standard deviation : Rs.384.39
  range (np.ptp)     : Rs.1,200
  cumulative total   : [ 1200  2700  3600  5400  7500  9100 11000]

=== day-by-day ===
  day             sales   vs average    share  bar
  Monday          1,200      -371.43    10.9%  ############
  Tuesday         1,500       -71.43    13.6%  ###############
  Wednesday         900      -671.43     8.2%  #########
  Thursday        1,800      +228.57    16.4%  ##################
  Friday          2,100      +528.57    19.1%  #####################
  Saturday        1,600       +28.57    14.5%  ################
  Sunday          1,900      +328.57    17.3%  ###################

=== days above the weekly average ===
  mask    : [False False False  True  True  True  True]
  days    : ['Thursday', 'Friday', 'Saturday', 'Sunday']
  amounts : [1800 2100 1600 1900]
  they contributed Rs.7,400 (67.3% of the week)

=== weekday vs weekend ===
  weekdays (Mon-Fri) : Rs.7,500  avg Rs.1,500.00
  weekend  (Sat-Sun) : Rs.3,500  avg Rs.1,750.00
  weekend uplift     : +16.7%

=== day-on-day change ===
  Monday     -> Tuesday        +300    +25.0%
  Tuesday    -> Wednesday      -600    -40.0%
  Wednesday  -> Thursday       +900   +100.0%
  Thursday   -> Friday         +300    +16.7%
  Friday     -> Saturday       -500    -23.8%
  Saturday   -> Sunday         +300    +18.8%
  biggest jump : Thursday (+900)
  biggest drop : Wednesday (-600)

=== vectorised what-if scenarios ===
  10% growth next week  : [1320 1650  990 1980 2310 1760 2090] -> Rs.12,100
  GST at 18% collected  : [216. 270. 162. 324. 378. 288. 342.]
  Rs.300 fixed cost/day : [ 900 1200  600 1500 1800 1300 1600] -> profit Rs.8,900
  days meeting the Rs.1,500 target: 5 of 7 -> ['Tuesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

=== 3-day moving average (np.convolve) ===
  Mon-Wed : Rs.1,200.00
  Tue-Thu : Rs.1,400.00
  Wed-Fri : Rs.1,600.00
  Thu-Sat : Rs.1,833.33
  Fri-Sun : Rs.1,866.67

```

</details>

---

## Experiment 10 - Question 3: Stock Price Analysis

Scenario: Closing stock prices for 5 companies are stored in a 2D array (5x5),
one row per company and one column per trading day.

Task:
  1) Find the average stock price of each company (row-wise).
  2) Find the day with the highest overall stock price.

Rubrics covered:
  * 2D array handling
  * correct row-wise average (axis=1)
  * highest price logic
  * result display

Requires: numpy

**File:** [`q3_stock_price_2d.py`](q3_stock_price_2d.py) &nbsp;&middot;&nbsp; **Run:** `python q3_stock_price_2d.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 10 - Question 3: Stock Price Analysis

Scenario: Closing stock prices for 5 companies are stored in a 2D array (5x5),
one row per company and one column per trading day.

Task:
  1) Find the average stock price of each company (row-wise).
  2) Find the day with the highest overall stock price.

Rubrics covered:
  * 2D array handling
  * correct row-wise average (axis=1)
  * highest price logic
  * result display

Requires: numpy
"""

import numpy as np

COMPANIES = ["TCS", "INFY", "RELIANCE", "HDFCBANK", "WIPRO"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]


def main():
    prices = np.array([
        [3850.00, 3920.50, 3870.25, 3990.00, 4015.75],   # TCS
        [1480.00, 1495.25, 1460.50, 1510.00, 1525.50],   # INFY
        [2890.50, 2935.00, 2910.75, 2880.25, 2955.00],   # RELIANCE
        [1620.00, 1605.50, 1640.00, 1655.75, 1648.25],   # HDFCBANK
        [ 452.00,  448.75,  455.50,  461.00,  458.25],   # WIPRO
    ])

    print("=== 2D price array ===")
    print(f"  shape {prices.shape}, dtype {prices.dtype}, "
          f"{prices.size} values, {prices.nbytes} bytes")
    print(f"\n  {'company':<10}" + "".join(f"{d:>11}" for d in DAYS))
    print("  " + "-" * 65)
    for name, row in zip(COMPANIES, prices):
        print(f"  {name:<10}" + "".join(f"{v:>11,.2f}" for v in row))

    # 1) row-wise average, axis=1 collapses the columns
    row_avg = prices.mean(axis=1)
    print("\n=== 1) average price per company (axis=1) ===")
    print(f"  prices.mean(axis=1) -> {np.round(row_avg, 2)}")
    print(f"\n  {'company':<10}{'average':>12}{'low':>11}{'high':>11}"
          f"{'swing':>9}")
    for name, avg, lo, hi in zip(COMPANIES, row_avg,
                                 prices.min(axis=1), prices.max(axis=1)):
        print(f"  {name:<10}{avg:>12,.2f}{lo:>11,.2f}{hi:>11,.2f}"
              f"{hi - lo:>9,.2f}")
    print(f"\n  costliest company on average : "
          f"{COMPANIES[row_avg.argmax()]} (Rs.{row_avg.max():,.2f})")
    print(f"  cheapest company on average  : "
          f"{COMPANIES[row_avg.argmin()]} (Rs.{row_avg.min():,.2f})")

    # 2) the single highest price in the whole array
    flat_index = prices.argmax()
    company_i, day_i = np.unravel_index(flat_index, prices.shape)

    print("\n=== 2) highest overall stock price ===")
    print(f"  prices.max()             : Rs.{prices.max():,.2f}")
    print(f"  prices.argmax()          : {flat_index} (flattened index)")
    print(f"  np.unravel_index(...)    : row {company_i}, column {day_i}")
    print(f"  that is {COMPANIES[company_i]} on {DAYS[day_i]} "
          f"at Rs.{prices[company_i, day_i]:,.2f}")

    col_sum = prices.sum(axis=0)
    print("\n=== the day with the highest total market value (axis=0) ===")
    print(f"  prices.sum(axis=0) -> {np.round(col_sum, 2)}")
    for day, total in zip(DAYS, col_sum):
        print(f"  {day:<5}Rs.{total:>12,.2f}  {'#' * int(total / 400)}")
    print(f"\n  strongest day : {DAYS[col_sum.argmax()]} "
          f"(Rs.{col_sum.max():,.2f})")
    print(f"  weakest day   : {DAYS[col_sum.argmin()]} "
          f"(Rs.{col_sum.min():,.2f})")

    print("\n=== column-wise average (axis=0) ===")
    col_avg = prices.mean(axis=0)
    for day, avg in zip(DAYS, col_avg):
        print(f"  {day:<5}Rs.{avg:>11,.2f}")

    print("\n=== axis recap ===")
    print(f"  prices.mean()        : {prices.mean():,.2f}  (every value)")
    print(f"  prices.mean(axis=0)  : shape {col_avg.shape} -> per day")
    print(f"  prices.mean(axis=1)  : shape {row_avg.shape} -> per company")

    print("\n=== weekly return per company ===")
    returns = (prices[:, -1] - prices[:, 0]) / prices[:, 0] * 100
    for name, open_, close, pct in zip(COMPANIES, prices[:, 0],
                                       prices[:, -1], returns):
        arrow = "up  " if pct > 0 else "down"
        print(f"  {name:<10}{open_:>10,.2f} -> {close:>10,.2f}  "
              f"{pct:>+7.2f}%  {arrow}")
    print(f"\n  best performer  : {COMPANIES[returns.argmax()]} "
          f"({returns.max():+.2f}%)")
    print(f"  worst performer : {COMPANIES[returns.argmin()]} "
          f"({returns.min():+.2f}%)")

    print("\n=== volatility (standard deviation per company) ===")
    vol = prices.std(axis=1)
    for name, v, avg in zip(COMPANIES, vol, row_avg):
        print(f"  {name:<10}Rs.{v:>8,.2f}  "
              f"({v / avg * 100:.2f}% of its average price)")
    print(f"  most volatile : {COMPANIES[vol.argmax()]}")

    print("\n=== slicing the 2D array ===")
    print(f"  prices[0]        (TCS row)      : {prices[0]}")
    print(f"  prices[:, 0]     (Monday col)   : {prices[:, 0]}")
    print(f"  prices[1:3, 2:4] (sub-block)    :\n{prices[1:3, 2:4]}")
    print(f"  diagonal                        : {np.round(prices.diagonal(), 2)}")
    print(f"  transpose shape                 : {prices.T.shape}")

    print("\n=== prices above Rs.2,000 ===")
    mask = prices > 2000
    print(f"  count : {int(mask.sum())} of {prices.size}")
    rows, cols = np.where(mask)
    for r, c in zip(rows, cols):
        print(f"    {COMPANIES[r]:<10}{DAYS[c]:<5}Rs.{prices[r, c]:,.2f}")


if __name__ == "__main__":
    main()
```

</details>

<details>
<summary>Program output</summary>

```text
=== 2D price array ===
  shape (5, 5), dtype float64, 25 values, 200 bytes

  company           Mon        Tue        Wed        Thu        Fri
  -----------------------------------------------------------------
  TCS          3,850.00   3,920.50   3,870.25   3,990.00   4,015.75
  INFY         1,480.00   1,495.25   1,460.50   1,510.00   1,525.50
  RELIANCE     2,890.50   2,935.00   2,910.75   2,880.25   2,955.00
  HDFCBANK     1,620.00   1,605.50   1,640.00   1,655.75   1,648.25
  WIPRO          452.00     448.75     455.50     461.00     458.25

=== 1) average price per company (axis=1) ===
  prices.mean(axis=1) -> [3929.3  1494.25 2914.3  1633.9   455.1 ]

  company        average        low       high    swing
  TCS           3,929.30   3,850.00   4,015.75   165.75
  INFY          1,494.25   1,460.50   1,525.50    65.00
  RELIANCE      2,914.30   2,880.25   2,955.00    74.75
  HDFCBANK      1,633.90   1,605.50   1,655.75    50.25
  WIPRO           455.10     448.75     461.00    12.25

  costliest company on average : TCS (Rs.3,929.30)
  cheapest company on average  : WIPRO (Rs.455.10)

=== 2) highest overall stock price ===
  prices.max()             : Rs.4,015.75
  prices.argmax()          : 4 (flattened index)
  np.unravel_index(...)    : row 0, column 4
  that is TCS on Fri at Rs.4,015.75

=== the day with the highest total market value (axis=0) ===
  prices.sum(axis=0) -> [10292.5  10405.   10337.   10497.   10602.75]
  Mon  Rs.   10,292.50  #########################
  Tue  Rs.   10,405.00  ##########################
  Wed  Rs.   10,337.00  #########################
  Thu  Rs.   10,497.00  ##########################
  Fri  Rs.   10,602.75  ##########################

  strongest day : Fri (Rs.10,602.75)
  weakest day   : Mon (Rs.10,292.50)

=== column-wise average (axis=0) ===
  Mon  Rs.   2,058.50
  Tue  Rs.   2,081.00
  Wed  Rs.   2,067.40
  Thu  Rs.   2,099.40
  Fri  Rs.   2,120.55

=== axis recap ===
  prices.mean()        : 2,085.37  (every value)
  prices.mean(axis=0)  : shape (5,) -> per day
  prices.mean(axis=1)  : shape (5,) -> per company

=== weekly return per company ===
  TCS         3,850.00 ->   4,015.75    +4.31%  up  
  INFY        1,480.00 ->   1,525.50    +3.07%  up  
  RELIANCE    2,890.50 ->   2,955.00    +2.23%  up  
  HDFCBANK    1,620.00 ->   1,648.25    +1.74%  up  
  WIPRO         452.00 ->     458.25    +1.38%  up  

  best performer  : TCS (+4.31%)
  worst performer : WIPRO (+1.38%)

=== volatility (standard deviation per company) ===
  TCS       Rs.   64.82  (1.65% of its average price)
  INFY      Rs.   22.66  (1.52% of its average price)
  RELIANCE  Rs.   27.65  (0.95% of its average price)
  HDFCBANK  Rs.   18.55  (1.14% of its average price)
  WIPRO     Rs.    4.35  (0.96% of its average price)
  most volatile : TCS

=== slicing the 2D array ===
  prices[0]        (TCS row)      : [3850.   3920.5  3870.25 3990.   4015.75]
  prices[:, 0]     (Monday col)   : [3850.  1480.  2890.5 1620.   452. ]
  prices[1:3, 2:4] (sub-block)    :
[[1460.5  1510.  ]
 [2910.75 2880.25]]
  diagonal                        : [3850.   1495.25 2910.75 1655.75  458.25]
  transpose shape                 : (5, 5)

=== prices above Rs.2,000 ===
  count : 10 of 25
    TCS       Mon  Rs.3,850.00
    TCS       Tue  Rs.3,920.50
    TCS       Wed  Rs.3,870.25
    TCS       Thu  Rs.3,990.00
    TCS       Fri  Rs.4,015.75
    RELIANCE  Mon  Rs.2,890.50
    RELIANCE  Tue  Rs.2,935.00
    RELIANCE  Wed  Rs.2,910.75
    RELIANCE  Thu  Rs.2,880.25
    RELIANCE  Fri  Rs.2,955.00

```

</details>

---

## Experiment 10 - Question 4: Matrix Operations

Scenario: Two 3x3 matrices represent transformations.

Task:
  1) Perform addition, subtraction and matrix multiplication between them.

Rubrics covered:
  * array creation
  * element-wise operations
  * matrix multiplication (np.dot or @)
  * correct results

Requires: numpy

**File:** [`q4_matrix_operations.py`](q4_matrix_operations.py) &nbsp;&middot;&nbsp; **Run:** `python q4_matrix_operations.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 10 - Question 4: Matrix Operations

Scenario: Two 3x3 matrices represent transformations.

Task:
  1) Perform addition, subtraction and matrix multiplication between them.

Rubrics covered:
  * array creation
  * element-wise operations
  * matrix multiplication (np.dot or @)
  * correct results

Requires: numpy
"""

import numpy as np


def show(label, matrix):
    print(f"\n  {label}")
    for row in matrix:
        print("    [" + "  ".join(f"{v:>8.2f}" if matrix.dtype.kind == "f"
                                  else f"{v:>5}" for v in row) + "]")


def main():
    A = np.array([[2, 0, 1],
                  [1, 3, 2],
                  [4, 1, 0]])

    B = np.array([[1, 2, 0],
                  [0, 1, 3],
                  [2, 1, 1]])

    print("=== the two 3x3 matrices ===")
    show("A =", A)
    show("B =", B)
    print(f"\n  A.shape {A.shape}, B.shape {B.shape}, dtype {A.dtype}")

    print("\n=== 1) addition (element-wise) ===")
    show("A + B =", A + B)
    print(f"  same as np.add(A, B) : {np.array_equal(A + B, np.add(A, B))}")

    print("\n=== 2) subtraction (element-wise) ===")
    show("A - B =", A - B)
    show("B - A =", B - A)
    print(f"  subtraction is not commutative: "
          f"{not np.array_equal(A - B, B - A)}")

    print("\n=== 3) matrix multiplication ===")
    product = A @ B
    show("A @ B =", product)
    print(f"  np.dot(A, B) gives the same : "
          f"{np.array_equal(product, np.dot(A, B))}")
    print(f"  np.matmul(A, B) too         : "
          f"{np.array_equal(product, np.matmul(A, B))}")
    show("B @ A =", B @ A)
    print(f"  matrix multiplication is not commutative: "
          f"{not np.array_equal(A @ B, B @ A)}")

    print("\n  how one cell is computed:")
    print(f"    (A @ B)[0, 0] = row A[0] . column B[:, 0]")
    print(f"                  = {A[0]} . {B[:, 0]}")
    print(f"                  = {' + '.join(f'{a}*{b}' for a, b in zip(A[0], B[:, 0]))}"
          f" = {product[0, 0]}")

    print("\n=== element-wise multiplication is a different operation ===")
    show("A * B (Hadamard) =", A * B)
    print(f"  A * B equals A @ B : {np.array_equal(A * B, A @ B)}")

    print("\n=== other transformations ===")
    show("A transposed =", A.T)
    print(f"  trace(A)        : {np.trace(A)}")
    print(f"  det(A)          : {np.linalg.det(A):.4f}")
    print(f"  det(B)          : {np.linalg.det(B):.4f}")
    print(f"  rank(A)         : {np.linalg.matrix_rank(A)}")

    if abs(np.linalg.det(A)) > 1e-9:
        inverse = np.linalg.inv(A)
        show("inverse of A =", inverse)
        identity = A @ inverse
        show("A @ inv(A) =", np.round(identity, 10))
        print(f"  equals the identity matrix : "
              f"{np.allclose(identity, np.eye(3))}")
    else:
        print("  A is singular, no inverse exists")

    print("\n=== scalar operations ===")
    show("A * 3 =", A * 3)
    show("A + 10 =", A + 10)
    show("A ** 2 (element-wise) =", A ** 2)
    show("matrix power A @ A =", np.linalg.matrix_power(A, 2))

    print("\n=== applying the transformations to a vector ===")
    v = np.array([1, 2, 3])
    print(f"  v        = {v}")
    print(f"  A @ v    = {A @ v}")
    print(f"  B @ v    = {B @ v}")
    print(f"  A @ B @ v= {A @ B @ v}")
    print(f"  (A@B) @ v == A @ (B @ v) : "
          f"{np.array_equal((A @ B) @ v, A @ (B @ v))}  "
          f"(matrix multiplication is associative)")

    print("\n=== aggregates ===")
    print(f"  A.sum()        : {A.sum()}")
    print(f"  A.sum(axis=0)  : {A.sum(axis=0)}  (column totals)")
    print(f"  A.sum(axis=1)  : {A.sum(axis=1)}  (row totals)")
    print(f"  A.max(), A.min(): {A.max()}, {A.min()}")
    print(f"  A.mean()       : {A.mean():.4f}")

    print("\n=== solving a linear system A x = b ===")
    b = np.array([5, 11, 9])
    if abs(np.linalg.det(A)) > 1e-9:
        x = np.linalg.solve(A, b)
        print(f"  b            = {b}")
        print(f"  x            = {np.round(x, 4)}")
        print(f"  check A @ x  = {np.round(A @ x, 4)}")
        print(f"  matches b    : {np.allclose(A @ x, b)}")

    print("\n=== eigenvalues of A ===")
    values = np.linalg.eigvals(A)
    print(f"  {np.round(values, 4)}")
    print(f"  sum of eigenvalues {np.real(values.sum()):.4f} "
          f"equals trace(A) {np.trace(A)}: "
          f"{np.isclose(np.real(values.sum()), np.trace(A))}")


if __name__ == "__main__":
    main()
```

</details>

<details>
<summary>Program output</summary>

```text
=== the two 3x3 matrices ===

  A =
    [    2      0      1]
    [    1      3      2]
    [    4      1      0]

  B =
    [    1      2      0]
    [    0      1      3]
    [    2      1      1]

  A.shape (3, 3), B.shape (3, 3), dtype int64

=== 1) addition (element-wise) ===

  A + B =
    [    3      2      1]
    [    1      4      5]
    [    6      2      1]
  same as np.add(A, B) : True

=== 2) subtraction (element-wise) ===

  A - B =
    [    1     -2      1]
    [    1      2     -1]
    [    2      0     -1]

  B - A =
    [   -1      2     -1]
    [   -1     -2      1]
    [   -2      0      1]
  subtraction is not commutative: True

=== 3) matrix multiplication ===

  A @ B =
    [    4      5      1]
    [    5      7     11]
    [    4      9      3]
  np.dot(A, B) gives the same : True
  np.matmul(A, B) too         : True

  B @ A =
    [    4      6      5]
    [   13      6      2]
    [    9      4      4]
  matrix multiplication is not commutative: True

  how one cell is computed:
    (A @ B)[0, 0] = row A[0] . column B[:, 0]
                  = [2 0 1] . [1 0 2]
                  = 2*1 + 0*0 + 1*2 = 4

=== element-wise multiplication is a different operation ===

  A * B (Hadamard) =
    [    2      0      0]
    [    0      3      6]
    [    8      1      0]
  A * B equals A @ B : False

=== other transformations ===

  A transposed =
    [    2      1      4]
    [    0      3      1]
    [    1      2      0]
  trace(A)        : 5
  det(A)          : -15.0000
  det(B)          : 10.0000
  rank(A)         : 3

  inverse of A =
    [    0.13     -0.07      0.20]
    [   -0.53      0.27      0.20]
    [    0.73      0.13     -0.40]

  A @ inv(A) =
    [    1.00     -0.00      0.00]
    [    0.00      1.00      0.00]
    [    0.00      0.00      1.00]
  equals the identity matrix : True

=== scalar operations ===

  A * 3 =
    [    6      0      3]
    [    3      9      6]
    [   12      3      0]

  A + 10 =
    [   12     10     11]
    [   11     13     12]
    [   14     11     10]

  A ** 2 (element-wise) =
    [    4      0      1]
    [    1      9      4]
    [   16      1      0]

  matrix power A @ A =
    [    8      1      2]
    [   13     11      7]
    [    9      3      6]

=== applying the transformations to a vector ===
  v        = [1 2 3]
  A @ v    = [ 5 13  6]
  B @ v    = [ 5 11  7]
  A @ B @ v= [17 52 31]
  (A@B) @ v == A @ (B @ v) : True  (matrix multiplication is associative)

=== aggregates ===
  A.sum()        : 14
  A.sum(axis=0)  : [7 4 3]  (column totals)
  A.sum(axis=1)  : [3 6 5]  (row totals)
  A.max(), A.min(): 4, 0
  A.mean()       : 1.5556

=== solving a linear system A x = b ===
  b            = [ 5 11  9]
  x            = [1.7333 2.0667 1.5333]
  check A @ x  = [ 5. 11.  9.]
  matches b    : True

=== eigenvalues of A ===
  [-1.5171+0.j  2.4036+0.j  4.1135+0.j]
  sum of eigenvalues 5.0000 equals trace(A) 5: True

```

</details>

---

## Experiment 10 - Question 5: Product Inventory Check

Scenario: A shop records the number of products sold in 4 categories across
5 days.

Task:
  1) Represent this as a 2D array.
  2) Find the total items sold per category and per day.

Rubrics covered:
  * array creation
  * row-wise and column-wise sum (axis=1, axis=0)
  * clear display of both results
  * accuracy

Requires: numpy

**File:** [`q5_product_inventory.py`](q5_product_inventory.py) &nbsp;&middot;&nbsp; **Run:** `python q5_product_inventory.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 10 - Question 5: Product Inventory Check

Scenario: A shop records the number of products sold in 4 categories across
5 days.

Task:
  1) Represent this as a 2D array.
  2) Find the total items sold per category and per day.

Rubrics covered:
  * array creation
  * row-wise and column-wise sum (axis=1, axis=0)
  * clear display of both results
  * accuracy

Requires: numpy
"""

import numpy as np

CATEGORIES = ["Medicines", "Devices", "Protective", "Supplements"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]


def main():
    # 1) the 2D array: rows = categories, columns = days
    sold = np.array([
        [142, 158, 131, 177, 190],     # Medicines
        [ 18,  22,  15,  27,  31],     # Devices
        [ 64,  71,  58,  83,  92],     # Protective
        [ 35,  41,  29,  46,  52],     # Supplements
    ])

    print("=== 2D inventory array ===")
    print(f"  shape {sold.shape} -> "
          f"{sold.shape[0]} categories x {sold.shape[1]} days")
    print(f"  dtype {sold.dtype}, {sold.size} values")
    print(f"\n  {'category':<13}" + "".join(f"{d:>7}" for d in DAYS))
    print("  " + "-" * 48)
    for name, row in zip(CATEGORIES, sold):
        print(f"  {name:<13}" + "".join(f"{v:>7}" for v in row))

    # 2a) per category: sum across the days -> axis=1
    per_category = sold.sum(axis=1)
    # 2b) per day: sum across the categories -> axis=0
    per_day = sold.sum(axis=0)
    grand_total = sold.sum()

    print("\n=== total per category (axis=1, collapses days) ===")
    print(f"  sold.sum(axis=1) -> {per_category}")
    print(f"\n  {'category':<13}{'units':>8}{'share':>9}{'daily avg':>12}  bar")
    for name, total, avg in zip(CATEGORIES, per_category,
                                sold.mean(axis=1)):
        print(f"  {name:<13}{total:>8,}{total / grand_total * 100:>8.1f}%"
              f"{avg:>12.1f}  {'#' * (total // 25)}")

    print("\n=== total per day (axis=0, collapses categories) ===")
    print(f"  sold.sum(axis=0) -> {per_day}")
    print(f"\n  {'day':<6}{'units':>8}{'share':>9}  bar")
    for day, total in zip(DAYS, per_day):
        print(f"  {day:<6}{total:>8,}{total / grand_total * 100:>8.1f}%  "
              f"{'#' * (total // 20)}")

    print("\n=== cross-check ===")
    print(f"  grand total (sold.sum())        : {grand_total:,}")
    print(f"  sum of category totals          : {per_category.sum():,}")
    print(f"  sum of day totals               : {per_day.sum():,}")
    print(f"  all three agree                 : "
          f"{grand_total == per_category.sum() == per_day.sum()}")

    print("\n=== full table with margins ===")
    print(f"  {'category':<13}" + "".join(f"{d:>7}" for d in DAYS) +
          f"{'TOTAL':>9}")
    print("  " + "-" * 58)
    for name, row, total in zip(CATEGORIES, sold, per_category):
        print(f"  {name:<13}" + "".join(f"{v:>7}" for v in row) +
              f"{total:>9,}")
    print("  " + "-" * 58)
    print(f"  {'TOTAL':<13}" + "".join(f"{v:>7}" for v in per_day) +
          f"{grand_total:>9,}")

    print("\n=== highlights ===")
    print(f"  best-selling category : {CATEGORIES[per_category.argmax()]} "
          f"({per_category.max():,} units)")
    print(f"  slowest category      : {CATEGORIES[per_category.argmin()]} "
          f"({per_category.min():,} units)")
    print(f"  busiest day           : {DAYS[per_day.argmax()]} "
          f"({per_day.max():,} units)")
    print(f"  quietest day          : {DAYS[per_day.argmin()]} "
          f"({per_day.min():,} units)")
    r, c = np.unravel_index(sold.argmax(), sold.shape)
    print(f"  single biggest cell   : {CATEGORIES[r]} on {DAYS[c]} "
          f"({sold[r, c]} units)")

    print("\n=== percentage breakdown per day (keepdims broadcasting) ===")
    share = sold / sold.sum(axis=0, keepdims=True) * 100
    print(f"  {'category':<13}" + "".join(f"{d:>8}" for d in DAYS))
    for name, row in zip(CATEGORIES, share):
        print(f"  {name:<13}" + "".join(f"{v:>7.1f}%" for v in row))

    print("\n=== day-on-day growth, whole shop ===")
    change = np.diff(per_day)
    for i, delta in enumerate(change):
        pct = delta / per_day[i] * 100
        print(f"  {DAYS[i]} -> {DAYS[i + 1]} : {delta:>+5} units "
              f"({pct:>+6.1f}%)")

    print("\n=== restocking signal: categories averaging over 50 a day ===")
    avg_per_day = sold.mean(axis=1)
    mask = avg_per_day > 50
    for name, avg in zip(np.array(CATEGORIES)[mask], avg_per_day[mask]):
        print(f"  {name:<13}{avg:>6.1f} units/day -> order "
              f"{int(np.ceil(avg * 7))} for next week")

    print("\n=== cumulative sales through the week ===")
    cumulative = sold.cumsum(axis=1)
    print(f"  {'category':<13}" + "".join(f"{d:>8}" for d in DAYS))
    for name, row in zip(CATEGORIES, cumulative):
        print(f"  {name:<13}" + "".join(f"{v:>8,}" for v in row))


if __name__ == "__main__":
    main()
```

</details>

<details>
<summary>Program output</summary>

```text
=== 2D inventory array ===
  shape (4, 5) -> 4 categories x 5 days
  dtype int64, 20 values

  category         Mon    Tue    Wed    Thu    Fri
  ------------------------------------------------
  Medicines        142    158    131    177    190
  Devices           18     22     15     27     31
  Protective        64     71     58     83     92
  Supplements       35     41     29     46     52

=== total per category (axis=1, collapses days) ===
  sold.sum(axis=1) -> [798 113 368 203]

  category        units    share   daily avg  bar
  Medicines         798    53.8%       159.6  ###############################
  Devices           113     7.6%        22.6  ####
  Protective        368    24.8%        73.6  ##############
  Supplements       203    13.7%        40.6  ########

=== total per day (axis=0, collapses categories) ===
  sold.sum(axis=0) -> [259 292 233 333 365]

  day      units    share  bar
  Mon        259    17.5%  ############
  Tue        292    19.7%  ##############
  Wed        233    15.7%  ###########
  Thu        333    22.5%  ################
  Fri        365    24.6%  ##################

=== cross-check ===
  grand total (sold.sum())        : 1,482
  sum of category totals          : 1,482
  sum of day totals               : 1,482
  all three agree                 : True

=== full table with margins ===
  category         Mon    Tue    Wed    Thu    Fri    TOTAL
  ----------------------------------------------------------
  Medicines        142    158    131    177    190      798
  Devices           18     22     15     27     31      113
  Protective        64     71     58     83     92      368
  Supplements       35     41     29     46     52      203
  ----------------------------------------------------------
  TOTAL            259    292    233    333    365    1,482

=== highlights ===
  best-selling category : Medicines (798 units)
  slowest category      : Devices (113 units)
  busiest day           : Fri (365 units)
  quietest day          : Wed (233 units)
  single biggest cell   : Medicines on Fri (190 units)

=== percentage breakdown per day (keepdims broadcasting) ===
  category          Mon     Tue     Wed     Thu     Fri
  Medicines       54.8%   54.1%   56.2%   53.2%   52.1%
  Devices          6.9%    7.5%    6.4%    8.1%    8.5%
  Protective      24.7%   24.3%   24.9%   24.9%   25.2%
  Supplements     13.5%   14.0%   12.4%   13.8%   14.2%

=== day-on-day growth, whole shop ===
  Mon -> Tue :   +33 units ( +12.7%)
  Tue -> Wed :   -59 units ( -20.2%)
  Wed -> Thu :  +100 units ( +42.9%)
  Thu -> Fri :   +32 units (  +9.6%)

=== restocking signal: categories averaging over 50 a day ===
  Medicines     159.6 units/day -> order 1118 for next week
  Protective     73.6 units/day -> order 516 for next week

=== cumulative sales through the week ===
  category          Mon     Tue     Wed     Thu     Fri
  Medicines         142     300     431     608     798
  Devices            18      40      55      82     113
  Protective         64     135     193     276     368
  Supplements        35      76     105     151     203

```

</details>

---

## Experiment 10 - Question 6: Weather Dataset Operations

Scenario: Rainfall data (in mm) is available for 12 months.

Task:
  1) Compute the total and average annual rainfall.
  2) Identify the months with rainfall above 100 mm.

Rubrics covered:
  * array handling
  * use of aggregation functions (sum, mean)
  * logical indexing (> 100)
  * correct output

Requires: numpy

**File:** [`q6_rainfall_analysis.py`](q6_rainfall_analysis.py) &nbsp;&middot;&nbsp; **Run:** `python q6_rainfall_analysis.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 10 - Question 6: Weather Dataset Operations

Scenario: Rainfall data (in mm) is available for 12 months.

Task:
  1) Compute the total and average annual rainfall.
  2) Identify the months with rainfall above 100 mm.

Rubrics covered:
  * array handling
  * use of aggregation functions (sum, mean)
  * logical indexing (> 100)
  * correct output

Requires: numpy
"""

import numpy as np

MONTHS = np.array(["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
THRESHOLD = 100.0


def main():
    # Pune-like monsoon pattern, mm per month
    rainfall = np.array([2.5, 1.0, 3.5, 12.0, 38.5, 142.0,
                         187.5, 164.0, 128.5, 74.0, 21.5, 6.0])

    print("=== the rainfall array ===")
    print(f"  values : {rainfall}")
    print(f"  shape {rainfall.shape}, dtype {rainfall.dtype}")

    total = rainfall.sum()
    average = rainfall.mean()

    print("\n=== 1) annual totals ===")
    print(f"  total annual rainfall   : {total:,.1f} mm")
    print(f"  average monthly rainfall: {average:,.2f} mm")
    print(f"  median                  : {np.median(rainfall):,.2f} mm")
    print(f"  standard deviation      : {rainfall.std():,.2f} mm")
    print(f"  wettest month           : {MONTHS[rainfall.argmax()]} "
          f"({rainfall.max():,.1f} mm)")
    print(f"  driest month            : {MONTHS[rainfall.argmin()]} "
          f"({rainfall.min():,.1f} mm)")

    print("\n=== monthly chart ===")
    print(f"  {'month':<7}{'mm':>8}{'share':>9}  bar")
    for month, mm in zip(MONTHS, rainfall):
        flag = "  <== above 100 mm" if mm > THRESHOLD else ""
        print(f"  {month:<7}{mm:>8.1f}{mm / total * 100:>8.1f}%  "
              f"{'#' * int(mm / 4)}{flag}")

    # 2) logical indexing
    mask = rainfall > THRESHOLD
    heavy_months = MONTHS[mask]
    heavy_values = rainfall[mask]

    print(f"\n=== 2) months above {THRESHOLD:.0f} mm (logical indexing) ===")
    print(f"  mask            : {mask}")
    print(f"  np.where(mask)  : {np.where(mask)[0]}")
    print(f"  months          : {heavy_months.tolist()}")
    print(f"  values          : {heavy_values}")
    print(f"  count           : {int(mask.sum())} of {rainfall.size}")
    print(f"  they carry      : {heavy_values.sum():,.1f} mm "
          f"({heavy_values.sum() / total * 100:.1f}% of the annual rainfall)")
    print(f"  their average   : {heavy_values.mean():,.2f} mm")

    print("\n  month by month:")
    for month, mm in zip(heavy_months, heavy_values):
        print(f"    {month:<5}{mm:>8.1f} mm  ({mm - THRESHOLD:+.1f} mm "
              f"above the threshold)")

    print("\n=== how the count changes with the threshold ===")
    for t in (50, 75, 100, 125, 150, 175):
        picked = MONTHS[rainfall > t]
        print(f"  above {t:>3} mm : {len(picked)} month(s)  "
              f"{picked.tolist()}")

    print("\n=== seasonal split (reshape into quarters) ===")
    quarters = rainfall.reshape(4, 3)
    labels = ["Q1 Jan-Mar", "Q2 Apr-Jun", "Q3 Jul-Sep", "Q4 Oct-Dec"]
    print(f"  reshaped to {quarters.shape}")
    for label, row, q_total in zip(labels, quarters, quarters.sum(axis=1)):
        print(f"  {label:<12}{row}  total {q_total:>7.1f} mm  "
              f"({q_total / total * 100:>5.1f}%)")
    print(f"\n  wettest quarter : {labels[quarters.sum(axis=1).argmax()]}")

    monsoon = rainfall[5:9]            # Jun to Sep
    rest = np.concatenate([rainfall[:5], rainfall[9:]])
    print("\n=== monsoon (Jun-Sep) vs the rest of the year ===")
    print(f"  monsoon    : {monsoon.sum():>7.1f} mm over 4 months  "
          f"(avg {monsoon.mean():.1f} mm)")
    print(f"  other      : {rest.sum():>7.1f} mm over 8 months  "
          f"(avg {rest.mean():.1f} mm)")
    print(f"  monsoon share: {monsoon.sum() / total * 100:.1f}% of the year")

    print("\n=== cumulative rainfall ===")
    cumulative = rainfall.cumsum()
    for month, value in zip(MONTHS, cumulative):
        print(f"  by end of {month} : {value:>8.1f} mm  "
              f"({value / total * 100:>5.1f}% of the year)")

    print("\n=== month-on-month change ===")
    change = np.diff(rainfall)
    print(f"  biggest rise : {MONTHS[change.argmax() + 1]} "
          f"({change.max():+.1f} mm)")
    print(f"  biggest fall : {MONTHS[change.argmin() + 1]} "
          f"({change.min():+.1f} mm)")

    print("\n=== dry months (under 10 mm) ===")
    dry = rainfall < 10
    print(f"  {MONTHS[dry].tolist()} -> {rainfall[dry]} mm")
    print(f"  {int(dry.sum())} effectively dry month(s)")

    print("\n=== np.select classification ===")
    labels_rain = np.select(
        [rainfall > 150, rainfall > 100, rainfall > 50, rainfall > 10],
        ["very heavy", "heavy", "moderate", "light"], default="negligible")
    for month, mm, label in zip(MONTHS, rainfall, labels_rain):
        print(f"  {month:<5}{mm:>8.1f} mm  {label}")


if __name__ == "__main__":
    main()
```

</details>

<details>
<summary>Program output</summary>

```text
=== the rainfall array ===
  values : [  2.5   1.    3.5  12.   38.5 142.  187.5 164.  128.5  74.   21.5   6. ]
  shape (12,), dtype float64

=== 1) annual totals ===
  total annual rainfall   : 781.0 mm
  average monthly rainfall: 65.08 mm
  median                  : 30.00 mm
  standard deviation      : 68.02 mm
  wettest month           : Jul (187.5 mm)
  driest month            : Feb (1.0 mm)

=== monthly chart ===
  month        mm    share  bar
  Jan         2.5     0.3%  
  Feb         1.0     0.1%  
  Mar         3.5     0.4%  
  Apr        12.0     1.5%  ###
  May        38.5     4.9%  #########
  Jun       142.0    18.2%  ###################################  <== above 100 mm
  Jul       187.5    24.0%  ##############################################  <== above 100 mm
  Aug       164.0    21.0%  #########################################  <== above 100 mm
  Sep       128.5    16.5%  ################################  <== above 100 mm
  Oct        74.0     9.5%  ##################
  Nov        21.5     2.8%  #####
  Dec         6.0     0.8%  #

=== 2) months above 100 mm (logical indexing) ===
  mask            : [False False False False False  True  True  True  True False False False]
  np.where(mask)  : [5 6 7 8]
  months          : ['Jun', 'Jul', 'Aug', 'Sep']
  values          : [142.  187.5 164.  128.5]
  count           : 4 of 12
  they carry      : 622.0 mm (79.6% of the annual rainfall)
  their average   : 155.50 mm

  month by month:
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

=== seasonal split (reshape into quarters) ===
  reshaped to (4, 3)
  Q1 Jan-Mar  [2.5 1.  3.5]  total     7.0 mm  (  0.9%)
  Q2 Apr-Jun  [ 12.   38.5 142. ]  total   192.5 mm  ( 24.6%)
  Q3 Jul-Sep  [187.5 164.  128.5]  total   480.0 mm  ( 61.5%)
  Q4 Oct-Dec  [74.  21.5  6. ]  total   101.5 mm  ( 13.0%)

  wettest quarter : Q3 Jul-Sep

=== monsoon (Jun-Sep) vs the rest of the year ===
  monsoon    :   622.0 mm over 4 months  (avg 155.5 mm)
  other      :   159.0 mm over 8 months  (avg 19.9 mm)
  monsoon share: 79.6% of the year

=== cumulative rainfall ===
  by end of Jan :      2.5 mm  (  0.3% of the year)
  by end of Feb :      3.5 mm  (  0.4% of the year)
  by end of Mar :      7.0 mm  (  0.9% of the year)
  by end of Apr :     19.0 mm  (  2.4% of the year)
  by end of May :     57.5 mm  (  7.4% of the year)
  by end of Jun :    199.5 mm  ( 25.5% of the year)
  by end of Jul :    387.0 mm  ( 49.6% of the year)
  by end of Aug :    551.0 mm  ( 70.6% of the year)
  by end of Sep :    679.5 mm  ( 87.0% of the year)
  by end of Oct :    753.5 mm  ( 96.5% of the year)
  by end of Nov :    775.0 mm  ( 99.2% of the year)
  by end of Dec :    781.0 mm  (100.0% of the year)

=== month-on-month change ===
  biggest rise : Jun (+103.5 mm)
  biggest fall : Oct (-54.5 mm)

=== dry months (under 10 mm) ===
  ['Jan', 'Feb', 'Mar', 'Dec'] -> [2.5 1.  3.5 6. ] mm
  4 effectively dry month(s)

=== np.select classification ===
  Jan       2.5 mm  negligible
  Feb       1.0 mm  negligible
  Mar       3.5 mm  negligible
  Apr      12.0 mm  light
  May      38.5 mm  light
  Jun     142.0 mm  heavy
  Jul     187.5 mm  very heavy
  Aug     164.0 mm  very heavy
  Sep     128.5 mm  heavy
  Oct      74.0 mm  moderate
  Nov      21.5 mm  light
  Dec       6.0 mm  negligible

```

</details>

---

## Experiment 10 - Question 7: E-commerce Order Analysis

Scenario: An e-commerce company stores order amounts in a NumPy array.

Task:
  1) Find how many orders are above Rs.1000.
  2) Calculate the percentage of such orders.

Rubrics covered:
  * array creation
  * logical condition (> 1000)
  * percentage calculation
  * correct output

Requires: numpy

**File:** [`q7_ecommerce_orders.py`](q7_ecommerce_orders.py) &nbsp;&middot;&nbsp; **Run:** `python q7_ecommerce_orders.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 10 - Question 7: E-commerce Order Analysis

Scenario: An e-commerce company stores order amounts in a NumPy array.

Task:
  1) Find how many orders are above Rs.1000.
  2) Calculate the percentage of such orders.

Rubrics covered:
  * array creation
  * logical condition (> 1000)
  * percentage calculation
  * correct output

Requires: numpy
"""

import numpy as np

THRESHOLD = 1000


def main():
    rng = np.random.default_rng(seed=2026)
    # a realistic long tail: many small orders, a few large ones
    orders = np.round(rng.lognormal(mean=6.4, sigma=0.9, size=40), 2)

    print("=== the order array ===")
    print(f"  orders generated : {orders.size}")
    print(f"  dtype {orders.dtype}, shape {orders.shape}, "
          f"{orders.nbytes} bytes")
    print("\n  values (Rs.):")
    for i in range(0, orders.size, 8):
        chunk = orders[i:i + 8]
        print(f"    {i:>2}-{i + len(chunk) - 1:<3}" +
              "".join(f"{v:>11,.2f}" for v in chunk))

    # 1) logical condition and count
    mask = orders > THRESHOLD
    high_value = orders[mask]
    count = int(mask.sum())

    # 2) percentage
    percent = count / orders.size * 100

    print(f"\n=== 1) orders above Rs.{THRESHOLD:,} ===")
    print(f"  condition      : orders > {THRESHOLD}")
    print(f"  boolean mask   : {mask[:12]} ... (first 12)")
    print(f"  count          : mask.sum() = {count}")
    print(f"  indices        : {np.where(mask)[0].tolist()}")

    print(f"\n=== 2) percentage of such orders ===")
    print(f"  {count} / {orders.size} x 100 = {percent:.2f}%")
    print(f"  the same via mask.mean() : {mask.mean() * 100:.2f}%")

    print(f"\n=== value contributed by those orders ===")
    print(f"  total order value       : Rs.{orders.sum():,.2f}")
    print(f"  value above Rs.{THRESHOLD:,}   : Rs.{high_value.sum():,.2f}")
    print(f"  share of total revenue  : "
          f"{high_value.sum() / orders.sum() * 100:.2f}%")
    print(f"  so {percent:.1f}% of orders bring in "
          f"{high_value.sum() / orders.sum() * 100:.1f}% of the revenue")

    print("\n=== the high-value orders ===")
    for i, value in zip(np.where(mask)[0], high_value):
        print(f"  order #{i:<4}Rs.{value:>11,.2f}  "
              f"({value / THRESHOLD:.2f}x the threshold)")

    print("\n=== overall statistics ===")
    print(f"  minimum  : Rs.{orders.min():>11,.2f}")
    print(f"  maximum  : Rs.{orders.max():>11,.2f} (order #{orders.argmax()})")
    print(f"  mean     : Rs.{orders.mean():>11,.2f}")
    print(f"  median   : Rs.{np.median(orders):>11,.2f}")
    print(f"  std dev  : Rs.{orders.std():>11,.2f}")
    print(f"  the mean sits above the median, the classic long-tail shape")

    print("\n=== percentiles ===")
    for p in (10, 25, 50, 75, 90, 95, 99):
        print(f"  p{p:<3} : Rs.{np.percentile(orders, p):>11,.2f}")

    print("\n=== how the answer moves with the threshold ===")
    print(f"  {'threshold':>11}{'orders':>9}{'percent':>10}{'revenue share':>16}")
    for t in (250, 500, 750, 1000, 1500, 2000, 3000):
        m = orders > t
        rev = orders[m].sum() / orders.sum() * 100 if m.any() else 0.0
        print(f"  Rs.{t:>8,}{int(m.sum()):>9}{m.mean() * 100:>9.2f}%"
              f"{rev:>15.2f}%")

    print("\n=== order size bands (np.histogram) ===")
    bins = np.array([0, 250, 500, 1000, 2000, 5000, np.inf])
    counts, _ = np.histogram(orders, bins=bins)
    labels = ["0-250", "250-500", "500-1000", "1000-2000",
              "2000-5000", "5000+"]
    for label, n in zip(labels, counts):
        print(f"  Rs.{label:<12}{n:>3} order(s)  "
              f"{n / orders.size * 100:>5.1f}%  {'#' * n}")

    print("\n=== combined conditions ===")
    mid = (orders > 500) & (orders <= 1000)
    print(f"  between Rs.500 and Rs.1,000 : {int(mid.sum())} order(s) "
          f"({mid.mean() * 100:.2f}%)")
    small_or_huge = (orders < 300) | (orders > 3000)
    print(f"  under Rs.300 or over Rs.3,000: {int(small_or_huge.sum())} "
          f"order(s) ({small_or_huge.mean() * 100:.2f}%)")

    print("\n=== np.where to tag every order ===")
    tags = np.where(orders > THRESHOLD, "HIGH", "normal")
    print(f"  first 10 tags : {tags[:10].tolist()}")
    print(f"  HIGH count    : {int((tags == 'HIGH').sum())}")

    print("\n=== business summary ===")
    print(f"  {orders.size} orders worth Rs.{orders.sum():,.2f}")
    print(f"  {count} order(s) above Rs.{THRESHOLD:,} ({percent:.2f}%)")
    print(f"  average order value Rs.{orders.mean():,.2f}")
    print(f"  raising the free-delivery bar to Rs.{THRESHOLD:,} would cover "
          f"{percent:.1f}% of orders")


if __name__ == "__main__":
    main()
```

</details>

<details>
<summary>Program output</summary>

```text
=== the order array ===
  orders generated : 40
  dtype float64, shape (40,), 320 bytes

  values (Rs.):
     0-7       294.77     747.34     109.21   2,113.70   1,068.99     462.74     454.52     791.12
     8-15      473.00     491.12   1,150.63     956.46     568.09     557.28     695.63     346.33
    16-23      418.48     985.78     535.16     174.69     391.68   1,086.76     488.31     526.44
    24-31    1,072.40   3,109.29     316.76   2,025.12     198.94     704.49     210.07   2,031.06
    32-39    1,274.78   1,675.63     271.24   1,114.43     377.24     398.76     949.45   1,324.84

=== 1) orders above Rs.1,000 ===
  condition      : orders > 1000
  boolean mask   : [False False False  True  True False False False False False  True False] ... (first 12)
  count          : mask.sum() = 12
  indices        : [3, 4, 10, 21, 24, 25, 27, 31, 32, 33, 35, 39]

=== 2) percentage of such orders ===
  12 / 40 x 100 = 30.00%
  the same via mask.mean() : 30.00%

=== value contributed by those orders ===
  total order value       : Rs.32,942.73
  value above Rs.1,000   : Rs.19,047.63
  share of total revenue  : 57.82%
  so 30.0% of orders bring in 57.8% of the revenue

=== the high-value orders ===
  order #3   Rs.   2,113.70  (2.11x the threshold)
  order #4   Rs.   1,068.99  (1.07x the threshold)
  order #10  Rs.   1,150.63  (1.15x the threshold)
  order #21  Rs.   1,086.76  (1.09x the threshold)
  order #24  Rs.   1,072.40  (1.07x the threshold)
  order #25  Rs.   3,109.29  (3.11x the threshold)
  order #27  Rs.   2,025.12  (2.03x the threshold)
  order #31  Rs.   2,031.06  (2.03x the threshold)
  order #32  Rs.   1,274.78  (1.27x the threshold)
  order #33  Rs.   1,675.63  (1.68x the threshold)
  order #35  Rs.   1,114.43  (1.11x the threshold)
  order #39  Rs.   1,324.84  (1.32x the threshold)

=== overall statistics ===
  minimum  : Rs.     109.21
  maximum  : Rs.   3,109.29 (order #25)
  mean     : Rs.     823.57
  median   : Rs.     562.68
  std dev  : Rs.     629.86
  the mean sits above the median, the classic long-tail shape

=== percentiles ===
  p10  : Rs.     265.12
  p25  : Rs.     396.99
  p50  : Rs.     562.68
  p75  : Rs.   1,075.99
  p90  : Rs.   1,710.58
  p95  : Rs.   2,035.19
  p99  : Rs.   2,721.01

=== how the answer moves with the threshold ===
    threshold   orders   percent   revenue share
  Rs.     250       36    90.00%          97.90%
  Rs.     500       23    57.50%          82.16%
  Rs.     750       16    40.00%          69.00%
  Rs.   1,000       12    30.00%          57.82%
  Rs.   1,500        5    12.50%          33.25%
  Rs.   2,000        4    10.00%          28.17%
  Rs.   3,000        1     2.50%           9.44%

=== order size bands (np.histogram) ===
  Rs.0-250         4 order(s)   10.0%  ####
  Rs.250-500      13 order(s)   32.5%  #############
  Rs.500-1000     11 order(s)   27.5%  ###########
  Rs.1000-2000     8 order(s)   20.0%  ########
  Rs.2000-5000     4 order(s)   10.0%  ####
  Rs.5000+         0 order(s)    0.0%  

=== combined conditions ===
  between Rs.500 and Rs.1,000 : 11 order(s) (27.50%)
  under Rs.300 or over Rs.3,000: 7 order(s) (17.50%)

=== np.where to tag every order ===
  first 10 tags : ['normal', 'normal', 'normal', 'HIGH', 'HIGH', 'normal', 'normal', 'normal', 'normal', 'normal']
  HIGH count    : 12

=== business summary ===
  40 orders worth Rs.32,942.73
  12 order(s) above Rs.1,000 (30.00%)
  average order value Rs.823.57
  raising the free-delivery bar to Rs.1,000 would cover 30.0% of orders

```

</details>

---

## Experiment 10 - Question 8: Scientific Experiment Data

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

**File:** [`q8_experiment_trials.py`](q8_experiment_trials.py) &nbsp;&middot;&nbsp; **Run:** `python q8_experiment_trials.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== 5x4 reading array ===
  shape (5, 4), dtype float64, 20 readings

  experiment         Trial 1   Trial 2   Trial 3   Trial 4
  ---------------------------------------------------------
  E1 Catalyst A        12.40     13.10     12.90     13.60
  E2 Catalyst B        15.80     16.20     15.50     17.10
  E3 Control            9.20      9.00      9.40      8.80
  E4 Catalyst C        14.10     13.80     18.90     14.40
  E5 Catalyst D        16.00     15.70     16.40     16.10

=== 1) average per experiment (axis=1) ===
  readings.mean(axis=1) -> [13.   16.15  9.1  15.3  16.05]

  experiment           mean     std     min     max   spread
  E1 Catalyst A      13.000   0.430   12.40   13.60     1.20
  E2 Catalyst B      16.150   0.602   15.50   17.10     1.60
  E3 Control          9.100   0.224    8.80    9.40     0.60
  E4 Catalyst C      15.300   2.089   13.80   18.90     5.10
  E5 Catalyst D      16.050   0.250   15.70   16.40     0.70

  best experiment  : E2 Catalyst B (mean 16.150)
  worst experiment : E3 Control (mean 9.100)

=== 2) maximum overall reading ===
  np.max(readings)      : 18.90
  np.argmax(readings)   : 14  (index into the flattened array)
  np.unravel_index      : row 3, column 2
  that is E4 Catalyst C, Trial 3 -> 18.90
  flattened array       : [12.4 13.1 12.9 13.6 15.8 16.2 15.5 17.1  9.2  9.   9.4  8.8 14.1 13.8
 18.9 14.4 16.  15.7 16.4 16.1]
  element 14 of the flat array is 18.90

=== best trial inside each experiment (argmax with axis=1) ===
  E1 Catalyst A   Trial 4     13.60
  E2 Catalyst B   Trial 4     17.10
  E3 Control      Trial 3      9.40
  E4 Catalyst C   Trial 3     18.90
  E5 Catalyst D   Trial 3     16.40

=== column-wise view: which trial number performs best? ===
  readings.mean(axis=0) -> [13.5  13.56 14.62 14.  ]
  Trial 1  mean   13.500  ###########################
  Trial 2  mean   13.560  ###########################
  Trial 3  mean   14.620  #############################
  Trial 4  mean   14.000  ############################
  strongest trial slot : Trial 3

=== repeatability check (lower std is better) ===
  1. E3 Control      std  0.224  highly repeatable
  2. E5 Catalyst D   std  0.250  highly repeatable
  3. E1 Catalyst A   std  0.430  highly repeatable
  4. E2 Catalyst B   std  0.602  acceptable
  5. E4 Catalyst C   std  2.089  poor, suspect an outlier

=== outlier detection (more than 2 std from its row mean) ===
  E4 Catalyst C   Trial 3     18.90  (1.72 std from its row mean 15.30)

=== comparison against the control (E3) ===
  E1 Catalyst A     13.000    +42.86% vs control (9.100)
  E2 Catalyst B     16.150    +77.47% vs control (9.100)
  E4 Catalyst C     15.300    +68.13% vs control (9.100)
  E5 Catalyst D     16.050    +76.37% vs control (9.100)

=== whole-dataset summary ===
  grand mean   : 13.920
  overall std  : 2.847
  minimum      : 8.80 at (np.int64(2), np.int64(3))
  maximum      : 18.90 at (np.int64(3), np.int64(2))
  range        : 10.10

```

</details>

---

## Experiment 10 - Question 9: Medical Data Analysis

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

**File:** [`q9_medical_blood_sugar.py`](q9_medical_blood_sugar.py) &nbsp;&middot;&nbsp; **Run:** `python q9_medical_blood_sugar.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== 5x4 blood sugar array (mg/dL) ===
  shape (5, 4), dtype int64

  patient             Morning      Noon   Evening     Night
  ----------------------------------------------------------
  P-101 Sharma             92       148       134       110
  P-102 Andhale            86       132       121        98
  P-103 Kulkarni          128       196       178       152
  P-104 Deshmukh           74       118       109        88
  P-105 Patil             112       172       160       131

=== 1) daily average per patient (axis=1) ===
  sugar.mean(axis=1) -> [121.   109.25 163.5   97.25 143.75]

  patient            daily avg    min    max   swing  status
  P-101 Sharma          121.00     92    148      56  borderline
  P-102 Andhale         109.25     86    132      46  within range
  P-103 Kulkarni        163.50    128    196      68  diabetic range
  P-104 Deshmukh         97.25     74    118      44  within range
  P-105 Patil           143.75    112    172      60  pre-diabetic

  highest daily average : P-103 Kulkarni (163.50 mg/dL)
  lowest daily average  : P-104 Deshmukh (97.25 mg/dL)

=== 2) average by time of day (axis=0) ===
  sugar.mean(axis=0) -> [ 98.4 153.2 140.4 115.8]

  time         average    min    max  bar
  Morning        98.40     74    128  ########################
  Noon          153.20    118    196  ######################################  <== highest
  Evening       140.40    109    178  ###################################
  Night         115.80     88    152  ############################

  np.argmax(sugar.mean(axis=0)) = 1
  the highest average blood sugar occurs at Noon (153.20 mg/dL)
  the lowest is at Morning (98.40 mg/dL)
  morning-to-noon rise: +54.80 mg/dL on average (the post-meal spike)

=== axis recap ===
  sugar.mean()       : 126.95  (all 20 readings)
  sugar.mean(axis=0) : shape (4,) -> one per time
  sugar.mean(axis=1) : shape (5,) -> one per patient

=== clinical flags ===
  fasting (Morning) normal range 70-100 mg/dL
    P-101 Sharma        92 mg/dL  normal
    P-102 Andhale       86 mg/dL  normal
    P-103 Kulkarni     128 mg/dL  HIGH fasting (+28 above normal)
    P-104 Deshmukh      74 mg/dL  normal
    P-105 Patil        112 mg/dL  HIGH fasting (+12 above normal)

  post-meal readings above 140 mg/dL:
    P-101 Sharma     Noon       148 mg/dL
    P-103 Kulkarni   Noon       196 mg/dL
    P-103 Kulkarni   Evening    178 mg/dL
    P-103 Kulkarni   Night      152 mg/dL
    P-105 Patil      Noon       172 mg/dL
    P-105 Patil      Evening    160 mg/dL
  total out-of-range post-meal readings: 6 of 15

=== patients needing review (any reading above 180) ===
  P-103 Kulkarni   [128 196 178 152]  peak 196 mg/dL

=== ward-level summary ===
  patients monitored : 5
  readings per day   : 4
  ward average       : 126.95 mg/dL
  ward median        : 124.50 mg/dL
  overall peak       : 196 mg/dL (P-103 Kulkarni at Noon)
  patients above 140 daily average: 2 of 5

=== normalised per patient (how each reading compares to that patient's own average) ===
  patient             Morning      Noon   Evening     Night
  P-101 Sharma          -29.0     +27.0     +13.0     -11.0
  P-102 Andhale         -23.2     +22.8     +11.8     -11.2
  P-103 Kulkarni        -35.5     +32.5     +14.5     -11.5
  P-104 Deshmukh        -23.2     +20.8     +11.8      -9.2
  P-105 Patil           -31.8     +28.2     +16.2     -12.8

```

</details>

---

## Experiment 10 - Question 10: Electricity Consumption Analysis

Scenario: A housing society records electricity consumption (in kWh) for
6 apartments over 7 days in a 6x7 NumPy array.

Task:
  1) Find the total consumption for each apartment (row-wise).
  2) Identify the apartment with the highest total consumption.

Rubrics covered:
  * correct 2D array representation
  * row-wise operation using axis
  * correct identification of the highest consumer
  * output clarity

Requires: numpy

**File:** [`q10_electricity_consumption.py`](q10_electricity_consumption.py) &nbsp;&middot;&nbsp; **Run:** `python q10_electricity_consumption.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 10 - Question 10: Electricity Consumption Analysis

Scenario: A housing society records electricity consumption (in kWh) for
6 apartments over 7 days in a 6x7 NumPy array.

Task:
  1) Find the total consumption for each apartment (row-wise).
  2) Identify the apartment with the highest total consumption.

Rubrics covered:
  * correct 2D array representation
  * row-wise operation using axis
  * correct identification of the highest consumer
  * output clarity

Requires: numpy
"""

import numpy as np

FLATS = ["A-101", "A-102", "B-201", "B-202", "C-301", "C-302"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
TARIFF = 8.40          # Rs. per kWh


def main():
    usage = np.array([
        [12.4, 11.8, 13.1, 12.0, 14.2, 18.5, 17.9],    # A-101
        [ 8.2,  7.9,  8.6,  8.1,  9.0, 11.4, 10.8],    # A-102
        [21.5, 22.8, 20.9, 23.4, 24.1, 27.6, 26.2],    # B-201
        [ 5.1,  4.8,  5.4,  5.0,  5.6,  7.2,  6.9],    # B-202
        [15.8, 16.4, 15.2, 16.9, 17.5, 20.3, 19.1],    # C-301
        [10.2, 10.8,  9.9, 11.1, 11.8, 14.0, 13.2],    # C-302
    ])

    print("=== 6x7 consumption array (kWh) ===")
    print(f"  shape {usage.shape} -> "
          f"{usage.shape[0]} apartments x {usage.shape[1]} days")
    print(f"  dtype {usage.dtype}, {usage.size} readings")
    print(f"\n  {'flat':<8}" + "".join(f"{d:>8}" for d in DAYS))
    print("  " + "-" * 64)
    for name, row in zip(FLATS, usage):
        print(f"  {name:<8}" + "".join(f"{v:>8.1f}" for v in row))

    # 1) row-wise total, axis=1 collapses the days
    per_flat = usage.sum(axis=1)

    print("\n=== 1) weekly total per apartment (axis=1) ===")
    print(f"  usage.sum(axis=1) -> {np.round(per_flat, 1)}")
    print(f"\n  {'flat':<8}{'total kWh':>11}{'daily avg':>12}"
          f"{'peak day':>11}{'bill':>12}  bar")
    for name, total, avg, peak in zip(FLATS, per_flat, usage.mean(axis=1),
                                      usage.argmax(axis=1)):
        print(f"  {name:<8}{total:>11.1f}{avg:>12.2f}"
              f"{DAYS[peak]:>11}{total * TARIFF:>11,.2f}  "
              f"{'#' * int(total / 4)}")

    # 2) the highest consumer
    top = per_flat.argmax()

    print("\n=== 2) highest consumer ===")
    print(f"  per_flat.argmax() -> index {top}")
    print(f"  apartment         : {FLATS[top]}")
    print(f"  weekly total      : {per_flat[top]:.1f} kWh")
    print(f"  daily average     : {usage[top].mean():.2f} kWh")
    print(f"  weekly bill       : Rs.{per_flat[top] * TARIFF:,.2f}")
    print(f"  readings          : {usage[top]}")
    print(f"  it used {per_flat[top] / per_flat.mean():.2f}x the society "
          f"average and {per_flat[top] / per_flat.min():.2f}x the lowest flat")

    print(f"\n  lowest consumer   : {FLATS[per_flat.argmin()]} "
          f"({per_flat.min():.1f} kWh, Rs.{per_flat.min() * TARIFF:,.2f})")

    print("\n=== consumption ranking ===")
    order = np.argsort(-per_flat)
    print(f"  {'rank':<6}{'flat':<8}{'kWh':>9}{'share':>9}{'bill':>12}")
    for rank, i in enumerate(order, 1):
        print(f"  {rank:<6}{FLATS[i]:<8}{per_flat[i]:>9.1f}"
              f"{per_flat[i] / per_flat.sum() * 100:>8.1f}%"
              f"{per_flat[i] * TARIFF:>11,.2f}")

    print("\n=== daily totals for the whole society (axis=0) ===")
    per_day = usage.sum(axis=0)
    print(f"  usage.sum(axis=0) -> {np.round(per_day, 1)}")
    for day, total in zip(DAYS, per_day):
        print(f"  {day:<5}{total:>8.1f} kWh  {'#' * int(total / 3)}")
    print(f"\n  busiest day : {DAYS[per_day.argmax()]} "
          f"({per_day.max():.1f} kWh)")
    print(f"  quietest day: {DAYS[per_day.argmin()]} "
          f"({per_day.min():.1f} kWh)")

    print("\n=== weekday vs weekend ===")
    weekday = usage[:, :5]
    weekend = usage[:, 5:]
    print(f"  weekday total : {weekday.sum():>8.1f} kWh over 5 days "
          f"(avg {weekday.sum() / 5:.1f} kWh/day)")
    print(f"  weekend total : {weekend.sum():>8.1f} kWh over 2 days "
          f"(avg {weekend.sum() / 2:.1f} kWh/day)")
    print(f"  weekend uplift: "
          f"{(weekend.sum() / 2) / (weekday.sum() / 5) * 100 - 100:+.1f}%")

    print("\n=== full table with margins ===")
    print(f"  {'flat':<8}" + "".join(f"{d:>8}" for d in DAYS) +
          f"{'TOTAL':>10}")
    print("  " + "-" * 74)
    for name, row, total in zip(FLATS, usage, per_flat):
        print(f"  {name:<8}" + "".join(f"{v:>8.1f}" for v in row) +
              f"{total:>10.1f}")
    print("  " + "-" * 74)
    print(f"  {'TOTAL':<8}" + "".join(f"{v:>8.1f}" for v in per_day) +
          f"{usage.sum():>10.1f}")

    print("\n=== society billing summary ===")
    print(f"  total units consumed : {usage.sum():.1f} kWh")
    print(f"  tariff               : Rs.{TARIFF:.2f} per kWh")
    print(f"  total bill           : Rs.{usage.sum() * TARIFF:,.2f}")
    print(f"  average per flat     : {per_flat.mean():.2f} kWh "
          f"(Rs.{per_flat.mean() * TARIFF:,.2f})")
    print(f"  median per flat      : {np.median(per_flat):.2f} kWh")
    print(f"  standard deviation   : {per_flat.std():.2f} kWh")

    print("\n=== flats above the society average ===")
    mask = per_flat > per_flat.mean()
    for name, total in zip(np.array(FLATS)[mask], per_flat[mask]):
        excess = total - per_flat.mean()
        print(f"  {name:<8}{total:>8.1f} kWh  "
              f"{excess:+.1f} kWh above average "
              f"(Rs.{excess * TARIFF:,.2f} extra)")

    print("\n=== slab check (over 150 kWh a month attracts a higher tariff) ===")
    projected = per_flat / 7 * 30
    for name, month in zip(FLATS, projected):
        slab = ("high slab" if month > 150 else
                "mid slab" if month > 100 else "low slab")
        print(f"  {name:<8}projected {month:>7.1f} kWh/month  {slab}")


if __name__ == "__main__":
    main()
```

</details>

<details>
<summary>Program output</summary>

```text
=== 6x7 consumption array (kWh) ===
  shape (6, 7) -> 6 apartments x 7 days
  dtype float64, 42 readings

  flat         Mon     Tue     Wed     Thu     Fri     Sat     Sun
  ----------------------------------------------------------------
  A-101       12.4    11.8    13.1    12.0    14.2    18.5    17.9
  A-102        8.2     7.9     8.6     8.1     9.0    11.4    10.8
  B-201       21.5    22.8    20.9    23.4    24.1    27.6    26.2
  B-202        5.1     4.8     5.4     5.0     5.6     7.2     6.9
  C-301       15.8    16.4    15.2    16.9    17.5    20.3    19.1
  C-302       10.2    10.8     9.9    11.1    11.8    14.0    13.2

=== 1) weekly total per apartment (axis=1) ===
  usage.sum(axis=1) -> [ 99.9  64.  166.5  40.  121.2  81. ]

  flat      total kWh   daily avg   peak day        bill  bar
  A-101          99.9       14.27        Sat     839.16  ########################
  A-102          64.0        9.14        Sat     537.60  ################
  B-201         166.5       23.79        Sat   1,398.60  #########################################
  B-202          40.0        5.71        Sat     336.00  ##########
  C-301         121.2       17.31        Sat   1,018.08  ##############################
  C-302          81.0       11.57        Sat     680.40  ####################

=== 2) highest consumer ===
  per_flat.argmax() -> index 2
  apartment         : B-201
  weekly total      : 166.5 kWh
  daily average     : 23.79 kWh
  weekly bill       : Rs.1,398.60
  readings          : [21.5 22.8 20.9 23.4 24.1 27.6 26.2]
  it used 1.74x the society average and 4.16x the lowest flat

  lowest consumer   : B-202 (40.0 kWh, Rs.336.00)

=== consumption ranking ===
  rank  flat          kWh    share        bill
  1     B-201       166.5    29.1%   1,398.60
  2     C-301       121.2    21.2%   1,018.08
  3     A-101        99.9    17.4%     839.16
  4     C-302        81.0    14.1%     680.40
  5     A-102        64.0    11.2%     537.60
  6     B-202        40.0     7.0%     336.00

=== daily totals for the whole society (axis=0) ===
  usage.sum(axis=0) -> [73.2 74.5 73.1 76.5 82.2 99.  94.1]
  Mon      73.2 kWh  ########################
  Tue      74.5 kWh  ########################
  Wed      73.1 kWh  ########################
  Thu      76.5 kWh  #########################
  Fri      82.2 kWh  ###########################
  Sat      99.0 kWh  #################################
  Sun      94.1 kWh  ###############################

  busiest day : Sat (99.0 kWh)
  quietest day: Wed (73.1 kWh)

=== weekday vs weekend ===
  weekday total :    379.5 kWh over 5 days (avg 75.9 kWh/day)
  weekend total :    193.1 kWh over 2 days (avg 96.5 kWh/day)
  weekend uplift: +27.2%

=== full table with margins ===
  flat         Mon     Tue     Wed     Thu     Fri     Sat     Sun     TOTAL
  --------------------------------------------------------------------------
  A-101       12.4    11.8    13.1    12.0    14.2    18.5    17.9      99.9
  A-102        8.2     7.9     8.6     8.1     9.0    11.4    10.8      64.0
  B-201       21.5    22.8    20.9    23.4    24.1    27.6    26.2     166.5
  B-202        5.1     4.8     5.4     5.0     5.6     7.2     6.9      40.0
  C-301       15.8    16.4    15.2    16.9    17.5    20.3    19.1     121.2
  C-302       10.2    10.8     9.9    11.1    11.8    14.0    13.2      81.0
  --------------------------------------------------------------------------
  TOTAL       73.2    74.5    73.1    76.5    82.2    99.0    94.1     572.6

=== society billing summary ===
  total units consumed : 572.6 kWh
  tariff               : Rs.8.40 per kWh
  total bill           : Rs.4,809.84
  average per flat     : 95.43 kWh (Rs.801.64)
  median per flat      : 90.45 kWh
  standard deviation   : 40.83 kWh

=== flats above the society average ===
  A-101       99.9 kWh  +4.5 kWh above average (Rs.37.52 extra)
  B-201      166.5 kWh  +71.1 kWh above average (Rs.596.96 extra)
  C-301      121.2 kWh  +25.8 kWh above average (Rs.216.44 extra)

=== slab check (over 150 kWh a month attracts a higher tariff) ===
  A-101   projected   428.1 kWh/month  high slab
  A-102   projected   274.3 kWh/month  high slab
  B-201   projected   713.6 kWh/month  high slab
  B-202   projected   171.4 kWh/month  high slab
  C-301   projected   519.4 kWh/month  high slab
  C-302   projected   347.1 kWh/month  high slab

```

</details>

---
