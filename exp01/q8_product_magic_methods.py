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
