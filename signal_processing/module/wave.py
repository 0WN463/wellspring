import numpy as np
from . import signal


def _repeat(signal, ts, T):
    factor = np.floor((ts + T/2)/T)
    t_primes = ts - T * factor
    return signal(t_primes)


def square(ts, T, A):
    return _repeat(lambda ts: A * signal.rect(ts, T), ts, 2 * T)


def tri(ts, T, A):
    return _repeat(lambda ts: 2 * A * signal.tri(ts, T) - A, ts, 2 * T)


def sawtooth(ts, T, A):
    return A * _repeat(lambda ts: ts, ts, T)
