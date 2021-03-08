import numpy as np

class Perceptron:
    def __init__(self, size, activation_function, weights=None):
        if weights is None:
            weights = np.random.rand(size+1) * 2 -1
        weights = np.array(weights)
        assert weights.shape == (size+1,)
        self.weights = weights
        self.size = size
        self.activation_function = activation_function
        
    def induce_field(self, input):
        input = np.array(input)
        assert input.shape == (self.size,)
        input = np.insert(input, 0, 1)
        return self.weights.T @ input
    
    def squash(self, induced_field):
        return self.activation_function.apply(induced_field)
    
    def get_output(self, input):
        field = self.induce_field(input)
        output = self.squash(field)
        return output


