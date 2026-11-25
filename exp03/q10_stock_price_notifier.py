"""
Experiment 3 - Question 10: Stock Price Notifier

Scenario: A stock monitoring app that notifies every subscribed user when the
price of a stock changes.

Rubrics covered:
  * Observer pattern used
  * subscribers added and removed
  * notification on every stock update
  * logs printed for each update
"""

from abc import ABC, abstractmethod
from datetime import datetime


class Subscriber(ABC):
    def __init__(self, name):
        self.name = name
        self.alerts = 0

    @abstractmethod
    def notify(self, symbol, old_price, new_price):
        ...

    def _log(self, text):
        self.alerts += 1
        stamp = datetime.now().strftime("%H:%M:%S")
        print(f"   [{stamp}] {self.name:<16} {text}")


class Stock:
    """Subject: holds the price and the subscriber list."""

    def __init__(self, symbol, price):
        self.symbol = symbol
        self._price = price
        self._subscribers = []
        self.log = []

    # ---- subscription management ----
    def add_subscriber(self, sub):
        if sub in self._subscribers:
            print(f"  {sub.name} already follows {self.symbol}")
            return False
        self._subscribers.append(sub)
        print(f"  + {sub.name} now follows {self.symbol} "
              f"({len(self._subscribers)} subscriber(s))")
        return True

    def remove_subscriber(self, sub):
        if sub not in self._subscribers:
            print(f"  {sub.name} does not follow {self.symbol}")
            return False
        self._subscribers.remove(sub)
        print(f"  - {sub.name} unfollowed {self.symbol} "
              f"({len(self._subscribers)} left)")
        return True

    # ---- price updates ----
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        old = self._price
        if new_price == old:
            print(f"\n[{self.symbol}] unchanged at Rs.{old:,.2f}, no notification")
            return
        self._price = new_price
        pct = (new_price - old) / old * 100
        entry = (f"{self.symbol} Rs.{old:,.2f} -> Rs.{new_price:,.2f} "
                 f"({pct:+.2f}%)")
        self.log.append(entry)
        print(f"\n[{self.symbol}] {entry}  notifying "
              f"{len(self._subscribers)} subscriber(s)")
        for sub in list(self._subscribers):
            sub.notify(self.symbol, old, new_price)


class RetailInvestor(Subscriber):
    def notify(self, symbol, old_price, new_price):
        direction = "UP" if new_price > old_price else "DOWN"
        self._log(f"{symbol} is {direction} to Rs.{new_price:,.2f}")


class ThresholdAlert(Subscriber):
    def __init__(self, name, buy_below, sell_above):
        super().__init__(name)
        self.buy_below = buy_below
        self.sell_above = sell_above

    def notify(self, symbol, old_price, new_price):
        if new_price <= self.buy_below:
            self._log(f"BUY SIGNAL {symbol} at Rs.{new_price:,.2f} "
                      f"(target <= {self.buy_below})")
        elif new_price >= self.sell_above:
            self._log(f"SELL SIGNAL {symbol} at Rs.{new_price:,.2f} "
                      f"(target >= {self.sell_above})")


class PortfolioTracker(Subscriber):
    def __init__(self, name, holdings):
        super().__init__(name)
        self.holdings = holdings           # symbol -> quantity

    def notify(self, symbol, old_price, new_price):
        qty = self.holdings.get(symbol, 0)
        if qty:
            change = (new_price - old_price) * qty
            self._log(f"{qty} shares of {symbol}: portfolio "
                      f"{change:+,.2f} (now Rs.{new_price * qty:,.2f})")


class VolatilityWatch(Subscriber):
    def notify(self, symbol, old_price, new_price):
        pct = abs(new_price - old_price) / old_price * 100
        if pct >= 5:
            self._log(f"VOLATILITY {pct:.2f}% move in {symbol}")


if __name__ == "__main__":
    tcs = Stock("TCS", 3850.00)

    spandan = RetailInvestor("Spandan")
    algo = ThresholdAlert("AlgoBot", buy_below=3600, sell_above=4100)
    portfolio = PortfolioTracker("PortfolioApp", {"TCS": 25})
    vol = VolatilityWatch("RiskDesk")

    print("=== subscriptions ===")
    for s in (spandan, algo, portfolio, vol):
        tcs.add_subscriber(s)
    tcs.add_subscriber(spandan)              # duplicate

    tcs.price = 3920.50
    tcs.price = 3920.50                      # no change, no notification
    tcs.price = 3570.00
    tcs.price = 4150.75

    print("\n=== one subscriber leaves ===")
    tcs.remove_subscriber(vol)
    tcs.remove_subscriber(RetailInvestor("Stranger"))
    tcs.price = 3999.00

    print("\n=== update log ===")
    for line in tcs.log:
        print("  ", line)

    print("\n=== alerts received ===")
    for s in (spandan, algo, portfolio, vol):
        print(f"  {s.name:<16} {s.alerts} alert(s)")
