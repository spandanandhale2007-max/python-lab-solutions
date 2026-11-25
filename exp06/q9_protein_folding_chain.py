"""
Experiment 6 - Question 9: Protein Folding Energy (Matrix Chain analogy)

Scenario: A biomedical tool identifies the optimal way to fold proteins based
on energy costs.

Rubrics covered:
  * list of folding steps with transition costs generated
  * multiplication cost defined from energy levels
  * total folding energy minimised
  * step-by-step energy reduction tracked with DP
"""

import random

SEGMENTS = ["Helix-A", "Loop-1", "Sheet-B", "Turn-2", "Helix-C", "Coil-D"]


def generate_energy_levels(seed=113):
    """energy[i] is the interface size between segment i-1 and segment i.
    Folding segments i..k and k+1..j together costs
    energy[i] * energy[k+1] * energy[j+1] units, exactly like multiplying
    two matrices whose shared dimension is the interface."""
    random.seed(seed)
    return [random.choice([4, 6, 8, 12, 16, 20, 24])
            for _ in range(len(SEGMENTS) + 1)]


def optimal_folding(energy):
    n = len(energy) - 1
    dp = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float("inf")
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + \
                    energy[i] * energy[k + 1] * energy[j + 1]
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    split[i][j] = k
    return dp, split


def fold_expression(split, i, j):
    if i == j:
        return SEGMENTS[i]
    k = split[i][j]
    return (f"({fold_expression(split, i, k)} + "
            f"{fold_expression(split, k + 1, j)})")


def fold_steps(split, energy, i, j, out=None):
    if out is None:
        out = []
    if i == j:
        return out
    k = split[i][j]
    fold_steps(split, energy, i, k, out)
    fold_steps(split, energy, k + 1, j, out)
    out.append((i, k, j, energy[i] * energy[k + 1] * energy[j + 1]))
    return out


def sequential_cost(energy):
    """Folding strictly from the N-terminus outwards, no optimisation."""
    n = len(energy) - 1
    return sum(energy[0] * energy[i] * energy[i + 1] for i in range(1, n))


if __name__ == "__main__":
    energy = generate_energy_levels()
    n = len(SEGMENTS)

    print("=== protein segments and interface energies ===")
    print(f"  interface vector: {energy}")
    print(f"  {'#':<4}{'segment':<12}{'interface':>14}{'self energy':>14}")
    for i, name in enumerate(SEGMENTS):
        print(f"  {i:<4}{name:<12}{f'{energy[i]}-{energy[i + 1]}':>14}"
              f"{energy[i] * energy[i + 1]:>14,}")

    dp, split = optimal_folding(energy)

    print("\n=== DP energy table (minimum units to fold segments i..j) ===")
    print("            " + "".join(f"{SEGMENTS[j][:8]:>10}" for j in range(n)))
    for i in range(n):
        row = "".join(f"{dp[i][j]:>10,}" if j >= i else f"{'-':>10}"
                      for j in range(n))
        print(f"  {SEGMENTS[i][:10]:<10}" + row)

    print("\n=== split table (which bond is formed last) ===")
    print("            " + "".join(f"{SEGMENTS[j][:8]:>10}" for j in range(n)))
    for i in range(n):
        row = "".join(f"{SEGMENTS[split[i][j]][:8]:>10}" if j > i
                      else f"{'-':>10}" for j in range(n))
        print(f"  {SEGMENTS[i][:10]:<10}" + row)

    best = dp[0][n - 1]
    print("\n=== optimal folding pathway ===")
    print(f"  minimum folding energy : {best:,} units")
    print(f"  grouping               : {fold_expression(split, 0, n - 1)}")

    print("\n=== step-by-step energy reduction ===")
    steps = fold_steps(split, energy, 0, n - 1)
    running = 0
    print(f"  {'step':<6}{'fold':<34}{'cost':>10}{'cumulative':>13}")
    for num, (i, k, j, cost) in enumerate(steps, 1):
        running += cost
        left = SEGMENTS[i] if i == k else f"{SEGMENTS[i][:6]}..{SEGMENTS[k][:6]}"
        right = (SEGMENTS[k + 1] if k + 1 == j
                 else f"{SEGMENTS[k + 1][:6]}..{SEGMENTS[j][:6]}")
        print(f"  {num:<6}{f'{left} + {right}':<34}{cost:>10,}{running:>13,}")
    print(f"  {'':6}{'TOTAL':<34}{'':>10}{running:>13,}")
    print(f"  matches the DP answer: {running == best}")

    naive = sequential_cost(energy)
    print("\n=== comparison with sequential folding ===")
    print(f"  optimal pathway    : {best:,} units")
    print(f"  N-to-C sequential  : {naive:,} units")
    print(f"  energy saved       : {naive - best:,} units "
          f"({(1 - best / naive) * 100:.1f}% less)")

    print("\n=== energy per sub-chain length ===")
    for length in range(1, n + 1):
        costs = [dp[i][i + length - 1] for i in range(n - length + 1)]
        print(f"  {length} segment(s): cheapest {min(costs):>8,}   "
              f"costliest {max(costs):>8,}")

    print("\n=== stability note ===")
    print(f"  the fold with the lowest energy, {best:,} units, is the most")
    print("  stable conformation this model predicts. Real folding also")
    print("  depends on solvent and chaperones; this is the DP exercise only.")
