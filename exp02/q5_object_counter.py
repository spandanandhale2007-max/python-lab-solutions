"""
Experiment 2 - Question 5: Object Counter

Scenario: Track how many user accounts have been created in a system.

Rubrics covered:
  * class variable counts instances
  * class method retrieves the count
  * multiple objects created to test it
  * total objects created displayed
"""


class UserAccount:
    _count = 0              # class variable: shared instance counter
    _deleted = 0
    _next_id = 1001

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.user_id = UserAccount._next_id
        UserAccount._next_id += 1
        UserAccount._count += 1

    # ---------- class methods to read / reset the counter ----------
    @classmethod
    def total_accounts(cls):
        return cls._count

    @classmethod
    def stats(cls):
        return {"created": cls._count + cls._deleted,
                "active": cls._count,
                "deleted": cls._deleted}

    @classmethod
    def reset_counter(cls):
        print(f"[ADMIN] counter reset (was {cls._count})")
        cls._count = 0
        cls._deleted = 0

    def close_account(self):
        UserAccount._count -= 1
        UserAccount._deleted += 1
        print(f"Closed account {self.user_id} ({self.username})")

    def __del__(self):
        # best-effort: fires when the object is garbage collected
        pass

    def __str__(self):
        return f"#{self.user_id} {self.username} <{self.email}>"


class PremiumAccount(UserAccount):
    """Subclass shares the parent counter because it never redefines _count."""

    def __init__(self, username, email, plan="Gold"):
        super().__init__(username, email)
        self.plan = plan

    def __str__(self):
        return super().__str__() + f" [{self.plan}]"


if __name__ == "__main__":
    print("Accounts at start :", UserAccount.total_accounts())

    accounts = [
        UserAccount("spandan", "spandan@example.com"),
        UserAccount("riya", "riya@example.com"),
        UserAccount("aman", "aman@example.com"),
        PremiumAccount("neha", "neha@example.com", plan="Platinum"),
    ]

    print("\n=== created accounts ===")
    for a in accounts:
        print(" ", a)

    print("\nTotal via class     :", UserAccount.total_accounts())
    print("Total via instance  :", accounts[0].total_accounts())
    print("Subclass sees same  :", PremiumAccount.total_accounts())

    print("\n=== closing one account ===")
    accounts[2].close_account()
    print("Active now:", UserAccount.total_accounts())
    print("Stats     :", UserAccount.stats())

    print("\n=== creating 3 more in a loop ===")
    for i in range(3):
        accounts.append(UserAccount(f"bulk_user_{i}", f"bulk{i}@example.com"))
    print("Active now:", UserAccount.total_accounts())
    print("Stats     :", UserAccount.stats())

    print("\nInstance counter is NOT per-object:")
    print("  '_count' in instance dict :", "_count" in accounts[0].__dict__)
    print("  it lives on the class     :", "_count" in UserAccount.__dict__)

    UserAccount.reset_counter()
    print("After reset:", UserAccount.stats())
