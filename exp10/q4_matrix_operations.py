"""
Experiment 10 - Question 4: Matrix Operations

Scenario: Two 3x3 matrices represent transformations.

Task:
  1) Perform addition, subtraction and matrix multiplication between them.

Rubrics covered:
  * array creation
  * element-wise operations
  * matrix multiplication (np.dot or @)
  * correct results

Requires: numpy
"""

import numpy as np


def show(label, matrix):
    print(f"\n  {label}")
    for row in matrix:
        print("    [" + "  ".join(f"{v:>8.2f}" if matrix.dtype.kind == "f"
                                  else f"{v:>5}" for v in row) + "]")


def main():
    A = np.array([[2, 0, 1],
                  [1, 3, 2],
                  [4, 1, 0]])

    B = np.array([[1, 2, 0],
                  [0, 1, 3],
                  [2, 1, 1]])

    print("=== the two 3x3 matrices ===")
    show("A =", A)
    show("B =", B)
    print(f"\n  A.shape {A.shape}, B.shape {B.shape}, dtype {A.dtype}")

    print("\n=== 1) addition (element-wise) ===")
    show("A + B =", A + B)
    print(f"  same as np.add(A, B) : {np.array_equal(A + B, np.add(A, B))}")

    print("\n=== 2) subtraction (element-wise) ===")
    show("A - B =", A - B)
    show("B - A =", B - A)
    print(f"  subtraction is not commutative: "
          f"{not np.array_equal(A - B, B - A)}")

    print("\n=== 3) matrix multiplication ===")
    product = A @ B
    show("A @ B =", product)
    print(f"  np.dot(A, B) gives the same : "
          f"{np.array_equal(product, np.dot(A, B))}")
    print(f"  np.matmul(A, B) too         : "
          f"{np.array_equal(product, np.matmul(A, B))}")
    show("B @ A =", B @ A)
    print(f"  matrix multiplication is not commutative: "
          f"{not np.array_equal(A @ B, B @ A)}")

    print("\n  how one cell is computed:")
    print(f"    (A @ B)[0, 0] = row A[0] . column B[:, 0]")
    print(f"                  = {A[0]} . {B[:, 0]}")
    print(f"                  = {' + '.join(f'{a}*{b}' for a, b in zip(A[0], B[:, 0]))}"
          f" = {product[0, 0]}")

    print("\n=== element-wise multiplication is a different operation ===")
    show("A * B (Hadamard) =", A * B)
    print(f"  A * B equals A @ B : {np.array_equal(A * B, A @ B)}")

    print("\n=== other transformations ===")
    show("A transposed =", A.T)
    print(f"  trace(A)        : {np.trace(A)}")
    print(f"  det(A)          : {np.linalg.det(A):.4f}")
    print(f"  det(B)          : {np.linalg.det(B):.4f}")
    print(f"  rank(A)         : {np.linalg.matrix_rank(A)}")

    if abs(np.linalg.det(A)) > 1e-9:
        inverse = np.linalg.inv(A)
        show("inverse of A =", inverse)
        identity = A @ inverse
        show("A @ inv(A) =", np.round(identity, 10))
        print(f"  equals the identity matrix : "
              f"{np.allclose(identity, np.eye(3))}")
    else:
        print("  A is singular, no inverse exists")

    print("\n=== scalar operations ===")
    show("A * 3 =", A * 3)
    show("A + 10 =", A + 10)
    show("A ** 2 (element-wise) =", A ** 2)
    show("matrix power A @ A =", np.linalg.matrix_power(A, 2))

    print("\n=== applying the transformations to a vector ===")
    v = np.array([1, 2, 3])
    print(f"  v        = {v}")
    print(f"  A @ v    = {A @ v}")
    print(f"  B @ v    = {B @ v}")
    print(f"  A @ B @ v= {A @ B @ v}")
    print(f"  (A@B) @ v == A @ (B @ v) : "
          f"{np.array_equal((A @ B) @ v, A @ (B @ v))}  "
          f"(matrix multiplication is associative)")

    print("\n=== aggregates ===")
    print(f"  A.sum()        : {A.sum()}")
    print(f"  A.sum(axis=0)  : {A.sum(axis=0)}  (column totals)")
    print(f"  A.sum(axis=1)  : {A.sum(axis=1)}  (row totals)")
    print(f"  A.max(), A.min(): {A.max()}, {A.min()}")
    print(f"  A.mean()       : {A.mean():.4f}")

    print("\n=== solving a linear system A x = b ===")
    b = np.array([5, 11, 9])
    if abs(np.linalg.det(A)) > 1e-9:
        x = np.linalg.solve(A, b)
        print(f"  b            = {b}")
        print(f"  x            = {np.round(x, 4)}")
        print(f"  check A @ x  = {np.round(A @ x, 4)}")
        print(f"  matches b    : {np.allclose(A @ x, b)}")

    print("\n=== eigenvalues of A ===")
    values = np.linalg.eigvals(A)
    print(f"  {np.round(values, 4)}")
    print(f"  sum of eigenvalues {np.real(values.sum()):.4f} "
          f"equals trace(A) {np.trace(A)}: "
          f"{np.isclose(np.real(values.sum()), np.trace(A))}")


if __name__ == "__main__":
    main()
