import numpy as np
from . import signal


def square(ts, T, A):
    return np.where(np.floor((ts + T/2) / T) % 2 == 0, A, 0)


def tri(ts, T, A):
    factor = np.floor((ts + T/2)/T)
    xs = ts - T * factor
    return A * signal.tri(xs, T/2) * np.where(factor % 2 == 0, 1, -1)
