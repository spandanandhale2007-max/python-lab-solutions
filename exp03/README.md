# Experiment 3 - Unit I

Generators, closures and design patterns: Singleton, Factory, Observer, Strategy

10 scenario questions, each solved in its own section and its own file. Every program below was executed and the real output is included.

[Back to the index](../README.md)

---

## Questions in this experiment

- [Experiment 3 - Question 1: Shopping Cart with Generator](#experiment-3---question-1-shopping-cart-with-generator)
- [Experiment 3 - Question 2: Multiplication Table Iterator](#experiment-3---question-2-multiplication-table-iterator)
- [Experiment 3 - Question 3: Discount Coupon Closure](#experiment-3---question-3-discount-coupon-closure)
- [Experiment 3 - Question 4: Singleton Logger](#experiment-3---question-4-singleton-logger)
- [Experiment 3 - Question 5: Notification Factory](#experiment-3---question-5-notification-factory)
- [Experiment 3 - Question 6: Weather Station Observer](#experiment-3---question-6-weather-station-observer)
- [Experiment 3 - Question 7: Strategy Pattern Payment](#experiment-3---question-7-strategy-pattern-payment)
- [Experiment 3 - Question 8: Vehicle Factory](#experiment-3---question-8-vehicle-factory)
- [Experiment 3 - Question 9: Sorter Strategy](#experiment-3---question-9-sorter-strategy)
- [Experiment 3 - Question 10: Stock Price Notifier](#experiment-3---question-10-stock-price-notifier)

---

## Experiment 3 - Question 1: Shopping Cart with Generator

Scenario: A shopping cart system where the total price is calculated using a
generator expression.

Rubrics covered:
  * generator used inside the sum() call
  * modular design with Cart and Product
  * add / remove items
  * detailed bill printed

**File:** [`q1_shopping_cart_generator.py`](q1_shopping_cart_generator.py) &nbsp;&middot;&nbsp; **Run:** `python q1_shopping_cart_generator.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 3 - Question 1: Shopping Cart with Generator

Scenario: A shopping cart system where the total price is calculated using a
generator expression.

Rubrics covered:
  * generator used inside the sum() call
  * modular design with Cart and Product
  * add / remove items
  * detailed bill printed
"""


class Product:
    def __init__(self, name, price, qty=1, gst=18):
        self.name = name
        self.price = float(price)
        self.qty = int(qty)
        self.gst = gst

    @property
    def net(self):
        return self.price * self.qty

    @property
    def tax(self):
        return self.net * self.gst / 100

    @property
    def gross(self):
        return self.net + self.tax

    def __str__(self):
        return (f"{self.name:<18} {self.qty:>3} x {self.price:>9,.2f} = "
                f"{self.net:>10,.2f}  +{self.gst}% GST {self.tax:>8,.2f}  "
                f"{self.gross:>11,.2f}")


class Cart:
    def __init__(self, owner):
        self.owner = owner
        self.items = []

    def add(self, product):
        for existing in self.items:
            if existing.name == product.name:
                existing.qty += product.qty
                print(f"+ {product.name} qty now {existing.qty}")
                return
        self.items.append(product)
        print(f"+ added {product.name} x{product.qty}")

    def remove(self, name, qty=None):
        for item in list(self.items):
            if item.name.lower() == name.lower():
                if qty is None or qty >= item.qty:
                    self.items.remove(item)
                    print(f"- removed {item.name} entirely")
                else:
                    item.qty -= qty
                    print(f"- removed {qty} x {item.name}, {item.qty} left")
                return True
        print(f"! {name} is not in the cart")
        return False

    # ---- every total is a generator expression consumed by sum() ----
    def subtotal(self):
        return sum(item.net for item in self.items)

    def total_tax(self):
        return sum(item.tax for item in self.items)

    def total(self):
        return sum(item.gross for item in self.items)

    def item_count(self):
        return sum(item.qty for item in self.items)

    def costliest(self):
        return max(self.items, key=lambda i: i.gross, default=None)

    def bill(self):
        print(f"\n{'=' * 78}")
        print(f"  BILL for {self.owner}")
        print(f"{'=' * 78}")
        print(f"{'ITEM':<18} {'QTY':>3}   {'RATE':>9}   {'NET':>10}   "
              f"{'TAX':>14}   {'AMOUNT':>11}")
        print("-" * 78)
        for item in self.items:
            print(item)
        print("-" * 78)
        print(f"{'Units':<18} {self.item_count():>3}")
        print(f"{'Subtotal':<40} {self.subtotal():>31,.2f}")
        print(f"{'GST':<40} {self.total_tax():>31,.2f}")
        print(f"{'TOTAL PAYABLE':<40} {self.total():>31,.2f}")
        top = self.costliest()
        if top:
            print(f"\n  Costliest line: {top.name} (Rs.{top.gross:,.2f})")
        print(f"{'=' * 78}")


if __name__ == "__main__":
    cart = Cart("Spandan Andhale")

    print("=== adding items ===")
    cart.add(Product("Rice 5kg", 420, 2, gst=5))
    cart.add(Product("Olive Oil 1L", 899, 1))
    cart.add(Product("Toothpaste", 115, 3, gst=12))
    cart.add(Product("Bluetooth Mouse", 899, 1))
    cart.add(Product("Rice 5kg", 420, 1, gst=5))     # merges with the first line

    print("\n=== removing items ===")
    cart.remove("Toothpaste", 1)
    cart.remove("Olive Oil 1L")
    cart.remove("Chocolate")                          # not present

    cart.bill()

    print("\n=== the generator expression itself ===")
    gen = (item.gross for item in cart.items)
    print("  object  :", gen)
    print("  sum()   :", round(sum(gen), 2))
    print("  reused? :", round(sum(gen), 2), "<- exhausted after one pass")
    print("  fresh   :", round(sum(item.gross for item in cart.items), 2))
```

</details>

<details>
<summary>Program output</summary>

```text
=== adding items ===
+ added Rice 5kg x2
+ added Olive Oil 1L x1
+ added Toothpaste x3
+ added Bluetooth Mouse x1
+ Rice 5kg qty now 3

=== removing items ===
- removed 1 x Toothpaste, 2 left
- removed Olive Oil 1L entirely
! Chocolate is not in the cart

==============================================================================
  BILL for Spandan Andhale
==============================================================================
ITEM               QTY        RATE          NET              TAX        AMOUNT
------------------------------------------------------------------------------
Rice 5kg             3 x    420.00 =   1,260.00  +5% GST    63.00     1,323.00
Toothpaste           2 x    115.00 =     230.00  +12% GST    27.60       257.60
Bluetooth Mouse      1 x    899.00 =     899.00  +18% GST   161.82     1,060.82
------------------------------------------------------------------------------
Units                6
Subtotal                                                        2,389.00
GST                                                               252.42
TOTAL PAYABLE                                                   2,641.42

  Costliest line: Rice 5kg (Rs.1,323.00)
==============================================================================

=== the generator expression itself ===
  object  : <generator object <genexpr> at 0x000001A57C43C7C0>
  sum()   : 2641.42
  reused? : 0 <- exhausted after one pass
  fresh   : 2641.42

```

</details>

---

## Experiment 3 - Question 2: Multiplication Table Iterator

Scenario: An iterator class that prints the multiplication table of any number
up to 10.

Rubrics covered:
  * custom iterator methods defined (__iter__, __next__)
  * input number accepted
  * results looped through
  * clear structured output

**File:** [`q2_multiplication_table_iterator.py`](q2_multiplication_table_iterator.py) &nbsp;&middot;&nbsp; **Run:** `python q2_multiplication_table_iterator.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 3 - Question 2: Multiplication Table Iterator

Scenario: An iterator class that prints the multiplication table of any number
up to 10.

Rubrics covered:
  * custom iterator methods defined (__iter__, __next__)
  * input number accepted
  * results looped through
  * clear structured output
"""


class MultiplicationTable:
    """Iterator yielding (multiplier, product) pairs for one number."""

    def __init__(self, number, upto=10, start=1):
        self.number = number
        self.upto = upto
        self.current = start - 1

    def __iter__(self):
        return self

    def __next__(self):
        self.current += 1
        if self.current > self.upto:
            raise StopIteration
        return self.current, self.number * self.current

    def __len__(self):
        return self.upto


class TableBook:
    """Iterable of iterables: tables for a whole range of numbers."""

    def __init__(self, numbers, upto=10):
        self.numbers = list(numbers)
        self.upto = upto

    def __iter__(self):
        for n in self.numbers:
            yield MultiplicationTable(n, self.upto)


def print_table(number, upto=10):
    print(f"\n--- Table of {number} (up to {upto}) ---")
    for multiplier, product in MultiplicationTable(number, upto):
        print(f"  {number:>3} x {multiplier:>2} = {product:>5}")


if __name__ == "__main__":
    try:
        raw = input("Enter a number for its table: ").strip()
        number = int(raw)
    except (EOFError, ValueError, OSError):
        number = 7
        print(f"(no input - using {number})")

    print_table(number)

    print("\n=== manual next() calls ===")
    it = MultiplicationTable(number, upto=3)
    for _ in range(4):
        try:
            print("  next():", next(it))
        except StopIteration:
            print("  StopIteration - table finished")

    print("\n=== grid for 2..5 using the iterable container ===")
    header = "     " + "".join(f"{m:>6}" for m in range(1, 11))
    print(header)
    print("     " + "-" * 60)
    for table in TableBook(range(2, 6)):
        row = f"{table.number:>3} |"
        for _, product in table:
            row += f"{product:>6}"
        print(row)

    print("\n=== squares picked out of the tables ===")
    for table in TableBook(range(1, 11)):
        for multiplier, product in table:
            if multiplier == table.number:
                print(f"  {table.number:>2}^2 = {product:>3}", end="")
    print()
```

</details>

<details>
<summary>Program output</summary>

```text
Enter a number for its table: (no input - using 7)

--- Table of 7 (up to 10) ---
    7 x  1 =     7
    7 x  2 =    14
    7 x  3 =    21
    7 x  4 =    28
    7 x  5 =    35
    7 x  6 =    42
    7 x  7 =    49
    7 x  8 =    56
    7 x  9 =    63
    7 x 10 =    70

=== manual next() calls ===
  next(): (1, 7)
  next(): (2, 14)
  next(): (3, 21)
  StopIteration - table finished

=== grid for 2..5 using the iterable container ===
          1     2     3     4     5     6     7     8     9    10
     ------------------------------------------------------------
  2 |     2     4     6     8    10    12    14    16    18    20
  3 |     3     6     9    12    15    18    21    24    27    30
  4 |     4     8    12    16    20    24    28    32    36    40
  5 |     5    10    15    20    25    30    35    40    45    50

=== squares picked out of the tables ===
   1^2 =   1   2^2 =   4   3^2 =   9   4^2 =  16   5^2 =  25   6^2 =  36   7^2 =  49   8^2 =  64   9^2 =  81  10^2 = 100

```

</details>

---

## Experiment 3 - Question 3: Discount Coupon Closure

Scenario: Generate discount functions using closures (10%, 20% and so on).

Rubrics covered:
  * closure returns a discount function
  * applied to different item prices
  * multiple closures with different rates
  * final price after discount printed

**File:** [`q3_discount_coupon_closure.py`](q3_discount_coupon_closure.py) &nbsp;&middot;&nbsp; **Run:** `python q3_discount_coupon_closure.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 3 - Question 3: Discount Coupon Closure

Scenario: Generate discount functions using closures (10%, 20% and so on).

Rubrics covered:
  * closure returns a discount function
  * applied to different item prices
  * multiple closures with different rates
  * final price after discount printed
"""


def make_coupon(code, percent, max_discount=None, min_order=0):
    """Returns a closure that remembers code, percent, caps and a usage count."""

    uses = 0

    def apply(price):
        nonlocal uses
        if price < min_order:
            print(f"  {code:<10} not valid: order Rs.{price:,.2f} is below the "
                  f"minimum Rs.{min_order:,.2f}")
            return price
        discount = price * percent / 100
        if max_discount is not None:
            discount = min(discount, max_discount)
        uses += 1
        final = price - discount
        print(f"  {code:<10} {percent:>2}% off Rs.{price:>9,.2f} -> "
              f"saved Rs.{discount:>8,.2f}  pay Rs.{final:>9,.2f}")
        return round(final, 2)

    apply.code = code
    apply.percent = percent
    apply.uses = lambda: uses
    return apply


def make_flat_coupon(code, amount, min_order=0):
    def apply(price):
        if price < min_order:
            print(f"  {code:<10} needs a minimum order of Rs.{min_order:,.2f}")
            return price
        final = max(0.0, price - amount)
        print(f"  {code:<10} flat Rs.{amount} off Rs.{price:,.2f} -> "
              f"pay Rs.{final:,.2f}")
        return round(final, 2)
    apply.code = code
    return apply


def best_offer(price, coupons):
    """Picks the coupon that gives the lowest final price."""
    quiet = []
    for c in coupons:
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            quiet.append((c(price), c.code))
    return min(quiet)


if __name__ == "__main__":
    # several independent closures, each with its own captured rate
    save10 = make_coupon("SAVE10", 10)
    save20 = make_coupon("SAVE20", 20, max_discount=500)
    festive30 = make_coupon("FESTIVE30", 30, max_discount=1500, min_order=2000)
    flat250 = make_flat_coupon("FLAT250", 250, min_order=999)

    prices = [499.00, 1899.00, 7499.00]

    for p in prices:
        print(f"\n=== cart value Rs.{p:,.2f} ===")
        for coupon in (save10, save20, festive30, flat250):
            coupon(p)

    print("\n=== each closure keeps its own usage counter ===")
    for coupon in (save10, save20, festive30):
        print(f"  {coupon.code:<10} used {coupon.uses()} time(s) "
              f"at {coupon.percent}%")

    print("\n=== closure internals ===")
    print("  free variables:", save20.__code__.co_freevars)
    print("  captured cells:", [c.cell_contents for c in save20.__closure__])

    print("\n=== best automatic offer per cart ===")
    for p in prices:
        final, code = best_offer(p, [save10, save20, festive30, flat250])
        print(f"  Rs.{p:>9,.2f} -> best is {code:<10} final Rs.{final:,.2f}")

    print("\n=== building coupons in a loop (late binding avoided) ===")
    tiered = [make_coupon(f"TIER{r}", r) for r in (5, 15, 25)]
    for t in tiered:
        t(1000)
```

</details>

<details>
<summary>Program output</summary>

```text
=== cart value Rs.499.00 ===
  SAVE10     10% off Rs.   499.00 -> saved Rs.   49.90  pay Rs.   449.10
  SAVE20     20% off Rs.   499.00 -> saved Rs.   99.80  pay Rs.   399.20
  FESTIVE30  not valid: order Rs.499.00 is below the minimum Rs.2,000.00
  FLAT250    needs a minimum order of Rs.999.00

=== cart value Rs.1,899.00 ===
  SAVE10     10% off Rs. 1,899.00 -> saved Rs.  189.90  pay Rs. 1,709.10
  SAVE20     20% off Rs. 1,899.00 -> saved Rs.  379.80  pay Rs. 1,519.20
  FESTIVE30  not valid: order Rs.1,899.00 is below the minimum Rs.2,000.00
  FLAT250    flat Rs.250 off Rs.1,899.00 -> pay Rs.1,649.00

=== cart value Rs.7,499.00 ===
  SAVE10     10% off Rs. 7,499.00 -> saved Rs.  749.90  pay Rs. 6,749.10
  SAVE20     20% off Rs. 7,499.00 -> saved Rs.  500.00  pay Rs. 6,999.00
  FESTIVE30  30% off Rs. 7,499.00 -> saved Rs.1,500.00  pay Rs. 5,999.00
  FLAT250    flat Rs.250 off Rs.7,499.00 -> pay Rs.7,249.00

=== each closure keeps its own usage counter ===
  SAVE10     used 3 time(s) at 10%
  SAVE20     used 3 time(s) at 20%
  FESTIVE30  used 1 time(s) at 30%

=== closure internals ===
  free variables: ('code', 'max_discount', 'min_order', 'percent', 'uses')
  captured cells: ['SAVE20', 500, 0, 20, 3]

=== best automatic offer per cart ===
  Rs.   499.00 -> best is SAVE20     final Rs.399.20
  Rs. 1,899.00 -> best is SAVE20     final Rs.1,519.20
  Rs. 7,499.00 -> best is FESTIVE30  final Rs.5,999.00

=== building coupons in a loop (late binding avoided) ===
  TIER5       5% off Rs. 1,000.00 -> saved Rs.   50.00  pay Rs.   950.00
  TIER15     15% off Rs. 1,000.00 -> saved Rs.  150.00  pay Rs.   850.00
  TIER25     25% off Rs. 1,000.00 -> saved Rs.  250.00  pay Rs.   750.00

```

</details>

---

## Experiment 3 - Question 4: Singleton Logger

Scenario: A logging system where all logs are saved in a single shared object.

Rubrics covered:
  * Singleton pattern implemented
  * one instance used for all logs
  * logs stored and printed
  * uniqueness demonstrated with id()

**File:** [`q4_singleton_logger.py`](q4_singleton_logger.py) &nbsp;&middot;&nbsp; **Run:** `python q4_singleton_logger.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
[Logger] single instance created (id=1569892980624)

=== uniqueness proof ===
  id(a) : 1569892980624
  id(b) : 1569892980624
  id(c) : 1569892980624
  a is b is c : True
  name kept from the first construction: AppLogger

=== logs written from different places land in one object ===
[08:42:57] INFO     application started
[08:42:57] INFO     PaymentService: charging Rs.1999
[08:42:57] INFO     AuthService: spandan signed in
[08:42:57] WARNING  AuthService: failed login for unknown_user
[08:42:57] INFO     PaymentService: charging Rs.90000
[08:42:57] ERROR    PaymentService: amount above the gateway ceiling
[08:42:57] INFO     application finished

=== AppLogger: 7 record(s) in ONE object ===
   [08:42:57] INFO     application started
   [08:42:57] INFO     PaymentService: charging Rs.1999
   [08:42:57] INFO     AuthService: spandan signed in
   [08:42:57] WARNING  AuthService: failed login for unknown_user
   [08:42:57] INFO     PaymentService: charging Rs.90000
   [08:42:57] ERROR    PaymentService: amount above the gateway ceiling
   [08:42:57] INFO     application finished

  b.records is a.records : True
  records seen through c : 7

```

</details>

---

## Experiment 3 - Question 5: Notification Factory

Scenario: A factory that returns different notification classes based on input:
Email, SMS or Push.

Rubrics covered:
  * factory returns the correct class
  * each notification type has a send() method
  * inheritance / a common interface used
  * easy to extend with new types

**File:** [`q5_notification_factory.py`](q5_notification_factory.py) &nbsp;&middot;&nbsp; **Run:** `python q5_notification_factory.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 3 - Question 5: Notification Factory

Scenario: A factory that returns different notification classes based on input:
Email, SMS or Push.

Rubrics covered:
  * factory returns the correct class
  * each notification type has a send() method
  * inheritance / a common interface used
  * easy to extend with new types
"""

from abc import ABC, abstractmethod


class Notification(ABC):
    """Common interface every channel must satisfy."""

    channel = "generic"

    def __init__(self, recipient):
        self.recipient = recipient
        self.sent = 0

    @abstractmethod
    def send(self, message):
        ...

    def _ok(self, detail):
        self.sent += 1
        print(f"  [{self.channel.upper():<5}] -> {self.recipient}: {detail}")
        return True


class EmailNotification(Notification):
    channel = "email"
    MAX_SUBJECT = 60

    def send(self, message, subject="Notification from MediVerse"):
        subject = subject[:self.MAX_SUBJECT]
        print(f"  Connecting to SMTP smtp.gmail.com:587 ...")
        return self._ok(f"subject={subject!r} body={message[:50]!r}")


class SMSNotification(Notification):
    channel = "sms"
    MAX_LEN = 160

    def send(self, message):
        parts = [message[i:i + self.MAX_LEN]
                 for i in range(0, len(message), self.MAX_LEN)] or [""]
        print(f"  Hitting SMS gateway for +91{self.recipient[-10:]} ...")
        return self._ok(f"{len(parts)} segment(s): {parts[0][:40]!r}")


class PushNotification(Notification):
    channel = "push"

    def send(self, message, title="MediVerse"):
        print("  Posting to FCM topic ...")
        return self._ok(f"title={title!r} payload={message[:40]!r}")


class WhatsAppNotification(Notification):
    """Added later: the factory needs one new line, nothing else changes."""
    channel = "wa"

    def send(self, message, template="appointment_reminder"):
        print("  Calling the WhatsApp Business API ...")
        return self._ok(f"template={template} text={message[:40]!r}")


class NotificationFactory:
    _registry = {
        "email": EmailNotification,
        "sms": SMSNotification,
        "push": PushNotification,
        "whatsapp": WhatsAppNotification,
    }

    @classmethod
    def create(cls, kind, recipient):
        try:
            klass = cls._registry[kind.strip().lower()]
        except KeyError:
            raise ValueError(
                f"unknown channel {kind!r}; available: "
                f"{', '.join(sorted(cls._registry))}") from None
        return klass(recipient)

    @classmethod
    def register(cls, kind, klass):
        """Extension point: plug in a new channel at runtime."""
        if not issubclass(klass, Notification):
            raise TypeError("channel must subclass Notification")
        cls._registry[kind] = klass
        print(f"[factory] registered new channel {kind!r} -> {klass.__name__}")

    @classmethod
    def channels(cls):
        return sorted(cls._registry)


if __name__ == "__main__":
    print("available channels:", NotificationFactory.channels())

    print("\n=== factory returns the matching class ===")
    for kind, who in (("email", "spandan@example.com"),
                      ("sms", "+919011223344"),
                      ("push", "device-token-ab12cd"),
                      ("whatsapp", "+919011223344")):
        obj = NotificationFactory.create(kind, who)
        print(f"  create({kind!r}) -> {type(obj).__name__}")

    print("\n=== same call, different behaviour ===")
    msg = "Your appointment with Dr. Kulkarni is confirmed for tomorrow 10:30 AM."
    for kind, who in (("email", "spandan@example.com"),
                      ("sms", "+919011223344"),
                      ("push", "device-token-ab12cd")):
        NotificationFactory.create(kind, who).send(msg)

    print("\n=== unknown channel ===")
    try:
        NotificationFactory.create("telegram", "@spandan")
    except ValueError as e:
        print("  ", e)

    print("\n=== extending the factory without touching existing code ===")
    class SlackNotification(Notification):
        channel = "slack"

        def send(self, message):
            return self._ok(f"posted to #{self.recipient}: {message[:30]!r}")

    NotificationFactory.register("slack", SlackNotification)
    NotificationFactory.create("slack", "ops-alerts").send(msg)
    print("  channels now:", NotificationFactory.channels())
```

</details>

<details>
<summary>Program output</summary>

```text
available channels: ['email', 'push', 'sms', 'whatsapp']

=== factory returns the matching class ===
  create('email') -> EmailNotification
  create('sms') -> SMSNotification
  create('push') -> PushNotification
  create('whatsapp') -> WhatsAppNotification

=== same call, different behaviour ===
  Connecting to SMTP smtp.gmail.com:587 ...
  [EMAIL] -> spandan@example.com: subject='Notification from MediVerse' body='Your appointment with Dr. Kulkarni is confirmed fo'
  Hitting SMS gateway for +919011223344 ...
  [SMS  ] -> +919011223344: 1 segment(s): 'Your appointment with Dr. Kulkarni is co'
  Posting to FCM topic ...
  [PUSH ] -> device-token-ab12cd: title='MediVerse' payload='Your appointment with Dr. Kulkarni is co'

=== unknown channel ===
   unknown channel 'telegram'; available: email, push, sms, whatsapp

=== extending the factory without touching existing code ===
[factory] registered new channel 'slack' -> SlackNotification
  [SLACK] -> ops-alerts: posted to #ops-alerts: 'Your appointment with Dr. Kulk'
  channels now: ['email', 'push', 'slack', 'sms', 'whatsapp']

```

</details>

---

## Experiment 3 - Question 6: Weather Station Observer

Scenario: A weather station where multiple displays update the temperature
whenever the sensor changes.

Rubrics covered:
  * observer pattern with subscribe / unsubscribe
  * all observers notified on change
  * sensor decoupled from the displays
  * updated data printed for each display

**File:** [`q6_weather_station_observer.py`](q6_weather_station_observer.py) &nbsp;&middot;&nbsp; **Run:** `python q6_weather_station_observer.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 3 - Question 6: Weather Station Observer

Scenario: A weather station where multiple displays update the temperature
whenever the sensor changes.

Rubrics covered:
  * observer pattern with subscribe / unsubscribe
  * all observers notified on change
  * sensor decoupled from the displays
  * updated data printed for each display
"""

from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, temperature, humidity, pressure):
        ...


class WeatherStation:
    """The subject. It knows nothing about the concrete display classes."""

    def __init__(self, name):
        self.name = name
        self._observers = []
        self.temperature = None
        self.humidity = None
        self.pressure = None

    def subscribe(self, observer):
        if observer in self._observers:
            print(f"  {type(observer).__name__} is already subscribed")
            return False
        self._observers.append(observer)
        print(f"  + {type(observer).__name__} subscribed "
              f"({len(self._observers)} total)")
        return True

    def unsubscribe(self, observer):
        if observer not in self._observers:
            print(f"  {type(observer).__name__} was not subscribed")
            return False
        self._observers.remove(observer)
        print(f"  - {type(observer).__name__} unsubscribed "
              f"({len(self._observers)} left)")
        return True

    def notify(self):
        for obs in list(self._observers):
            obs.update(self.temperature, self.humidity, self.pressure)

    def set_measurements(self, temperature, humidity, pressure):
        print(f"\n[{self.name}] sensor reading: {temperature} C, "
              f"{humidity}% RH, {pressure} hPa")
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.notify()


class CurrentConditionsDisplay(Observer):
    def update(self, temperature, humidity, pressure):
        print(f"   [Current ] {temperature:.1f} C and {humidity:.0f}% humidity")


class StatisticsDisplay(Observer):
    def __init__(self):
        self.readings = []

    def update(self, temperature, humidity, pressure):
        self.readings.append(temperature)
        print(f"   [Stats   ] avg/min/max = "
              f"{sum(self.readings) / len(self.readings):.1f} / "
              f"{min(self.readings):.1f} / {max(self.readings):.1f} C "
              f"over {len(self.readings)} reading(s)")


class ForecastDisplay(Observer):
    def __init__(self):
        self.last_pressure = None

    def update(self, temperature, humidity, pressure):
        if self.last_pressure is None:
            trend = "no previous reading"
        elif pressure > self.last_pressure:
            trend = "improving weather on the way"
        elif pressure < self.last_pressure:
            trend = "cooler, rainy weather on the way"
        else:
            trend = "more of the same"
        self.last_pressure = pressure
        print(f"   [Forecast] {trend}")


class HeatAlertDisplay(Observer):
    THRESHOLD = 40.0

    def update(self, temperature, humidity, pressure):
        if temperature >= self.THRESHOLD:
            print(f"   [ALERT   ] heat warning, {temperature:.1f} C "
                  f"is above {self.THRESHOLD} C")


if __name__ == "__main__":
    station = WeatherStation("Pune Shivajinagar")

    current = CurrentConditionsDisplay()
    stats = StatisticsDisplay()
    forecast = ForecastDisplay()
    alert = HeatAlertDisplay()

    print("=== subscribing displays ===")
    for display in (current, stats, forecast, alert):
        station.subscribe(display)
    station.subscribe(current)                 # duplicate rejected

    station.set_measurements(31.4, 62, 1012)
    station.set_measurements(34.9, 55, 1009)

    print("\n=== one display unsubscribes, the rest keep working ===")
    station.unsubscribe(forecast)
    station.set_measurements(41.2, 38, 1005)

    print("\n=== resubscribing and removing an unknown observer ===")
    station.subscribe(forecast)
    station.unsubscribe(HeatAlertDisplay())    # never subscribed
    station.set_measurements(28.0, 71, 1011)

    print("\n=== the station is decoupled from display types ===")
    print("  station only stores:", [type(o).__name__ for o in station._observers])
    print("  all are Observer subclasses:",
          all(isinstance(o, Observer) for o in station._observers))
```

</details>

<details>
<summary>Program output</summary>

```text
=== subscribing displays ===
  + CurrentConditionsDisplay subscribed (1 total)
  + StatisticsDisplay subscribed (2 total)
  + ForecastDisplay subscribed (3 total)
  + HeatAlertDisplay subscribed (4 total)
  CurrentConditionsDisplay is already subscribed

[Pune Shivajinagar] sensor reading: 31.4 C, 62% RH, 1012 hPa
   [Current ] 31.4 C and 62% humidity
   [Stats   ] avg/min/max = 31.4 / 31.4 / 31.4 C over 1 reading(s)
   [Forecast] no previous reading

[Pune Shivajinagar] sensor reading: 34.9 C, 55% RH, 1009 hPa
   [Current ] 34.9 C and 55% humidity
   [Stats   ] avg/min/max = 33.1 / 31.4 / 34.9 C over 2 reading(s)
   [Forecast] cooler, rainy weather on the way

=== one display unsubscribes, the rest keep working ===
  - ForecastDisplay unsubscribed (3 left)

[Pune Shivajinagar] sensor reading: 41.2 C, 38% RH, 1005 hPa
   [Current ] 41.2 C and 38% humidity
   [Stats   ] avg/min/max = 35.8 / 31.4 / 41.2 C over 3 reading(s)
   [ALERT   ] heat warning, 41.2 C is above 40.0 C

=== resubscribing and removing an unknown observer ===
  + ForecastDisplay subscribed (4 total)
  HeatAlertDisplay was not subscribed

[Pune Shivajinagar] sensor reading: 28.0 C, 71% RH, 1011 hPa
   [Current ] 28.0 C and 71% humidity
   [Stats   ] avg/min/max = 33.9 / 28.0 / 41.2 C over 4 reading(s)
   [Forecast] improving weather on the way

=== the station is decoupled from display types ===
  station only stores: ['CurrentConditionsDisplay', 'StatisticsDisplay', 'HeatAlertDisplay', 'ForecastDisplay']
  all are Observer subclasses: True

```

</details>

---

## Experiment 3 - Question 7: Strategy Pattern Payment

Scenario: Users select different payment strategies: CreditCard, UPI or Wallet.

Rubrics covered:
  * strategy classes defined
  * strategy switched at runtime
  * a context class executes the chosen strategy
  * realistic use case

**File:** [`q7_strategy_pattern_payment.py`](q7_strategy_pattern_payment.py) &nbsp;&middot;&nbsp; **Run:** `python q7_strategy_pattern_payment.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== no strategy chosen yet ===
[context] choose a payment method first

=== runtime switching between strategies ===
[context] Spandan switched to UPI
[context] paying Rs.2,499.00 using UPI (fee Rs.0.00)
   Paid Rs.2,499.00 via spandan@okaxis (zero fee), balance Rs.1,501.00

[context] Spandan switched to Wallet
[context] paying Rs.899.00 using Wallet (fee Rs.0.00)
   Paid Rs.899.00 from Paytm, cashback Rs.17.98, balance Rs.318.98

[context] Spandan switched to CreditCard
[context] paying Rs.15,999.00 using CreditCard (fee Rs.239.98)
   Paid Rs.16,238.98 with card ****5678 (Spandan Andhale), 3-D Secure OK

[context] Spandan switched to CreditCard
[context] paying Rs.9,999.00 using CreditCard (fee Rs.149.98)
   DECLINED: limit Rs.20,000, already spent Rs.16,238.98

[context] Spandan switched to COD
[context] paying Rs.599.00 using COD (fee Rs.40.00)
   Collect Rs.639.00 at the door (includes Rs.40 handling)

=== transaction history ===
  UPI          Rs. 2,499.00  OK
  Wallet       Rs.   899.00  OK
  CreditCard   Rs.15,999.00  OK
  CreditCard   Rs. 9,999.00  DECLINED
  COD          Rs.   599.00  OK

=== picking a strategy from user input ===
1 Card  2 UPI  3 Wallet  4 COD : [context] Spandan switched to UPI
[context] paying Rs.500.00 using UPI (fee Rs.0.00)
   Paid Rs.500.00 via spandan@okaxis (zero fee), balance Rs.1,001.00

```

</details>

---

## Experiment 3 - Question 8: Vehicle Factory

Scenario: A rental service that returns different vehicle classes from a
factory based on the type requested (Bike, Car, Truck).

Rubrics covered:
  * factory returns the appropriate object
  * polymorphic rent() method
  * clean vehicle hierarchy
  * easy future expansion

**File:** [`q8_vehicle_factory.py`](q8_vehicle_factory.py) &nbsp;&middot;&nbsp; **Run:** `python q8_vehicle_factory.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 3 - Question 8: Vehicle Factory

Scenario: A rental service that returns different vehicle classes from a
factory based on the type requested (Bike, Car, Truck).

Rubrics covered:
  * factory returns the appropriate object
  * polymorphic rent() method
  * clean vehicle hierarchy
  * easy future expansion
"""

from abc import ABC, abstractmethod


class Vehicle(ABC):
    wheels = 0
    licence_required = "LMV"

    def __init__(self, model, reg_no, daily_rate):
        self.model = model
        self.reg_no = reg_no
        self.daily_rate = daily_rate
        self.rented_to = None

    @abstractmethod
    def rent(self, customer, days):
        ...

    def is_available(self):
        return self.rented_to is None

    def base_cost(self, days):
        return self.daily_rate * days

    def return_vehicle(self):
        if self.rented_to is None:
            print(f"  {self.model} was not rented out")
            return False
        print(f"  {self.model} returned by {self.rented_to}")
        self.rented_to = None
        return True

    def __str__(self):
        state = "available" if self.is_available() else f"with {self.rented_to}"
        return (f"{type(self).__name__:<6} {self.model:<16} {self.reg_no:<12} "
                f"{self.wheels} wheels  Rs.{self.daily_rate:>5}/day  [{state}]")


class Bike(Vehicle):
    wheels = 2
    licence_required = "MCWG"

    def __init__(self, model, reg_no, daily_rate=399, helmets=2):
        super().__init__(model, reg_no, daily_rate)
        self.helmets = helmets

    def rent(self, customer, days):
        if not self.is_available():
            print(f"  {self.model} is already rented")
            return None
        cost = self.base_cost(days)
        self.rented_to = customer
        print(f"  BIKE  : {self.model} to {customer} for {days} day(s) "
              f"= Rs.{cost:,.0f} (+{self.helmets} helmets, "
              f"{self.licence_required} licence)")
        return cost


class Car(Vehicle):
    wheels = 4

    def __init__(self, model, reg_no, daily_rate=2199, seats=5, ac=True):
        super().__init__(model, reg_no, daily_rate)
        self.seats = seats
        self.ac = ac

    def rent(self, customer, days):
        if not self.is_available():
            print(f"  {self.model} is already rented")
            return None
        cost = self.base_cost(days)
        if days >= 7:
            cost *= 0.9                    # weekly discount
        self.rented_to = customer
        print(f"  CAR   : {self.model} to {customer} for {days} day(s) "
              f"= Rs.{cost:,.0f} ({self.seats} seats, "
              f"{'AC' if self.ac else 'non-AC'})")
        return cost


class Truck(Vehicle):
    wheels = 6
    licence_required = "HMV"

    def __init__(self, model, reg_no, daily_rate=4999, payload_tonnes=9):
        super().__init__(model, reg_no, daily_rate)
        self.payload_tonnes = payload_tonnes

    def rent(self, customer, days):
        if not self.is_available():
            print(f"  {self.model} is already rented")
            return None
        cost = self.base_cost(days) + 1500          # loading charge
        self.rented_to = customer
        print(f"  TRUCK : {self.model} to {customer} for {days} day(s) "
              f"= Rs.{cost:,.0f} (payload {self.payload_tonnes} t, "
              f"{self.licence_required} licence, Rs.1,500 loading)")
        return cost


class VehicleFactory:
    _catalogue = {
        "bike": (Bike, ("Royal Enfield Classic 350", "MH12-AB-1234")),
        "car": (Car, ("Hyundai Creta", "MH12-CD-5678")),
        "truck": (Truck, ("Tata LPT 1109", "MH12-EF-9012")),
    }

    @classmethod
    def create(cls, kind, **overrides):
        key = kind.strip().lower()
        if key not in cls._catalogue:
            raise ValueError(f"we do not rent {kind!r}; available: "
                             f"{', '.join(sorted(cls._catalogue))}")
        klass, defaults = cls._catalogue[key]
        model, reg = overrides.pop("model", defaults[0]), \
            overrides.pop("reg_no", defaults[1])
        return klass(model, reg, **overrides)

    @classmethod
    def register(cls, kind, klass, defaults):
        cls._catalogue[kind] = (klass, defaults)
        print(f"[factory] new vehicle type available: {kind}")

    @classmethod
    def types(cls):
        return sorted(cls._catalogue)


if __name__ == "__main__":
    print("rentable types:", VehicleFactory.types())

    print("\n=== the factory decides the class ===")
    fleet = [VehicleFactory.create(k) for k in ("bike", "car", "truck")]
    for v in fleet:
        print("  create ->", type(v).__name__, "|", v)

    print("\n=== polymorphic rent() through one loop ===")
    total = 0
    for v, customer, days in zip(fleet, ("Spandan", "Riya", "Shree Logistics"),
                                 (2, 8, 3)):
        amount = v.rent(customer, days)
        total += amount or 0
    print(f"  revenue booked: Rs.{total:,.0f}")

    print("\n=== double rent and return ===")
    fleet[0].rent("Aman", 1)
    fleet[0].return_vehicle()
    fleet[0].rent("Aman", 1)

    print("\n=== unknown type ===")
    try:
        VehicleFactory.create("helicopter")
    except ValueError as e:
        print("  ", e)

    print("\n=== extending the fleet later ===")
    class EScooter(Vehicle):
        wheels = 2
        licence_required = "none"

        def rent(self, customer, days):
            cost = self.base_cost(days)
            self.rented_to = customer
            print(f"  ESCOOT: {self.model} to {customer} for {days} day(s) "
                  f"= Rs.{cost:,.0f} (no licence needed)")
            return cost

    VehicleFactory.register("escooter", EScooter, ("Ather 450X", "MH12-GH-3456"))
    VehicleFactory.create("escooter", daily_rate=299).rent("Neha", 4)
    print("  rentable types now:", VehicleFactory.types())

    print("\n=== final fleet state ===")
    for v in fleet:
        print("  ", v)
```

</details>

<details>
<summary>Program output</summary>

```text
rentable types: ['bike', 'car', 'truck']

=== the factory decides the class ===
  create -> Bike | Bike   Royal Enfield Classic 350 MH12-AB-1234 2 wheels  Rs.  399/day  [available]
  create -> Car | Car    Hyundai Creta    MH12-CD-5678 4 wheels  Rs. 2199/day  [available]
  create -> Truck | Truck  Tata LPT 1109    MH12-EF-9012 6 wheels  Rs. 4999/day  [available]

=== polymorphic rent() through one loop ===
  BIKE  : Royal Enfield Classic 350 to Spandan for 2 day(s) = Rs.798 (+2 helmets, MCWG licence)
  CAR   : Hyundai Creta to Riya for 8 day(s) = Rs.15,833 (5 seats, AC)
  TRUCK : Tata LPT 1109 to Shree Logistics for 3 day(s) = Rs.16,497 (payload 9 t, HMV licence, Rs.1,500 loading)
  revenue booked: Rs.33,128

=== double rent and return ===
  Royal Enfield Classic 350 is already rented
  Royal Enfield Classic 350 returned by Spandan
  BIKE  : Royal Enfield Classic 350 to Aman for 1 day(s) = Rs.399 (+2 helmets, MCWG licence)

=== unknown type ===
   we do not rent 'helicopter'; available: bike, car, truck

=== extending the fleet later ===
[factory] new vehicle type available: escooter
  ESCOOT: Ather 450X to Neha for 4 day(s) = Rs.1,196 (no licence needed)
  rentable types now: ['bike', 'car', 'escooter', 'truck']

=== final fleet state ===
   Bike   Royal Enfield Classic 350 MH12-AB-1234 2 wheels  Rs.  399/day  [with Aman]
   Car    Hyundai Creta    MH12-CD-5678 4 wheels  Rs. 2199/day  [with Riya]
   Truck  Tata LPT 1109    MH12-EF-9012 6 wheels  Rs. 4999/day  [with Shree Logistics]

```

</details>

---

## Experiment 3 - Question 9: Sorter Strategy

Scenario: Different sorting algorithms (bubble, quick) implemented as
strategies that can be applied at runtime.

Rubrics covered:
  * strategy classes implemented
  * a context class applies the selected strategy
  * both sorting methods demonstrated
  * pros and cons analysed

**File:** [`q9_sorter_strategy.py`](q9_sorter_strategy.py) &nbsp;&middot;&nbsp; **Run:** `python q9_sorter_strategy.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 3 - Question 9: Sorter Strategy

Scenario: Different sorting algorithms (bubble, quick) implemented as
strategies that can be applied at runtime.

Rubrics covered:
  * strategy classes implemented
  * a context class applies the selected strategy
  * both sorting methods demonstrated
  * pros and cons analysed
"""

import random
import time
from abc import ABC, abstractmethod


class SortStrategy(ABC):
    name = "strategy"
    complexity = ""
    stable = None
    extra_space = ""

    @abstractmethod
    def sort(self, data):
        """Returns a new sorted list and the number of comparisons made."""


class BubbleSort(SortStrategy):
    name = "BubbleSort"
    complexity = "O(n^2) average and worst, O(n) best"
    stable = True
    extra_space = "O(1) in place"

    def sort(self, data):
        arr = list(data)
        comparisons = swaps = 0
        n = len(arr)
        for i in range(n - 1):
            swapped = False
            for j in range(n - 1 - i):
                comparisons += 1
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swaps += 1
                    swapped = True
            if not swapped:                     # already sorted
                break
        return arr, comparisons, swaps


class QuickSort(SortStrategy):
    name = "QuickSort"
    complexity = "O(n log n) average, O(n^2) worst"
    stable = False
    extra_space = "O(log n) recursion stack"

    def sort(self, data):
        self.comparisons = 0
        arr = self._quick(list(data))
        return arr, self.comparisons, 0

    def _quick(self, arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        less, equal, greater = [], [], []
        for x in arr:
            self.comparisons += 1
            if x < pivot:
                less.append(x)
            elif x > pivot:
                greater.append(x)
            else:
                equal.append(x)
        return self._quick(less) + equal + self._quick(greater)


class InsertionSort(SortStrategy):
    name = "InsertionSort"
    complexity = "O(n^2) worst, O(n) nearly sorted"
    stable = True
    extra_space = "O(1) in place"

    def sort(self, data):
        arr = list(data)
        comparisons = shifts = 0
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0:
                comparisons += 1
                if arr[j] > key:
                    arr[j + 1] = arr[j]
                    shifts += 1
                    j -= 1
                else:
                    break
            arr[j + 1] = key
        return arr, comparisons, shifts


class TimSortBuiltin(SortStrategy):
    name = "Python sorted()"
    complexity = "O(n log n) worst (Timsort)"
    stable = True
    extra_space = "O(n)"

    def sort(self, data):
        return sorted(data), 0, 0


class Sorter:
    """Context: holds a strategy, which can be replaced at runtime."""

    def __init__(self, strategy=None):
        self._strategy = strategy

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        if not isinstance(strategy, SortStrategy):
            raise TypeError("needs a SortStrategy")
        self._strategy = strategy

    def run(self, data, show=True):
        if self._strategy is None:
            raise RuntimeError("no sorting strategy selected")
        start = time.perf_counter()
        result, comparisons, moves = self._strategy.sort(data)
        elapsed = (time.perf_counter() - start) * 1000
        if show:
            preview = result[:10]
            print(f"  {self._strategy.name:<16} {elapsed:>8.3f} ms  "
                  f"comparisons={comparisons:<7} moves={moves:<7} "
                  f"-> {preview}{' ...' if len(result) > 10 else ''}")
        return result, comparisons, elapsed


if __name__ == "__main__":
    random.seed(3)
    strategies = [BubbleSort(), QuickSort(), InsertionSort(), TimSortBuiltin()]
    sorter = Sorter()

    small = [42, 7, 19, 73, 3, 56, 88, 1, 64, 25]
    print(f"=== small random list: {small} ===")
    for s in strategies:
        sorter.strategy = s                     # runtime switch
        sorter.run(small)

    nearly = list(range(1, 31))
    nearly[5], nearly[6] = nearly[6], nearly[5]
    print("\n=== nearly sorted list of 30 (bubble/insertion shine here) ===")
    for s in strategies:
        sorter.strategy = s
        sorter.run(nearly)

    big = [random.randint(1, 10000) for _ in range(800)]
    print("\n=== random list of 800 (quadratic sorts fall behind) ===")
    for s in strategies:
        sorter.strategy = s
        sorter.run(big)

    print("\n=== all strategies produce the same answer ===")
    answers = [tuple(Sorter(s).run(big, show=False)[0]) for s in strategies]
    print("  identical results:", len(set(answers)) == 1)

    print("\n=== pros and cons ===")
    print(f"  {'Strategy':<16} {'Complexity':<34} {'Stable':<7} Extra space")
    print("  " + "-" * 76)
    for s in strategies:
        print(f"  {s.name:<16} {s.complexity:<34} {str(s.stable):<7} "
              f"{s.extra_space}")
    print("\n  Bubble/Insertion : simple, in place, fine for tiny or nearly"
          " sorted data.")
    print("  Quick            : fastest in practice, but recursive and not"
          " stable.")
    print("  sorted()         : C-implemented Timsort, the right default in"
          " real code.")
```

</details>

<details>
<summary>Program output</summary>

```text
=== small random list: [42, 7, 19, 73, 3, 56, 88, 1, 64, 25] ===
  BubbleSort          0.012 ms  comparisons=44      moves=21      -> [1, 3, 7, 19, 25, 42, 56, 64, 73, 88]
  QuickSort           0.014 ms  comparisons=27      moves=0       -> [1, 3, 7, 19, 25, 42, 56, 64, 73, 88]
  InsertionSort       0.007 ms  comparisons=27      moves=21      -> [1, 3, 7, 19, 25, 42, 56, 64, 73, 88]
  Python sorted()     0.003 ms  comparisons=0       moves=0       -> [1, 3, 7, 19, 25, 42, 56, 64, 73, 88]

=== nearly sorted list of 30 (bubble/insertion shine here) ===
  BubbleSort          0.006 ms  comparisons=57      moves=1       -> [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] ...
  QuickSort           0.020 ms  comparisons=111     moves=0       -> [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] ...
  InsertionSort       0.005 ms  comparisons=30      moves=1       -> [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] ...
  Python sorted()     0.001 ms  comparisons=0       moves=0       -> [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] ...

=== random list of 800 (quadratic sorts fall behind) ===
  BubbleSort         28.988 ms  comparisons=319545  moves=167173  -> [30, 39, 45, 58, 60, 77, 81, 113, 119, 123] ...
  QuickSort           0.905 ms  comparisons=8585    moves=0       -> [30, 39, 45, 58, 60, 77, 81, 113, 119, 123] ...
  InsertionSort      15.877 ms  comparisons=167966  moves=167173  -> [30, 39, 45, 58, 60, 77, 81, 113, 119, 123] ...
  Python sorted()     0.062 ms  comparisons=0       moves=0       -> [30, 39, 45, 58, 60, 77, 81, 113, 119, 123] ...

=== all strategies produce the same answer ===
  identical results: True

=== pros and cons ===
  Strategy         Complexity                         Stable  Extra space
  ----------------------------------------------------------------------------
  BubbleSort       O(n^2) average and worst, O(n) best True    O(1) in place
  QuickSort        O(n log n) average, O(n^2) worst   False   O(log n) recursion stack
  InsertionSort    O(n^2) worst, O(n) nearly sorted   True    O(1) in place
  Python sorted()  O(n log n) worst (Timsort)         True    O(n)

  Bubble/Insertion : simple, in place, fine for tiny or nearly sorted data.
  Quick            : fastest in practice, but recursive and not stable.
  sorted()         : C-implemented Timsort, the right default in real code.

```

</details>

---

## Experiment 3 - Question 10: Stock Price Notifier

Scenario: A stock monitoring app that notifies every subscribed user when the
price of a stock changes.

Rubrics covered:
  * Observer pattern used
  * subscribers added and removed
  * notification on every stock update
  * logs printed for each update

**File:** [`q10_stock_price_notifier.py`](q10_stock_price_notifier.py) &nbsp;&middot;&nbsp; **Run:** `python q10_stock_price_notifier.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== subscriptions ===
  + Spandan now follows TCS (1 subscriber(s))
  + AlgoBot now follows TCS (2 subscriber(s))
  + PortfolioApp now follows TCS (3 subscriber(s))
  + RiskDesk now follows TCS (4 subscriber(s))
  Spandan already follows TCS

[TCS] TCS Rs.3,850.00 -> Rs.3,920.50 (+1.83%)  notifying 4 subscriber(s)
   [08:42:58] Spandan          TCS is UP to Rs.3,920.50
   [08:42:58] PortfolioApp     25 shares of TCS: portfolio +1,762.50 (now Rs.98,012.50)

[TCS] unchanged at Rs.3,920.50, no notification

[TCS] TCS Rs.3,920.50 -> Rs.3,570.00 (-8.94%)  notifying 4 subscriber(s)
   [08:42:58] Spandan          TCS is DOWN to Rs.3,570.00
   [08:42:58] AlgoBot          BUY SIGNAL TCS at Rs.3,570.00 (target <= 3600)
   [08:42:58] PortfolioApp     25 shares of TCS: portfolio -8,762.50 (now Rs.89,250.00)
   [08:42:58] RiskDesk         VOLATILITY 8.94% move in TCS

[TCS] TCS Rs.3,570.00 -> Rs.4,150.75 (+16.27%)  notifying 4 subscriber(s)
   [08:42:58] Spandan          TCS is UP to Rs.4,150.75
   [08:42:58] AlgoBot          SELL SIGNAL TCS at Rs.4,150.75 (target >= 4100)
   [08:42:58] PortfolioApp     25 shares of TCS: portfolio +14,518.75 (now Rs.103,768.75)
   [08:42:58] RiskDesk         VOLATILITY 16.27% move in TCS

=== one subscriber leaves ===
  - RiskDesk unfollowed TCS (3 left)
  Stranger does not follow TCS

[TCS] TCS Rs.4,150.75 -> Rs.3,999.00 (-3.66%)  notifying 3 subscriber(s)
   [08:42:58] Spandan          TCS is DOWN to Rs.3,999.00
   [08:42:58] PortfolioApp     25 shares of TCS: portfolio -3,793.75 (now Rs.99,975.00)

=== update log ===
   TCS Rs.3,850.00 -> Rs.3,920.50 (+1.83%)
   TCS Rs.3,920.50 -> Rs.3,570.00 (-8.94%)
   TCS Rs.3,570.00 -> Rs.4,150.75 (+16.27%)
   TCS Rs.4,150.75 -> Rs.3,999.00 (-3.66%)

=== alerts received ===
  Spandan          4 alert(s)
  AlgoBot          2 alert(s)
  PortfolioApp     4 alert(s)
  RiskDesk         2 alert(s)

```

</details>

---
