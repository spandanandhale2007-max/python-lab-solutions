"""
Experiment 11 - Question 4: Matrix Operations with Pandas

Scenario: Two 3x3 matrices represent transformations.

Task:
  1) Perform addition, subtraction and matrix multiplication between them.

Note: the sheet repeats Experiment 10 Question 4 here; this version uses
Pandas DataFrames, which is the topic of Experiment 11. It also shows where
Pandas aligns on labels and NumPy does not.

Rubrics covered:
  * DataFrame creation
  * element-wise operations
  * matrix multiplication (DataFrame.dot / @)
  * correct results

Requires: pandas, numpy
"""

import numpy as np
import pandas as pd

LABELS = ["r0", "r1", "r2"]
COLS = ["c0", "c1", "c2"]


def main():
    A = pd.DataFrame([[2, 0, 1],
                      [1, 3, 2],
                      [4, 1, 0]], index=LABELS, columns=COLS)

    B = pd.DataFrame([[1, 2, 0],
                      [0, 1, 3],
                      [2, 1, 1]], index=LABELS, columns=COLS)

    print("=== matrix A ===")
    print(A.to_string())
    print("\n=== matrix B ===")
    print(B.to_string())
    print(f"\n  shapes {A.shape} and {B.shape}, dtype {A.dtypes.iloc[0]}")

    print("\n=== 1) addition (element-wise, label aligned) ===")
    print((A + B).to_string())
    print(f"\n  A.add(B) gives the same: "
          f"{(A + B).equals(A.add(B))}")

    print("\n=== 2) subtraction ===")
    print("A - B")
    print((A - B).to_string())
    print("\nB - A")
    print((B - A).to_string())
    print(f"\n  not commutative: {not (A - B).equals(B - A)}")

    print("\n=== 3) matrix multiplication ===")
    # dot() needs A's columns to line up with B's index
    B_aligned = B.copy()
    B_aligned.index = COLS                 # c0, c1, c2 so A.columns match
    product = A.dot(B_aligned)
    print("A.dot(B)  (B re-indexed so A.columns match B.index)")
    print(product.to_string())
    print(f"\n  the @ operator does the same: "
          f"{(A @ B_aligned).equals(product)}")
    print(f"  NumPy agrees: "
          f"{np.array_equal(product.to_numpy(), A.to_numpy() @ B.to_numpy())}")

    print("\n  how one cell is computed:")
    row, col = A.iloc[0], B_aligned.iloc[:, 0]
    terms = " + ".join(f"{a}*{b}" for a, b in zip(row, col))
    print(f"    A.loc['r0'] . B[:, 'c0'] = {terms} = {product.iloc[0, 0]}")

    print("\n=== element-wise multiplication is different ===")
    print((A * B).to_string())
    print(f"\n  A * B equals A.dot(B): "
          f"{(A * B).to_numpy().tolist() == product.to_numpy().tolist()}")

    print("\n=== transpose ===")
    print(A.T.to_string())

    print("\n=== linear algebra via NumPy on the underlying values ===")
    a_np = A.to_numpy()
    print(f"  trace       : {np.trace(a_np)}")
    print(f"  determinant : {np.linalg.det(a_np):.4f}")
    print(f"  rank        : {np.linalg.matrix_rank(a_np)}")
    if abs(np.linalg.det(a_np)) > 1e-9:
        inv = pd.DataFrame(np.linalg.inv(a_np), index=LABELS, columns=COLS)
        print("\n  inverse of A:")
        print(inv.round(4).to_string())
        identity = A.dot(pd.DataFrame(np.linalg.inv(a_np),
                                      index=COLS, columns=COLS))
        print("\n  A @ inv(A):")
        print(identity.round(10).to_string())
        print(f"  is the identity: "
              f"{np.allclose(identity.to_numpy(), np.eye(3))}")

    print("\n=== scalar operations ===")
    print("A * 3")
    print((A * 3).to_string())
    print("\nA ** 2 (element-wise)")
    print((A ** 2).to_string())

    print("\n=== Pandas aggregations the raw array does not label ===")
    print(f"  column sums  :\n{A.sum(axis=0).to_string()}")
    print(f"\n  row sums     :\n{A.sum(axis=1).to_string()}")
    print(f"\n  column means :\n{A.mean(axis=0).round(4).to_string()}")
    print(f"\n  describe():")
    print(A.describe().round(3).to_string())

    print("\n=== label alignment: the real difference from NumPy ===")
    C = pd.DataFrame([[1, 1], [1, 1]], index=["r0", "r9"],
                     columns=["c0", "c9"])
    print("  C (different labels):")
    print(C.to_string())
    print("\n  A + C aligns on labels and fills the gaps with NaN:")
    print((A + C).to_string())
    print("\n  A.add(C, fill_value=0) treats the missing entries as zero:")
    print(A.add(C, fill_value=0).to_string())
    print("\n  NumPy would simply refuse: shapes (3,3) and (2,2) do not"
          " broadcast.")

    print("\n=== applying the transformation to a vector ===")
    v = pd.Series([1, 2, 3], index=COLS, name="v")
    print(f"  v        :\n{v.to_string()}")
    print(f"\n  A.dot(v) :\n{A.dot(v).to_string()}")


if __name__ == "__main__":
    main()
