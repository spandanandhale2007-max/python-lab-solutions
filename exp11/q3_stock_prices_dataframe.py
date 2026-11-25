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
