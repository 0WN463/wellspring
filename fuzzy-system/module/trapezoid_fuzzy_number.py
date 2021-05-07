from sympy import symbols, Piecewise, integrate, Min, solve
import sympy as sp
from numpy import arange
from .alpha_cut import AlphaCut

x, a = symbols('x a')
class TrapezoidFuzzyNumber:
    """Section 1: """
    def __init__(self, domain, left_func, right_func):
        l, r = domain
        
        core_l, core_r = solve(left_func - 1, x), solve(right_func - 1, x)
        
        assert len(core_l) == len(core_r) == 1
        core_l, core_r = core_l[0], core_r[0]

        self.formula = Piecewise(
            (0, x <= l),
            (0, x > r),
            ( left_func, (l < x) & (x <= core_l)),
            ( 1, (core_l < x) & (x <= core_r)),
            ( right_func, (core_r < x) & (x <= r) )
        )
        self.left_func = left_func
        self.right_func = right_func
        self.domain = (l, r)
    @property
    def alpha_cut(self):
        left_bound = solve(self.left_func-a, x)[0]
        right_bound = solve(self.right_func - a, x)[0]
        return AlphaCut(left_bound, right_bound)
    
    def __add__(self, other):
        new_alpha = self.alpha_cut + other.alpha_cut
        return new_alpha.to_fuzzy()
    
    def __sub__(self, other):
        new_alpha = self.alpha_cut - other.alpha_cut
        return new_alpha.to_fuzzy()
    
    def plot(self, show=True):
        x_lim = int(self.domain[0] - 2), int(self.domain[1] + 2)
        plt = sp.plotting.plot(self.formula, (x, x_lim[0], x_lim[1]), show=False)
        plt.xlim = x_lim
        plt.ylim = (0, 1.5)
        if show:
            plt.show()
        return plt
    
    """Section 2: Defuzzification"""

    @property
    def centroid(self):
        l, r = self.domain
        return integrate(self.formula*x, (x, l, r))/ integrate(self.formula, (x, l, r))
    
    def get_strength(self, other):
        interval = min(*self.domain, *other.domain), max(*self.domain, *other.domain)
        overlap_formula = Min(self.formula, other.formula)
        return max([overlap_formula.subs(x, i) for i in arange(*interval, 0.01)])

