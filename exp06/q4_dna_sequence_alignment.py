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
