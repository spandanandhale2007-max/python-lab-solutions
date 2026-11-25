"""
Experiment 1 - Question 3: Bank with Static Interest Rate

Scenario: A bank applies the same interest rate to all savings accounts.
Calculate compound interest and allow updating the rate across all accounts.

Rubrics covered:
  * static/class variable for the interest rate
  * class method to update the rate
  * instance method to calculate interest
  * effect of a rate change is shown
"""


class SavingsAccount:
    interest_rate = 6.5          # class variable shared by every account
    compounds_per_year = 4       # quarterly compounding

    def __init__(self, holder, principal):
        self.holder = holder
        self.principal = principal

    @classmethod
    def update_interest_rate(cls, new_rate):
        if new_rate < 0:
            raise ValueError("interest rate cannot be negative")
        old = cls.interest_rate
        cls.interest_rate = new_rate
        print(f"[BANK] Interest rate changed for ALL accounts: {old}% -> {new_rate}%")

    @staticmethod
    def compound_amount(principal, rate, years, n):
        return principal * (1 + (rate / 100) / n) ** (n * years)

    def maturity_amount(self, years):
        return self.compound_amount(self.principal, SavingsAccount.interest_rate,
                                    years, SavingsAccount.compounds_per_year)

    def interest_earned(self, years):
        return self.maturity_amount(years) - self.principal

    def __str__(self):
        return (f"{self.holder:<10} principal=Rs.{self.principal:>9,.2f} "
                f"rate={SavingsAccount.interest_rate}%")


if __name__ == "__main__":
    accounts = [
        SavingsAccount("Spandan", 50000),
        SavingsAccount("Riya", 125000),
        SavingsAccount("Aman", 8000),
    ]
    YEARS = 3

    def report(label):
        print(f"\n=== {label} (rate = {SavingsAccount.interest_rate}%) ===")
        for a in accounts:
            print(f"{a.holder:<10} maturity(3y)=Rs.{a.maturity_amount(YEARS):>12,.2f} "
                  f"interest=Rs.{a.interest_earned(YEARS):>10,.2f}")

    report("Before rate change")
    SavingsAccount.update_interest_rate(7.25)
    report("After rate change")

    print("\nEvery instance sees the same class variable:")
    for a in accounts:
        print("  ", a)
