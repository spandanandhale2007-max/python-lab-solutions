# Experiment 1 - Unit I

OOP fundamentals: classes, encapsulation, inheritance, polymorphism, magic methods

10 scenario questions, each solved in its own section and its own file. Every program below was executed and the real output is included.

[Back to the index](../README.md)

---

## Questions in this experiment

- [Experiment 1 - Question 1: Student Record System](#experiment-1---question-1-student-record-system)
- [Experiment 1 - Question 2: ATM Simulation](#experiment-1---question-2-atm-simulation)
- [Experiment 1 - Question 3: Bank with Static Interest Rate](#experiment-1---question-3-bank-with-static-interest-rate)
- [Experiment 1 - Question 4: Library Book Borrowing](#experiment-1---question-4-library-book-borrowing)
- [Experiment 1 - Question 5: Shape Hierarchy](#experiment-1---question-5-shape-hierarchy)
- [Experiment 1 - Question 6: Car vs ElectricCar](#experiment-1---question-6-car-vs-electriccar)
- [Experiment 1 - Question 7: Movie Ticket Booking](#experiment-1---question-7-movie-ticket-booking)
- [Experiment 1 - Question 8: Product with Magic Methods](#experiment-1---question-8-product-with-magic-methods)
- [Experiment 1 - Question 9: Thermostat Controller](#experiment-1---question-9-thermostat-controller)
- [Experiment 1 - Question 10: School Staff and Students](#experiment-1---question-10-school-staff-and-students)

---

## Experiment 1 - Question 1: Student Record System

Scenario: A college system maintains student records. Each student has a name,
roll number and three subject marks. Calculate the average and display
formatted details.

Rubrics covered:
  * __init__ initialises student data
  * instance methods for average and display
  * __str__ overridden for clean print
  * multiple students instantiated

**File:** [`q1_student_record_system.py`](q1_student_record_system.py) &nbsp;&middot;&nbsp; **Run:** `python q1_student_record_system.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 1 - Question 1: Student Record System

Scenario: A college system maintains student records. Each student has a name,
roll number and three subject marks. Calculate the average and display
formatted details.

Rubrics covered:
  * __init__ initialises student data
  * instance methods for average and display
  * __str__ overridden for clean print
  * multiple students instantiated
"""


class Student:
    def __init__(self, name, roll_no, marks):
        if len(marks) != 3:
            raise ValueError("exactly three subject marks are required")
        self.name = name
        self.roll_no = roll_no
        self.marks = list(marks)

    def average(self):
        return sum(self.marks) / len(self.marks)

    def grade(self):
        avg = self.average()
        for cutoff, letter in ((90, "A+"), (80, "A"), (70, "B"), (60, "C"), (40, "D")):
            if avg >= cutoff:
                return letter
        return "F"

    def display(self):
        print(f"Roll No : {self.roll_no}")
        print(f"Name    : {self.name}")
        print(f"Marks   : {self.marks}")
        print(f"Average : {self.average():.2f}  (Grade {self.grade()})")
        print("-" * 40)

    def __str__(self):
        return (f"{self.roll_no} | {self.name:<12} | marks={self.marks} | "
                f"avg={self.average():.2f} | grade={self.grade()}")


if __name__ == "__main__":
    students = [
        Student("Spandan", "CSE2301", [88, 92, 79]),
        Student("Riya", "CSE2302", [95, 91, 98]),
        Student("Aman", "CSE2303", [55, 61, 48]),
    ]

    print("=== Detailed report (display method) ===")
    for s in students:
        s.display()

    print("=== One-line report (__str__ override) ===")
    for s in students:
        print(s)

    topper = max(students, key=Student.average)
    print(f"\nClass topper: {topper.name} with {topper.average():.2f}")
```

</details>

<details>
<summary>Program output</summary>

```text
=== Detailed report (display method) ===
Roll No : CSE2301
Name    : Spandan
Marks   : [88, 92, 79]
Average : 86.33  (Grade A)
----------------------------------------
Roll No : CSE2302
Name    : Riya
Marks   : [95, 91, 98]
Average : 94.67  (Grade A+)
----------------------------------------
Roll No : CSE2303
Name    : Aman
Marks   : [55, 61, 48]
Average : 54.67  (Grade D)
----------------------------------------
=== One-line report (__str__ override) ===
CSE2301 | Spandan      | marks=[88, 92, 79] | avg=86.33 | grade=A
CSE2302 | Riya         | marks=[95, 91, 98] | avg=94.67 | grade=A+
CSE2303 | Aman         | marks=[55, 61, 48] | avg=54.67 | grade=D

Class topper: Riya with 94.67

```

</details>

---

## Experiment 1 - Question 2: ATM Simulation

Scenario: Simulate an ATM. A user can deposit, withdraw and check balance.
The balance must not be directly accessible or modifiable from outside.

Rubrics covered:
  * private variable for balance (name-mangled __balance)
  * instance variables plus class variables used correctly
  * validation for withdrawal limits
  * user-friendly interaction methods

**File:** [`q2_atm_simulation.py`](q2_atm_simulation.py) &nbsp;&middot;&nbsp; **Run:** `python q2_atm_simulation.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
State Bank of Pune | Spandan Andhale | Balance Rs.5000

-- valid transactions --
Deposited Rs.2000. Available balance Rs.7000
Please collect Rs.1500. Available balance Rs.5500

-- validation checks --
Withdrawal failed: only multiples of Rs.100 are dispensed.
Withdrawal failed: per-transaction limit is Rs.10000
Withdrawal failed: balance cannot fall below Rs.500 (available Rs.5500)
Deposit failed: amount must be positive.

-- encapsulation proof --
Direct assignment blocked: property 'balance' of 'ATMAccount' object has no setter
Stored privately as: ['_ATMAccount__balance']
State Bank of Pune | Spandan Andhale | Balance Rs.5500

```

</details>

---

## Experiment 1 - Question 3: Bank with Static Interest Rate

Scenario: A bank applies the same interest rate to all savings accounts.
Calculate compound interest and allow updating the rate across all accounts.

Rubrics covered:
  * static/class variable for the interest rate
  * class method to update the rate
  * instance method to calculate interest
  * effect of a rate change is shown

**File:** [`q3_bank_static_interest.py`](q3_bank_static_interest.py) &nbsp;&middot;&nbsp; **Run:** `python q3_bank_static_interest.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== Before rate change (rate = 6.5%) ===
Spandan    maturity(3y)=Rs.   60,670.38 interest=Rs. 10,670.38
Riya       maturity(3y)=Rs.  151,675.95 interest=Rs. 26,675.95
Aman       maturity(3y)=Rs.    9,707.26 interest=Rs.  1,707.26
[BANK] Interest rate changed for ALL accounts: 6.5% -> 7.25%

=== After rate change (rate = 7.25%) ===
Spandan    maturity(3y)=Rs.   62,027.35 interest=Rs. 12,027.35
Riya       maturity(3y)=Rs.  155,068.37 interest=Rs. 30,068.37
Aman       maturity(3y)=Rs.    9,924.38 interest=Rs.  1,924.38

Every instance sees the same class variable:
   Spandan    principal=Rs.50,000.00 rate=7.25%
   Riya       principal=Rs.125,000.00 rate=7.25%
   Aman       principal=Rs. 8,000.00 rate=7.25%

```

</details>

---

## Experiment 1 - Question 4: Library Book Borrowing

Scenario: A library system where members borrow books. Each book has a title,
author and availability status. A member can borrow/return books and view the
borrowed list.

Rubrics covered:
  * two classes: Book and Member
  * composition (a Member holds Book objects)
  * book status tracked (borrowed/available)
  * borrowing and returning logic implemented

**File:** [`q4_library_borrowing.py`](q4_library_borrowing.py) &nbsp;&middot;&nbsp; **Run:** `python q4_library_borrowing.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 1 - Question 4: Library Book Borrowing

Scenario: A library system where members borrow books. Each book has a title,
author and availability status. A member can borrow/return books and view the
borrowed list.

Rubrics covered:
  * two classes: Book and Member
  * composition (a Member holds Book objects)
  * book status tracked (borrowed/available)
  * borrowing and returning logic implemented
"""


class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = True
        self.borrowed_by = None

    def __str__(self):
        state = "available" if self.is_available else f"with {self.borrowed_by}"
        return f"{self.title:<28} by {self.author:<18} [{state}]"


class Member:
    MAX_BOOKS = 3

    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed = []          # composition: Member has-a list of Book

    def borrow(self, book):
        if not book.is_available:
            print(f"DENIED  : '{book.title}' is already borrowed by {book.borrowed_by}")
            return False
        if len(self.borrowed) >= Member.MAX_BOOKS:
            print(f"DENIED  : {self.name} already holds {Member.MAX_BOOKS} books")
            return False
        book.is_available = False
        book.borrowed_by = self.name
        self.borrowed.append(book)
        print(f"ISSUED  : '{book.title}' -> {self.name}")
        return True

    def return_book(self, book):
        if book not in self.borrowed:
            print(f"DENIED  : {self.name} did not borrow '{book.title}'")
            return False
        self.borrowed.remove(book)
        book.is_available = True
        book.borrowed_by = None
        print(f"RETURNED: '{book.title}' <- {self.name}")
        return True

    def view_borrowed(self):
        print(f"\n{self.name} ({self.member_id}) has {len(self.borrowed)} book(s):")
        if not self.borrowed:
            print("   (none)")
        for b in self.borrowed:
            print("   -", b.title)

    def __str__(self):
        return f"<Member {self.name} books={len(self.borrowed)}>"


class Library:
    def __init__(self, name):
        self.name = name
        self.catalogue = []

    def add_book(self, book):
        self.catalogue.append(book)

    def show_catalogue(self):
        print(f"\n=== {self.name} catalogue ===")
        for b in self.catalogue:
            print("  ", b)


if __name__ == "__main__":
    lib = Library("MIT-WPU Central Library")
    b1 = Book("Python Crash Course", "Eric Matthes", "978-1593279288")
    b2 = Book("Clean Code", "Robert Martin", "978-0132350884")
    b3 = Book("Introduction to Algorithms", "Cormen", "978-0262033848")
    b4 = Book("Fluent Python", "Luciano Ramalho", "978-1492056355")
    for b in (b1, b2, b3, b4):
        lib.add_book(b)

    spandan = Member("Spandan", "M-101")
    riya = Member("Riya", "M-102")

    lib.show_catalogue()

    print("\n--- borrowing ---")
    spandan.borrow(b1)
    spandan.borrow(b2)
    riya.borrow(b1)          # already issued
    riya.borrow(b3)

    spandan.view_borrowed()
    riya.view_borrowed()

    print("\n--- returning ---")
    spandan.return_book(b1)
    spandan.return_book(b4)  # never borrowed
    riya.borrow(b1)          # now free

    lib.show_catalogue()
    spandan.view_borrowed()
    riya.view_borrowed()
```

</details>

<details>
<summary>Program output</summary>

```text
=== MIT-WPU Central Library catalogue ===
   Python Crash Course          by Eric Matthes       [available]
   Clean Code                   by Robert Martin      [available]
   Introduction to Algorithms   by Cormen             [available]
   Fluent Python                by Luciano Ramalho    [available]

--- borrowing ---
ISSUED  : 'Python Crash Course' -> Spandan
ISSUED  : 'Clean Code' -> Spandan
DENIED  : 'Python Crash Course' is already borrowed by Spandan
ISSUED  : 'Introduction to Algorithms' -> Riya

Spandan (M-101) has 2 book(s):
   - Python Crash Course
   - Clean Code

Riya (M-102) has 1 book(s):
   - Introduction to Algorithms

--- returning ---
RETURNED: 'Python Crash Course' <- Spandan
DENIED  : Spandan did not borrow 'Fluent Python'
ISSUED  : 'Python Crash Course' -> Riya

=== MIT-WPU Central Library catalogue ===
   Python Crash Course          by Eric Matthes       [with Riya]
   Clean Code                   by Robert Martin      [with Spandan]
   Introduction to Algorithms   by Cormen             [with Riya]
   Fluent Python                by Luciano Ramalho    [available]

Spandan (M-101) has 1 book(s):
   - Clean Code

Riya (M-102) has 2 book(s):
   - Introduction to Algorithms
   - Python Crash Course

```

</details>

---

## Experiment 1 - Question 5: Shape Hierarchy

Scenario: A geometry toolkit with a base class Shape and derived classes
Circle, Rectangle and Triangle with area calculations.

Rubrics covered:
  * common behaviour inherited from Shape
  * area() overridden (polymorphism)
  * base class reference used for derived objects
  * constructor chaining with super()

**File:** [`q5_shape_hierarchy.py`](q5_shape_hierarchy.py) &nbsp;&middot;&nbsp; **Run:** `python q5_shape_hierarchy.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 1 - Question 5: Shape Hierarchy

Scenario: A geometry toolkit with a base class Shape and derived classes
Circle, Rectangle and Triangle with area calculations.

Rubrics covered:
  * common behaviour inherited from Shape
  * area() overridden (polymorphism)
  * base class reference used for derived objects
  * constructor chaining with super()
"""

import math
from abc import ABC, abstractmethod


class Shape(ABC):
    def __init__(self, name):
        self.name = name            # common state for every shape

    @abstractmethod
    def area(self):
        ...

    @abstractmethod
    def perimeter(self):
        ...

    def describe(self):             # common behaviour, inherited as-is
        return (f"{self.name:<10} area={self.area():8.2f}  "
                f"perimeter={self.perimeter():8.2f}")

    def __str__(self):
        return self.describe()


class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Circle")          # constructor chaining
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    def __init__(self, width, height):
        super().__init__("Rectangle")
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)        # two-level constructor chaining
        self.name = "Square"


class Triangle(Shape):
    def __init__(self, a, b, c):
        super().__init__("Triangle")
        if a + b <= c or b + c <= a or a + c <= b:
            raise ValueError("sides do not form a triangle")
        self.a, self.b, self.c = a, b, c

    def area(self):
        s = self.perimeter() / 2            # Heron's formula
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self):
        return self.a + self.b + self.c


if __name__ == "__main__":
    # a list of base-class references holding derived objects
    shapes = [Circle(5), Rectangle(8, 3), Square(4), Triangle(3, 4, 5)]

    print("=== polymorphic dispatch through Shape references ===")
    for s in shapes:
        print(s)

    print(f"\nTotal area of all shapes : {sum(s.area() for s in shapes):.2f}")
    biggest = max(shapes, key=lambda s: s.area())
    print(f"Largest shape            : {biggest.name} ({biggest.area():.2f})")

    print("\nType checks:")
    sq = shapes[2]
    print("  Square is a Rectangle :", isinstance(sq, Rectangle))
    print("  Square is a Shape     :", isinstance(sq, Shape))
    print("  Shape cannot be built :", end=" ")
    try:
        Shape("generic")
    except TypeError as e:
        print(type(e).__name__, "-", e)
```

</details>

<details>
<summary>Program output</summary>

```text
=== polymorphic dispatch through Shape references ===
Circle     area=   78.54  perimeter=   31.42
Rectangle  area=   24.00  perimeter=   22.00
Square     area=   16.00  perimeter=   16.00
Triangle   area=    6.00  perimeter=   12.00

Total area of all shapes : 124.54
Largest shape            : Circle (78.54)

Type checks:
  Square is a Rectangle : True
  Square is a Shape     : True
  Shape cannot be built : TypeError - Can't instantiate abstract class Shape without an implementation for abstract methods 'area', 'perimeter'

```

</details>

---

## Experiment 1 - Question 6: Car vs ElectricCar

Scenario: A car showroom simulation. Class Car has properties like fuel type;
ElectricCar overrides behaviour to simulate electric-specific features.

Rubrics covered:
  * inheritance and method overriding
  * refuel() differs in base vs derived class
  * constructor reuse with super()
  * realistic attributes and methods

**File:** [`q6_car_vs_electriccar.py`](q6_car_vs_electriccar.py) &nbsp;&middot;&nbsp; **Run:** `python q6_car_vs_electriccar.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 1 - Question 6: Car vs ElectricCar

Scenario: A car showroom simulation. Class Car has properties like fuel type;
ElectricCar overrides behaviour to simulate electric-specific features.

Rubrics covered:
  * inheritance and method overriding
  * refuel() differs in base vs derived class
  * constructor reuse with super()
  * realistic attributes and methods
"""


class Car:
    def __init__(self, brand, model, price, fuel_type="Petrol",
                 tank_capacity=40, mileage=18.0):
        self.brand = brand
        self.model = model
        self.price = price
        self.fuel_type = fuel_type
        self.tank_capacity = tank_capacity     # litres
        self.mileage = mileage                 # km per litre
        self.fuel_level = 0.0
        self.odometer = 0.0

    def refuel(self, litres):
        space = self.tank_capacity - self.fuel_level
        added = min(litres, space)
        self.fuel_level += added
        print(f"[{self.model}] Pumped {added:.1f} L of {self.fuel_type}. "
              f"Tank {self.fuel_level:.1f}/{self.tank_capacity} L")
        if added < litres:
            print(f"   (tank full, {litres - added:.1f} L not taken)")

    def range_left(self):
        return self.fuel_level * self.mileage

    def drive(self, km):
        if km > self.range_left():
            print(f"[{self.model}] Cannot drive {km} km, range is only "
                  f"{self.range_left():.0f} km")
            return False
        self.fuel_level -= km / self.mileage
        self.odometer += km
        print(f"[{self.model}] Drove {km} km. Range left {self.range_left():.0f} km")
        return True

    def running_cost_per_km(self, fuel_price=106.0):
        return fuel_price / self.mileage

    def __str__(self):
        return (f"{self.brand} {self.model} | {self.fuel_type} | "
                f"Rs.{self.price:,} | {self.mileage} km/L | "
                f"odo {self.odometer:.0f} km")


class ElectricCar(Car):
    def __init__(self, brand, model, price, battery_kwh, km_per_kwh,
                 charger_kw=7.2):
        # constructor reuse: tank_capacity -> battery kWh, mileage -> km per kWh
        super().__init__(brand, model, price, fuel_type="Electric",
                         tank_capacity=battery_kwh, mileage=km_per_kwh)
        self.battery_kwh = battery_kwh
        self.charger_kw = charger_kw

    def battery_percent(self):
        return 100.0 * self.fuel_level / self.battery_kwh

    # --- overridden behaviour ---
    def refuel(self, kwh):
        space = self.battery_kwh - self.fuel_level
        added = min(kwh, space)
        self.fuel_level += added
        hours = added / self.charger_kw
        print(f"[{self.model}] Charged {added:.1f} kWh in {hours:.1f} h on a "
              f"{self.charger_kw} kW charger. Battery {self.battery_percent():.0f}%")
        if added < kwh:
            print(f"   (battery full, {kwh - added:.1f} kWh not taken)")

    def running_cost_per_km(self, unit_price=9.0):
        return unit_price / self.mileage

    def __str__(self):
        return (f"{self.brand} {self.model} | Electric | Rs.{self.price:,} | "
                f"{self.battery_kwh} kWh | {self.mileage} km/kWh | "
                f"battery {self.battery_percent():.0f}% | odo {self.odometer:.0f} km")


if __name__ == "__main__":
    showroom = [
        Car("Maruti", "Swift VXi", 799000, tank_capacity=37, mileage=22.4),
        ElectricCar("Tata", "Nexon EV", 1499000, battery_kwh=40.5, km_per_kwh=7.0),
    ]

    print("=== Showroom stock ===")
    for c in showroom:
        print(" ", c)

    print("\n=== refuel() resolves differently for each class ===")
    for c in showroom:
        c.refuel(20)

    print("\n=== same drive() inherited by both ===")
    for c in showroom:
        c.drive(120)

    print("\n=== running cost comparison ===")
    for c in showroom:
        print(f"  {c.model:<12} Rs.{c.running_cost_per_km():.2f} per km")

    print("\n=== final state ===")
    for c in showroom:
        print(" ", c)

    print("\nElectricCar is a Car:", isinstance(showroom[1], Car))
    print("MRO:", [k.__name__ for k in ElectricCar.__mro__])
```

</details>

<details>
<summary>Program output</summary>

```text
=== Showroom stock ===
  Maruti Swift VXi | Petrol | Rs.799,000 | 22.4 km/L | odo 0 km
  Tata Nexon EV | Electric | Rs.1,499,000 | 40.5 kWh | 7.0 km/kWh | battery 0% | odo 0 km

=== refuel() resolves differently for each class ===
[Swift VXi] Pumped 20.0 L of Petrol. Tank 20.0/37 L
[Nexon EV] Charged 20.0 kWh in 2.8 h on a 7.2 kW charger. Battery 49%

=== same drive() inherited by both ===
[Swift VXi] Drove 120 km. Range left 328 km
[Nexon EV] Drove 120 km. Range left 20 km

=== running cost comparison ===
  Swift VXi    Rs.4.73 per km
  Nexon EV     Rs.1.29 per km

=== final state ===
  Maruti Swift VXi | Petrol | Rs.799,000 | 22.4 km/L | odo 120 km
  Tata Nexon EV | Electric | Rs.1,499,000 | 40.5 kWh | 7.0 km/kWh | battery 7% | odo 120 km

ElectricCar is a Car: True
MRO: ['ElectricCar', 'Car', 'object']

```

</details>

---

## Experiment 1 - Question 7: Movie Ticket Booking

Scenario: A ticket booking system. Each theatre has a limited number of seats.
A customer can book a seat and the system tracks which seats are available.

Rubrics covered:
  * static (class) variables track seat availability and ticket count
  * double booking handled with a custom exception
  * modular design: Theater, Ticket, Customer classes
  * booking summary displayed

**File:** [`q7_movie_ticket_booking.py`](q7_movie_ticket_booking.py) &nbsp;&middot;&nbsp; **Run:** `python q7_movie_ticket_booking.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 1 - Question 7: Movie Ticket Booking

Scenario: A ticket booking system. Each theatre has a limited number of seats.
A customer can book a seat and the system tracks which seats are available.

Rubrics covered:
  * static (class) variables track seat availability and ticket count
  * double booking handled with a custom exception
  * modular design: Theater, Ticket, Customer classes
  * booking summary displayed
"""


class SeatUnavailableError(Exception):
    """Raised when a seat is already booked or does not exist."""


class Ticket:
    total_tickets_issued = 0          # static counter shared by all tickets

    def __init__(self, movie, seat, customer, price):
        Ticket.total_tickets_issued += 1
        self.ticket_id = f"TK{Ticket.total_tickets_issued:04d}"
        self.movie = movie
        self.seat = seat
        self.customer = customer
        self.price = price

    def __str__(self):
        return (f"{self.ticket_id} | {self.movie:<14} | seat {self.seat:<4} | "
                f"{self.customer:<10} | Rs.{self.price}")


class Customer:
    def __init__(self, name):
        self.name = name
        self.tickets = []

    def total_spent(self):
        return sum(t.price for t in self.tickets)

    def __str__(self):
        return f"{self.name} ({len(self.tickets)} ticket(s), Rs.{self.total_spent()})"


class Theater:
    seats_available = 0               # static view across all screens

    def __init__(self, name, movie, rows=3, cols=4, price=250):
        self.name = name
        self.movie = movie
        self.price = price
        self.seats = {f"{chr(65 + r)}{c + 1}": None
                      for r in range(rows) for c in range(cols)}
        Theater.seats_available += len(self.seats)

    def book(self, customer, seat):
        seat = seat.upper()
        if seat not in self.seats:
            raise SeatUnavailableError(f"seat {seat} does not exist in {self.name}")
        if self.seats[seat] is not None:
            raise SeatUnavailableError(
                f"seat {seat} is already booked by {self.seats[seat].customer}")
        ticket = Ticket(self.movie, seat, customer.name, self.price)
        self.seats[seat] = ticket
        customer.tickets.append(ticket)
        Theater.seats_available -= 1
        print(f"BOOKED  : {ticket}")
        return ticket

    def cancel(self, seat):
        seat = seat.upper()
        ticket = self.seats.get(seat)
        if ticket is None:
            raise SeatUnavailableError(f"seat {seat} is not booked")
        self.seats[seat] = None
        Theater.seats_available += 1
        print(f"CANCELED: {ticket}")

    def seat_map(self):
        print(f"\n--- {self.name}: {self.movie} ---")
        row = None
        for seat in sorted(self.seats):
            if seat[0] != row:
                row = seat[0]
                print(f"\n  Row {row}: ", end="")
            print("[XX]" if self.seats[seat] else f"[{seat}]", end=" ")
        free = sum(1 for t in self.seats.values() if t is None)
        print(f"\n  free {free}/{len(self.seats)}   (XX = booked)")

    def summary(self):
        sold = [t for t in self.seats.values() if t]
        print(f"\n=== Booking summary: {self.name} ===")
        for t in sold:
            print("  ", t)
        print(f"  Tickets sold : {len(sold)}")
        print(f"  Revenue      : Rs.{sum(t.price for t in sold)}")


if __name__ == "__main__":
    pvr = Theater("PVR Screen 2", "Dune Part Two", rows=3, cols=4, price=280)
    spandan, riya = Customer("Spandan"), Customer("Riya")

    pvr.seat_map()

    print("\n--- bookings ---")
    pvr.book(spandan, "A1")
    pvr.book(spandan, "A2")
    pvr.book(riya, "B3")

    print("\n--- double booking and a bad seat ---")
    for cust, seat in ((riya, "A1"), (riya, "Z9")):
        try:
            pvr.book(cust, seat)
        except SeatUnavailableError as e:
            print("REJECTED:", e)

    print("\n--- cancellation then rebooking ---")
    pvr.cancel("A2")
    pvr.book(riya, "A2")

    pvr.seat_map()
    pvr.summary()
    print(f"\nStatic counters -> tickets issued: {Ticket.total_tickets_issued}, "
          f"seats free across all screens: {Theater.seats_available}")
    print("Customers:", spandan, "|", riya)
```

</details>

<details>
<summary>Program output</summary>

```text
--- PVR Screen 2: Dune Part Two ---

  Row A: [A1] [A2] [A3] [A4] 
  Row B: [B1] [B2] [B3] [B4] 
  Row C: [C1] [C2] [C3] [C4] 
  free 12/12   (XX = booked)

--- bookings ---
BOOKED  : TK0001 | Dune Part Two  | seat A1   | Spandan    | Rs.280
BOOKED  : TK0002 | Dune Part Two  | seat A2   | Spandan    | Rs.280
BOOKED  : TK0003 | Dune Part Two  | seat B3   | Riya       | Rs.280

--- double booking and a bad seat ---
REJECTED: seat A1 is already booked by Spandan
REJECTED: seat Z9 does not exist in PVR Screen 2

--- cancellation then rebooking ---
CANCELED: TK0002 | Dune Part Two  | seat A2   | Spandan    | Rs.280
BOOKED  : TK0004 | Dune Part Two  | seat A2   | Riya       | Rs.280

--- PVR Screen 2: Dune Part Two ---

  Row A: [XX] [XX] [A3] [A4] 
  Row B: [B1] [B2] [XX] [B4] 
  Row C: [C1] [C2] [C3] [C4] 
  free 9/12   (XX = booked)

=== Booking summary: PVR Screen 2 ===
   TK0001 | Dune Part Two  | seat A1   | Spandan    | Rs.280
   TK0004 | Dune Part Two  | seat A2   | Riya       | Rs.280
   TK0003 | Dune Part Two  | seat B3   | Riya       | Rs.280
  Tickets sold : 3
  Revenue      : Rs.840

Static counters -> tickets issued: 4, seats free across all screens: 9
Customers: Spandan (2 ticket(s), Rs.560) | Riya (2 ticket(s), Rs.560)

```

</details>

---

## Experiment 1 - Question 8: Product with Magic Methods

Scenario: A Product class that allows adding products together (combining total
cost), comparing prices and printing readable output.

Rubrics covered:
  * __add__, __str__, __repr__ implemented
  * object addition simulates combining products
  * pretty output via magic methods
  * input/output interaction (falls back to a demo cart when no stdin)

**File:** [`q8_product_magic_methods.py`](q8_product_magic_methods.py) &nbsp;&middot;&nbsp; **Run:** `python q8_product_magic_methods.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 1 - Question 8: Product with Magic Methods

Scenario: A Product class that allows adding products together (combining total
cost), comparing prices and printing readable output.

Rubrics covered:
  * __add__, __str__, __repr__ implemented
  * object addition simulates combining products
  * pretty output via magic methods
  * input/output interaction (falls back to a demo cart when no stdin)
"""

from functools import total_ordering


@total_ordering                       # fills in <=, >, >= from __eq__ and __lt__
class Product:
    def __init__(self, name, price, qty=1):
        self.name = name
        self.price = float(price)
        self.qty = int(qty)

    @property
    def total(self):
        return self.price * self.qty

    # --- combining ---
    def __add__(self, other):
        if isinstance(other, Product):
            return Product(f"{self.name}+{other.name}", self.total + other.total, 1)
        if isinstance(other, (int, float)):
            return Product(self.name, self.price + other, self.qty)
        return NotImplemented

    def __radd__(self, other):        # lets sum() start from 0
        if other == 0:
            return self
        return self.__add__(other)

    def __mul__(self, n):             # bulk order: product * 3
        if isinstance(n, int):
            return Product(self.name, self.price, self.qty * n)
        return NotImplemented

    # --- comparing by price ---
    def __eq__(self, other):
        return isinstance(other, Product) and self.price == other.price

    def __lt__(self, other):
        return self.price < other.price

    # --- output ---
    def __str__(self):
        return (f"{self.name:<16} Rs.{self.price:>8,.2f} x{self.qty:<3} "
                f"= Rs.{self.total:>9,.2f}")

    def __repr__(self):
        return f"Product(name={self.name!r}, price={self.price!r}, qty={self.qty!r})"

    def __len__(self):
        return self.qty


if __name__ == "__main__":
    laptop = Product("Laptop", 54999, 1)
    mouse = Product("Mouse", 899, 2)
    bag = Product("Laptop Bag", 1499, 1)

    print("=== __str__ (readable) ===")
    for p in (laptop, mouse, bag):
        print(p)

    print("\n=== __repr__ (unambiguous) ===")
    print([laptop, mouse, bag])

    print("\n=== __add__ combines cost ===")
    print(laptop + mouse + bag)
    print("sum() via __radd__: Rs.{:,.2f}".format(sum([laptop, mouse, bag]).total))

    print("\n=== __mul__ bulk order ===")
    print(mouse * 5)

    print("\n=== comparisons (by price) ===")
    print("laptop > mouse :", laptop > mouse)
    print("mouse == bag   :", mouse == bag)
    print("sorted:", [p.name for p in sorted([laptop, mouse, bag])])
    print("costliest:", max(laptop, mouse, bag).name)
    print("len(mouse) -> qty:", len(mouse))

    print("\n=== interactive bill ===")
    cart = []
    try:
        n = int(input("How many items? ") or 0)
        for i in range(n):
            raw = input(f"item {i + 1} as name,price,qty : ")
            name, price, qty = [x.strip() for x in raw.split(",")]
            cart.append(Product(name, price, qty))
    except (EOFError, ValueError, OSError):
        print("(no input available - using demo cart)")
    if not cart:
        cart = [laptop, mouse, bag]

    print("\n------------- BILL -------------")
    for p in cart:
        print(p)
    print("-" * 32)
    print(f"{'TOTAL':<16} {'':>13} Rs.{sum(c.total for c in cart):>9,.2f}")
```

</details>

<details>
<summary>Program output</summary>

```text
=== __str__ (readable) ===
Laptop           Rs.54,999.00 x1   = Rs.54,999.00
Mouse            Rs.  899.00 x2   = Rs. 1,798.00
Laptop Bag       Rs.1,499.00 x1   = Rs. 1,499.00

=== __repr__ (unambiguous) ===
[Product(name='Laptop', price=54999.0, qty=1), Product(name='Mouse', price=899.0, qty=2), Product(name='Laptop Bag', price=1499.0, qty=1)]

=== __add__ combines cost ===
Laptop+Mouse+Laptop Bag Rs.58,296.00 x1   = Rs.58,296.00
sum() via __radd__: Rs.58,296.00

=== __mul__ bulk order ===
Mouse            Rs.  899.00 x10  = Rs. 8,990.00

=== comparisons (by price) ===
laptop > mouse : True
mouse == bag   : False
sorted: ['Mouse', 'Laptop Bag', 'Laptop']
costliest: Laptop
len(mouse) -> qty: 2

=== interactive bill ===
How many items? (no input available - using demo cart)

------------- BILL -------------
Laptop           Rs.54,999.00 x1   = Rs.54,999.00
Mouse            Rs.  899.00 x2   = Rs. 1,798.00
Laptop Bag       Rs.1,499.00 x1   = Rs. 1,499.00
--------------------------------
TOTAL                          Rs.58,296.00

```

</details>

---

## Experiment 1 - Question 9: Thermostat Controller

Scenario: A smart thermostat keeps a room between 18 C and 30 C. It must not
allow values outside the allowed range.

Rubrics covered:
  * encapsulation with validation in the setter
  * feedback on invalid input
  * current status shown via __str__
  * private temperature variable

**File:** [`q9_thermostat_controller.py`](q9_thermostat_controller.py) &nbsp;&middot;&nbsp; **Run:** `python q9_thermostat_controller.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 1 - Question 9: Thermostat Controller

Scenario: A smart thermostat keeps a room between 18 C and 30 C. It must not
allow values outside the allowed range.

Rubrics covered:
  * encapsulation with validation in the setter
  * feedback on invalid input
  * current status shown via __str__
  * private temperature variable
"""


class Thermostat:
    MIN_TEMP = 18.0
    MAX_TEMP = 30.0

    def __init__(self, room, target=24.0):
        self.room = room
        self.__temperature = None        # private
        self.__history = []
        self.set_temperature(target)

    # ---- controlled access ----
    @property
    def temperature(self):
        return self.__temperature

    @temperature.setter
    def temperature(self, value):
        self.set_temperature(value)

    def set_temperature(self, value):
        try:
            value = float(value)
        except (TypeError, ValueError):
            print(f"REJECTED: '{value}' is not a number. Temperature unchanged "
                  f"at {self.__temperature} C")
            return False
        if value < Thermostat.MIN_TEMP:
            print(f"REJECTED: {value} C is below the minimum "
                  f"{Thermostat.MIN_TEMP} C. Request ignored.")
            return False
        if value > Thermostat.MAX_TEMP:
            print(f"REJECTED: {value} C is above the maximum "
                  f"{Thermostat.MAX_TEMP} C. Request ignored.")
            return False
        self.__temperature = value
        self.__history.append(value)
        print(f"ACCEPTED: {self.room} target set to {value} C")
        return True

    def warmer(self, step=1.0):
        return self.set_temperature((self.__temperature or 0) + step)

    def cooler(self, step=1.0):
        return self.set_temperature((self.__temperature or 0) - step)

    def mode(self):
        if self.__temperature <= 20:
            return "HEATING"
        if self.__temperature >= 28:
            return "COOLING"
        return "IDLE"

    def history(self):
        return list(self.__history)

    def __str__(self):
        span = self.MAX_TEMP - self.MIN_TEMP
        pos = int((self.__temperature - self.MIN_TEMP) / span * 20)
        bar = "=" * pos + "o" + "-" * (20 - pos)
        return (f"[{self.room}] {self.__temperature:.1f} C  |{bar}|  "
                f"mode={self.mode()}  range {self.MIN_TEMP}-{self.MAX_TEMP} C")


if __name__ == "__main__":
    t = Thermostat("Bedroom", 24)
    print(t)

    print("\n--- valid adjustments ---")
    t.warmer(3)
    print(t)
    t.cooler(5)
    print(t)

    print("\n--- invalid adjustments get feedback, state is protected ---")
    t.set_temperature(45)
    t.set_temperature(5)
    t.set_temperature("hot")
    t.temperature = 99          # goes through the property setter -> rejected
    print(t)

    print("\n--- boundaries are allowed ---")
    t.set_temperature(18)
    t.set_temperature(30)
    print(t)

    print("\nPrivate attribute is name-mangled, not directly reachable:")
    print("  'temperature' in instance dict:", "temperature" in t.__dict__)
    print("  stored as:", [k for k in t.__dict__ if "temperature" in k])
    print("  accepted history:", t.history())
```

</details>

<details>
<summary>Program output</summary>

```text
ACCEPTED: Bedroom target set to 24.0 C
[Bedroom] 24.0 C  |==========o----------|  mode=IDLE  range 18.0-30.0 C

--- valid adjustments ---
ACCEPTED: Bedroom target set to 27.0 C
[Bedroom] 27.0 C  |===============o-----|  mode=IDLE  range 18.0-30.0 C
ACCEPTED: Bedroom target set to 22.0 C
[Bedroom] 22.0 C  |======o--------------|  mode=IDLE  range 18.0-30.0 C

--- invalid adjustments get feedback, state is protected ---
REJECTED: 45.0 C is above the maximum 30.0 C. Request ignored.
REJECTED: 5.0 C is below the minimum 18.0 C. Request ignored.
REJECTED: 'hot' is not a number. Temperature unchanged at 22.0 C
REJECTED: 99.0 C is above the maximum 30.0 C. Request ignored.
[Bedroom] 22.0 C  |======o--------------|  mode=IDLE  range 18.0-30.0 C

--- boundaries are allowed ---
ACCEPTED: Bedroom target set to 18.0 C
ACCEPTED: Bedroom target set to 30.0 C
[Bedroom] 30.0 C  |====================o|  mode=COOLING  range 18.0-30.0 C

Private attribute is name-mangled, not directly reachable:
  'temperature' in instance dict: False
  stored as: ['_Thermostat__temperature']
  accepted history: [24.0, 27.0, 22.0, 18.0, 30.0]

```

</details>

---

## Experiment 1 - Question 10: School Staff and Students

Scenario: A school management system differentiates Staff and Students while
sharing common features like name and address. Staff has subjects taught,
students have grades.

Rubrics covered:
  * inheritance from a base Person class
  * methods overridden in child classes
  * polymorphic display method
  * isinstance() / issubclass() demonstrated

**File:** [`q10_school_staff_students.py`](q10_school_staff_students.py) &nbsp;&middot;&nbsp; **Run:** `python q10_school_staff_students.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 1 - Question 10: School Staff and Students

Scenario: A school management system differentiates Staff and Students while
sharing common features like name and address. Staff has subjects taught,
students have grades.

Rubrics covered:
  * inheritance from a base Person class
  * methods overridden in child classes
  * polymorphic display method
  * isinstance() / issubclass() demonstrated
"""


class Person:
    def __init__(self, name, age, address, phone):
        self.name = name
        self.age = age
        self.address = address
        self.phone = phone

    def role(self):
        return "Person"

    def display(self):                      # overridden by children
        print(f"{self.role():<8} | {self.name:<14} | age {self.age:<3} | "
              f"{self.address:<18} | {self.phone}")

    def __str__(self):
        return f"{self.role()}: {self.name}"


class Staff(Person):
    def __init__(self, name, age, address, phone, employee_id,
                 subjects, salary, department):
        super().__init__(name, age, address, phone)
        self.employee_id = employee_id
        self.subjects = list(subjects)
        self.salary = salary
        self.department = department

    def role(self):
        return "Staff"

    def teaching_load(self):
        return len(self.subjects)

    def display(self):                      # override
        super().display()
        print(f"         | emp-id {self.employee_id} | dept {self.department} | "
              f"subjects {', '.join(self.subjects)} | "
              f"load {self.teaching_load()} | Rs.{self.salary:,}/month")


class Student(Person):
    def __init__(self, name, age, address, phone, roll_no, standard, grades):
        super().__init__(name, age, address, phone)
        self.roll_no = roll_no
        self.standard = standard
        self.grades = dict(grades)          # subject -> marks

    def role(self):
        return "Student"

    def percentage(self):
        return sum(self.grades.values()) / len(self.grades) if self.grades else 0.0

    def result(self):
        return "PASS" if all(m >= 35 for m in self.grades.values()) else "FAIL"

    def display(self):                      # override
        super().display()
        marks = "  ".join(f"{s}:{m}" for s, m in self.grades.items())
        print(f"         | roll {self.roll_no} | std {self.standard} | {marks} | "
              f"{self.percentage():.2f}% | {self.result()}")


if __name__ == "__main__":
    people = [
        Staff("Mrs. Kulkarni", 41, "Kothrud, Pune", "9822001122",
              "EMP-17", ["Mathematics", "Statistics"], 68000, "Science"),
        Student("Spandan", 19, "Wakad, Pune", "9011223344",
                "CSE2301", "SY-CSE", {"Python": 88, "DSA": 92, "DBMS": 79}),
        Staff("Mr. Deshmukh", 35, "Hadapsar, Pune", "9765432100",
              "EMP-22", ["History"], 52000, "Humanities"),
        Student("Aman", 18, "Baner, Pune", "9834567812",
                "CSE2303", "SY-CSE", {"Python": 31, "DSA": 61, "DBMS": 48}),
    ]

    print("=== Polymorphic display(): one loop, four different outputs ===")
    for p in people:
        p.display()
        print("-" * 80)

    print("=== isinstance() filtering ===")
    staff = [p for p in people if isinstance(p, Staff)]
    students = [p for p in people if isinstance(p, Student)]
    print("Staff   :", [s.name for s in staff])
    print("Students:", [s.name for s in students])
    print(f"Monthly salary bill : Rs.{sum(s.salary for s in staff):,}")
    print(f"Class average       : "
          f"{sum(s.percentage() for s in students) / len(students):.2f}%")

    print("\n=== issubclass() checks ===")
    print("  Staff   subclass of Person :", issubclass(Staff, Person))
    print("  Student subclass of Person :", issubclass(Student, Person))
    print("  Student subclass of Staff  :", issubclass(Student, Staff))
    print("  every object is a Person   :", all(isinstance(p, Person) for p in people))
```

</details>

<details>
<summary>Program output</summary>

```text
=== Polymorphic display(): one loop, four different outputs ===
Staff    | Mrs. Kulkarni  | age 41  | Kothrud, Pune      | 9822001122
         | emp-id EMP-17 | dept Science | subjects Mathematics, Statistics | load 2 | Rs.68,000/month
--------------------------------------------------------------------------------
Student  | Spandan        | age 19  | Wakad, Pune        | 9011223344
         | roll CSE2301 | std SY-CSE | Python:88  DSA:92  DBMS:79 | 86.33% | PASS
--------------------------------------------------------------------------------
Staff    | Mr. Deshmukh   | age 35  | Hadapsar, Pune     | 9765432100
         | emp-id EMP-22 | dept Humanities | subjects History | load 1 | Rs.52,000/month
--------------------------------------------------------------------------------
Student  | Aman           | age 18  | Baner, Pune        | 9834567812
         | roll CSE2303 | std SY-CSE | Python:31  DSA:61  DBMS:48 | 46.67% | FAIL
--------------------------------------------------------------------------------
=== isinstance() filtering ===
Staff   : ['Mrs. Kulkarni', 'Mr. Deshmukh']
Students: ['Spandan', 'Aman']
Monthly salary bill : Rs.120,000
Class average       : 66.50%

=== issubclass() checks ===
  Staff   subclass of Person : True
  Student subclass of Person : True
  Student subclass of Staff  : False
  every object is a Person   : True

```

</details>

---
