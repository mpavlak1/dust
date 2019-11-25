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
                 activation_fn = sigmoid, activationprime_fn = sigmoid_prime):
        
        self.inputlayers  = inputlayers
        self.outputlayers = outputlayers
        self.hiddenlayers = hiddenlayers

        self.activation_fn = activation_fn
        self.activationprime_fn = activationprime_fn
        self.learning_rate = learning_rate

        self.weight_ih = np.random.uniform(0,1, (inputlayers, hiddenlayers))
        self.weight_hh = np.random.uniform(0,1, (hiddenlayers, hiddenlayers))
        self.weight_ho = np.random.uniform(0,1, (hiddenlayers, outputlayers))

        self.H = None

    def forward_proc(self, X):

        # a(t) = b + W*h(t-1) + U*x(t)
        # h(t) = activation(a(t))
        # o(t) = c + V*h(t)

        if(self.H is None):
            raise Exception('Lag H not set')
        
        wxh = np.dot(self.H, self.weight_hh)
        uxx  = np.dot(X, self.weight_ih)

        a = uxx + wxh 
        h = self.activation_fn(a)

        self.H = h
        vxh = np.dot(h, self.weight_ho)
        self.activation_y =  vxh

        return self.activation_fn(self.activation_y)
              

    def backward_proc(self, X, output, expected_output):

        errors_y = expected_output - output
        deltas_y = errors_y * self.activationprime_fn(output)

        self.errors_y = errors_y
        self.deltas_y = deltas_y

        self.errors_h2 = np.dot(self.deltas_y, self.weight_ho.T)
        self.deltas_h2 = self.errors_h2 * self.activationprime_fn(self.H)

##        self.errors_hh = np.dot(self.deltas_h2, self.weight_ih.T)
##        self.deltas_hh = self.errors_hh * self.activationprime_fn(X)

        self.weight_ho += self.learning_rate * self.activation_y.T.dot(deltas_y)
        self.weight_hh += self.learning_rate * self.H.T.dot(self.deltas_h2)
        self.weight_ih += self.learning_rate * self.H.T.dot(self.deltas_h2)

    def train_epoc(self, X, Y, N=100, prune_rate = 0.0001):

        
        estart = -1
        for _ in range(N):
            self.H = self.activation_fn(np.dot(X[0], self.weight_ih))
            outputs = []
            for i in range(1, X.shape[0]):
                output = self.forward_proc(X[i])
                outputs.append(output)
                self.backward_proc(X[i], output, Y[i])
            ientropy = sum(sum(abs(Y[1:]-np.array(outputs))))
            eend = ientropy
            print('Entropy: {}'.format(ientropy))

            if(estart > 0 and estart - eend < prune_rate):
                print('No info gained ({}). Pruning at {} iterations'.format(estart-eend, _))
                break
            else: estart=eend

