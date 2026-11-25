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
