import numpy as np


def square(ts, T, A):
    return np.where(np.floor((ts + T/2) / T) % 2 == 0, A, 0)
