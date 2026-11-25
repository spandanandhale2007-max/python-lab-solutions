"""
Experiment 6 - Question 2: Shortest Delivery Time Across Routes

Scenario: A delivery app calculates the shortest delivery time across multiple
routes between warehouses and customers.

Rubrics covered:
  * 2D matrix of travel times between points generated
  * diagonal, row-wise and column-wise paths extracted
  * minimum path time computed using DP
  * different routes compared with a bottom-up approach
"""

import random

SIZE = 6
NODES = ["W1", "H1", "H2", "H3", "H4", "C1"]      # warehouse -> hubs -> customer


def generate_matrix(seed=61):
    """time[i][j] = minutes to move from stage i to stage j of the route grid."""
    random.seed(seed)
    return [[random.randint(4, 30) for _ in range(SIZE)] for _ in range(SIZE)]


def print_matrix(matrix, title):
    print(f"\n=== {title} ===")
    print("        " + "".join(f"{NODES[j]:>6}" for j in range(SIZE)))
    for i, row in enumerate(matrix):
        print(f"  {NODES[i]:<6}" + "".join(f"{v:>6}" for v in row))


def min_path_bottom_up(grid):
    """Minimum time to travel from the top-left to the bottom-right cell,
    moving only right or down. dp[i][j] = grid[i][j] + min(up, left)."""
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]
    for j in range(1, cols):
        dp[0][j] = dp[0][j - 1] + grid[0][j]
    for i in range(1, rows):
        dp[i][0] = dp[i - 1][0] + grid[i][0]
    for i in range(1, rows):
        for j in range(1, cols):
            dp[i][j] = grid[i][j] + min(dp[i - 1][j], dp[i][j - 1])

    # walk back to recover the route
    path, i, j = [], rows - 1, cols - 1
    while (i, j) != (0, 0):
        path.append((i, j))
        if i == 0:
            j -= 1
        elif j == 0:
            i -= 1
        elif dp[i - 1][j] <= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    path.append((0, 0))
    path.reverse()
    return dp[rows - 1][cols - 1], path, dp


def min_path_with_diagonal(grid):
    """Same problem but a diagonal move is also allowed (an express lane)."""
    rows, cols = len(grid), len(grid[0])
    INF = float("inf")
    dp = [[INF] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]
    for i in range(rows):
        for j in range(cols):
            if i == 0 and j == 0:
                continue
            options = []
            if i:
                options.append(dp[i - 1][j])
            if j:
                options.append(dp[i][j - 1])
            if i and j:
                options.append(dp[i - 1][j - 1])
            dp[i][j] = grid[i][j] + min(options)
    return dp[rows - 1][cols - 1], dp


if __name__ == "__main__":
    times = generate_matrix()
    print_matrix(times, "travel time matrix (minutes)")

    print("\n=== extracting paths from the matrix ===")
    diagonal = [times[i][i] for i in range(SIZE)]
    anti_diag = [times[i][SIZE - 1 - i] for i in range(SIZE)]
    print(f"  main diagonal      : {diagonal}  total {sum(diagonal)} min")
    print(f"  anti-diagonal      : {anti_diag}  total {sum(anti_diag)} min")

    print("\n  row-wise routes (one hub handles the whole leg):")
    for i, row in enumerate(times):
        print(f"    row {NODES[i]:<4} {row}  total {sum(row):>3} min  "
              f"avg {sum(row) / SIZE:>5.1f}")
    best_row = min(range(SIZE), key=lambda i: sum(times[i]))
    print(f"    fastest row  : {NODES[best_row]} ({sum(times[best_row])} min)")

    print("\n  column-wise routes:")
    for j in range(SIZE):
        col = [times[i][j] for i in range(SIZE)]
        print(f"    col {NODES[j]:<4} {col}  total {sum(col):>3} min")
    best_col = min(range(SIZE),
                   key=lambda j: sum(times[i][j] for i in range(SIZE)))
    print(f"    fastest column: {NODES[best_col]} "
          f"({sum(times[i][best_col] for i in range(SIZE))} min)")

    best, path, dp = min_path_bottom_up(times)
    print("\n=== minimum delivery time, right/down moves only (bottom-up DP) ===")
    print(f"  shortest total time : {best} minutes")
    print(f"  cells visited       : {len(path)}")
    print("  route               : " +
          " -> ".join(f"({NODES[i]},{NODES[j]})" for i, j in path))
    print(f"  leg times           : {[times[i][j] for i, j in path]}")

    print("\n=== the DP table (cheapest time to reach each cell) ===")
    print("        " + "".join(f"{NODES[j]:>6}" for j in range(SIZE)))
    for i, row in enumerate(dp):
        marks = ["*" if (i, j) in path else " " for j in range(SIZE)]
        print(f"  {NODES[i]:<6}" +
              "".join(f"{v:>5}{m}" for v, m in zip(row, marks)))
    print("  (* marks the chosen route)")

    diag_best, diag_dp = min_path_with_diagonal(times)
    print("\n=== comparing route policies ===")
    print(f"  right/down only            : {best} minutes")
    print(f"  right/down/diagonal        : {diag_best} minutes "
          f"({best - diag_best} min faster)")
    print(f"  naive main-diagonal route  : {sum(diagonal)} minutes")
    print(f"  best single row            : {sum(times[best_row])} minutes")
    print(f"  DP beats the naive diagonal by "
          f"{sum(diagonal) - best} minutes "
          f"({(1 - best / sum(diagonal)) * 100:.1f}% quicker)")

    print("\n=== promised delivery window ===")
    print(f"  optimal route {best} min + 10 min handling = "
          f"{best + 10} min promise to the customer")
