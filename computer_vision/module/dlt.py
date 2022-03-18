import numpy as np


def dlt(ps, p_primes):
    assert len(ps) == len(p_primes)
    xs, ys = ps[:, 0], ps[:, 1]
    x_primes, y_primes = p_primes[:, 0], p_primes[:, 1]

    arr = []
    for x, x_p, y, y_p in zip(xs, x_primes, ys, y_primes):
        arr.append([-x, -y, -1, 0, 0, 0, x * x_p, y * x_p, x_p])
        arr.append([0, 0, 0, -x, -y, -1, x * y_p, y * y_p, y_p])
    A = np.array(arr)
    H = np.linalg.svd(A)[-1][-1].reshape(3, 3)

    return H / H[2][2]  # Make bottom right corner 1 for ease of representation
