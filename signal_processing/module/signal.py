import numpy as np


def unit_step(ts):
    return np.where(ts < 0, 0, 1)


def sign(ts):
    return np.where(ts < 0, -1, 1)


def rect(ts, T):
    return np.where(np.abs(ts) <= T/2, 1, 0)


def tri(ts, T):
    return np.where(np.abs(ts) <= T, 1 - np.abs(ts) / T, 0)


def sinc(ts, T):
    inner = np.pi * (ts + (ts == 0)) / T
    return np.where(ts == 0, 1, np.sin(inner) / (inner))


def exp(ts, sigma):
    return np.exp(-sigma * ts)


def _f_to_omega(f):
    return f * 2 * np.pi


def sinusoid(ts, mu=1, phi=0, omega=None, f=None):
    assert not (omega is None and f is None)
    if omega is None:
        omega = _f_to_omega(f)

    return mu * np.exp(1j * (omega * ts + phi))


def cos(ts, mu=1, phi=0, omega=None, f=None):
    assert not (omega is None and f is None)
    if omega is None:
        omega = _f_to_omega(f)
    return mu * np.cos(omega * ts + phi)


def sin(ts, mu=1, phi=0, omega=None, f=None):
    assert not (omega is None and f is None)
    if omega is None:
        omega = _f_to_omega(f)
    return mu * np.sin(omega * ts + phi)
