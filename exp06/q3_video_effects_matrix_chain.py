"""
Experiment 6 - Question 3: Video Effect Merge Order (Matrix Chain Multiplication)

Scenario: A video editing app merges multiple video effects that have different
processing costs. Optimise the order of merging.

Rubrics covered:
  * list of video segments with render costs generated
  * multiplication cost defined between effects
  * optimal parenthesis placement logic applied
  * minimum processing time tracked in a DP table
"""

import random

EFFECTS = ["ColorGrade", "Denoise", "Stabilise", "Sharpen", "Bloom", "Grain"]


def generate_dimensions(seed=71):
    """dims[i] x dims[i+1] is the cost shape of effect i.
    Think of each effect as a transform matrix: merging two adjacent effects
    costs rows * shared * cols render units."""
    random.seed(seed)
    return [random.choice([5, 10, 15, 20, 25, 30, 40])
            for _ in range(len(EFFECTS) + 1)]


def matrix_chain_order(dims):
    """dp[i][j] = minimum cost to merge effects i..j.
    split[i][j] remembers where the best parenthesis goes."""
    n = len(dims) - 1                       # number of effects
    dp = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]

    for length in range(2, n + 1):          # chain length
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float("inf")
            for k in range(i, j):
                cost = (dp[i][k] + dp[k + 1][j] +
                        dims[i] * dims[k + 1] * dims[j + 1])
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    split[i][j] = k
    return dp, split


def build_expression(split, i, j):
    if i == j:
        return EFFECTS[i]
    k = split[i][j]
    return f"({build_expression(split, i, k)} x {build_expression(split, k + 1, j)})"


def left_to_right_cost(dims):
    """Cost of ((E1 x E2) x E3) x ... - merging in the order the user added
    the effects. Each step multiplies a dims[0] x dims[i] block by the next."""
    n = len(dims) - 1
    return sum(dims[0] * dims[i] * dims[i + 1] for i in range(1, n))


def right_to_left_cost(dims):
    """Cost of E1 x (E2 x (E3 x ...)) - merging from the end backwards."""
    n = len(dims) - 1
    return sum(dims[i - 1] * dims[i] * dims[n] for i in range(1, n))


if __name__ == "__main__":
    dims = generate_dimensions()
    n = len(EFFECTS)

    print("=== effect chain ===")
    print(f"  dimension vector: {dims}")
    print(f"  {'#':<4}{'effect':<14}{'shape':>12}{'render units':>16}")
    for i, name in enumerate(EFFECTS):
        print(f"  {i:<4}{name:<14}{f'{dims[i]}x{dims[i + 1]}':>12}"
              f"{dims[i] * dims[i + 1]:>16,}")

    dp, split = matrix_chain_order(dims)

    print("\n=== DP cost table (minimum units to merge effects i..j) ===")
    print("        " + "".join(f"{EFFECTS[j][:7]:>9}" for j in range(n)))
    for i in range(n):
        row = ""
        for j in range(n):
            row += f"{dp[i][j]:>9,}" if j >= i else f"{'-':>9}"
        print(f"  {EFFECTS[i][:7]:<7}" + row)

    print("\n=== split table (where the best parenthesis goes) ===")
    print("        " + "".join(f"{EFFECTS[j][:7]:>9}" for j in range(n)))
    for i in range(n):
        row = ""
        for j in range(n):
            row += (f"{EFFECTS[split[i][j]][:7]:>9}" if j > i else f"{'-':>9}")
        print(f"  {EFFECTS[i][:7]:<7}" + row)

    best = dp[0][n - 1]
    print("\n=== optimal merge plan ===")
    print(f"  minimum render cost : {best:,} units")
    print(f"  parenthesisation    : {build_expression(split, 0, n - 1)}")

    print("\n=== merge sequence, innermost first ===")
    def steps(i, j, out):
        if i == j:
            return
        k = split[i][j]
        steps(i, k, out)
        steps(k + 1, j, out)
        out.append((i, k, j, dims[i] * dims[k + 1] * dims[j + 1]))
        return out
    order = steps(0, n - 1, []) or []
    for num, (i, k, j, cost) in enumerate(order, 1):
        left = EFFECTS[i] if i == k else f"{EFFECTS[i]}..{EFFECTS[k]}"
        right = (EFFECTS[k + 1] if k + 1 == j
                 else f"{EFFECTS[k + 1]}..{EFFECTS[j]}")
        print(f"  step {num}: merge [{left}] with [{right}] -> {cost:,} units")

    naive_lr = left_to_right_cost(dims)
    naive_rl = right_to_left_cost(dims)
    print("\n=== comparison with naive orders ===")
    print(f"  optimal (DP)        : {best:,} units")
    print(f"  left-to-right merge : {naive_lr:,} units "
          f"({naive_lr / best:.2f}x the optimum)")
    print(f"  right-to-left merge : {naive_rl:,} units "
          f"({naive_rl / best:.2f}x the optimum)")
    print(f"  saved by reordering : {naive_lr - best:,} units "
          f"({(1 - best / naive_lr) * 100:.1f}% less rendering)")

    print("\n=== render time estimate at 2,000 units per second ===")
    for label, cost in (("optimal", best), ("left-to-right", naive_lr)):
        print(f"  {label:<16} {cost / 2000:>8.2f} s")

    print("\n=== cost of every possible first split ===")
    for k in range(n - 1):
        cost = dp[0][k] + dp[k + 1][n - 1] + dims[0] * dims[k + 1] * dims[n]
        marker = "  <- chosen" if k == split[0][n - 1] else ""
        print(f"  split after {EFFECTS[k]:<12} -> {cost:>10,} units{marker}")
