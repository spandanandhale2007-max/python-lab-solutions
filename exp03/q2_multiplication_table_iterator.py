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
