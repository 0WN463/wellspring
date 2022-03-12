import numpy as np


def homography(H, ps):
    Ps = np.hstack((ps, np.ones((ps.shape[0], 1))))

    P_primes = np.array([H @ p for p in Ps])
    p_primes = (P_primes[:, 0:2] / P_primes[:,
                2].reshape((-1, 1)))
    p_primes = p_primes.reshape(ps.shape)
    return p_primes


def indices(image):
    return np.indices(image.shape).transpose(
        (1, 2, 0)).reshape((-1, 2))
