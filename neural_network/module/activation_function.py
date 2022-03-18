import math

class HardLimiter:
    def apply(self, induced_field):
        return 0 if induced_field < 0 else 1

class Linear:
    def apply(self, induced_field):
        return induced_field

    def diff(self, x):
        return 1

class Sigmoid:
    def apply(self, x):
        return 1/(1+math.exp(-x))

    def diff(self, x):
        return math.exp(-x)/(1+math.exp(-x))**2


class PiecewiseLinear:
    def apply(self, x):
        return 1 if x > 0.5 else (0 if x < -0.5 else x + 0.5)


