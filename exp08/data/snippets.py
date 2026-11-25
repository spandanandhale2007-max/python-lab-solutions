"""Collected snippets from the Python lab."""
import math

# snippet 1: average of a list
def average(values):
    return sum(values) / len(values) if values else 0.0


# snippet 2: Fibonacci generator
def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


# snippet 3: circle area
def circle_area(r):
    return math.pi * r ** 2


# snippet 4: read a file into a list of lines
def read_lines(path):
    with open(path, encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh]


class Counter:
    """snippet 5: a tiny counter class"""

    def __init__(self):
        self.n = 0

    def tick(self):
        self.n += 1
        return self.n
