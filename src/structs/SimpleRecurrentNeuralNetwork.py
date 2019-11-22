#/dust/src/structs/SimpleRecurrentNeuralNetwork.py

# Built-ins
# Package
import __init__

# Additional Packages
import numpy as np
from scipy.special import expit

def sigmoid(s): return expit(s)
def sigmoid_prime(s): return s*(1-s)

class SimpleRNN():

    def __init__(self, inputlayers, outputlayers, hiddenlayers=10, learning_rate=1,
                 activation_fn = sigmoid):
        
        self.inputlayers  = inputlayers
        self.outputlayers = outputlayers
        self.hiddenlayers = hiddenlayers

        self.activation_fn = activation_fn
        self.learning_rate = learning_rate

        self.weight_ih = np.random.uniform(0,1, (inputlayers, hiddenlayers))
        self.weight_hh = np.random.uniform(0,1, (hiddenlayers, hiddenlayers))
        self.weight_ho = np.random.uniform(0,1, (hiddenlayers, outputlayers))

        self.H = None

    def forward_proc(self, X):
        
        #self.H = np.dot(X, self.weight_ih)
        self.H1 = np.dot(self.H, self.weight_hh)

        self.activation_h = self.activation_fn(self.H1)
        self.activation_o = self.activation_fn(np.dot(self.activation_h, self.weight_ho))
        
        return self.activation_o
        
