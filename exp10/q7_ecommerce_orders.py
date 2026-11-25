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
