import numpy as np
from .perceptron import Perceptron

class LearningPerceptron(Perceptron):
    def __init__(self, size, activation_function, weights=None, learning_rate=1):
        if weights is None:
            weights = np.random.rand(size+1)*2-1
        weights = np.array(weights)
        assert weights.shape == (size+1,)
        super().__init__(size, activation_function, weights=weights)
        self.learning_rate = learning_rate

    def calculate_error(self, input, correct_label):
        return correct_label - self.get_output(input)
    
    def update_weights(self, input, error):
        self.weights = self.weights + self.learning_rate * error * np.insert(input, 0, 1)
        
    def train(self, input, correct_label):
        input = np.array(input)
        error = self.calculate_error(input, correct_label)
        self.update_weights(input, error)
        
    def train_epoch(self, inputs, labels, epochs=5):
        assert len(inputs) == len(labels)
        for _ in range(epochs):
            prev_weights = self.weights
            for input, label in zip(inputs, labels):
                self.train(input, label)
            if np.array_equal(prev_weights, self.weights):
                break

