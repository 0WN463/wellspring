from math import comb as m_comb
from math import factorial
import numpy as np


def comb(n, k):
    if n < 0 or k < 0:
        return 0
    return m_comb(n, k)


def uniform(xs):
    n = len(xs)
    return lambda x: 1/n if x in xs else 0


def bernoulli(p):
    return lambda x: p ** x * (1-p)**(1-x)


def binomial(n, p):
    return lambda x: comb(n, x) * p ** x * (1-p)**(n-x)


def negative_binomial(k, p):
    return lambda x: comb(x-1, k-1) * p ** k * (1-p)**(x-k)


def poisson(lamb):
    return lambda x: np.exp(-lamb) * lamb ** x / factorial(x)


def c_uniform(a, b):
    return lambda x: np.where(a <= x <= b, 1/(b-a), 0)


def exponential(alpha):
    return lambda x: alpha * np.exp(-alpha * x)


def normal(m=0, s=1):
    return lambda x: 1/(s * np.sqrt(2 * np.pi)) * np.exp(- (x - m)**2/(2 * s**2))
