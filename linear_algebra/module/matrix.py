import numpy as np
from .elimination import gauss_jordan_elim

def mult(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    assert A.shape[1] == B.shape[0]

    result = np.zeros((A.shape[0], B.shape[1])).astype('object')

    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            result[i][j] = np.sum(A[i] * B[:, j])

    return result

def mults(*As):
    arr = As[0]
    
    for A in As[1:]:
        arr = mult(arr, A)

    return arr

def inv(A: np.ndarray) -> np.ndarray | None:
    assert A.ndim == 2
    assert A.shape[0] == A.shape[1]

    I = np.identity(A.shape[0]).astype('int')

    R, B = gauss_jordan_elim(A, I)

    return B if np.all(R == I) else None

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
