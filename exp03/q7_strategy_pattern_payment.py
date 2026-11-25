"""
Experiment 3 - Question 7: Strategy Pattern Payment

Scenario: Users select different payment strategies: CreditCard, UPI or Wallet.

Rubrics covered:
  * strategy classes defined
  * strategy switched at runtime
  * a context class executes the chosen strategy
  * realistic use case
"""

from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    """Strategy interface."""

    name = "strategy"

    @abstractmethod
    def pay(self, amount):
        ...

    def fee(self, amount):
        return 0.0


class CreditCardStrategy(PaymentStrategy):
    name = "CreditCard"

    def __init__(self, holder, number, cvv, limit=50000):
        self.holder = holder
        self.number = number
        self.cvv = cvv
        self.limit = limit
        self.spent = 0.0

    def fee(self, amount):
        return round(amount * 0.015, 2)      # 1.5% MDR

    def pay(self, amount):
        total = amount + self.fee(amount)
        if self.spent + total > self.limit:
            print(f"   DECLINED: limit Rs.{self.limit:,.0f}, "
                  f"already spent Rs.{self.spent:,.2f}")
            return False
        self.spent += total
        print(f"   Paid Rs.{total:,.2f} with card ****{self.number[-4:]} "
              f"({self.holder}), 3-D Secure OK")
        return True


class UPIStrategy(PaymentStrategy):
    name = "UPI"

    def __init__(self, upi_id, balance):
        self.upi_id = upi_id
        self.balance = balance

    def pay(self, amount):
        if amount > self.balance:
            print(f"   DECLINED: UPI balance Rs.{self.balance:,.2f}")
            return False
        self.balance -= amount
        print(f"   Paid Rs.{amount:,.2f} via {self.upi_id} (zero fee), "
              f"balance Rs.{self.balance:,.2f}")
        return True


class WalletStrategy(PaymentStrategy):
    name = "Wallet"

    def __init__(self, provider, balance, cashback_pct=2):
        self.provider = provider
        self.balance = balance
        self.cashback_pct = cashback_pct

    def pay(self, amount):
        if amount > self.balance:
            print(f"   DECLINED: {self.provider} has only Rs.{self.balance:,.2f}")
            return False
        self.balance -= amount
        cashback = round(amount * self.cashback_pct / 100, 2)
        self.balance += cashback
        print(f"   Paid Rs.{amount:,.2f} from {self.provider}, cashback "
              f"Rs.{cashback:,.2f}, balance Rs.{self.balance:,.2f}")
        return True


class CashOnDeliveryStrategy(PaymentStrategy):
    name = "COD"

    def fee(self, amount):
        return 40.0

    def pay(self, amount):
        print(f"   Collect Rs.{amount + self.fee(amount):,.2f} at the door "
              f"(includes Rs.{self.fee(amount):,.0f} handling)")
        return True


class CheckoutContext:
    """Context: holds a strategy and delegates to it. It can be swapped
    at any time without the context knowing the concrete class."""

    def __init__(self, customer, strategy=None):
        self.customer = customer
        self._strategy = strategy
        self.history = []

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        if not isinstance(strategy, PaymentStrategy):
            raise TypeError("needs a PaymentStrategy")
        print(f"[context] {self.customer} switched to {strategy.name}")
        self._strategy = strategy

    def checkout(self, amount):
        if self._strategy is None:
            print("[context] choose a payment method first")
            return False
        print(f"[context] paying Rs.{amount:,.2f} using {self._strategy.name} "
              f"(fee Rs.{self._strategy.fee(amount):,.2f})")
        ok = self._strategy.pay(amount)
        self.history.append((self._strategy.name, amount, ok))
        return ok


if __name__ == "__main__":
    card = CreditCardStrategy("Spandan Andhale", "4111111111115678", "123", 20000)
    upi = UPIStrategy("spandan@okaxis", 4000)
    wallet = WalletStrategy("Paytm", 1200)
    cod = CashOnDeliveryStrategy()

    cart = CheckoutContext("Spandan")

    print("=== no strategy chosen yet ===")
    cart.checkout(999)

    print("\n=== runtime switching between strategies ===")
    for strategy, amount in ((upi, 2499), (wallet, 899), (card, 15999),
                             (card, 9999), (cod, 599)):
        cart.strategy = strategy
        cart.checkout(amount)
        print()

    print("=== transaction history ===")
    for mode, amount, ok in cart.history:
        print(f"  {mode:<12} Rs.{amount:>9,.2f}  {'OK' if ok else 'DECLINED'}")

    print("\n=== picking a strategy from user input ===")
    options = {"1": card, "2": upi, "3": wallet, "4": cod}
    try:
        choice = input("1 Card  2 UPI  3 Wallet  4 COD : ").strip()
    except (EOFError, OSError):
        choice = ""
    picked = options.get(choice, upi)
    cart.strategy = picked
    cart.checkout(500)
