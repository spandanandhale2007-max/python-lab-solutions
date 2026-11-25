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
