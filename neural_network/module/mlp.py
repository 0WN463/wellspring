import numpy as np
from .activation_function import Sigmoid
from .learning_perceptron import LearningPerceptron

class MLP:
    def __init__(self, shape, activation_functions=Sigmoid(), learning_rate=0.1):
        assert len(shape) >= 2
        shape = np.array(shape)
        self.input_size = shape[0]
        self.output_size = shape[-1]
        self.size = len(shape) -1 
        self.shape = shape
        self.neurons = [[LearningPerceptron(prev_size, activation_functions, learning_rate=learning_rate) \
                         for _ in range(size)] for size, prev_size in zip(shape[1:], shape)]
        self.neurons.insert(0, []) # Maintain that layer 0 is input
        
    def get_outputs(self, input, layer=None):
        assert len(input) == self.input_size
        
        if layer == None:
            layer = self.size
        
        if layer == 0:
            return input
        
        prev_layer_outputs = self.get_outputs(input, layer-1)
        
        output = [p.get_output(prev_layer_outputs) for p in self.neurons[layer]]
        
        return np.array(output)

    
    def get_fields(self, input, layer=None):
        assert len(input) == self.input_size
        
        if layer == None:
            layer = self.size
        
        if layer == 0:
            return input
        
        prev_layer_outputs = self.get_outputs(input, layer-1)
        fields = [p.induce_field(prev_layer_outputs) for p in self.neurons[layer]]
        
        return fields
    
    def get_deltas(self, input, labels, layer=None):
        assert len(input) == self.input_size
        input = np.array(input)
        labels = np.array(labels)
        if layer == None:
            layer = self.size
        
        fields = self.get_fields(input, layer)

        if layer == self.size:
            return (labels - self.get_outputs(input, layer)) * \
        np.array([neuron.activation_function.diff(f) for neuron, f in zip(self.neurons[layer], fields)])
        
        next_deltas = self.get_deltas(input, labels, layer+1)
        deltas = []
        for i, (neuron, field) in enumerate(zip(self.neurons[layer], fields)):
            total = 0
            for next_neuron, delta in zip(self.neurons[layer+1], next_deltas):
                total += next_neuron.weights[i+1] * delta # Skip bias weights
            deltas.append(total * neuron.activation_function.diff(field))
        return np.array(deltas)
    

    def update_weights(self, input, labels):
        all_deltas = [self.get_deltas(input, labels, layer) for layer in range(self.size+1)]
        outs = [self.get_outputs(input, layer) for layer in range(self.size)]
        for deltas, layer, out in zip(all_deltas[1:], self.neurons[1:], outs):
            for delta, neuron in zip(deltas, layer):
                neuron.update_weights(out, delta)
