"""
Experiment 6 - Question 8: Warehouse Robot Minimum Cost Path

Scenario: A robot in a warehouse moves from the top-left to the bottom-right
of a grid. Minimise the total travel cost based on terrain difficulty.

Rubrics covered:
  * 2D terrain cost matrix generated
  * the robot's movement path tracked
  * DP used to compute the minimum cost path
  * obstacles and high-cost cells highlighted
"""

import random

ROWS, COLS = 8, 8
OBSTACLE = 99
HIGH_COST = 7
INF = float("inf")


def generate_terrain(seed=103):
    """Cost of rolling over each cell: 1 smooth floor .. 8 ramps, 99 shelving."""
    random.seed(seed)
    grid = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            roll = random.random()
            if roll < 0.10 and (r, c) not in ((0, 0), (ROWS - 1, COLS - 1)):
                row.append(OBSTACLE)                   # shelf, impassable
            elif roll < 0.25:
                row.append(random.randint(HIGH_COST, 9))
            else:
                row.append(random.randint(1, 4))
        grid.append(row)
    return grid


def min_cost_path(grid):
    """dp[r][c] = cheapest cost to reach (r, c) moving right or down."""
    dp = [[INF] * COLS for _ in range(ROWS)]
    dp[0][0] = grid[0][0]
    for c in range(1, COLS):
        if grid[0][c] != OBSTACLE and dp[0][c - 1] != INF:
            dp[0][c] = dp[0][c - 1] + grid[0][c]
    for r in range(1, ROWS):
        if grid[r][0] != OBSTACLE and dp[r - 1][0] != INF:
            dp[r][0] = dp[r - 1][0] + grid[r][0]
    for r in range(1, ROWS):
        for c in range(1, COLS):
            if grid[r][c] == OBSTACLE:
                continue
            best = min(dp[r - 1][c], dp[r][c - 1])
            if best != INF:
                dp[r][c] = best + grid[r][c]

    total = dp[ROWS - 1][COLS - 1]
    if total == INF:
        return INF, [], dp
    path, r, c = [], ROWS - 1, COLS - 1
    while (r, c) != (0, 0):
        path.append((r, c))
        if r == 0:
            c -= 1
        elif c == 0:
            r -= 1
        elif dp[r - 1][c] <= dp[r][c - 1]:
            r -= 1
        else:
            c -= 1
    path.append((0, 0))
    path.reverse()
    return total, path, dp


def render(grid, path=None):
    path = set(path or [])
    print("       " + "".join(f"{c:>5}" for c in range(COLS)))
    for r in range(ROWS):
        cells = []
        for c in range(COLS):
            v = grid[r][c]
            if v == OBSTACLE:
                text = "###"
            elif v >= HIGH_COST:
                text = f"{v}!"
            else:
                text = str(v)
            cells.append(f"[{text}]" if (r, c) in path else f"{text:>5}")
        print(f"  r{r:<4}" + "".join(f"{t:>5}" for t in cells))
    print("  ### obstacle   n! high cost   [n] robot path")


if __name__ == "__main__":
    terrain = generate_terrain()

    print("=== warehouse terrain cost map ===")
    render(terrain)

    obstacles = [(r, c) for r in range(ROWS) for c in range(COLS)
                 if terrain[r][c] == OBSTACLE]
    expensive = [(r, c) for r in range(ROWS) for c in range(COLS)
                 if HIGH_COST <= terrain[r][c] < OBSTACLE]
    print(f"\n  obstacles ({len(obstacles)}): {obstacles}")
    print(f"  high-cost cells ({len(expensive)}): {expensive}")
    passable = ROWS * COLS - len(obstacles)
    print(f"  passable cells: {passable}/{ROWS * COLS}")

    total, path, dp = min_cost_path(terrain)

    print("\n=== minimum cost path (bottom-up DP) ===")
    if total == INF:
        print("  the robot cannot reach the dock, shelving blocks every route")
    else:
        print(f"  minimum total cost : {total}")
        print(f"  cells traversed    : {len(path)} "
              f"(the shortest possible is {ROWS + COLS - 1})")
        print(f"  path               : {path}")
        print(f"  cost of each step  : {[terrain[r][c] for r, c in path]}")
        print(f"  average cell cost  : {total / len(path):.2f}")
        print(f"  high-cost cells used: "
              f"{sum(1 for r, c in path if terrain[r][c] >= HIGH_COST)}")

    print("\n=== DP cost-to-reach table ===")
    print("       " + "".join(f"{c:>6}" for c in range(COLS)))
    for r in range(ROWS):
        cells = [f"{'inf' if dp[r][c] == INF else dp[r][c]:>6}"
                 for c in range(COLS)]
        print(f"  r{r:<4}" + "".join(cells))

    if path:
        print("\n=== path highlighted on the terrain ===")
        render(terrain, path)

    print("\n=== comparison with naive routes ===")
    top_then_right = None
    if all(terrain[0][c] != OBSTACLE for c in range(COLS)) and \
            all(terrain[r][COLS - 1] != OBSTACLE for r in range(ROWS)):
        top_then_right = (sum(terrain[0][c] for c in range(COLS)) +
                          sum(terrain[r][COLS - 1] for r in range(1, ROWS)))
    left_then_bottom = None
    if all(terrain[r][0] != OBSTACLE for r in range(ROWS)) and \
            all(terrain[ROWS - 1][c] != OBSTACLE for c in range(COLS)):
        left_then_bottom = (sum(terrain[r][0] for r in range(ROWS)) +
                            sum(terrain[ROWS - 1][c] for c in range(1, COLS)))
    for label, cost in (("along the top then down the right edge", top_then_right),
                        ("down the left edge then along the bottom",
                         left_then_bottom)):
        if cost is None:
            print(f"  {label:<42} blocked by shelving")
        else:
            print(f"  {label:<42} cost {cost} "
                  f"({cost - total:+} vs optimal)")

    print("\n=== battery estimate at 1.5 Wh per cost unit ===")
    if total != INF:
        print(f"  optimal route uses about {total * 1.5:.1f} Wh")
        print(f"  a 60 Wh battery allows about {60 / (total * 1.5):.1f} "
              f"round trips")
