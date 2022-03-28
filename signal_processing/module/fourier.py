from scipy.integrate import quad
import numpy as np


def series(func, Tp, c_range):
    cks = [quad(lambda t:  (func(t) * np.exp(-2j * np.pi * m * t/Tp)
                            ).real, 0, Tp)[0] / Tp for m in c_range]

    return np.array(cks)


def reconstruct(span, c_func, ts, Tp):
    ks = np.arange(-span, span + 1)
    harmonics = np.array(
        [c_func(k) * np.exp(2j * np.pi * k * ts / Tp).real for k in ks])
    return harmonics.sum(axis=0)
