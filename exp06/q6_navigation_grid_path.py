"""
Experiment 6 - Question 6: Fastest Walking Path Through City Blocks

Scenario: A navigation app calculates the fastest walking path through a grid
of city blocks, allowing for blocked paths and delays.

Rubrics covered:
  * 2D grid generated with random weights (walking times)
  * shortest path found with bottom-up DP
  * blocked or delayed paths marked
  * optimal total time and the path indices returned
"""

import heapq
import random

ROWS, COLS = 7, 8
BLOCKED = -1
INF = float("inf")


def generate_grid(seed=91, block_chance=0.12, delay_chance=0.15):
    """Each cell holds the minutes needed to cross that block.
    BLOCKED means construction, no walking through."""
    random.seed(seed)
    grid = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            roll = random.random()
            if roll < block_chance and (r, c) not in ((0, 0), (ROWS - 1, COLS - 1)):
                row.append(BLOCKED)
            elif roll < block_chance + delay_chance:
                row.append(random.randint(9, 15))      # delayed block
            else:
                row.append(random.randint(1, 6))
            row[-1] = row[-1]
        grid.append(row)
    return grid


def print_grid(grid, path=None, title="grid"):
    path = set(path or [])
    print(f"\n=== {title} ===")
    print("       " + "".join(f"{c:>6}" for c in range(COLS)))
    for r in range(ROWS):
        cells = []
        for c in range(COLS):
            v = grid[r][c]
            text = "XXX" if v == BLOCKED else str(v)
            if (r, c) in path:
                text = f"[{text}]"
            cells.append(f"{text:>6}")
        print(f"  r{r:<4}" + "".join(cells))
    print("  XXX = blocked, [n] = chosen path")


def shortest_path_dp(grid):
    """Bottom-up DP for right/down moves only.
    dp[r][c] = grid[r][c] + min(dp[r-1][c], dp[r][c-1])"""
    dp = [[INF] * COLS for _ in range(ROWS)]
    if grid[0][0] == BLOCKED:
        return INF, [], dp
    dp[0][0] = grid[0][0]
    for c in range(1, COLS):
        if grid[0][c] != BLOCKED and dp[0][c - 1] != INF:
            dp[0][c] = dp[0][c - 1] + grid[0][c]
    for r in range(1, ROWS):
        if grid[r][0] != BLOCKED and dp[r - 1][0] != INF:
            dp[r][0] = dp[r - 1][0] + grid[r][0]
    for r in range(1, ROWS):
        for c in range(1, COLS):
            if grid[r][c] == BLOCKED:
                continue
            best_prev = min(dp[r - 1][c], dp[r][c - 1])
            if best_prev != INF:
                dp[r][c] = best_prev + grid[r][c]

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


def shortest_path_any_direction(grid):
    """Dijkstra, allowing all four directions - DP cannot handle cycles."""
    dist = {(0, 0): grid[0][0]}
    parent = {}
    pq = [(grid[0][0], 0, 0)]
    target = (ROWS - 1, COLS - 1)
    while pq:
        d, r, c = heapq.heappop(pq)
        if (r, c) == target:
            break
        if d > dist.get((r, c), INF):
            continue
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if not (0 <= nr < ROWS and 0 <= nc < COLS):
                continue
            if grid[nr][nc] == BLOCKED:
                continue
            nd = d + grid[nr][nc]
            if nd < dist.get((nr, nc), INF):
                dist[(nr, nc)] = nd
                parent[(nr, nc)] = (r, c)
                heapq.heappush(pq, (nd, nr, nc))
    if target not in dist:
        return INF, []
    path, node = [], target
    while node != (0, 0):
        path.append(node)
        node = parent[node]
    path.append((0, 0))
    path.reverse()
    return dist[target], path


if __name__ == "__main__":
    grid = generate_grid()
    print_grid(grid, title="walking time per block (minutes)")

    blocked = [(r, c) for r in range(ROWS) for c in range(COLS)
               if grid[r][c] == BLOCKED]
    delayed = [(r, c) for r in range(ROWS) for c in range(COLS)
               if grid[r][c] >= 9]
    print(f"\n  blocked blocks ({len(blocked)}): {blocked}")
    print(f"  delayed blocks ({len(delayed)}): {delayed}")

    total, path, dp = shortest_path_dp(grid)

    print("\n=== bottom-up DP, right and down moves only ===")
    if total == INF:
        print("  no right/down route exists, construction blocks every path")
    else:
        print(f"  fastest total time : {total} minutes")
        print(f"  blocks crossed     : {len(path)}")
        print(f"  path indices       : {path}")
        print(f"  per-block times    : {[grid[r][c] for r, c in path]}")

    print("\n=== DP table (fastest time to reach each block) ===")
    print("       " + "".join(f"{c:>7}" for c in range(COLS)))
    for r in range(ROWS):
        cells = []
        for c in range(COLS):
            v = dp[r][c]
            cells.append(f"{'inf' if v == INF else v:>7}")
        print(f"  r{r:<4}" + "".join(cells))

    if path:
        print_grid(grid, path, "chosen route")

    d_total, d_path = shortest_path_any_direction(grid)
    print("\n=== allowing all four directions (Dijkstra) ===")
    if d_total == INF:
        print("  the destination is completely walled off")
    else:
        print(f"  fastest time       : {d_total} minutes")
        print(f"  blocks crossed     : {len(d_path)}")
        print(f"  path indices       : {d_path}")
        if total != INF:
            print(f"  detouring upward/leftward saves "
                  f"{total - d_total} minute(s)")

    print("\n=== why the restriction matters ===")
    print("  Right/down only gives a clean O(rows*cols) DP because the")
    print("  subproblems have no cycles. Allowing up/left creates cycles,")
    print("  so the same grid then needs Dijkstra instead of tabulation.")
