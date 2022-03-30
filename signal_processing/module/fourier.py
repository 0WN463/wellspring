from scipy.integrate import quad
import numpy as np
from .signal import sinusoid


def _clip_zeroes(arr):
    reals = arr.real
    reals = np.where(np.isclose(reals, 0), 0, reals)

    imags = arr.imag * 1j
    imags = np.where(np.isclose(imags, 0), 0, imags)
    if np.all(imags == 0):
        return reals

    return reals + imags


def series(func, Tp, c_range):
    ck_rs = [quad(lambda t:  (func(t) * np.exp(-2j * np.pi * m * t/Tp)
                              ).real, 0, Tp)[0] / Tp for m in c_range]
    ck_is = [quad(lambda t:  (func(t) * np.exp(-2j * np.pi * m * t/Tp)
                              ).imag, 0, Tp)[0] / Tp for m in c_range]
    return _clip_zeroes(np.array(ck_rs) + np.array(ck_is) * 1j)


def reconstruct(span, c_func, ts, Tp):
    ks = np.arange(-span, span + 1)
    harmonics = np.array(
        [sinusoid(ts, mu=np.abs(c_func(k)), f=k/Tp, phi=np.angle(c_func(k))) for k in ks])
    return _clip_zeroes(harmonics.sum(axis=0))
