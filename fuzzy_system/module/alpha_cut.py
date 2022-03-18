from sympy import symbols, solve

x, a = symbols('x a')

class AlphaCut:
    def __init__(self, left_bound, right_bound):
        self.left_bound = left_bound
        self.right_bound = right_bound

    def __add__(self, other):
        return AlphaCut(self.left_bound + other.left_bound, self.right_bound + other.right_bound)

    def __sub__(self, other):
        return AlphaCut(self.left_bound - other.right_bound, self.right_bound - other.left_bound)
    
    def to_fuzzy(self):
        from .trapezoid_fuzzy_number import TrapezoidFuzzyNumber
        domain = self.left_bound.subs(a, 0), self.right_bound.subs(a, 0)
        left_func = solve(self.left_bound - x, a)[0]
        right_func = solve(self.right_bound - x, a)[0]
        l, r = domain
        return TrapezoidFuzzyNumber((l, r), left_func, right_func)

