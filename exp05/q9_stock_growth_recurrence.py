"""
Experiment 5 - Question 9: Stock Growth Prediction (Fibonacci-style recurrence)

Scenario: A stock app tracks price changes hourly. Predict future growth using
previous trends.

Rubrics covered:
  * hourly price changes generated
  * price growth modelled with a recurrence relation
  * next value predicted using DP
  * computed values stored to avoid repetition
"""

import random
import time
from functools import lru_cache

HOURS = 24


def generate_changes(seed=27):
    """Hourly percentage change in the stock price."""
    random.seed(seed)
    return [round(random.gauss(0.18, 1.1), 2) for _ in range(HOURS)]


def rebuild_prices(start, changes):
    prices = [start]
    for pct in changes:
        prices.append(round(prices[-1] * (1 + pct / 100), 2))
    return prices


# ---------- recurrence 1: momentum model, m(t) = a*m(t-1) + b*m(t-2) ----------
def momentum_naive(t, seed_values, a=0.6, b=0.3, counter=None):
    """Plain recursion: every call recomputes the same subproblems."""
    if counter is not None:
        counter["n"] += 1
    if t < len(seed_values):
        return seed_values[t]
    return (a * momentum_naive(t - 1, seed_values, a, b, counter) +
            b * momentum_naive(t - 2, seed_values, a, b, counter))


def momentum_memo(t, seed_values, a=0.6, b=0.3, memo=None, counter=None):
    """Top-down DP: each t is computed once and stored."""
    if memo is None:
        memo = {}
    if counter is not None:
        counter["n"] += 1
    if t < len(seed_values):
        return seed_values[t]
    if t in memo:
        return memo[t]
    memo[t] = (a * momentum_memo(t - 1, seed_values, a, b, memo, counter) +
               b * momentum_memo(t - 2, seed_values, a, b, memo, counter))
    return memo[t]


def momentum_bottom_up(n, seed_values, a=0.6, b=0.3):
    """Tabulation: fill the table forwards, no recursion at all."""
    table = list(seed_values)
    for t in range(len(seed_values), n + 1):
        table.append(a * table[t - 1] + b * table[t - 2])
    return table


# ---------- recurrence 2: Fibonacci-weighted forecast ----------
@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def fib_weighted_forecast(history, horizon=5, window=5):
    """Weight the last `window` observations by Fibonacci numbers, so the
    most recent hours matter most, then roll the forecast forward."""
    series = list(history)
    for _ in range(horizon):
        recent = series[-window:]
        weights = [fib(i + 2) for i in range(len(recent))]
        nxt = sum(v * w for v, w in zip(recent, weights)) / sum(weights)
        series.append(round(nxt, 3))
    return series[len(history):]


if __name__ == "__main__":
    changes = generate_changes()
    prices = rebuild_prices(1500.0, changes)

    print("=== hourly price changes and the resulting price ===")
    print(f"  {'hour':<6}{'change %':>10}{'price':>12}")
    for h, (pct, price) in enumerate(zip(changes, prices[1:])):
        arrow = "up" if pct > 0 else "down" if pct < 0 else "flat"
        print(f"  {h:<6}{pct:>+10.2f}{price:>12,.2f}  {arrow}")

    print(f"\n  opening price : Rs.{prices[0]:,.2f}")
    print(f"  closing price : Rs.{prices[-1]:,.2f}")
    print(f"  net move      : {(prices[-1] / prices[0] - 1) * 100:+.2f}%")
    print(f"  best hour     : {max(changes):+.2f}% at hour "
          f"{changes.index(max(changes))}")
    print(f"  worst hour    : {min(changes):+.2f}% at hour "
          f"{changes.index(min(changes))}")

    seed_values = changes[:2]
    print("\n=== momentum recurrence  m(t) = 0.6*m(t-1) + 0.3*m(t-2) ===")
    print(f"  seed: m(0)={seed_values[0]:+.2f}%, m(1)={seed_values[1]:+.2f}%")

    naive_counter = {"n": 0}
    memo_counter = {"n": 0}
    t = 22
    t0 = time.perf_counter()
    naive_val = momentum_naive(t, seed_values, counter=naive_counter)
    naive_ms = (time.perf_counter() - t0) * 1000
    t0 = time.perf_counter()
    memo_val = momentum_memo(t, seed_values, counter=memo_counter)
    memo_ms = (time.perf_counter() - t0) * 1000

    print(f"\n  m({t}) naive  = {naive_val:+.6f}%  "
          f"({naive_counter['n']:,} calls, {naive_ms:.2f} ms)")
    print(f"  m({t}) memo   = {memo_val:+.6f}%  "
          f"({memo_counter['n']:,} calls, {memo_ms:.3f} ms)")
    print(f"  identical            : {abs(naive_val - memo_val) < 1e-9}")
    print(f"  calls avoided        : "
          f"{naive_counter['n'] - memo_counter['n']:,} "
          f"({naive_counter['n'] / memo_counter['n']:.0f}x fewer)")

    table = momentum_bottom_up(t, seed_values)
    print(f"  bottom-up table[{t}] = {table[t]:+.6f}%  (matches: "
          f"{abs(table[t] - memo_val) < 1e-9})")

    print("\n=== stored subproblem table (bottom-up) ===")
    for h in range(0, len(table), 4):
        row = table[h:h + 4]
        print(f"  t={h:>2}-{h + len(row) - 1:<2} " +
              " ".join(f"{v:>+9.4f}" for v in row))

    print("\n=== Fibonacci-weighted forecast for the next 5 hours ===")
    forecast = fib_weighted_forecast(changes, horizon=5)
    future_price = prices[-1]
    print(f"  weights used (Fibonacci): "
          f"{[fib(i + 2) for i in range(5)]} - the latest hour weighs most")
    for i, pct in enumerate(forecast, 1):
        future_price = round(future_price * (1 + pct / 100), 2)
        print(f"  hour +{i}: predicted change {pct:+.3f}%  "
              f"-> price Rs.{future_price:,.2f}")
    print(f"\n  fib() cache after the run: {fib.cache_info()}")
    print(f"  predicted move over 5 hours: "
          f"{(future_price / prices[-1] - 1) * 100:+.2f}%")

    print("\n  Note: this is a lab exercise in recurrences and memoisation,")
    print("  not a trading model. Real prices are not Fibonacci-generated.")
