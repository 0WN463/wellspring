import numpy as np


def det(A: np.ndarray) -> float:
    if A.ndim == 1:
        return A[0]

    assert A.ndim == 2
    assert A.shape[0] == A.shape[1]
    n = A.shape[0]

    if n == 1:
        return A[0][0]
    if n == 2:
        a, b, c, d = A.ravel()
        return a * d - b * c

    return sum(A[0][i] * det(A[1:, [j for j in range(n) if j != i]]) * (-1) ** i for i in range(n))
