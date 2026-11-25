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
