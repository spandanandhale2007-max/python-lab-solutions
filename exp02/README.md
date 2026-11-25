# Experiment 2 - Unit I

Composition, abstraction, decorators, generators, iterators, closures

10 scenario questions, each solved in its own section and its own file. Every program below was executed and the real output is included.

[Back to the index](../README.md)

---

## Questions in this experiment

- [Experiment 2 - Question 1: Game Character with Equipment](#experiment-2---question-1-game-character-with-equipment)
- [Experiment 2 - Question 2: Email Validation System](#experiment-2---question-2-email-validation-system)
- [Experiment 2 - Question 3: Animal Zoo with Polymorphism](#experiment-2---question-3-animal-zoo-with-polymorphism)
- [Experiment 2 - Question 4: Payment Gateway with Abstraction](#experiment-2---question-4-payment-gateway-with-abstraction)
- [Experiment 2 - Question 5: Object Counter](#experiment-2---question-5-object-counter)
- [Experiment 2 - Question 6: Function Logger Decorator](#experiment-2---question-6-function-logger-decorator)
- [Experiment 2 - Question 7: Fibonacci Sequence Generator](#experiment-2---question-7-fibonacci-sequence-generator)
- [Experiment 2 - Question 8: Email Filter with Iterator](#experiment-2---question-8-email-filter-with-iterator)
- [Experiment 2 - Question 9: Temperature Conversion Closure](#experiment-2---question-9-temperature-conversion-closure)
- [Experiment 2 - Question 10: Retry Logic with Decorators](#experiment-2---question-10-retry-logic-with-decorators)

---

## Experiment 2 - Question 1: Game Character with Equipment

Scenario: A simple RPG system where each Character is equipped with a Weapon
and Armor. Equipment affects the character's total attack/defence power.

Rubrics covered:
  * composition: Character has-a Weapon and an Armor
  * modular design of each class
  * aggregated calculation of stats
  * full character summary printed

**File:** [`q1_game_character_equipment.py`](q1_game_character_equipment.py) &nbsp;&middot;&nbsp; **Run:** `python q1_game_character_equipment.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 2 - Question 1: Game Character with Equipment

Scenario: A simple RPG system where each Character is equipped with a Weapon
and Armor. Equipment affects the character's total attack/defence power.

Rubrics covered:
  * composition: Character has-a Weapon and an Armor
  * modular design of each class
  * aggregated calculation of stats
  * full character summary printed
"""


class Weapon:
    def __init__(self, name, attack, crit_chance=0.1):
        self.name = name
        self.attack = attack
        self.crit_chance = crit_chance

    def __str__(self):
        return f"{self.name} (+{self.attack} atk, {self.crit_chance:.0%} crit)"


class Armor:
    def __init__(self, name, defence, weight):
        self.name = name
        self.defence = defence
        self.weight = weight

    def __str__(self):
        return f"{self.name} (+{self.defence} def, {self.weight} kg)"


class Character:
    """Composition: the character owns a Weapon object and an Armor object."""

    def __init__(self, name, cls_name, base_attack, base_defence,
                 weapon=None, armor=None):
        self.name = name
        self.cls_name = cls_name
        self.base_attack = base_attack
        self.base_defence = base_defence
        self.weapon = weapon          # has-a
        self.armor = armor            # has-a
        self.hp = 100

    def equip_weapon(self, weapon):
        self.weapon = weapon
        print(f"{self.name} equips {weapon.name}")

    def equip_armor(self, armor):
        self.armor = armor
        print(f"{self.name} equips {armor.name}")

    # --- aggregated stats ---
    def total_attack(self):
        return self.base_attack + (self.weapon.attack if self.weapon else 0)

    def total_defence(self):
        return self.base_defence + (self.armor.defence if self.armor else 0)

    def speed(self):
        return max(1, 20 - (self.armor.weight if self.armor else 0))

    def power_score(self):
        return self.total_attack() * 2 + self.total_defence() + self.speed()

    def attack_target(self, other):
        damage = max(1, self.total_attack() - other.total_defence() // 2)
        other.hp -= damage
        print(f"{self.name} hits {other.name} for {damage} "
              f"({other.name} hp -> {max(0, other.hp)})")

    def summary(self):
        print(f"\n===== {self.name} the {self.cls_name} =====")
        print(f"  Weapon       : {self.weapon or 'bare hands'}")
        print(f"  Armor        : {self.armor or 'cloth rags'}")
        print(f"  Attack       : {self.base_attack} base -> {self.total_attack()}")
        print(f"  Defence      : {self.base_defence} base -> {self.total_defence()}")
        print(f"  Speed        : {self.speed()}")
        print(f"  HP           : {self.hp}")
        print(f"  Power score  : {self.power_score()}")


if __name__ == "__main__":
    excalibur = Weapon("Excalibur", 35, 0.25)
    dagger = Weapon("Rusty Dagger", 8, 0.05)
    plate = Armor("Steel Plate", 30, 14)
    leather = Armor("Leather Vest", 10, 3)

    knight = Character("Arthur", "Knight", 20, 15, excalibur, plate)
    thief = Character("Mira", "Thief", 14, 6, dagger, leather)

    knight.summary()
    thief.summary()

    print("\n--- swapping equipment changes aggregated stats ---")
    thief.equip_weapon(excalibur)
    thief.summary()

    print("\n--- combat round ---")
    knight.equip_weapon(dagger)
    knight.attack_target(thief)
    thief.attack_target(knight)

    print("\n--- final power ranking ---")
    for c in sorted([knight, thief], key=Character.power_score, reverse=True):
        print(f"  {c.name:<8} power={c.power_score()}  hp={c.hp}")
```

</details>

<details>
<summary>Program output</summary>

```text
===== Arthur the Knight =====
  Weapon       : Excalibur (+35 atk, 25% crit)
  Armor        : Steel Plate (+30 def, 14 kg)
  Attack       : 20 base -> 55
  Defence      : 15 base -> 45
  Speed        : 6
  HP           : 100
  Power score  : 161

===== Mira the Thief =====
  Weapon       : Rusty Dagger (+8 atk, 5% crit)
  Armor        : Leather Vest (+10 def, 3 kg)
  Attack       : 14 base -> 22
  Defence      : 6 base -> 16
  Speed        : 17
  HP           : 100
  Power score  : 77

--- swapping equipment changes aggregated stats ---
Mira equips Excalibur

===== Mira the Thief =====
  Weapon       : Excalibur (+35 atk, 25% crit)
  Armor        : Leather Vest (+10 def, 3 kg)
  Attack       : 14 base -> 49
  Defence      : 6 base -> 16
  Speed        : 17
  HP           : 100
  Power score  : 131

--- combat round ---
Arthur equips Rusty Dagger
Arthur hits Mira for 20 (Mira hp -> 80)
Mira hits Arthur for 27 (Arthur hp -> 73)

--- final power ranking ---
  Mira     power=131  hp=80
  Arthur   power=107  hp=73

```

</details>

---

## Experiment 2 - Question 2: Email Validation System

Scenario: A class stores valid email addresses. The system rejects and does not
store invalid formats (missing '@', missing domain, and so on).

Rubrics covered:
  * static methods used for validation
  * a list of emails is taken as input and filtered
  * only valid addresses are stored
  * the valid email list is printed

**File:** [`q2_email_validation_system.py`](q2_email_validation_system.py) &nbsp;&middot;&nbsp; **Run:** `python q2_email_validation_system.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 2 - Question 2: Email Validation System

Scenario: A class stores valid email addresses. The system rejects and does not
store invalid formats (missing '@', missing domain, and so on).

Rubrics covered:
  * static methods used for validation
  * a list of emails is taken as input and filtered
  * only valid addresses are stored
  * the valid email list is printed
"""

import re


class EmailBook:
    PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$")

    def __init__(self, owner):
        self.owner = owner
        self.valid = []
        self.rejected = []

    # ---------- static validation helpers ----------
    @staticmethod
    def is_valid(email):
        if not isinstance(email, str):
            return False
        email = email.strip()
        if email.count("@") != 1:
            return False
        if ".." in email or email.startswith(".") or email.endswith("."):
            return False
        return bool(EmailBook.PATTERN.match(email))

    @staticmethod
    def reason(email):
        e = (email or "").strip()
        if not e:
            return "empty string"
        if e.count("@") == 0:
            return "missing '@'"
        if e.count("@") > 1:
            return "more than one '@'"
        local, _, domain = e.partition("@")
        if not local:
            return "missing local part"
        if not domain:
            return "missing domain"
        if "." not in domain:
            return "domain has no dot / no TLD"
        if len(domain.rsplit(".", 1)[1]) < 2:
            return "TLD too short"
        if " " in e:
            return "contains a space"
        return "does not match the allowed character pattern"

    @staticmethod
    def normalise(email):
        return email.strip().lower()

    # ---------- storage ----------
    def add(self, email):
        if EmailBook.is_valid(email):
            clean = EmailBook.normalise(email)
            if clean in self.valid:
                self.rejected.append((email, "duplicate"))
                return False
            self.valid.append(clean)
            return True
        self.rejected.append((email, EmailBook.reason(email)))
        return False

    def add_many(self, emails):
        return sum(self.add(e) for e in emails)

    def report(self):
        print(f"\n=== {self.owner}: {len(self.valid)} stored address(es) ===")
        for i, e in enumerate(self.valid, 1):
            print(f"  {i}. {e}")
        print(f"\n=== {len(self.rejected)} rejected ===")
        for e, why in self.rejected:
            print(f"  {str(e)!r:<32} -> {why}")


if __name__ == "__main__":
    raw_input_list = [
        "spandanandhale@example.com",
        "riya.sharma+college@mitwpu.edu.in",
        "plainaddress",                 # no @
        "no-at-sign.com",               # no @
        "two@@signs.com",               # two @
        "@nolocalpart.com",             # no local part
        "missingdomain@",               # no domain
        "user@nodot",                   # no TLD
        "user@short.c",                 # TLD too short
        "has space@mail.com",           # space
        "aman_k99@sub.domain.co.in",
        "SPANDANANDHALE@EXAMPLE.COM",   # duplicate after normalising
    ]

    book = EmailBook("Newsletter subscribers")
    stored = book.add_many(raw_input_list)

    print(f"Processed {len(raw_input_list)} entries, stored {stored}.")
    book.report()

    print("\n=== static method can be used without an instance ===")
    for probe in ("abc@def.com", "abc@def"):
        print(f"  EmailBook.is_valid({probe!r}) -> {EmailBook.is_valid(probe)}")
```

</details>

<details>
<summary>Program output</summary>

```text
Processed 12 entries, stored 3.

=== Newsletter subscribers: 3 stored address(es) ===
  1. spandanandhale@example.com
  2. riya.sharma+college@mitwpu.edu.in
  3. aman_k99@sub.domain.co.in

=== 9 rejected ===
  'plainaddress'                   -> missing '@'
  'no-at-sign.com'                 -> missing '@'
  'two@@signs.com'                 -> more than one '@'
  '@nolocalpart.com'               -> missing local part
  'missingdomain@'                 -> missing domain
  'user@nodot'                     -> domain has no dot / no TLD
  'user@short.c'                   -> TLD too short
  'has space@mail.com'             -> contains a space
  'SPANDANANDHALE@EXAMPLE.COM'     -> duplicate

=== static method can be used without an instance ===
  EmailBook.is_valid('abc@def.com') -> True
  EmailBook.is_valid('abc@def') -> False

```

</details>

---

## Experiment 2 - Question 3: Animal Zoo with Polymorphism

Scenario: A zoo simulator. Each animal has a speak() method. Lion, Monkey and
Snake inherit from a base Animal class and override the behaviour.

Rubrics covered:
  * class hierarchy implemented
  * polymorphism demonstrated through speak()
  * a list of mixed animal objects is used
  * a loop invokes the behaviour dynamically

**File:** [`q3_animal_zoo_polymorphism.py`](q3_animal_zoo_polymorphism.py) &nbsp;&middot;&nbsp; **Run:** `python q3_animal_zoo_polymorphism.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 2 - Question 3: Animal Zoo with Polymorphism

Scenario: A zoo simulator. Each animal has a speak() method. Lion, Monkey and
Snake inherit from a base Animal class and override the behaviour.

Rubrics covered:
  * class hierarchy implemented
  * polymorphism demonstrated through speak()
  * a list of mixed animal objects is used
  * a loop invokes the behaviour dynamically
"""


class Animal:
    def __init__(self, name, age, diet="omnivore"):
        self.name = name
        self.age = age
        self.diet = diet

    def speak(self):
        return "..."

    def move(self):
        return "moves around"

    def enclosure(self):
        return "General Enclosure"

    def info(self):
        return (f"{type(self).__name__:<8} {self.name:<8} age {self.age:<3} "
                f"{self.diet:<10} | says {self.speak():<22} | {self.move():<18} "
                f"| {self.enclosure()}")


class Lion(Animal):
    def __init__(self, name, age, mane_size="large"):
        super().__init__(name, age, diet="carnivore")
        self.mane_size = mane_size

    def speak(self):
        return "ROAAAR!"

    def move(self):
        return "prowls on 4 legs"

    def enclosure(self):
        return "Big Cat Safari"


class Monkey(Animal):
    def __init__(self, name, age, troop_size=5):
        super().__init__(name, age, diet="frugivore")
        self.troop_size = troop_size

    def speak(self):
        return "Ooh ooh aah aah!"

    def move(self):
        return "swings on branches"

    def enclosure(self):
        return "Primate Canopy"


class Snake(Animal):
    def __init__(self, name, age, venomous=True):
        super().__init__(name, age, diet="carnivore")
        self.venomous = venomous

    def speak(self):
        return "Ssssssss..."

    def move(self):
        return "slithers"

    def enclosure(self):
        return "Reptile House" + (" (venomous)" if self.venomous else "")


class Parrot(Animal):
    def __init__(self, name, age, phrase="Hello!"):
        super().__init__(name, age, diet="granivore")
        self.phrase = phrase

    def speak(self):
        return f"{self.phrase} {self.phrase}"

    def move(self):
        return "flies"

    def enclosure(self):
        return "Aviary"


if __name__ == "__main__":
    # a single list holding objects of different concrete types
    zoo = [
        Lion("Simba", 7),
        Monkey("Rafiki", 4, troop_size=11),
        Snake("Kaa", 3, venomous=False),
        Parrot("Iago", 2, phrase="Polly wants a samosa!"),
        Animal("Mystery", 1),
    ]

    print("=== Morning roll call (one loop, many behaviours) ===")
    for animal in zoo:
        print(animal.info())

    print("\n=== Feeding round: dispatch decided at runtime ===")
    for animal in zoo:
        print(f"  {animal.name:<8} ({animal.diet:<10}) -> {animal.speak()}")

    print("\n=== Grouping by enclosure ===")
    groups = {}
    for animal in zoo:
        groups.setdefault(animal.enclosure(), []).append(animal.name)
    for place, names in groups.items():
        print(f"  {place:<24} {', '.join(names)}")

    print("\n=== Same method name, different code objects ===")
    for cls in (Lion, Monkey, Snake, Parrot):
        print(f"  {cls.__name__:<8} speak defined in -> "
              f"{cls.speak.__qualname__}  (overrides Animal.speak: "
              f"{cls.speak is not Animal.speak})")
```

</details>

<details>
<summary>Program output</summary>

```text
=== Morning roll call (one loop, many behaviours) ===
Lion     Simba    age 7   carnivore  | says ROAAAR!                | prowls on 4 legs   | Big Cat Safari
Monkey   Rafiki   age 4   frugivore  | says Ooh ooh aah aah!       | swings on branches | Primate Canopy
Snake    Kaa      age 3   carnivore  | says Ssssssss...            | slithers           | Reptile House
Parrot   Iago     age 2   granivore  | says Polly wants a samosa! Polly wants a samosa! | flies              | Aviary
Animal   Mystery  age 1   omnivore   | says ...                    | moves around       | General Enclosure

=== Feeding round: dispatch decided at runtime ===
  Simba    (carnivore ) -> ROAAAR!
  Rafiki   (frugivore ) -> Ooh ooh aah aah!
  Kaa      (carnivore ) -> Ssssssss...
  Iago     (granivore ) -> Polly wants a samosa! Polly wants a samosa!
  Mystery  (omnivore  ) -> ...

=== Grouping by enclosure ===
  Big Cat Safari           Simba
  Primate Canopy           Rafiki
  Reptile House            Kaa
  Aviary                   Iago
  General Enclosure        Mystery

=== Same method name, different code objects ===
  Lion     speak defined in -> Lion.speak  (overrides Animal.speak: True)
  Monkey   speak defined in -> Monkey.speak  (overrides Animal.speak: True)
  Snake    speak defined in -> Snake.speak  (overrides Animal.speak: True)
  Parrot   speak defined in -> Parrot.speak  (overrides Animal.speak: True)

```

</details>

---

## Experiment 2 - Question 4: Payment Gateway with Abstraction

Scenario: A payment gateway with modes like UPI, NetBanking and CreditCard,
each with its own implementation of pay().

Rubrics covered:
  * abstract base class Payment
  * all derived classes implemented
  * runtime selection of the payment mode
  * realistic flow and method design

**File:** [`q4_payment_gateway_abstraction.py`](q4_payment_gateway_abstraction.py) &nbsp;&middot;&nbsp; **Run:** `python q4_payment_gateway_abstraction.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== abstract class cannot be instantiated ===
   TypeError - Can't instantiate abstract class Payment without an implementation for abstract methods 'mode_name', 'pay'

Order total: Rs.8,499.00
Modes: 1 UPI   2 NetBanking   3 CreditCard   4 Wallet
Choose a payment mode (1-4): (no input - demonstrating every mode instead)


[UPI] Checkout for Spandan: Rs.8,499.00 + fee Rs.0.00
   Opening UPI app for spandan@okaxis ...
   Verifying 4-digit UPI PIN ...
   Debited instantly. Remaining Rs.6,501.00
[UPI] SUCCESS  total paid Rs.8,499.00

[NetBanking] Checkout for Spandan: Rs.8,499.00 + fee Rs.12.00
   Redirecting to HDFC Bank internet banking ...
   Logging in for account ****7890
   Waiting for OTP ... received
   Transfer complete. Remaining Rs.33,489.00
[NetBanking] SUCCESS  total paid Rs.8,511.00

[CreditCard] Checkout for Spandan: Rs.8,499.00 + fee Rs.152.98
   Card ****1234 - running 3-D Secure ...
   Authorised. Outstanding Rs.13,651.98 of limit Rs.75,000.00
[CreditCard] SUCCESS  total paid Rs.8,651.98

[Wallet] Checkout for Spandan: Rs.8,499.00 + fee Rs.0.00
   Paytm wallet balance Rs.900.00
   Top up the wallet and retry
[Wallet] FAILED

=== runtime polymorphism over a list of Payment references ===
  UPI          fee on Rs.1000 = Rs.0.00  (isinstance of Payment: True)
  NetBanking   fee on Rs.1000 = Rs.12.00  (isinstance of Payment: True)
  CreditCard   fee on Rs.1000 = Rs.18.00  (isinstance of Payment: True)
  Wallet       fee on Rs.1000 = Rs.0.00  (isinstance of Payment: True)

```

</details>

---

## Experiment 2 - Question 5: Object Counter

Scenario: Track how many user accounts have been created in a system.

Rubrics covered:
  * class variable counts instances
  * class method retrieves the count
  * multiple objects created to test it
  * total objects created displayed

**File:** [`q5_object_counter.py`](q5_object_counter.py) &nbsp;&middot;&nbsp; **Run:** `python q5_object_counter.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
Accounts at start : 0

=== created accounts ===
  #1001 spandan <spandan@example.com>
  #1002 riya <riya@example.com>
  #1003 aman <aman@example.com>
  #1004 neha <neha@example.com> [Platinum]

Total via class     : 4
Total via instance  : 4
Subclass sees same  : 4

=== closing one account ===
Closed account 1003 (aman)
Active now: 3
Stats     : {'created': 4, 'active': 3, 'deleted': 1}

=== creating 3 more in a loop ===
Active now: 6
Stats     : {'created': 7, 'active': 6, 'deleted': 1}

Instance counter is NOT per-object:
  '_count' in instance dict : False
  it lives on the class     : True
[ADMIN] counter reset (was 6)
After reset: {'created': 0, 'active': 0, 'deleted': 0}

```

</details>

---

## Experiment 2 - Question 6: Function Logger Decorator

Scenario: A decorator that logs the function name, input and output every time
a function is called (for auditing).

Rubrics covered:
  * @decorator syntax used
  * arguments and return values captured
  * timestamp included
  * applied to multiple functions

**File:** [`q6_function_logger_decorator.py`](q6_function_logger_decorator.py) &nbsp;&middot;&nbsp; **Run:** `python q6_function_logger_decorator.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 2 - Question 6: Function Logger Decorator

Scenario: A decorator that logs the function name, input and output every time
a function is called (for auditing).

Rubrics covered:
  * @decorator syntax used
  * arguments and return values captured
  * timestamp included
  * applied to multiple functions
"""

import functools
import time
from datetime import datetime

AUDIT_TRAIL = []


def audit_log(func):
    """Logs name, args, kwargs, return value, duration and a timestamp."""

    @functools.wraps(func)                 # keeps __name__, __doc__ intact
    def wrapper(*args, **kwargs):
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        shown_args = ", ".join(repr(a) for a in args)
        shown_kwargs = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
        signature = ", ".join(p for p in (shown_args, shown_kwargs) if p)

        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
        except Exception as exc:
            elapsed = (time.perf_counter() - start) * 1000
            line = (f"[{stamp}] CALL {func.__name__}({signature}) "
                    f"RAISED {type(exc).__name__}: {exc} ({elapsed:.2f} ms)")
            print(line)
            AUDIT_TRAIL.append(line)
            raise
        elapsed = (time.perf_counter() - start) * 1000
        line = (f"[{stamp}] CALL {func.__name__}({signature}) "
                f"-> {result!r} ({elapsed:.2f} ms)")
        print(line)
        AUDIT_TRAIL.append(line)
        return result

    return wrapper


# ---------------- applied to several functions ----------------
@audit_log
def add(a, b):
    """Adds two numbers."""
    return a + b


@audit_log
def apply_gst(amount, rate=18):
    return round(amount * (1 + rate / 100), 2)


@audit_log
def grade(marks):
    if not 0 <= marks <= 100:
        raise ValueError("marks must be between 0 and 100")
    return "A" if marks >= 80 else "B" if marks >= 60 else "C"


@audit_log
def slow_square(n):
    time.sleep(0.05)
    return n * n


if __name__ == "__main__":
    print("=== audited calls ===")
    add(12, 30)
    apply_gst(1500)
    apply_gst(2000, rate=5)
    grade(88)
    slow_square(9)

    print("\n=== an exception is also audited ===")
    try:
        grade(140)
    except ValueError as e:
        print("  caught by caller:", e)

    print("\n=== metadata preserved by functools.wraps ===")
    print("  add.__name__ :", add.__name__)
    print("  add.__doc__  :", add.__doc__)

    print(f"\n=== audit trail ({len(AUDIT_TRAIL)} entries) ===")
    for line in AUDIT_TRAIL:
        print("  ", line)
```

</details>

<details>
<summary>Program output</summary>

```text
=== audited calls ===
[2026-11-25 08:42:53] CALL add(12, 30) -> 42 (0.00 ms)
[2026-11-25 08:42:53] CALL apply_gst(1500) -> 1770.0 (0.01 ms)
[2026-11-25 08:42:53] CALL apply_gst(2000, rate=5) -> 2100.0 (0.00 ms)
[2026-11-25 08:42:53] CALL grade(88) -> 'A' (0.00 ms)
[2026-11-25 08:42:53] CALL slow_square(9) -> 81 (50.43 ms)

=== an exception is also audited ===
[2026-11-25 08:42:53] CALL grade(140) RAISED ValueError: marks must be between 0 and 100 (0.01 ms)
  caught by caller: marks must be between 0 and 100

=== metadata preserved by functools.wraps ===
  add.__name__ : add
  add.__doc__  : Adds two numbers.

=== audit trail (6 entries) ===
   [2026-11-25 08:42:53] CALL add(12, 30) -> 42 (0.00 ms)
   [2026-11-25 08:42:53] CALL apply_gst(1500) -> 1770.0 (0.01 ms)
   [2026-11-25 08:42:53] CALL apply_gst(2000, rate=5) -> 2100.0 (0.00 ms)
   [2026-11-25 08:42:53] CALL grade(88) -> 'A' (0.00 ms)
   [2026-11-25 08:42:53] CALL slow_square(9) -> 81 (50.43 ms)
   [2026-11-25 08:42:53] CALL grade(140) RAISED ValueError: marks must be between 0 and 100 (0.01 ms)

```

</details>

---

## Experiment 2 - Question 7: Fibonacci Sequence Generator

Scenario: A generator function that yields Fibonacci numbers indefinitely or
until a given limit.

Rubrics covered:
  * yield used, internal state maintained
  * first N values printed
  * memory-efficient implementation
  * option to break after a limit

**File:** [`q7_fibonacci_generator.py`](q7_fibonacci_generator.py) &nbsp;&middot;&nbsp; **Run:** `python q7_fibonacci_generator.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 2 - Question 7: Fibonacci Sequence Generator

Scenario: A generator function that yields Fibonacci numbers indefinitely or
until a given limit.

Rubrics covered:
  * yield used, internal state maintained
  * first N values printed
  * memory-efficient implementation
  * option to break after a limit
"""

import itertools
import sys


def fibonacci():
    """Infinite generator: state lives in a and b, nothing is stored."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def fibonacci_upto(limit):
    """Stops when the value would exceed limit."""
    for value in fibonacci():
        if value > limit:
            return
        yield value


def fibonacci_n(n):
    """Yields exactly n terms."""
    return itertools.islice(fibonacci(), n)


def fib_list(n):
    """Eager version, kept only to compare memory use."""
    out, a, b = [], 0, 1
    for _ in range(n):
        out.append(a)
        a, b = b, a + b
    return out


if __name__ == "__main__":
    print("=== first 15 terms (islice over the infinite generator) ===")
    print(list(fibonacci_n(15)))

    print("\n=== terms up to a limit of 500 ===")
    print(list(fibonacci_upto(500)))

    print("\n=== manual stepping with next(), state is remembered ===")
    gen = fibonacci()
    print("  ", [next(gen) for _ in range(5)], "<- first five")
    print("  ", [next(gen) for _ in range(5)], "<- the generator resumed")

    print("\n=== breaking out of an infinite generator ===")
    for i, value in enumerate(fibonacci()):
        if value > 1000:
            print(f"   stopped at index {i}, value {value} (> 1000)")
            break

    print("\n=== memory: generator vs list for 100000 terms ===")
    gen_obj = fibonacci()
    print(f"   generator object : {sys.getsizeof(gen_obj)} bytes (constant)")
    big = fib_list(2000)
    print(f"   list of 2000     : {sys.getsizeof(big)} bytes for the list alone")
    print("   the generator never holds the whole sequence in memory")

    print("\n=== a 300-digit term is reachable without storing the series ===")
    big_term = next(itertools.islice(fibonacci(), 1000, None))
    print(f"   F(1000) has {len(str(big_term))} digits, starts {str(big_term)[:20]}...")

    print("\n=== sum of even Fibonacci numbers below 4,000,000 ===")
    print("   ", sum(v for v in fibonacci_upto(4_000_000) if v % 2 == 0))
```

</details>

<details>
<summary>Program output</summary>

```text
=== first 15 terms (islice over the infinite generator) ===
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]

=== terms up to a limit of 500 ===
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]

=== manual stepping with next(), state is remembered ===
   [0, 1, 1, 2, 3] <- first five
   [5, 8, 13, 21, 34] <- the generator resumed

=== breaking out of an infinite generator ===
   stopped at index 17, value 1597 (> 1000)

=== memory: generator vs list for 100000 terms ===
   generator object : 200 bytes (constant)
   list of 2000     : 16184 bytes for the list alone
   the generator never holds the whole sequence in memory

=== a 300-digit term is reachable without storing the series ===
   F(1000) has 209 digits, starts 43466557686937456435...

=== sum of even Fibonacci numbers below 4,000,000 ===
    4613732

```

</details>

---

## Experiment 2 - Question 8: Email Filter with Iterator

Scenario: A custom iterator that walks a list of strings and yields only the
valid email addresses.

Rubrics covered:
  * __iter__ and __next__ implemented
  * email validated during iteration
  * StopIteration raised when the list ends
  * all valid emails printed

**File:** [`q8_email_filter_iterator.py`](q8_email_filter_iterator.py) &nbsp;&middot;&nbsp; **Run:** `python q8_email_filter_iterator.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 2 - Question 8: Email Filter with Iterator

Scenario: A custom iterator that walks a list of strings and yields only the
valid email addresses.

Rubrics covered:
  * __iter__ and __next__ implemented
  * email validated during iteration
  * StopIteration raised when the list ends
  * all valid emails printed
"""

import re

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}$")


class EmailFilterIterator:
    """Custom iterator: skips invalid entries instead of returning them."""

    def __init__(self, items):
        self.items = list(items)
        self.index = 0
        self.checked = 0
        self.skipped = 0

    def __iter__(self):
        return self                       # the iterator is its own iterable

    def __next__(self):
        while self.index < len(self.items):
            candidate = str(self.items[self.index]).strip()
            self.index += 1
            self.checked += 1
            if EMAIL_RE.match(candidate):
                return candidate.lower()
            self.skipped += 1
        raise StopIteration               # list exhausted

    def reset(self):
        self.index = self.checked = self.skipped = 0


class Mailbox:
    """Iterable container: a fresh iterator is produced on every for-loop."""

    def __init__(self, raw_lines):
        self.raw_lines = raw_lines

    def __iter__(self):
        return EmailFilterIterator(self.raw_lines)

    def __len__(self):
        return len(self.raw_lines)


if __name__ == "__main__":
    raw = [
        "spandan@example.com",
        "not-an-email",
        "riya.sharma@mitwpu.edu.in",
        "@missinglocal.com",
        "  AMAN_K99@Sub.Domain.CO  ",
        "user@nodot",
        "neha+promo@gmail.com",
        12345,
        "double@@at.com",
        "last.valid@zoho.in",
    ]

    print("=== iterating with a for loop ===")
    it = EmailFilterIterator(raw)
    for email in it:
        print("  valid ->", email)
    print(f"  checked {it.checked}, skipped {it.skipped}")

    print("\n=== manual next() until StopIteration ===")
    it2 = EmailFilterIterator(raw)
    while True:
        try:
            print("  next():", next(it2))
        except StopIteration:
            print("  StopIteration raised - list ended")
            break

    print("\n=== reusable iterable container ===")
    box = Mailbox(raw)
    print("  pass 1:", list(box))
    print("  pass 2:", list(box), "(a new iterator each time)")
    print(f"  {len(list(box))} valid out of {len(box)} raw lines")

    print("\n=== collected list of valid emails ===")
    for i, e in enumerate(Mailbox(raw), 1):
        print(f"  {i}. {e}")
```

</details>

<details>
<summary>Program output</summary>

```text
=== iterating with a for loop ===
  valid -> spandan@example.com
  valid -> neha+promo@gmail.com
  valid -> last.valid@zoho.in
  checked 10, skipped 7

=== manual next() until StopIteration ===
  next(): spandan@example.com
  next(): neha+promo@gmail.com
  next(): last.valid@zoho.in
  StopIteration raised - list ended

=== reusable iterable container ===
  pass 1: ['spandan@example.com', 'neha+promo@gmail.com', 'last.valid@zoho.in']
  pass 2: ['spandan@example.com', 'neha+promo@gmail.com', 'last.valid@zoho.in'] (a new iterator each time)
  3 valid out of 10 raw lines

=== collected list of valid emails ===
  1. spandan@example.com
  2. neha+promo@gmail.com
  3. last.valid@zoho.in

```

</details>

---

## Experiment 2 - Question 9: Temperature Conversion Closure

Scenario: A closure that generates a function converting Celsius to Fahrenheit
and vice versa, based on user input.

Rubrics covered:
  * closure with internal state
  * converts in both directions
  * a separate closure for each direction
  * clean function design

**File:** [`q9_temperature_closure.py`](q9_temperature_closure.py) &nbsp;&middot;&nbsp; **Run:** `python q9_temperature_closure.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 2 - Question 9: Temperature Conversion Closure

Scenario: A closure that generates a function converting Celsius to Fahrenheit
and vice versa, based on user input.

Rubrics covered:
  * closure with internal state
  * converts in both directions
  * a separate closure for each direction
  * clean function design
"""


def make_converter(direction, precision=2):
    """Factory returning a closure. direction, precision and the call counter
    stay alive in the enclosing scope after make_converter has returned."""

    direction = direction.upper()
    if direction not in ("C2F", "F2C"):
        raise ValueError("direction must be 'C2F' or 'F2C'")

    calls = 0                 # internal state captured by the closure

    def convert(value):
        nonlocal calls
        calls += 1
        if direction == "C2F":
            result = value * 9 / 5 + 32
            label = f"{value} C = {round(result, precision)} F"
        else:
            result = (value - 32) * 5 / 9
            label = f"{value} F = {round(result, precision)} C"
        print(f"  [{direction} call #{calls}] {label}")
        return round(result, precision)

    def usage():
        return calls

    convert.usage = usage      # expose the captured counter
    convert.direction = direction
    return convert


def make_scaled_converter(factor, offset, unit_in, unit_out):
    """Generic closure: any linear unit conversion."""
    def convert(value):
        return round(value * factor + offset, 2)
    convert.__doc__ = f"{unit_in} -> {unit_out}"
    return convert


if __name__ == "__main__":
    c_to_f = make_converter("C2F")
    f_to_c = make_converter("F2C")

    print("=== two independent closures, two separate states ===")
    for c in (0, 37, 100, -40):
        c_to_f(c)
    for f in (32, 98.6, 212, -40):
        f_to_c(f)

    print(f"\n  c_to_f was used {c_to_f.usage()} times")
    print(f"  f_to_c was used {f_to_c.usage()} times  (counters are separate)")

    print("\n=== round trip proves both directions agree ===")
    original = 36.6
    there = c_to_f(original)
    back = f_to_c(there)
    print(f"  {original} C -> {there} F -> {back} C")

    print("\n=== the captured variables live in the closure cell ===")
    print("  free variables:", c_to_f.__code__.co_freevars)
    print("  cell contents :", [cell.cell_contents for cell in c_to_f.__closure__])

    print("\n=== generic closure factory ===")
    k_from_c = make_scaled_converter(1, 273.15, "Celsius", "Kelvin")
    mi_from_km = make_scaled_converter(0.621371, 0, "km", "miles")
    print("  25 C in Kelvin :", k_from_c(25))
    print("  100 km in miles:", mi_from_km(100))

    print("\n=== user input (falls back to a demo value) ===")
    try:
        choice = input("Convert [1] C->F or [2] F->C : ").strip()
        value = float(input("Enter the temperature: ").strip())
    except (EOFError, ValueError, OSError):
        choice, value = "1", 42.0
        print(f"  (no input - demonstrating with {value} C)")
    (c_to_f if choice != "2" else f_to_c)(value)
```

</details>

<details>
<summary>Program output</summary>

```text
=== two independent closures, two separate states ===
  [C2F call #1] 0 C = 32.0 F
  [C2F call #2] 37 C = 98.6 F
  [C2F call #3] 100 C = 212.0 F
  [C2F call #4] -40 C = -40.0 F
  [F2C call #1] 32 F = 0.0 C
  [F2C call #2] 98.6 F = 37.0 C
  [F2C call #3] 212 F = 100.0 C
  [F2C call #4] -40 F = -40.0 C

  c_to_f was used 4 times
  f_to_c was used 4 times  (counters are separate)

=== round trip proves both directions agree ===
  [C2F call #5] 36.6 C = 97.88 F
  [F2C call #5] 97.88 F = 36.6 C
  36.6 C -> 97.88 F -> 36.6 C

=== the captured variables live in the closure cell ===
  free variables: ('calls', 'direction', 'precision')
  cell contents : [5, 'C2F', 2]

=== generic closure factory ===
  25 C in Kelvin : 298.15
  100 km in miles: 62.14

=== user input (falls back to a demo value) ===
Convert [1] C->F or [2] F->C :   (no input - demonstrating with 42.0 C)
  [C2F call #6] 42.0 C = 107.6 F

```

</details>

---

## Experiment 2 - Question 10: Retry Logic with Decorators

Scenario: Decorate a function that simulates an API call so it retries on
failure (failures are generated randomly).

Rubrics covered:
  * retry mechanism inside a decorator
  * try/except used
  * random failures simulated
  * retries capped by a limit

**File:** [`q10_retry_decorator.py`](q10_retry_decorator.py) &nbsp;&middot;&nbsp; **Run:** `python q10_retry_decorator.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 2 - Question 10: Retry Logic with Decorators

Scenario: Decorate a function that simulates an API call so it retries on
failure (failures are generated randomly).

Rubrics covered:
  * retry mechanism inside a decorator
  * try/except used
  * random failures simulated
  * retries capped by a limit
"""

import functools
import random
import time


class APIError(Exception):
    """Simulated transient server error."""


def retry(times=3, delay=0.2, backoff=2.0, exceptions=(APIError,)):
    """Parameterised decorator: retries the call up to `times` attempts with
    an exponentially growing delay, then re-raises the last error."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wait = delay
            last_error = None
            for attempt in range(1, times + 1):
                try:
                    result = func(*args, **kwargs)
                    if attempt > 1:
                        print(f"   -> succeeded on attempt {attempt}/{times}")
                    return result
                except exceptions as exc:
                    last_error = exc
                    print(f"   attempt {attempt}/{times} failed: "
                          f"{type(exc).__name__}: {exc}")
                    if attempt < times:
                        print(f"   retrying in {wait:.2f}s ...")
                        time.sleep(wait)
                        wait *= backoff
            print(f"   -> giving up after {times} attempts")
            raise last_error
        wrapper.max_attempts = times
        return wrapper
    return decorator


# ---------------- simulated flaky services ----------------
@retry(times=5, delay=0.1)
def fetch_user_profile(user_id, failure_rate=0.6):
    """Fails randomly, like a real network call."""
    if random.random() < failure_rate:
        raise APIError(f"504 gateway timeout for user {user_id}")
    return {"id": user_id, "name": "Spandan Andhale", "plan": "student"}


@retry(times=3, delay=0.05)
def charge_payment(amount, failure_rate=1.0):
    """Always fails, to show the retry limit being reached."""
    if random.random() < failure_rate:
        raise APIError(f"payment gateway refused Rs.{amount}")
    return f"charged Rs.{amount}"


@retry(times=4, delay=0.05, exceptions=(APIError, ConnectionError))
def upload_report(name):
    roll = random.random()
    if roll < 0.3:
        raise ConnectionError("DNS lookup failed")
    if roll < 0.6:
        raise APIError("413 payload too large")
    return f"{name} uploaded"


if __name__ == "__main__":
    random.seed(7)            # reproducible run for the lab record

    print("=== 1. flaky GET, succeeds within the retry budget ===")
    try:
        print("  result:", fetch_user_profile(42))
    except APIError as e:
        print("  final failure:", e)

    print("\n=== 2. permanent failure, retry limit enforced ===")
    try:
        charge_payment(1999)
    except APIError as e:
        print("  caller sees:", type(e).__name__, "-", e)

    print("\n=== 3. retrying more than one exception type ===")
    try:
        print("  result:", upload_report("marks.csv"))
    except (APIError, ConnectionError) as e:
        print("  final failure:", type(e).__name__, "-", e)

    print("\n=== decorator metadata ===")
    print("  fetch_user_profile.__name__       :", fetch_user_profile.__name__)
    print("  fetch_user_profile.max_attempts   :", fetch_user_profile.max_attempts)
    print("  charge_payment.max_attempts       :", charge_payment.max_attempts)

    print("\n=== success rate over 10 independent calls ===")
    ok = 0
    for i in range(10):
        try:
            fetch_user_profile(i, failure_rate=0.5)
            ok += 1
        except APIError:
            pass
    print(f"  {ok}/10 calls eventually succeeded thanks to retries")
```

</details>

<details>
<summary>Program output</summary>

```text
=== 1. flaky GET, succeeds within the retry budget ===
   attempt 1/5 failed: APIError: 504 gateway timeout for user 42
   retrying in 0.10s ...
   attempt 2/5 failed: APIError: 504 gateway timeout for user 42
   retrying in 0.20s ...
   -> succeeded on attempt 3/5
  result: {'id': 42, 'name': 'Spandan Andhale', 'plan': 'student'}

=== 2. permanent failure, retry limit enforced ===
   attempt 1/3 failed: APIError: payment gateway refused Rs.1999
   retrying in 0.05s ...
   attempt 2/3 failed: APIError: payment gateway refused Rs.1999
   retrying in 0.10s ...
   attempt 3/3 failed: APIError: payment gateway refused Rs.1999
   -> giving up after 3 attempts
  caller sees: APIError - payment gateway refused Rs.1999

=== 3. retrying more than one exception type ===
   attempt 1/4 failed: ConnectionError: DNS lookup failed
   retrying in 0.05s ...
   attempt 2/4 failed: APIError: 413 payload too large
   retrying in 0.10s ...
   attempt 3/4 failed: ConnectionError: DNS lookup failed
   retrying in 0.20s ...
   attempt 4/4 failed: APIError: 413 payload too large
   -> giving up after 4 attempts
  final failure: APIError - 413 payload too large

=== decorator metadata ===
  fetch_user_profile.__name__       : fetch_user_profile
  fetch_user_profile.max_attempts   : 5
  charge_payment.max_attempts       : 3

=== success rate over 10 independent calls ===
   attempt 1/5 failed: APIError: 504 gateway timeout for user 0
   retrying in 0.10s ...
   attempt 2/5 failed: APIError: 504 gateway timeout for user 0
   retrying in 0.20s ...
   attempt 3/5 failed: APIError: 504 gateway timeout for user 0
   retrying in 0.40s ...
   -> succeeded on attempt 4/5
   attempt 1/5 failed: APIError: 504 gateway timeout for user 1
   retrying in 0.10s ...
   attempt 2/5 failed: APIError: 504 gateway timeout for user 1
   retrying in 0.20s ...
   -> succeeded on attempt 3/5
   attempt 1/5 failed: APIError: 504 gateway timeout for user 4
   retrying in 0.10s ...
   -> succeeded on attempt 2/5
   attempt 1/5 failed: APIError: 504 gateway timeout for user 5
   retrying in 0.10s ...
   -> succeeded on attempt 2/5
   attempt 1/5 failed: APIError: 504 gateway timeout for user 6
   retrying in 0.10s ...
   attempt 2/5 failed: APIError: 504 gateway timeout for user 6
   retrying in 0.20s ...
   attempt 3/5 failed: APIError: 504 gateway timeout for user 6
   retrying in 0.40s ...
   attempt 4/5 failed: APIError: 504 gateway timeout for user 6
   retrying in 0.80s ...
   -> succeeded on attempt 5/5
   attempt 1/5 failed: APIError: 504 gateway timeout for user 7
   retrying in 0.10s ...
   -> succeeded on attempt 2/5
   attempt 1/5 failed: APIError: 504 gateway timeout for user 9
   retrying in 0.10s ...
   -> succeeded on attempt 2/5
  10/10 calls eventually succeeded thanks to retries

```

</details>

---
