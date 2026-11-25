"""
Experiment 3 - Question 4: Singleton Logger

Scenario: A logging system where all logs are saved in a single shared object.

Rubrics covered:
  * Singleton pattern implemented
  * one instance used for all logs
  * logs stored and printed
  * uniqueness demonstrated with id()
"""

from datetime import datetime


class Logger:
    """Singleton: __new__ returns the same object every time."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialised = False
        return cls._instance

    def __init__(self, name="AppLogger"):
        if self._initialised:          # guard so repeated calls do not reset state
            return
        self.name = name
        self.records = []
        self._initialised = True
        print(f"[Logger] single instance created (id={id(self)})")

    # ---- logging API ----
    def log(self, level, message):
        stamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{stamp}] {level:<8} {message}"
        self.records.append(entry)
        print(entry)

    def info(self, msg):
        self.log("INFO", msg)

    def warning(self, msg):
        self.log("WARNING", msg)

    def error(self, msg):
        self.log("ERROR", msg)

    def dump(self):
        print(f"\n=== {self.name}: {len(self.records)} record(s) in ONE object ===")
        for r in self.records:
            print("  ", r)

    def clear(self):
        self.records.clear()


# ---- two unrelated modules that each "create" a logger ----
class PaymentService:
    def __init__(self):
        self.log = Logger()            # gets the same instance

    def charge(self, amount):
        self.log.info(f"PaymentService: charging Rs.{amount}")
        if amount > 50000:
            self.log.error("PaymentService: amount above the gateway ceiling")
            return False
        return True


class AuthService:
    def __init__(self):
        self.log = Logger()            # gets the same instance

    def login(self, user, ok=True):
        if ok:
            self.log.info(f"AuthService: {user} signed in")
        else:
            self.log.warning(f"AuthService: failed login for {user}")


if __name__ == "__main__":
    a = Logger("AppLogger")
    b = Logger("ADifferentName")       # ignored, instance already exists
    c = Logger()

    print("\n=== uniqueness proof ===")
    print("  id(a) :", id(a))
    print("  id(b) :", id(b))
    print("  id(c) :", id(c))
    print("  a is b is c :", a is b is c)
    print("  name kept from the first construction:", a.name)

    print("\n=== logs written from different places land in one object ===")
    a.info("application started")
    PaymentService().charge(1999)
    AuthService().login("spandan")
    AuthService().login("unknown_user", ok=False)
    PaymentService().charge(90000)
    c.info("application finished")

    a.dump()
    print(f"\n  b.records is a.records : {b.records is a.records}")
    print(f"  records seen through c : {len(c.records)}")
