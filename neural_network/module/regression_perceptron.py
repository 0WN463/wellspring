from .learning_perceptron import LearningPerceptron
from .activation_function import Linear

class RegressionPerceptron(LearningPerceptron):
    def __init__(self, size, weights=None, learning_rate=1):
        super().__init__(size, Linear(), weights, learning_rate)

