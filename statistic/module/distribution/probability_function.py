from math import comb as m_comb
from math import factorial
import numpy as np
from scipy.special import gamma

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

def chi_square(df):
    return lambda x: (x ** (df/2-1) * np.exp(-x/2)) / (2 ** (df/2) * gamma(df/2))

def t(n):
    return lambda x: gamma((n+1)/2) / (np.sqrt(n * np.pi) * gamma(n/2)) * (1 + x **2/n)**(-(n+1)/2) 

def F(n1, n2):
    def func(x):
        top_left = n1 ** (n1 / 2) * n2 ** (n2/2) *gamma((n1 + n2)/2)
        bottom_left = gamma(n1 / 2) * gamma(n2/2)
        top_right = x **(n1/2 - 1)
        bottom_right = (n1 * x + n2) **((n1 + n2)/2)
        return top_left * top_right / bottom_left / bottom_right
    return func
