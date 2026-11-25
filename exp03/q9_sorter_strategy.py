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
