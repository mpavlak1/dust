# /dust/src/structs/SimpleNeuralNetwork.py

# Package
import __init__

# Additional Packages
import numpy as np
from scipy.special import expit

def sigmoid(s): return expit(s)
def sigmoid_prime(s): return s*(1-s)


class nLayerNeuralNetwork():

    def __init__(self, inputlayers, outputlayers, hiddenlayers=(7,7,7),
                 activation_fn = sigmoid, activationprime_fn = sigmoid_prime,
                 trainX = None, trainY = None, epochs=1000):
        
        self.inputlayers = inputlayers
        self.outputlayers = outputlayers
        self.hiddenlayers = hiddenlayers

        self.activation_fn = activation_fn
        self.activationprime_fn = activationprime_fn

        weight_ih0 = np.random.randn(self.inputlayers, self.hiddenlayers[0])
        hidden_weights = [np.random.randn(self.hiddenlayers[i], self.hiddenlayers[i+1]) \
                               for i in range(len(self.hiddenlayers[0:-1]))]
        weight_hNo = np.random.randn(self.hiddenlayers[-1], self.outputlayers)

        self.weights = [weight_ih0, *hidden_weights, weight_hNo]

        if(trainX is not None and trainY is not None):
            self.train(trainX, trainY, N=epochs)

    def forward_prop(self, X):
        activations = []
        p = X
        for i in range(len(self.weights)):
            p = self.activation_fn(np.dot(p, self.weights[i]))
            activations.append(p)
        self.activations = activations
        return activations[-1]

    def backward_prop(self, X, output, expected_output):

        errors, deltas = [], []

        errors.append(expected_output - output)
        deltas.append(errors[-1] * self.activationprime_fn(output))
        
        for i in range(len(self.weights)-1, 0, -1):
            e = errors[-1].dot(self.weights[i].T)
            d = e*self.activationprime_fn(self.activations[i-1])

            errors.append(e)
            deltas.append(d)

        errors.reverse()
        deltas.reverse()

        a = [X] + self.activations
        for i in range(len(self.weights)):
            self.weights[i] += a[i].T.dot(deltas[i])

        self.errors = errors
        self.deltas = deltas

    def train(self, X, expected_outputs, N=1, prune_rate = 1/10000):
        for _ in range(N):
            try:
                p_error = sum(self.errors[-1])
            except AttributeError: p_error = np.zeros(self.outputlayers)

            output = self.forward_prop(X)
            self.backward_prop(X, output, expected_outputs)

            c_error = sum(self.errors[-1])

            ientropy = sum(abs(p_error - c_error))
            if(ientropy < prune_rate):
                print('Entropy = {}'.format(ientropy))
                print('No new info gained; pruning at {}'.format(_))
                break

        
     

x0 = np.array([0,0,0,1,1,1]) #class A
x1 = np.array([0,0,0,0,1,1]) #class A
x2 = np.array([0,0,0,1,1,0]) #class A
x3 = np.array([0,0,0,1,0,1]) #class A
x4 = np.array([1,1,1,0,0,0]) #class B
x5 = np.array([1,1,0,0,0,0]) #class B
x6 = np.array([0,1,1,0,0,0]) #class B
x7 = np.array([1,0,1,0,0,0]) #class B
x8 = np.array([1,0,0,0,0,1]) #class C
x9 = np.array([1,1,0,0,0,1]) #class C
xa = np.array([1,0,0,0,1,1]) #class C
xb = np.array([1,1,0,0,1,1]) #class C

X0 = np.array([x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,xa,xb])

y0 = np.array([1,0,0]) #A
y1 = np.array([1,0,0]) #A
y2 = np.array([1,0,0]) #A
y3 = np.array([1,0,0]) #A
y4 = np.array([0,1,0]) #B
y5 = np.array([0,1,0]) #B
y6 = np.array([0,1,0]) #B
y7 = np.array([0,1,0]) #B
y8 = np.array([0,0,1]) #C
y9 = np.array([0,0,1]) #C
ya = np.array([0,0,1]) #C
yb = np.array([0,0,1]) #C

Y0 = np.array([y0,y1,y2,y3,y4,y5,y6,y7,y8,y9,ya,yb])

X = X0
Y = Y0

nn=nLayerNeuralNetwork(6, 3, [7,9], trainX=X, trainY=Y)  
from dust.src.structs.metrics import accuracy
