"""
Experiment 6 - Question 10: Game AI Minimum Risk Path

Scenario: A game AI plans movement across zones to reach a target with minimal
health loss.

Rubrics covered:
  * grid generated with risk values per cell
  * start and goal positions defined
  * path with the lowest cumulative risk computed
  * health drop visualised along the path
"""

import heapq
import random

ROWS, COLS = 8, 10
START = (0, 0)
GOAL = (ROWS - 1, COLS - 1)
MAX_HP = 100


def generate_risk_grid(seed=127):
    """Risk = health points lost when entering a zone."""
    random.seed(seed)
    grid = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            roll = random.random()
            if roll < 0.08:
                row.append(random.randint(18, 26))      # boss zone
            elif roll < 0.28:
                row.append(random.randint(8, 14))       # enemy patrol
            else:
                row.append(random.randint(0, 5))        # safe ground
            row[-1] = row[-1]
        grid.append(row)
    grid[START[0]][START[1]] = 0                        # spawn is safe
    return grid


def min_risk_dijkstra(grid, start, goal):
    """All four directions allowed, so Dijkstra rather than plain DP."""
    dist = {start: grid[start[0]][start[1]]}
    parent = {}
    pq = [(dist[start], start)]
    while pq:
        d, node = heapq.heappop(pq)
        if node == goal:
            break
        if d > dist.get(node, float("inf")):
            continue
        r, c = node
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if not (0 <= nr < ROWS and 0 <= nc < COLS):
                continue
            nd = d + grid[nr][nc]
            if nd < dist.get((nr, nc), float("inf")):
                dist[(nr, nc)] = nd
                parent[(nr, nc)] = node
                heapq.heappush(pq, (nd, (nr, nc)))
    if goal not in dist:
        return float("inf"), []
    path, node = [], goal
    while node != start:
        path.append(node)
        node = parent[node]
    path.append(start)
    path.reverse()
    return dist[goal], path


def min_risk_dp(grid, start, goal):
    """Right/down only: a clean bottom-up DP table."""
    dp = [[float("inf")] * COLS for _ in range(ROWS)]
    dp[start[0]][start[1]] = grid[start[0]][start[1]]
    for r in range(start[0], ROWS):
        for c in range(start[1], COLS):
            if (r, c) == start:
                continue
            best = float("inf")
            if r > start[0]:
                best = min(best, dp[r - 1][c])
            if c > start[1]:
                best = min(best, dp[r][c - 1])
            if best != float("inf"):
                dp[r][c] = best + grid[r][c]
    total = dp[goal[0]][goal[1]]
    path, (r, c) = [], goal
    while (r, c) != start:
        path.append((r, c))
        if r == start[0]:
            c -= 1
        elif c == start[1]:
            r -= 1
        elif dp[r - 1][c] <= dp[r][c - 1]:
            r -= 1
        else:
            c -= 1
    path.append(start)
    path.reverse()
    return total, path, dp


def render(grid, path=None):
    path = set(path or [])
    print("       " + "".join(f"{c:>5}" for c in range(COLS)))
    for r in range(ROWS):
        cells = []
        for c in range(COLS):
            v = grid[r][c]
            text = f"{v}"
            if (r, c) == START:
                text = "S"
            elif (r, c) == GOAL:
                text = "G"
            cells.append(f"[{text}]" if (r, c) in path else f"{text}")
        print(f"  r{r:<4}" + "".join(f"{t:>5}" for t in cells))
    print("  S start   G goal   [n] chosen path   numbers = HP lost per zone")


if __name__ == "__main__":
    grid = generate_risk_grid()

    print(f"=== risk map, start {START} -> goal {GOAL} ===")
    render(grid)

    danger = [(r, c) for r in range(ROWS) for c in range(COLS)
              if grid[r][c] >= 18]
    print(f"\n  boss zones (18+ risk): {danger}")
    print(f"  average zone risk    : "
          f"{sum(sum(row) for row in grid) / (ROWS * COLS):.2f} HP")

    dp_total, dp_path, dp_table = min_risk_dp(grid, START, GOAL)
    dij_total, dij_path = min_risk_dijkstra(grid, START, GOAL)

    print("\n=== right/down only (bottom-up DP) ===")
    print(f"  cumulative risk : {dp_total} HP")
    print(f"  zones crossed   : {len(dp_path)}")
    print(f"  path            : {dp_path}")

    print("\n=== all four directions (Dijkstra) ===")
    print(f"  cumulative risk : {dij_total} HP")
    print(f"  zones crossed   : {len(dij_path)}")
    print(f"  path            : {dij_path}")
    print(f"  detours save    : {dp_total - dij_total} HP")

    best_total, best_path = ((dij_total, dij_path) if dij_total < dp_total
                             else (dp_total, dp_path))

    print("\n=== chosen route on the map ===")
    render(grid, best_path)

    print("\n=== health drop along the path ===")
    hp = MAX_HP
    print(f"  {'step':<6}{'zone':<10}{'risk':>6}{'HP left':>10}  health bar")
    for step, (r, c) in enumerate(best_path):
        hp -= grid[r][c]
        bar = "#" * max(0, hp // 3)
        state = "DEAD" if hp <= 0 else ""
        print(f"  {step:<6}{f'({r},{c})':<10}{grid[r][c]:>6}{hp:>10}  "
              f"|{bar} {state}")

    print(f"\n  starting HP : {MAX_HP}")
    print(f"  total risk  : {best_total}")
    print(f"  final HP    : {hp}")
    print(f"  survives    : {hp > 0}")
    if hp > 0:
        print(f"  margin      : {hp} HP ({hp / MAX_HP * 100:.0f}% remaining)")
    else:
        print(f"  the AI needs {abs(hp) + 1} more HP or a safer route")

    print("\n=== DP table (minimum risk to reach each zone, right/down) ===")
    print("       " + "".join(f"{c:>6}" for c in range(COLS)))
    for r in range(ROWS):
        cells = [f"{'inf' if dp_table[r][c] == float('inf') else dp_table[r][c]:>6}"
                 for c in range(COLS)]
        print(f"  r{r:<4}" + "".join(cells))

    print("\n=== comparison with a reckless straight-line run ===")
    straight = (sum(grid[0][c] for c in range(COLS)) +
                sum(grid[r][COLS - 1] for r in range(1, ROWS)))
    print(f"  along the top then down the right edge: {straight} HP")
    print(f"  optimal route                        : {best_total} HP")
    print(f"  the AI saves {straight - best_total} HP by planning")
