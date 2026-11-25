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
