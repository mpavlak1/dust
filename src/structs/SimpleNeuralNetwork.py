# /dust/src/structs/SimpleNeuralNetwork.py

# Package
import __init__

# Additional Packages
import numpy as np
from scipy.special import expit

def sigmoid(s):
    return expit(s)
    return 1/(1+np.exp(-s))

def sigmoid_prime(s): return s*(1-s)

class twoLayerNeuralNetwork():

    def __init__(self, inputlayers, outputlayers, hiddenlayers0 = 10, hiddenlayers1 = 10,
                 activation_fn = sigmoid, activationprime_fn = sigmoid_prime, learning_rate=0.01):

        self.inputlayers = inputlayers
        self.outputlayers = outputlayers
        self.hiddenlayers0 = hiddenlayers0
        self.hiddenlayers1 = hiddenlayers1

        self.activation_fn = activation_fn
        self.activationprime_fn = activationprime_fn
        self.learning_rate = learning_rate

        self.weight_ih0  = np.random.randn(self.inputlayers ,  self.hiddenlayers0)
        self.weight_h0h1 = np.random.randn(self.hiddenlayers0, self.hiddenlayers1)
        self.weight_h1o  = np.random.randn(self.hiddenlayers1, self.outputlayers)

    def forward_prop(self, X):

        self.h0active = self.activation_fn(np.dot(X, self.weight_ih0))
        self.h1active = self.activation_fn(np.dot(self.h0active, self.weight_h0h1))
        output = self.activation_fn(np.dot(self.h1active, self.weight_h1o))
        return output

    def backward_prop(self, X, output, expected_output):

        self.output_error = expected_output - output
        self.output_delta = self.output_error * self.activationprime_fn(output)

        self.hidden1_error = self.output_error.dot(self.weight_h1o.T)
        self.hidden1_delta = self.hidden1_error * self.activationprime_fn(self.h1active)

        self.hidden0_error = self.hidden1_error.dot(self.weight_h0h1.T)
        self.hidden0_delta = self.hidden0_error * self.activationprime_fn(self.h0active)

        self.weight_ih0  += self.learning_rate * X.T.dot(self.hidden0_delta)
        self.weight_h0h1 += self.learning_rate *self.h0active.T.dot(self.hidden1_delta)
        self.weight_h1o  += self.learning_rate *self.h1active.T.dot(self.output_delta)

    def train(self, X, expected_outputs, N=1, prune_rate = 0.00001):
        for _ in range(N):
            try:
                p_error = sum(self.output_error)
            except AttributeError:
                p_error = np.zeros(self.outputlayers)

            output = self.forward_prop(X)
            self.backward_prop(X, output, expected_outputs)

            c_error = sum(self.output_error)

            ientropy = sum(abs(p_error - c_error))
            if(_ < 10):
                continue
            if(ientropy < prune_rate):
                print('Entropy = {}'.format(ientropy))
                print('No new info gained; pruning at {}'.format(_))
                break
        


class SimpleNeuralNetwork():

    def __init__(self, inputlayers, outputlayers, hiddenlayers=10,
                 activation_fn = sigmoid, activationprime_fn = sigmoid_prime, learning_rate=0.01):

        self.inputlayers = inputlayers
        self.outputlayers = outputlayers
        self.hiddenlayers = hiddenlayers

        self.activation_fn = activation_fn
        self.activationprime_fn = activationprime_fn

        self.weight_ih = np.random.randn(self.inputlayers, self.hiddenlayers)
        self.weight_ho = np.random.randn(self.hiddenlayers, self.outputlayers)

    def forward_prop(self, X):
        self.hactive = self.activation_fn(np.dot(X, self.weight_ih))
        output = self.activation_fn(np.dot(self.hactive, self.weight_ho))
        return output

    def backward_prop(self, X, output, expected_output):

        self.output_error = expected_output - output
        self.output_delta = self.output_error * self.activationprime_fn(output)

        self.hidden_error = self.output_error.dot(self.weight_ho.T)
        self.hidden_delta = self.hidden_error*self.activationprime_fn(self.hactive)

        self.weight_ih += X.T.dot(self.hidden_delta)
        self.weight_ho += self.hactive.T.dot(self.output_delta)

    def train(self, X, expected_outputs, N=1, prune_rate = 0.00001):
        for _ in range(N):
            try:
                p_error = sum(self.output_error)
            except AttributeError:
                p_error = np.zeros(self.outputlayers)
            output = self.forward_prop(X)
            self.backward_prop(X, output, expected_outputs)

            c_error = sum(self.output_error)

            ientropy = sum(abs(p_error - c_error))
            if(ientropy < prune_rate and _ > 10):
                print('Entropy = {}'.format(ientropy))
                print('No new info gained; pruning at {}'.format(_))
                break

