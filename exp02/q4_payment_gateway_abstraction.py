"""
Experiment 2 - Question 4: Payment Gateway with Abstraction

Scenario: A payment gateway with modes like UPI, NetBanking and CreditCard,
each with its own implementation of pay().

Rubrics covered:
  * abstract base class Payment
  * all derived classes implemented
  * runtime selection of the payment mode
  * realistic flow and method design
"""

from abc import ABC, abstractmethod


class Payment(ABC):
    """Abstract base class: cannot be instantiated directly."""

    def __init__(self, payer):
        self.payer = payer
        self.receipts = []

    @abstractmethod
    def pay(self, amount):
        """Every mode must implement its own payment flow."""

    @abstractmethod
    def mode_name(self):
        ...

    def transaction_fee(self, amount):     # default policy, may be overridden
        return 0.0

    # concrete template method shared by all modes
    def checkout(self, amount):
        fee = self.transaction_fee(amount)
        print(f"\n[{self.mode_name()}] Checkout for {self.payer}: "
              f"Rs.{amount:,.2f} + fee Rs.{fee:,.2f}")
        ok = self.pay(amount + fee)
        if ok:
            self.receipts.append(amount + fee)
            print(f"[{self.mode_name()}] SUCCESS  total paid Rs.{amount + fee:,.2f}")
        else:
            print(f"[{self.mode_name()}] FAILED")
        return ok


class UPIPayment(Payment):
    def __init__(self, payer, upi_id, balance):
        super().__init__(payer)
        self.upi_id = upi_id
        self.balance = balance

    def mode_name(self):
        return "UPI"

    def pay(self, amount):
        print(f"   Opening UPI app for {self.upi_id} ...")
        print("   Verifying 4-digit UPI PIN ...")
        if amount > self.balance:
            print(f"   Insufficient balance (Rs.{self.balance:,.2f})")
            return False
        if amount > 100000:
            print("   NPCI per-transaction limit of Rs.1,00,000 exceeded")
            return False
        self.balance -= amount
        print(f"   Debited instantly. Remaining Rs.{self.balance:,.2f}")
        return True


class NetBankingPayment(Payment):
    def __init__(self, payer, bank, account_no, balance):
        super().__init__(payer)
        self.bank = bank
        self.account_no = account_no
        self.balance = balance

    def mode_name(self):
        return "NetBanking"

    def transaction_fee(self, amount):
        return 12.0                        # flat bank charge

    def pay(self, amount):
        print(f"   Redirecting to {self.bank} internet banking ...")
        print(f"   Logging in for account ****{self.account_no[-4:]}")
        print("   Waiting for OTP ... received")
        if amount > self.balance:
            print(f"   Transaction declined: balance Rs.{self.balance:,.2f}")
            return False
        self.balance -= amount
        print(f"   Transfer complete. Remaining Rs.{self.balance:,.2f}")
        return True


class CreditCardPayment(Payment):
    def __init__(self, payer, number, limit, outstanding=0.0):
        super().__init__(payer)
        self.number = number
        self.limit = limit
        self.outstanding = outstanding

    def mode_name(self):
        return "CreditCard"

    def transaction_fee(self, amount):
        return round(amount * 0.018, 2)    # 1.8% gateway charge

    def available_credit(self):
        return self.limit - self.outstanding

    def pay(self, amount):
        print(f"   Card ****{self.number[-4:]} - running 3-D Secure ...")
        if amount > self.available_credit():
            print(f"   Declined: available credit Rs.{self.available_credit():,.2f}")
            return False
        self.outstanding += amount
        print(f"   Authorised. Outstanding Rs.{self.outstanding:,.2f} "
              f"of limit Rs.{self.limit:,.2f}")
        return True


class WalletPayment(Payment):
    def __init__(self, payer, provider, balance):
        super().__init__(payer)
        self.provider = provider
        self.balance = balance

    def mode_name(self):
        return "Wallet"

    def pay(self, amount):
        print(f"   {self.provider} wallet balance Rs.{self.balance:,.2f}")
        if amount > self.balance:
            print("   Top up the wallet and retry")
            return False
        self.balance -= amount
        print(f"   Paid from wallet. Remaining Rs.{self.balance:,.2f}")
        return True


def get_gateway(choice, payer="Spandan"):
    """Factory used for runtime selection of the payment mode."""
    options = {
        "1": lambda: UPIPayment(payer, "spandan@okaxis", 15000),
        "2": lambda: NetBankingPayment(payer, "HDFC Bank", "901234567890", 42000),
        "3": lambda: CreditCardPayment(payer, "4111111111111234", 75000, 5000),
        "4": lambda: WalletPayment(payer, "Paytm", 900),
    }
    maker = options.get(str(choice))
    return maker() if maker else None


if __name__ == "__main__":
    print("=== abstract class cannot be instantiated ===")
    try:
        Payment("nobody")
    except TypeError as e:
        print("  ", type(e).__name__, "-", e)

    CART_TOTAL = 8499.00
    print(f"\nOrder total: Rs.{CART_TOTAL:,.2f}")
    print("Modes: 1 UPI   2 NetBanking   3 CreditCard   4 Wallet")

    try:
        picked = input("Choose a payment mode (1-4): ").strip()
    except (EOFError, OSError):
        picked = ""
    if picked not in {"1", "2", "3", "4"}:
        print("(no input - demonstrating every mode instead)\n")
        for c in ("1", "2", "3", "4"):
            get_gateway(c).checkout(CART_TOTAL)
    else:
        get_gateway(picked).checkout(CART_TOTAL)

    print("\n=== runtime polymorphism over a list of Payment references ===")
    gateways = [get_gateway(c) for c in ("1", "2", "3", "4")]
    for g in gateways:
        print(f"  {g.mode_name():<12} fee on Rs.1000 = "
              f"Rs.{g.transaction_fee(1000):,.2f}  (isinstance of Payment: "
              f"{isinstance(g, Payment)})")
