from .perceptron import Perceptron
from .activation_function import HardLimiter
class ClassicalPerceptron(Perceptron):
    def __init__(self, size, weights=None):
        super().__init__(size, HardLimiter(), weights)
