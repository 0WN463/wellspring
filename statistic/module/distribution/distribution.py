from inspect import signature
import numpy as np
from . import probability_function as pf


class Distribution:
    def __init__(self, name, symbol, fx):
        self.name = name
        self.symbol = symbol
        self.fx = fx
        self.num_params = signature(fx).parameters

    def f(self, xs, *args):
        try:
            arg_str = ','.join(map(lambda x: f'{x:.4g}', args))
        except TypeError:
            arg_str = ""
        return (f"{self.name}: {self.symbol}({arg_str})", np.vectorize(self.fx(*args))(xs))


def uniform():
    return Distribution("Uniform discrete distribution", "f", pf.uniform)


def bernoulli():
    return Distribution("Bernoulli distribution", "f", pf.bernoulli)


def binomial():
    return Distribution("Binomial distribution", "B", pf.binomial)


def negative_binomial():
    return Distribution("Negative binomial distribution", "NB", pf.negative_binomial)

def poisson():
    return Distribution("Poisson distribution", "P", pf.poisson)

def chi_square():
    return Distribution('Chi square', 'χ²', pf.chi_square)

def t():
    return Distribution('t-distribution', 't', pf.t)

def F():
    return Distribution('F-distribution', 'F', pf.F)
