"""
Experiment 8 - Question 7: Code Snippet Extractor

Scenario: snippets.py contains several code snippets. Count how many lines of
code there are and extract the first two lines, writing them to
snippet_preview.py.

Run: python q7_code_snippet_extractor.py
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "snippets.py")
OUTPUT_FILE = os.path.join(DATA, "snippet_preview.py")

SAMPLE = '''"""Collected snippets from the Python lab."""
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
        return [line.rstrip("\\n") for line in fh]


class Counter:
    """snippet 5: a tiny counter class"""

    def __init__(self):
        self.n = 0

    def tick(self):
        self.n += 1
        return self.n
'''


def ensure_sample():
    os.makedirs(DATA, exist_ok=True)
    if not os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, "w", encoding="utf-8") as fh:
            fh.write(SAMPLE)
        print(f"[setup] created sample input {INPUT_FILE}")


def classify(line):
    stripped = line.strip()
    if not stripped:
        return "blank"
    if stripped.startswith("#"):
        return "comment"
    if stripped.startswith(("def ", "async def ")):
        return "function"
    if stripped.startswith("class "):
        return "class"
    if stripped.startswith(("import ", "from ")):
        return "import"
    return "code"


if __name__ == "__main__":
    ensure_sample()

    with open(INPUT_FILE, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    print(f"=== read {os.path.basename(INPUT_FILE)} ===")
    print(f"  total lines        : {len(lines)}")
    print(f"  file size          : {os.path.getsize(INPUT_FILE)} bytes")

    kinds = {}
    for line in lines:
        k = classify(line)
        kinds[k] = kinds.get(k, 0) + 1

    print("\n=== line breakdown ===")
    for kind in ("import", "class", "function", "code", "comment", "blank"):
        n = kinds.get(kind, 0)
        print(f"  {kind:<10}{n:>4}  {'#' * n}")
    loc = len(lines) - kinds.get("blank", 0) - kinds.get("comment", 0)
    print(f"\n  effective lines of code (no blanks or comments): {loc}")
    print(f"  comment density : "
          f"{kinds.get('comment', 0) / len(lines) * 100:.1f}%")

    first_two = lines[:2]
    print("\n=== first two lines ===")
    for i, line in enumerate(first_two, 1):
        print(f"  {i}. {line!r}")

    print("\n=== functions and classes defined ===")
    for n, line in enumerate(lines, 1):
        kind = classify(line)
        if kind in ("function", "class"):
            name = line.strip().split()[1].split("(")[0].rstrip(":")
            print(f"  line {n:>3}  {kind:<9}{name}")

    print("\n=== imports ===")
    for n, line in enumerate(lines, 1):
        if classify(line) == "import":
            print(f"  line {n:>3}  {line.strip()}")

    print("\n=== longest lines (style check, 79-char limit) ===")
    long_lines = [(n, line) for n, line in enumerate(lines, 1)
                  if len(line) > 79]
    if long_lines:
        for n, line in long_lines:
            print(f"  line {n:>3}  {len(line)} chars")
    else:
        print(f"  none, the longest line is "
              f"{max(len(line) for line in lines)} chars")

    print("\n=== indentation depth ===")
    depths = {}
    for line in lines:
        if line.strip():
            indent = len(line) - len(line.lstrip())
            depths[indent] = depths.get(indent, 0) + 1
    for indent in sorted(depths):
        print(f"  {indent:>2} space(s): {depths[indent]:>3} line(s)")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        for line in first_two:
            fh.write(line + "\n")

    print(f"\n=== wrote {OUTPUT_FILE} ===")
    with open(OUTPUT_FILE, "r", encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            print(f"  {i}: {line.rstrip()}")

    print(f"\n  preview holds "
          f"{sum(1 for _ in open(OUTPUT_FILE, encoding='utf-8'))} of "
          f"{len(lines)} lines "
          f"({2 / len(lines) * 100:.1f}% of the file)")
