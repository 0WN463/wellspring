from .learning_perceptron import LearningPerceptron
import numpy as np

class RegressionPerceptron(LearningPerceptron):
    '''Main difference is the lack of squash and classify function'''
        
    def calculate_error(self, input, correct_label):
        return correct_label - self.induce_field(input)
