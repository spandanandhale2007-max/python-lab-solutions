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
