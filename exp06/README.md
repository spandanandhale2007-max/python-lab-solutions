# Experiment 6 - Unit II

2D dynamic programming: grid paths, matrix chain, sequence alignment, edit distance

10 scenario questions, each solved in its own section and its own file. Every program below was executed and the real output is included.

[Back to the index](../README.md)

---

## Questions in this experiment

- [Experiment 6 - Question 1: Fitness Band Heart Rate Analysis](#experiment-6---question-1-fitness-band-heart-rate-analysis)
- [Experiment 6 - Question 2: Shortest Delivery Time Across Routes](#experiment-6---question-2-shortest-delivery-time-across-routes)
- [Experiment 6 - Question 3: Video Effect Merge Order (Matrix Chain Multiplication)](#experiment-6---question-3-video-effect-merge-order-matrix-chain-multiplication)
- [Experiment 6 - Question 4: DNA Sequence Alignment](#experiment-6---question-4-dna-sequence-alignment)
- [Experiment 6 - Question 5: Edit Distance Between Answers](#experiment-6---question-5-edit-distance-between-answers)
- [Experiment 6 - Question 6: Fastest Walking Path Through City Blocks](#experiment-6---question-6-fastest-walking-path-through-city-blocks)
- [Experiment 6 - Question 7: Text Similarity by Alignment](#experiment-6---question-7-text-similarity-by-alignment)
- [Experiment 6 - Question 8: Warehouse Robot Minimum Cost Path](#experiment-6---question-8-warehouse-robot-minimum-cost-path)
- [Experiment 6 - Question 9: Protein Folding Energy (Matrix Chain analogy)](#experiment-6---question-9-protein-folding-energy-matrix-chain-analogy)
- [Experiment 6 - Question 10: Game AI Minimum Risk Path](#experiment-6---question-10-game-ai-minimum-risk-path)

---

## Experiment 6 - Question 1: Fitness Band Heart Rate Analysis

Scenario: A fitness band records the heart rate every minute for 10 minutes.
Analyse this data.

Note: the question sheet repeats this scenario from Experiment 5 Question 1.
This version answers the same rubrics using the statistics module and a
10-minute session stored as a list of (minute, bpm) pairs, so the two
submissions are not identical code.

Rubrics covered:
  * random heart rate data generated
  * first 5 minutes indexed
  * min, max and average computed
  * high heart rate values (above 120 bpm) filtered

**File:** [`q1_heart_rate_analysis.py`](q1_heart_rate_analysis.py) &nbsp;&middot;&nbsp; **Run:** `python q1_heart_rate_analysis.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 6 - Question 1: Fitness Band Heart Rate Analysis

Scenario: A fitness band records the heart rate every minute for 10 minutes.
Analyse this data.

Note: the question sheet repeats this scenario from Experiment 5 Question 1.
This version answers the same rubrics using the statistics module and a
10-minute session stored as a list of (minute, bpm) pairs, so the two
submissions are not identical code.

Rubrics covered:
  * random heart rate data generated
  * first 5 minutes indexed
  * min, max and average computed
  * high heart rate values (above 120 bpm) filtered
"""

import random
import statistics

MINUTES = 10
HIGH_BPM = 120
RESTING = 68


def generate_session(seed=52):
    """Returns a list of (minute, bpm) tuples for a 10-minute workout."""
    random.seed(seed)
    profile = [0.05, 0.18, 0.42, 0.68, 0.86, 1.00, 0.95, 0.72, 0.44, 0.22]
    peak_extra = 80                       # bpm added at full effort
    return [(minute + 1, int(RESTING + peak_extra * factor + random.gauss(0, 4)))
            for minute, factor in enumerate(profile)]


def effort_label(bpm):
    if bpm > HIGH_BPM:
        return "HIGH"
    if bpm > 100:
        return "moderate"
    if bpm > 80:
        return "light"
    return "resting"


if __name__ == "__main__":
    session = generate_session()
    bpm_values = [bpm for _, bpm in session]

    print("=== session log ===")
    print(f"  {'minute':<8}{'bpm':>6}{'zone':>12}   trace")
    for minute, bpm in session:
        print(f"  {minute:<8}{bpm:>6}{effort_label(bpm):>12}   "
              f"{'*' * ((bpm - 60) // 3)}")

    print("\n=== indexing ===")
    first_five = session[:5]
    second_five = session[5:]
    print(f"  first 5 minutes  : {[b for _, b in first_five]}")
    print(f"  last 5 minutes   : {[b for _, b in second_five]}")
    print(f"  minute 1         : {session[0][1]} bpm")
    print(f"  minute 6 (peak)  : {session[5][1]} bpm")
    print(f"  final minute     : {session[-1][1]} bpm")
    print(f"  first-half avg   : "
          f"{statistics.mean(b for _, b in first_five):.2f} bpm")
    print(f"  second-half avg  : "
          f"{statistics.mean(b for _, b in second_five):.2f} bpm")

    print("\n=== statistics (statistics module) ===")
    print(f"  readings            : {len(bpm_values)}")
    print(f"  minimum             : {min(bpm_values)} bpm "
          f"(minute {bpm_values.index(min(bpm_values)) + 1})")
    print(f"  maximum             : {max(bpm_values)} bpm "
          f"(minute {bpm_values.index(max(bpm_values)) + 1})")
    print(f"  mean                : {statistics.mean(bpm_values):.2f} bpm")
    print(f"  median              : {statistics.median(bpm_values):.1f} bpm")
    print(f"  standard deviation  : {statistics.stdev(bpm_values):.2f} bpm")
    print(f"  spread              : {max(bpm_values) - min(bpm_values)} bpm")

    high = [(m, b) for m, b in session if b > HIGH_BPM]
    print(f"\n=== high heart rate filter (above {HIGH_BPM} bpm) ===")
    if high:
        for minute, bpm in high:
            print(f"  minute {minute:>2}: {bpm} bpm  "
                  f"({bpm - HIGH_BPM:+} over the threshold)")
        print(f"\n  minutes in the high zone : {len(high)}/{MINUTES} "
              f"({len(high) / MINUTES * 100:.0f}%)")
        print(f"  average while high       : "
              f"{statistics.mean(b for _, b in high):.1f} bpm")
        print(f"  peak effort              : {max(b for _, b in high)} bpm")
    else:
        print("  no reading crossed the threshold")

    print("\n=== calorie estimate (rough, 20-year-old, 65 kg) ===")
    # Keytel formula, simplified for a one-minute step
    kcal = sum((-55.0969 + 0.6309 * b + 0.1988 * 65 + 0.2017 * 20) / 4.184
               for _, b in session)
    print(f"  approximately {kcal:.1f} kcal burned in {MINUTES} minutes")

    print("\n=== recovery ===")
    drop = max(bpm_values) - bpm_values[-1]
    print(f"  peak {max(bpm_values)} -> final {bpm_values[-1]} bpm "
          f"(down {drop} bpm)")
    print("  recovery rating:", "excellent" if drop >= 40 else
          "good" if drop >= 25 else "take a longer cool-down")
```

</details>

<details>
<summary>Program output</summary>

```text
=== session log ===
  minute     bpm        zone   trace
  1           73     resting   ****
  2           82       light   *******
  3          100       light   *************
  4          117    moderate   *******************
  5          140        HIGH   **************************
  6          146        HIGH   ****************************
  7          146        HIGH   ****************************
  8          124        HIGH   *********************
  9          107    moderate   ***************
  10          85       light   ********

=== indexing ===
  first 5 minutes  : [73, 82, 100, 117, 140]
  last 5 minutes   : [146, 146, 124, 107, 85]
  minute 1         : 73 bpm
  minute 6 (peak)  : 146 bpm
  final minute     : 85 bpm
  first-half avg   : 102.40 bpm
  second-half avg  : 121.60 bpm

=== statistics (statistics module) ===
  readings            : 10
  minimum             : 73 bpm (minute 1)
  maximum             : 146 bpm (minute 6)
  mean                : 112.00 bpm
  median              : 112.0 bpm
  standard deviation  : 27.05 bpm
  spread              : 73 bpm

=== high heart rate filter (above 120 bpm) ===
  minute  5: 140 bpm  (+20 over the threshold)
  minute  6: 146 bpm  (+26 over the threshold)
  minute  7: 146 bpm  (+26 over the threshold)
  minute  8: 124 bpm  (+4 over the threshold)

  minutes in the high zone : 4/10 (40%)
  average while high       : 139.0 bpm
  peak effort              : 146 bpm

=== calorie estimate (rough, 20-year-old, 65 kg) ===
  approximately 77.7 kcal burned in 10 minutes

=== recovery ===
  peak 146 -> final 85 bpm (down 61 bpm)
  recovery rating: excellent

```

</details>

---

## Experiment 6 - Question 2: Shortest Delivery Time Across Routes

Scenario: A delivery app calculates the shortest delivery time across multiple
routes between warehouses and customers.

Rubrics covered:
  * 2D matrix of travel times between points generated
  * diagonal, row-wise and column-wise paths extracted
  * minimum path time computed using DP
  * different routes compared with a bottom-up approach

**File:** [`q2_delivery_time_matrix.py`](q2_delivery_time_matrix.py) &nbsp;&middot;&nbsp; **Run:** `python q2_delivery_time_matrix.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== travel time matrix (minutes) ===
            W1    H1    H2    H3    H4    C1
  W1        19     9    21    10    29    14
  H1        13    14    29    26     4    19
  H2        15    15     6    16    18    14
  H3         9    14    24     4    20    26
  H4         6    24     9    14     4    17
  C1        29     8     8    27    16    13

=== extracting paths from the matrix ===
  main diagonal      : [19, 14, 6, 4, 4, 13]  total 60 min
  anti-diagonal      : [14, 4, 16, 24, 24, 29]  total 111 min

  row-wise routes (one hub handles the whole leg):
    row W1   [19, 9, 21, 10, 29, 14]  total 102 min  avg  17.0
    row H1   [13, 14, 29, 26, 4, 19]  total 105 min  avg  17.5
    row H2   [15, 15, 6, 16, 18, 14]  total  84 min  avg  14.0
    row H3   [9, 14, 24, 4, 20, 26]  total  97 min  avg  16.2
    row H4   [6, 24, 9, 14, 4, 17]  total  74 min  avg  12.3
    row C1   [29, 8, 8, 27, 16, 13]  total 101 min  avg  16.8
    fastest row  : H4 (74 min)

  column-wise routes:
    col W1   [19, 13, 15, 9, 6, 29]  total  91 min
    col H1   [9, 14, 15, 14, 24, 8]  total  84 min
    col H2   [21, 29, 6, 24, 9, 8]  total  97 min
    col H3   [10, 26, 16, 4, 14, 27]  total  97 min
    col H4   [29, 4, 18, 20, 4, 16]  total  91 min
    col C1   [14, 19, 14, 26, 17, 13]  total 103 min
    fastest column: H1 (84 min)

=== minimum delivery time, right/down moves only (bottom-up DP) ===
  shortest total time : 130 minutes
  cells visited       : 11
  route               : (W1,W1) -> (W1,H1) -> (H1,H1) -> (H2,H1) -> (H2,H2) -> (H2,H3) -> (H3,H3) -> (H4,H3) -> (H4,H4) -> (C1,H4) -> (C1,C1)
  leg times           : [19, 9, 14, 15, 6, 16, 4, 14, 4, 16, 13]

=== the DP table (cheapest time to reach each cell) ===
            W1    H1    H2    H3    H4    C1
  W1       19*   28*   49    59    88   102 
  H1       32    42*   71    85    89   108 
  H2       47    57*   63*   79*   97   111 
  H3       56    70    87    83*  103   129 
  H4       62    86    95    97*  101*  118 
  C1       91    94   102   124   117*  130*
  (* marks the chosen route)

=== comparing route policies ===
  right/down only            : 130 minutes
  right/down/diagonal        : 60 minutes (70 min faster)
  naive main-diagonal route  : 60 minutes
  best single row            : 74 minutes
  DP beats the naive diagonal by -70 minutes (-116.7% quicker)

=== promised delivery window ===
  optimal route 130 min + 10 min handling = 140 min promise to the customer

```

</details>

---

## Experiment 6 - Question 3: Video Effect Merge Order (Matrix Chain Multiplication)

Scenario: A video editing app merges multiple video effects that have different
processing costs. Optimise the order of merging.

Rubrics covered:
  * list of video segments with render costs generated
  * multiplication cost defined between effects
  * optimal parenthesis placement logic applied
  * minimum processing time tracked in a DP table

**File:** [`q3_video_effects_matrix_chain.py`](q3_video_effects_matrix_chain.py) &nbsp;&middot;&nbsp; **Run:** `python q3_video_effects_matrix_chain.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== effect chain ===
  dimension vector: [15, 25, 25, 40, 5, 15, 10]
  #   effect               shape    render units
  0   ColorGrade           15x25             375
  1   Denoise              25x25             625
  2   Stabilise            25x40           1,000
  3   Sharpen               40x5             200
  4   Bloom                 5x15              75
  5   Grain                15x10             150

=== DP cost table (minimum units to merge effects i..j) ===
          ColorGr  Denoise  Stabili  Sharpen    Bloom    Grain
  ColorGr        0    9,375   24,375   10,000   11,125   11,500
  Denoise        -        0   25,000    8,125   10,000   10,125
  Stabili        -        -        0    5,000    6,875    7,000
  Sharpen        -        -        -        0    3,000    2,750
  Bloom          -        -        -        -        0      750
  Grain          -        -        -        -        -        0

=== split table (where the best parenthesis goes) ===
          ColorGr  Denoise  Stabili  Sharpen    Bloom    Grain
  ColorGr        -  ColorGr  Denoise  ColorGr  Sharpen  Sharpen
  Denoise        -        -  Denoise  Denoise  Sharpen  Sharpen
  Stabili        -        -        -  Stabili  Sharpen  Sharpen
  Sharpen        -        -        -        -  Sharpen  Sharpen
  Bloom          -        -        -        -        -    Bloom
  Grain          -        -        -        -        -        -

=== optimal merge plan ===
  minimum render cost : 11,500 units
  parenthesisation    : ((ColorGrade x (Denoise x (Stabilise x Sharpen))) x (Bloom x Grain))

=== merge sequence, innermost first ===
  step 1: merge [Stabilise] with [Sharpen] -> 5,000 units
  step 2: merge [Denoise] with [Stabilise..Sharpen] -> 3,125 units
  step 3: merge [ColorGrade] with [Denoise..Sharpen] -> 1,875 units
  step 4: merge [Bloom] with [Grain] -> 750 units
  step 5: merge [ColorGrade..Sharpen] with [Bloom..Grain] -> 750 units

=== comparison with naive orders ===
  optimal (DP)        : 11,500 units
  left-to-right merge : 30,750 units (2.67x the optimum)
  right-to-left merge : 22,750 units (1.98x the optimum)
  saved by reordering : 19,250 units (62.6% less rendering)

=== render time estimate at 2,000 units per second ===
  optimal              5.75 s
  left-to-right       15.38 s

=== cost of every possible first split ===
  split after ColorGrade   ->     13,875 units
  split after Denoise      ->     20,125 units
  split after Stabilise    ->     33,125 units
  split after Sharpen      ->     11,500 units  <- chosen
  split after Bloom        ->     13,375 units

```

</details>

---

## Experiment 6 - Question 4: DNA Sequence Alignment

Scenario: A genetics tool compares two DNA sequences to identify mutations.

Rubrics covered:
  * two random DNA strings generated (A, T, G, C)
  * alignment score computed using gap penalties
  * insertions, deletions and substitutions tracked
  * scores stored in a 2D matrix using tabulation

**File:** [`q4_dna_sequence_alignment.py`](q4_dna_sequence_alignment.py) &nbsp;&middot;&nbsp; **Run:** `python q4_dna_sequence_alignment.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 6 - Question 4: DNA Sequence Alignment

Scenario: A genetics tool compares two DNA sequences to identify mutations.

Rubrics covered:
  * two random DNA strings generated (A, T, G, C)
  * alignment score computed using gap penalties
  * insertions, deletions and substitutions tracked
  * scores stored in a 2D matrix using tabulation
"""

import random

BASES = "ATGC"
MATCH = 2
MISMATCH = -1
GAP = -2


def generate_dna(length, seed=None):
    if seed is not None:
        random.seed(seed)
    return "".join(random.choice(BASES) for _ in range(length))


def mutate(seq, n_mutations=5, seed=88):
    """Produce a related sequence with substitutions, insertions, deletions."""
    random.seed(seed)
    out = list(seq)
    for _ in range(n_mutations):
        kind = random.choice(["sub", "ins", "del"])
        if not out:
            break
        pos = random.randrange(len(out))
        if kind == "sub":
            out[pos] = random.choice(BASES.replace(out[pos], ""))
        elif kind == "ins":
            out.insert(pos, random.choice(BASES))
        else:
            out.pop(pos)
    return "".join(out)


def needleman_wunsch(a, b, match=MATCH, mismatch=MISMATCH, gap=GAP):
    """Global alignment by tabulation.
    score[i][j] = best score aligning a[:i] with b[:j]."""
    n, m = len(a), len(b)
    score = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        score[i][0] = score[i - 1][0] + gap
    for j in range(1, m + 1):
        score[0][j] = score[0][j - 1] + gap

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            diag = score[i - 1][j - 1] + (match if a[i - 1] == b[j - 1]
                                          else mismatch)
            up = score[i - 1][j] + gap          # deletion from a
            left = score[i][j - 1] + gap        # insertion into a
            score[i][j] = max(diag, up, left)

    # traceback
    align_a, align_b, ops = [], [], []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            diag = score[i - 1][j - 1] + (match if a[i - 1] == b[j - 1]
                                          else mismatch)
        else:
            diag = None
        if i > 0 and j > 0 and score[i][j] == diag:
            align_a.append(a[i - 1])
            align_b.append(b[j - 1])
            ops.append("match" if a[i - 1] == b[j - 1] else "substitution")
            i -= 1
            j -= 1
        elif i > 0 and score[i][j] == score[i - 1][j] + gap:
            align_a.append(a[i - 1])
            align_b.append("-")
            ops.append("deletion")
            i -= 1
        else:
            align_a.append("-")
            align_b.append(b[j - 1])
            ops.append("insertion")
            j -= 1

    return (score[n][m], "".join(reversed(align_a)), "".join(reversed(align_b)),
            list(reversed(ops)), score)


if __name__ == "__main__":
    seq_a = generate_dna(18, seed=77)
    seq_b = mutate(seq_a, n_mutations=6)

    print("=== input sequences ===")
    print(f"  reference (A): {seq_a}   length {len(seq_a)}")
    print(f"  sample    (B): {seq_b}   length {len(seq_b)}")
    print(f"  scoring: match {MATCH:+}, mismatch {MISMATCH:+}, gap {GAP:+}")

    score, a_aligned, b_aligned, ops, table = needleman_wunsch(seq_a, seq_b)

    print("\n=== alignment ===")
    markers = "".join("|" if x == y else ("." if "-" not in (x, y) else " ")
                      for x, y in zip(a_aligned, b_aligned))
    print(f"  A : {a_aligned}")
    print(f"      {markers}")
    print(f"  B : {b_aligned}")
    print("  (| identical, . substitution, blank gap)")
    print(f"\n  optimal alignment score: {score}")

    counts = {k: ops.count(k) for k in
              ("match", "substitution", "insertion", "deletion")}
    print("\n=== mutation report ===")
    for kind, count in counts.items():
        print(f"  {kind:<14} {count}")
    identity = counts["match"] / len(a_aligned) * 100
    print(f"  alignment length : {len(a_aligned)}")
    print(f"  identity         : {identity:.1f}%")

    print("\n=== position-by-position operations ===")
    for pos, (x, y, op) in enumerate(zip(a_aligned, b_aligned, ops), 1):
        if op != "match":
            print(f"  position {pos:>2}: {x} -> {y}   {op}")

    print("\n=== DP score matrix (tabulation) ===")
    header = "       -  " + "  ".join(f"{c}" for c in seq_b)
    print("   " + header)
    for i, row in enumerate(table):
        label = "-" if i == 0 else seq_a[i - 1]
        print(f"   {label}  " + "".join(f"{v:>4}" for v in row))

    print("\n=== effect of the gap penalty ===")
    print(f"  {'gap penalty':<14}{'score':>8}{'gaps opened':>14}")
    for g in (-1, -2, -4, -8):
        s, aa, bb, o, _ = needleman_wunsch(seq_a, seq_b, gap=g)
        gaps = o.count("insertion") + o.count("deletion")
        print(f"  {g:<14}{s:>8}{gaps:>14}")
    print("  a harsher gap penalty forces substitutions instead of gaps")

    print("\n=== identical sequences sanity check ===")
    s_same, _, _, ops_same, _ = needleman_wunsch(seq_a, seq_a)
    print(f"  aligning A with itself: score {s_same} "
          f"(= {MATCH} x {len(seq_a)} bases), "
          f"mismatches {ops_same.count('substitution')}")
```

</details>

<details>
<summary>Program output</summary>

```text
=== input sequences ===
  reference (A): GGTTTAGCTTAGACTTCT   length 18
  sample    (B): GTTCATGCTTAGACTTTCT   length 19
  scoring: match +2, mismatch -1, gap -2

=== alignment ===
  A : GGTTTA-GCTTAGAC-TTCT
       |||.| |||||||| ||||
  B : -GTTCATGCTTAGACTTTCT
  (| identical, . substitution, blank gap)

  optimal alignment score: 25

=== mutation report ===
  match          16
  substitution   1
  insertion      2
  deletion       1
  alignment length : 20
  identity         : 80.0%

=== position-by-position operations ===
  position  1: G -> -   deletion
  position  5: T -> C   substitution
  position  7: - -> T   insertion
  position 16: - -> T   insertion

=== DP score matrix (tabulation) ===
          -  G  T  T  C  A  T  G  C  T  T  A  G  A  C  T  T  T  C  T
   -     0  -2  -4  -6  -8 -10 -12 -14 -16 -18 -20 -22 -24 -26 -28 -30 -32 -34 -36 -38
   G    -2   2   0  -2  -4  -6  -8 -10 -12 -14 -16 -18 -20 -22 -24 -26 -28 -30 -32 -34
   G    -4   0   1  -1  -3  -5  -7  -6  -8 -10 -12 -14 -16 -18 -20 -22 -24 -26 -28 -30
   T    -6  -2   2   3   1  -1  -3  -5  -7  -6  -8 -10 -12 -14 -16 -18 -20 -22 -24 -26
   T    -8  -4   0   4   2   0   1  -1  -3  -5  -4  -6  -8 -10 -12 -14 -16 -18 -20 -22
   T   -10  -6  -2   2   3   1   2   0  -2  -1  -3  -5  -7  -9 -11 -10 -12 -14 -16 -18
   A   -12  -8  -4   0   1   5   3   1  -1  -3  -2  -1  -3  -5  -7  -9 -11 -13 -15 -17
   G   -14 -10  -6  -2  -1   3   4   5   3   1  -1  -3   1  -1  -3  -5  -7  -9 -11 -13
   C   -16 -12  -8  -4   0   1   2   3   7   5   3   1  -1   0   1  -1  -3  -5  -7  -9
   T   -18 -14 -10  -6  -2  -1   3   1   5   9   7   5   3   1  -1   3   1  -1  -3  -5
   T   -20 -16 -12  -8  -4  -3   1   2   3   7  11   9   7   5   3   1   5   3   1  -1
   A   -22 -18 -14 -10  -6  -2  -1   0   1   5   9  13  11   9   7   5   3   4   2   0
   G   -24 -20 -16 -12  -8  -4  -3   1  -1   3   7  11  15  13  11   9   7   5   3   1
   A   -26 -22 -18 -14 -10  -6  -5  -1   0   1   5   9  13  17  15  13  11   9   7   5
   C   -28 -24 -20 -16 -12  -8  -7  -3   1  -1   3   7  11  15  19  17  15  13  11   9
   T   -30 -26 -22 -18 -14 -10  -6  -5  -1   3   1   5   9  13  17  21  19  17  15  13
   T   -32 -28 -24 -20 -16 -12  -8  -7  -3   1   5   3   7  11  15  19  23  21  19  17
   C   -34 -30 -26 -22 -18 -14 -10  -9  -5  -1   3   4   5   9  13  17  21  22  23  21
   T   -36 -32 -28 -24 -20 -16 -12 -11  -7  -3   1   2   3   7  11  15  19  23  21  25

=== effect of the gap penalty ===
  gap penalty      score   gaps opened
  -1                  28             3
  -2                  25             3
  -4                  20             1
  -8                  16             1
  a harsher gap penalty forces substitutions instead of gaps

=== identical sequences sanity check ===
  aligning A with itself: score 36 (= 2 x 18 bases), mismatches 0

```

</details>

---

## Experiment 6 - Question 5: Edit Distance Between Answers

Scenario: An e-learning platform aligns students' answers to the correct
solutions to detect how far off their responses were.

Rubrics covered:
  * two lists generated: student answers and correct answers
  * sequences aligned using edit operations (insert / delete / replace)
  * minimum edit distance calculated
  * visualised with a DP matrix

**File:** [`q5_edit_distance_answers.py`](q5_edit_distance_answers.py) &nbsp;&middot;&nbsp; **Run:** `python q5_edit_distance_answers.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 6 - Question 5: Edit Distance Between Answers

Scenario: An e-learning platform aligns students' answers to the correct
solutions to detect how far off their responses were.

Rubrics covered:
  * two lists generated: student answers and correct answers
  * sequences aligned using edit operations (insert / delete / replace)
  * minimum edit distance calculated
  * visualised with a DP matrix
"""


CORRECT = ["list", "tuple", "set", "dict", "string", "int", "float"]
STUDENT = ["list", "set", "dictionary", "tuple", "string", "complex"]


def edit_distance(a, b):
    """dp[i][j] = minimum operations to turn a[:i] into b[:j]."""
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i                       # delete everything
    for j in range(m + 1):
        dp[0][j] = j                       # insert everything

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],      # delete
                                   dp[i][j - 1],      # insert
                                   dp[i - 1][j - 1])  # replace
    return dp[n][m], dp


def traceback(a, b, dp):
    """Recover the operation list from the finished table."""
    ops = []
    i, j = len(a), len(b)
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i - 1] == b[j - 1] and dp[i][j] == dp[i - 1][j - 1]:
            ops.append(("keep", a[i - 1], b[j - 1], i, j))
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            ops.append(("replace", a[i - 1], b[j - 1], i, j))
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            ops.append(("delete", a[i - 1], "-", i, j))
            i -= 1
        else:
            ops.append(("insert", "-", b[j - 1], i, j))
            j -= 1
    return list(reversed(ops))


def print_matrix(a, b, dp, label):
    print(f"\n=== {label} ===")
    width = max(len(str(x)) for x in list(a) + list(b) + [""]) + 1
    width = max(width, 5)
    print(" " * (width + 4) + "".join(f"{str(x)[:width]:>{width + 1}}"
                                      for x in ["-"] + list(b)))
    for i, row in enumerate(dp):
        label_i = "-" if i == 0 else str(a[i - 1])[:width]
        print(f"  {label_i:>{width + 1}}  " +
              "".join(f"{v:>{width + 1}}" for v in row))


if __name__ == "__main__":
    print("=== answer sheets ===")
    print(f"  correct answers ({len(CORRECT)}): {CORRECT}")
    print(f"  student answers ({len(STUDENT)}): {STUDENT}")

    distance, dp = edit_distance(STUDENT, CORRECT)
    print(f"\n=== minimum edit distance = {distance} operation(s) ===")
    print(f"  the student's list is {distance} edits away from the key")
    max_len = max(len(STUDENT), len(CORRECT))
    print(f"  similarity: {(1 - distance / max_len) * 100:.1f}%")

    print_matrix(STUDENT, CORRECT, dp, "DP table (rows = student, cols = key)")

    ops = traceback(STUDENT, CORRECT, dp)
    print("\n=== alignment of the two answer lists ===")
    print(f"  {'student':<14}{'key':<14}operation")
    print("  " + "-" * 40)
    for kind, s, c, _, _ in ops:
        print(f"  {str(s):<14}{str(c):<14}{kind}")

    counts = {k: sum(1 for o in ops if o[0] == k)
              for k in ("keep", "replace", "insert", "delete")}
    print("\n=== operation summary ===")
    for kind, count in counts.items():
        print(f"  {kind:<10} {count}")

    print("\n=== feedback for the student ===")
    for kind, s, c, _, _ in ops:
        if kind == "replace":
            print(f"  you wrote '{s}' where '{c}' was expected")
        elif kind == "insert":
            print(f"  you missed '{c}' entirely")
        elif kind == "delete":
            print(f"  '{s}' is not part of the answer key")
    score = counts["keep"] / len(CORRECT) * 100
    print(f"\n  marks: {counts['keep']}/{len(CORRECT)} correct ({score:.1f}%)")

    print("\n=== character-level distance on single answers ===")
    pairs = [("dictionary", "dict"), ("complex", "float"),
             ("tuple", "tuple"), ("stirng", "string")]
    for typed, expected in pairs:
        d, _ = edit_distance(typed, expected)
        verdict = ("exact" if d == 0 else
                   "likely a typo" if d <= 2 else "wrong answer")
        print(f"  {typed:<12} vs {expected:<10} distance {d}  {verdict}")

    print("\n=== spelling-tolerant regrade ===")
    tolerant = 0
    for answer in STUDENT:
        best = min((edit_distance(answer, key)[0], key) for key in CORRECT)
        if best[0] <= 2:
            tolerant += 1
            print(f"  '{answer}' accepted as '{best[1]}' (distance {best[0]})")
    print(f"  tolerant score: {tolerant}/{len(CORRECT)} "
          f"({tolerant / len(CORRECT) * 100:.1f}%)")
```

</details>

<details>
<summary>Program output</summary>

```text
=== answer sheets ===
  correct answers (7): ['list', 'tuple', 'set', 'dict', 'string', 'int', 'float']
  student answers (6): ['list', 'set', 'dictionary', 'tuple', 'string', 'complex']

=== minimum edit distance = 5 operation(s) ===
  the student's list is 5 edits away from the key
  similarity: 28.6%

=== DP table (rows = student, cols = key) ===
                          -        list       tuple         set        dict      string         int       float
             -             0           1           2           3           4           5           6           7
          list             1           0           1           2           3           4           5           6
           set             2           1           1           1           2           3           4           5
    dictionary             3           2           2           2           2           3           4           5
         tuple             4           3           2           3           3           3           4           5
        string             5           4           3           3           4           3           4           5
       complex             6           5           4           4           4           4           4           5

=== alignment of the two answer lists ===
  student       key           operation
  ----------------------------------------
  list          list          keep
  -             tuple         insert
  set           set           keep
  dictionary    dict          replace
  tuple         string        replace
  string        int           replace
  complex       float         replace

=== operation summary ===
  keep       2
  replace    4
  insert     1
  delete     0

=== feedback for the student ===
  you missed 'tuple' entirely
  you wrote 'dictionary' where 'dict' was expected
  you wrote 'tuple' where 'string' was expected
  you wrote 'string' where 'int' was expected
  you wrote 'complex' where 'float' was expected

  marks: 2/7 correct (28.6%)

=== character-level distance on single answers ===
  dictionary   vs dict       distance 6  wrong answer
  complex      vs float      distance 7  wrong answer
  tuple        vs tuple      distance 0  exact
  stirng       vs string     distance 2  likely a typo

=== spelling-tolerant regrade ===
  'list' accepted as 'list' (distance 0)
  'set' accepted as 'set' (distance 0)
  'tuple' accepted as 'tuple' (distance 0)
  'string' accepted as 'string' (distance 0)
  tolerant score: 4/7 (57.1%)

```

</details>

---

## Experiment 6 - Question 6: Fastest Walking Path Through City Blocks

Scenario: A navigation app calculates the fastest walking path through a grid
of city blocks, allowing for blocked paths and delays.

Rubrics covered:
  * 2D grid generated with random weights (walking times)
  * shortest path found with bottom-up DP
  * blocked or delayed paths marked
  * optimal total time and the path indices returned

**File:** [`q6_navigation_grid_path.py`](q6_navigation_grid_path.py) &nbsp;&middot;&nbsp; **Run:** `python q6_navigation_grid_path.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== walking time per block (minutes) ===
            0     1     2     3     4     5     6     7
  r0       10     6    12     6     4     2    15     4
  r1       15    15   XXX     6     5     4     3     6
  r2        6     2     4     6     2     1     1     4
  r3       10   XXX     4     3     3     5     4     3
  r4        5     2     4     1     2     6     3    13
  r5        2     4   XXX     3     2   XXX     4   XXX
  r6        3    11   XXX     6     2     4     2     3
  XXX = blocked, [n] = chosen path

  blocked blocks (6): [(1, 2), (3, 1), (5, 2), (5, 5), (5, 7), (6, 2)]
  delayed blocks (8): [(0, 0), (0, 2), (0, 6), (1, 0), (1, 1), (3, 0), (4, 7), (6, 1)]

=== bottom-up DP, right and down moves only ===
  fastest total time : 60 minutes
  blocks crossed     : 14
  path indices       : [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2), (3, 2), (3, 3), (4, 3), (4, 4), (5, 4), (6, 4), (6, 5), (6, 6), (6, 7)]
  per-block times    : [10, 6, 15, 2, 4, 4, 3, 1, 2, 2, 2, 4, 2, 3]

=== DP table (fastest time to reach each block) ===
             0      1      2      3      4      5      6      7
  r0        10     16     28     34     38     40     55     59
  r1        25     31    inf     40     43     44     47     53
  r2        31     33     37     43     45     45     46     50
  r3        41    inf     41     44     47     50     50     53
  r4        46     48     45     45     47     53     53     66
  r5        48     52    inf     48     49    inf     57    inf
  r6        51     62    inf     54     51     55     57     60

=== chosen route ===
            0     1     2     3     4     5     6     7
  r0     [10]   [6]    12     6     4     2    15     4
  r1       15  [15]   XXX     6     5     4     3     6
  r2        6   [2]   [4]     6     2     1     1     4
  r3       10   XXX   [4]   [3]     3     5     4     3
  r4        5     2     4   [1]   [2]     6     3    13
  r5        2     4   XXX     3   [2]   XXX     4   XXX
  r6        3    11   XXX     6   [2]   [4]   [2]   [3]
  XXX = blocked, [n] = chosen path

=== allowing all four directions (Dijkstra) ===
  fastest time       : 60 minutes
  blocks crossed     : 14
  path indices       : [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2), (3, 2), (3, 3), (4, 3), (4, 4), (5, 4), (6, 4), (6, 5), (6, 6), (6, 7)]
  detouring upward/leftward saves 0 minute(s)

=== why the restriction matters ===
  Right/down only gives a clean O(rows*cols) DP because the
  subproblems have no cycles. Allowing up/left creates cycles,
  so the same grid then needs Dijkstra instead of tabulation.

```

</details>

---

## Experiment 6 - Question 7: Text Similarity by Alignment

Scenario: A text comparison tool aligns two paragraphs to measure similarity.

Rubrics covered:
  * paragraphs converted into word / token sequences
  * DP used to compute the longest common subsequence
  * a similarity score generated
  * unmatched tokens filtered out

**File:** [`q7_text_similarity_lcs.py`](q7_text_similarity_lcs.py) &nbsp;&middot;&nbsp; **Run:** `python q7_text_similarity_lcs.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 6 - Question 7: Text Similarity by Alignment

Scenario: A text comparison tool aligns two paragraphs to measure similarity.

Rubrics covered:
  * paragraphs converted into word / token sequences
  * DP used to compute the longest common subsequence
  * a similarity score generated
  * unmatched tokens filtered out
"""

import re

PARA_A = """Python is a high level programming language. It supports object
oriented programming and dynamic typing. Python is widely used for data
analysis and web development."""

PARA_B = """Python is a high level language for programming. It supports
dynamic typing and object oriented design. Python is widely used in data
science and in web development."""


def tokenise(text):
    """Lowercase word tokens, punctuation dropped."""
    return re.findall(r"[a-z0-9']+", text.lower())


def lcs_table(a, b):
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp


def lcs_sequence(a, b, dp):
    i, j, out = len(a), len(b), []
    while i and j:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return list(reversed(out))


def alignment(a, b, dp):
    """Returns a list of (token_a, token_b, status)."""
    i, j, rows = len(a), len(b), []
    while i or j:
        if i and j and a[i - 1] == b[j - 1]:
            rows.append((a[i - 1], b[j - 1], "match"))
            i -= 1
            j -= 1
        elif j and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
            rows.append(("-", b[j - 1], "only in B"))
            j -= 1
        else:
            rows.append((a[i - 1], "-", "only in A"))
            i -= 1
    return list(reversed(rows))


if __name__ == "__main__":
    tokens_a = tokenise(PARA_A)
    tokens_b = tokenise(PARA_B)

    print("=== paragraph A ===")
    print("  " + " ".join(PARA_A.split()))
    print(f"  {len(tokens_a)} tokens")
    print("\n=== paragraph B ===")
    print("  " + " ".join(PARA_B.split()))
    print(f"  {len(tokens_b)} tokens")

    print(f"\n  tokens A: {tokens_a}")
    print(f"  tokens B: {tokens_b}")

    dp = lcs_table(tokens_a, tokens_b)
    lcs = lcs_sequence(tokens_a, tokens_b, dp)
    length = dp[len(tokens_a)][len(tokens_b)]

    print(f"\n=== longest common subsequence: {length} tokens ===")
    print("  " + " ".join(lcs))

    print("\n=== similarity scores ===")
    lcs_ratio = 2 * length / (len(tokens_a) + len(tokens_b)) * 100
    containment_a = length / len(tokens_a) * 100
    containment_b = length / len(tokens_b) * 100
    set_a, set_b = set(tokens_a), set(tokens_b)
    jaccard = len(set_a & set_b) / len(set_a | set_b) * 100
    print(f"  LCS-based similarity (harmonic) : {lcs_ratio:.2f}%")
    print(f"  share of A matched              : {containment_a:.2f}%")
    print(f"  share of B matched              : {containment_b:.2f}%")
    print(f"  Jaccard on unique words         : {jaccard:.2f}%")
    print(f"  verdict                         : " +
          ("near-duplicate text" if lcs_ratio > 80 else
           "heavily reworded but same content" if lcs_ratio > 55 else
           "different content"))

    rows = alignment(tokens_a, tokens_b, dp)
    print("\n=== token alignment ===")
    print(f"  {'A':<16}{'B':<16}status")
    print("  " + "-" * 46)
    for ta, tb, status in rows:
        print(f"  {ta:<16}{tb:<16}{status}")

    only_a = [ta for ta, tb, s in rows if s == "only in A"]
    only_b = [tb for ta, tb, s in rows if s == "only in B"]
    print("\n=== unmatched tokens filtered out ===")
    print(f"  only in A ({len(only_a)}): {only_a}")
    print(f"  only in B ({len(only_b)}): {only_b}")
    print(f"  words unique to A: {sorted(set_a - set_b)}")
    print(f"  words unique to B: {sorted(set_b - set_a)}")
    print(f"  shared vocabulary: {len(set_a & set_b)} word(s)")

    print("\n=== DP table corner (last 8 x 8 cells) ===")
    tail_a = tokens_a[-7:]
    tail_b = tokens_b[-7:]
    print("              " + "".join(f"{t[:8]:>9}" for t in tail_b))
    for i, token in enumerate(tail_a):
        row_index = len(tokens_a) - len(tail_a) + i + 1
        values = dp[row_index][len(tokens_b) - len(tail_b) + 1:]
        print(f"  {token[:12]:<12}" + "".join(f"{v:>9}" for v in values))

    print("\n=== sentence-level similarity ===")
    sents_a = [s.strip() for s in PARA_A.replace("\n", " ").split(".") if s.strip()]
    sents_b = [s.strip() for s in PARA_B.replace("\n", " ").split(".") if s.strip()]
    for i, sa in enumerate(sents_a, 1):
        ta = tokenise(sa)
        best_score, best_j = 0.0, None
        for j, sb in enumerate(sents_b, 1):
            tb = tokenise(sb)
            d = lcs_table(ta, tb)
            score = 2 * d[len(ta)][len(tb)] / (len(ta) + len(tb)) * 100
            if score > best_score:
                best_score, best_j = score, j
        print(f"  A sentence {i} best matches B sentence {best_j} "
              f"at {best_score:.1f}%")
```

</details>

<details>
<summary>Program output</summary>

```text
=== paragraph A ===
  Python is a high level programming language. It supports object oriented programming and dynamic typing. Python is widely used for data analysis and web development.
  25 tokens

=== paragraph B ===
  Python is a high level language for programming. It supports dynamic typing and object oriented design. Python is widely used in data science and in web development.
  27 tokens

  tokens A: ['python', 'is', 'a', 'high', 'level', 'programming', 'language', 'it', 'supports', 'object', 'oriented', 'programming', 'and', 'dynamic', 'typing', 'python', 'is', 'widely', 'used', 'for', 'data', 'analysis', 'and', 'web', 'development']
  tokens B: ['python', 'is', 'a', 'high', 'level', 'language', 'for', 'programming', 'it', 'supports', 'dynamic', 'typing', 'and', 'object', 'oriented', 'design', 'python', 'is', 'widely', 'used', 'in', 'data', 'science', 'and', 'in', 'web', 'development']

=== longest common subsequence: 18 tokens ===
  python is a high level programming it supports object oriented python is widely used data and web development

=== similarity scores ===
  LCS-based similarity (harmonic) : 69.23%
  share of A matched              : 72.00%
  share of B matched              : 66.67%
  Jaccard on unique words         : 83.33%
  verdict                         : heavily reworded but same content

=== token alignment ===
  A               B               status
  ----------------------------------------------
  python          python          match
  is              is              match
  a               a               match
  high            high            match
  level           level           match
  programming     -               only in A
  language        language        match
  -               for             only in B
  -               programming     only in B
  it              it              match
  supports        supports        match
  object          -               only in A
  oriented        -               only in A
  programming     -               only in A
  and             -               only in A
  dynamic         dynamic         match
  typing          typing          match
  -               and             only in B
  -               object          only in B
  -               oriented        only in B
  -               design          only in B
  python          python          match
  is              is              match
  widely          widely          match
  used            used            match
  for             -               only in A
  -               in              only in B
  data            data            match
  analysis        -               only in A
  -               science         only in B
  and             and             match
  -               in              only in B
  web             web             match
  development     development     match

=== unmatched tokens filtered out ===
  only in A (7): ['programming', 'object', 'oriented', 'programming', 'and', 'for', 'analysis']
  only in B (9): ['for', 'programming', 'and', 'object', 'oriented', 'design', 'in', 'science', 'in']
  words unique to A: ['analysis']
  words unique to B: ['design', 'in', 'science']
  shared vocabulary: 20 word(s)

=== DP table corner (last 8 x 8 cells) ===
                     in     data  science      and       in      web developm
  used               14       14       14       14       14       14       14
  for                14       14       14       14       14       14       14
  data               14       15       15       15       15       15       15
  analysis           14       15       15       15       15       15       15
  and                14       15       15       16       16       16       16
  web                14       15       15       16       16       17       17
  development        14       15       15       16       16       17       18

=== sentence-level similarity ===
  A sentence 1 best matches B sentence 1 at 80.0%
  A sentence 2 best matches B sentence 2 at 50.0%
  A sentence 3 best matches B sentence 3 at 76.2%

```

</details>

---

## Experiment 6 - Question 8: Warehouse Robot Minimum Cost Path

Scenario: A robot in a warehouse moves from the top-left to the bottom-right
of a grid. Minimise the total travel cost based on terrain difficulty.

Rubrics covered:
  * 2D terrain cost matrix generated
  * the robot's movement path tracked
  * DP used to compute the minimum cost path
  * obstacles and high-cost cells highlighted

**File:** [`q8_warehouse_robot_min_cost.py`](q8_warehouse_robot_min_cost.py) &nbsp;&middot;&nbsp; **Run:** `python q8_warehouse_robot_min_cost.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== warehouse terrain cost map ===
           0    1    2    3    4    5    6    7
  r0       4    2    1    4    1    2   7!  ###
  r1       2    3   8!    4   9!    2  ###   7!
  r2       4    3    4    3  ###    2    3    4
  r3       1    1    1    1    3  ###    4    4
  r4       1   7!    3    2    2   8!   7!    4
  r5     ###    1    1    2    4    2   8!    1
  r6       4    3    1    4    2    3    3    3
  r7       3    4    4    4   8!    1   7!    2
  ### obstacle   n! high cost   [n] robot path

  obstacles (5): [(0, 7), (1, 6), (2, 4), (3, 5), (5, 0)]
  high-cost cells (10): [(0, 6), (1, 2), (1, 4), (1, 7), (4, 1), (4, 5), (4, 6), (5, 6), (7, 4), (7, 6)]
  passable cells: 59/64

=== minimum cost path (bottom-up DP) ===
  minimum total cost : 35
  cells traversed    : 15 (the shortest possible is 15)
  path               : [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3), (4, 3), (4, 4), (5, 4), (5, 5), (6, 5), (6, 6), (6, 7), (7, 7)]
  cost of each step  : [4, 2, 4, 1, 1, 1, 1, 2, 2, 4, 2, 3, 3, 3, 2]
  average cell cost  : 2.33
  high-cost cells used: 0

=== DP cost-to-reach table ===
            0     1     2     3     4     5     6     7
  r0        4     6     7    11    12    14    21   inf
  r1        6     9    15    15    21    16   inf   inf
  r2       10    12    16    18   inf    18    21    25
  r3       11    12    13    14    17   inf    25    29
  r4       12    19    16    16    18    26    32    33
  r5      inf    20    17    18    22    24    32    33
  r6      inf    23    18    22    24    27    30    33
  r7      inf    27    22    26    32    28    35    35

=== path highlighted on the terrain ===
           0    1    2    3    4    5    6    7
  r0     [4]    2    1    4    1    2   7!  ###
  r1     [2]    3   8!    4   9!    2  ###   7!
  r2     [4]    3    4    3  ###    2    3    4
  r3     [1]  [1]  [1]  [1]    3  ###    4    4
  r4       1   7!    3  [2]  [2]   8!   7!    4
  r5     ###    1    1    2  [4]  [2]   8!    1
  r6       4    3    1    4    2  [3]  [3]  [3]
  r7       3    4    4    4   8!    1   7!  [2]
  ### obstacle   n! high cost   [n] robot path

=== comparison with naive routes ===
  along the top then down the right edge     blocked by shelving
  down the left edge then along the bottom   blocked by shelving

=== battery estimate at 1.5 Wh per cost unit ===
  optimal route uses about 52.5 Wh
  a 60 Wh battery allows about 1.1 round trips

```

</details>

---

## Experiment 6 - Question 9: Protein Folding Energy (Matrix Chain analogy)

Scenario: A biomedical tool identifies the optimal way to fold proteins based
on energy costs.

Rubrics covered:
  * list of folding steps with transition costs generated
  * multiplication cost defined from energy levels
  * total folding energy minimised
  * step-by-step energy reduction tracked with DP

**File:** [`q9_protein_folding_chain.py`](q9_protein_folding_chain.py) &nbsp;&middot;&nbsp; **Run:** `python q9_protein_folding_chain.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== protein segments and interface energies ===
  interface vector: [4, 20, 24, 24, 20, 8, 4]
  #   segment          interface   self energy
  0   Helix-A               4-20            80
  1   Loop-1               20-24           480
  2   Sheet-B              24-24           576
  3   Turn-2               24-20           480
  4   Helix-C               20-8           160
  5   Coil-D                 8-4            32

=== DP energy table (minimum units to fold segments i..j) ===
               Helix-A    Loop-1   Sheet-B    Turn-2   Helix-C    Coil-D
  Helix-A            0     1,920     4,224     6,144     6,784     6,912
  Loop-1             -         0    11,520    21,120    12,288     6,784
  Sheet-B            -         -         0    11,520     8,448     4,864
  Turn-2             -         -         -         0     3,840     2,560
  Helix-C            -         -         -         -         0       640
  Coil-D             -         -         -         -         -         0

=== split table (which bond is formed last) ===
               Helix-A    Loop-1   Sheet-B    Turn-2   Helix-C    Coil-D
  Helix-A            -   Helix-A    Loop-1   Sheet-B    Turn-2   Helix-C
  Loop-1             -         -    Loop-1    Loop-1    Loop-1    Loop-1
  Sheet-B            -         -         -   Sheet-B   Sheet-B   Sheet-B
  Turn-2             -         -         -         -    Turn-2    Turn-2
  Helix-C            -         -         -         -         -   Helix-C
  Coil-D             -         -         -         -         -         -

=== optimal folding pathway ===
  minimum folding energy : 6,912 units
  grouping               : (((((Helix-A + Loop-1) + Sheet-B) + Turn-2) + Helix-C) + Coil-D)

=== step-by-step energy reduction ===
  step  fold                                    cost   cumulative
  1     Helix-A + Loop-1                       1,920        1,920
  2     Helix-..Loop-1 + Sheet-B               2,304        4,224
  3     Helix-..Sheet- + Turn-2                1,920        6,144
  4     Helix-..Turn-2 + Helix-C                 640        6,784
  5     Helix-..Helix- + Coil-D                  128        6,912
        TOTAL                                               6,912
  matches the DP answer: True

=== comparison with sequential folding ===
  optimal pathway    : 6,912 units
  N-to-C sequential  : 6,912 units
  energy saved       : 0 units (0.0% less)

=== energy per sub-chain length ===
  1 segment(s): cheapest        0   costliest        0
  2 segment(s): cheapest      640   costliest   11,520
  3 segment(s): cheapest    2,560   costliest   21,120
  4 segment(s): cheapest    4,864   costliest   12,288
  5 segment(s): cheapest    6,784   costliest    6,784
  6 segment(s): cheapest    6,912   costliest    6,912

=== stability note ===
  the fold with the lowest energy, 6,912 units, is the most
  stable conformation this model predicts. Real folding also
  depends on solvent and chaperones; this is the DP exercise only.

```

</details>

---

## Experiment 6 - Question 10: Game AI Minimum Risk Path

Scenario: A game AI plans movement across zones to reach a target with minimal
health loss.

Rubrics covered:
  * grid generated with risk values per cell
  * start and goal positions defined
  * path with the lowest cumulative risk computed
  * health drop visualised along the path

**File:** [`q10_game_ai_risk_path.py`](q10_game_ai_risk_path.py) &nbsp;&middot;&nbsp; **Run:** `python q10_game_ai_risk_path.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== risk map, start (0, 0) -> goal (7, 9) ===
           0    1    2    3    4    5    6    7    8    9
  r0       S   22    3   13    2    0    4    0    3    8
  r1       2    0    1    5    3    0    2    2    0   13
  r2      10    1    0    2   14    5    1    3   14    5
  r3       0    4   10    5   12    4    4    0    5   12
  r4       1   14    4    4   13    2    3    2    2    3
  r5      18    1    8   10    4   23   13    8    1   24
  r6       0    2    1   11    3    9    0    4    5    5
  r7       1   11    9    3   11    1    5   23    5    G
  S start   G goal   [n] chosen path   numbers = HP lost per zone

  boss zones (18+ risk): [(0, 1), (5, 0), (5, 5), (5, 9), (7, 7)]
  average zone risk    : 5.90 HP

=== right/down only (bottom-up DP) ===
  cumulative risk : 43 HP
  zones crossed   : 17
  path            : [(0, 0), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 6), (2, 7), (3, 7), (4, 7), (4, 8), (5, 8), (6, 8), (6, 9), (7, 9)]

=== all four directions (Dijkstra) ===
  cumulative risk : 43 HP
  zones crossed   : 17
  path            : [(0, 0), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 6), (2, 7), (3, 7), (4, 7), (4, 8), (5, 8), (6, 8), (6, 9), (7, 9)]
  detours save    : 0 HP

=== chosen route on the map ===
           0    1    2    3    4    5    6    7    8    9
  r0     [S]   22    3   13    2    0    4    0    3    8
  r1     [2]  [0]  [1]  [5]  [3]  [0]  [2]    2    0   13
  r2      10    1    0    2   14    5  [1]  [3]   14    5
  r3       0    4   10    5   12    4    4  [0]    5   12
  r4       1   14    4    4   13    2    3  [2]  [2]    3
  r5      18    1    8   10    4   23   13    8  [1]   24
  r6       0    2    1   11    3    9    0    4  [5]  [5]
  r7       1   11    9    3   11    1    5   23    5  [G]
  S start   G goal   [n] chosen path   numbers = HP lost per zone

=== health drop along the path ===
  step  zone        risk   HP left  health bar
  0     (0,0)          0       100  |################################# 
  1     (1,0)          2        98  |################################ 
  2     (1,1)          0        98  |################################ 
  3     (1,2)          1        97  |################################ 
  4     (1,3)          5        92  |############################## 
  5     (1,4)          3        89  |############################# 
  6     (1,5)          0        89  |############################# 
  7     (1,6)          2        87  |############################# 
  8     (2,6)          1        86  |############################ 
  9     (2,7)          3        83  |########################### 
  10    (3,7)          0        83  |########################### 
  11    (4,7)          2        81  |########################### 
  12    (4,8)          2        79  |########################## 
  13    (5,8)          1        78  |########################## 
  14    (6,8)          5        73  |######################## 
  15    (6,9)          5        68  |###################### 
  16    (7,9)         11        57  |################### 

  starting HP : 100
  total risk  : 43
  final HP    : 57
  survives    : True
  margin      : 57 HP (57% remaining)

=== DP table (minimum risk to reach each zone, right/down) ===
            0     1     2     3     4     5     6     7     8     9
  r0        0    22    25    38    40    40    44    44    47    55
  r1        2     2     3     8    11    11    13    15    15    28
  r2       12     3     3     5    19    16    14    17    29    33
  r3       12     7    13    10    22    20    18    17    22    34
  r4       13    21    17    14    27    22    21    19    21    24
  r5       31    22    25    24    28    45    34    27    22    46
  r6       31    24    25    35    31    40    34    31    27    32
  r7       32    35    34    37    42    41    39    54    32    43

=== comparison with a reckless straight-line run ===
  along the top then down the right edge: 128 HP
  optimal route                        : 43 HP
  the AI saves 85 HP by planning

```

</details>

---
