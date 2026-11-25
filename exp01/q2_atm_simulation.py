"""
Experiment 1 - Question 2: ATM Simulation

Scenario: Simulate an ATM. A user can deposit, withdraw and check balance.
The balance must not be directly accessible or modifiable from outside.

Rubrics covered:
  * private variable for balance (name-mangled __balance)
  * instance variables plus class variables used correctly
  * validation for withdrawal limits
  * user-friendly interaction methods
"""


class ATMAccount:
    bank_name = "State Bank of Pune"       # class variable - shared
    min_balance = 500                      # class variable - policy
    withdrawal_limit = 10000               # class variable - per transaction

    def __init__(self, holder, pin, opening_balance=0):
        self.holder = holder               # instance variable
        self.__pin = pin                   # private
        self.__balance = 0                 # private
        if opening_balance > 0:
            self.deposit(opening_balance, silent=True)

    # read-only access: balance can never be assigned from outside
    @property
    def balance(self):
        return self.__balance

    def verify_pin(self, pin):
        return pin == self.__pin

    def deposit(self, amount, silent=False):
        if amount <= 0:
            print("Deposit failed: amount must be positive.")
            return False
        self.__balance += amount
        if not silent:
            print(f"Deposited Rs.{amount}. Available balance Rs.{self.__balance}")
        return True

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal failed: amount must be positive.")
            return False
        if amount % 100 != 0:
            print("Withdrawal failed: only multiples of Rs.100 are dispensed.")
            return False
        if amount > ATMAccount.withdrawal_limit:
            print(f"Withdrawal failed: per-transaction limit is "
                  f"Rs.{ATMAccount.withdrawal_limit}")
            return False
        if self.__balance - amount < ATMAccount.min_balance:
            print(f"Withdrawal failed: balance cannot fall below "
                  f"Rs.{ATMAccount.min_balance} (available Rs.{self.__balance})")
            return False
        self.__balance -= amount
        print(f"Please collect Rs.{amount}. Available balance Rs.{self.__balance}")
        return True

    def check_balance(self):
        print(f"{ATMAccount.bank_name} | {self.holder} | Balance Rs.{self.__balance}")

    def __str__(self):
        return f"<ATMAccount {self.holder} balance=Rs.{self.__balance}>"


if __name__ == "__main__":
    acc = ATMAccount("Spandan Andhale", pin="4321", opening_balance=5000)
    acc.check_balance()

    print("\n-- valid transactions --")
    acc.deposit(2000)
    acc.withdraw(1500)

    print("\n-- validation checks --")
    acc.withdraw(50)         # not a multiple of 100
    acc.withdraw(50000)      # over per-transaction limit
    acc.withdraw(5400)       # would break the minimum balance
    acc.deposit(-100)        # negative deposit

    print("\n-- encapsulation proof --")
    try:
        acc.balance = 999999             # property has no setter
    except AttributeError as e:
        print("Direct assignment blocked:", e)
    print("Stored privately as:", [k for k in acc.__dict__ if "balance" in k])
    acc.check_balance()
