# /dust/src/structs/SimpleNeuralNetwork.py

# Package
import __init__

# Additional Packages
import numpy as np


def sigmoid(s): return 1/(1+np.exp(-s))
def sigmoid_prime(s): return s*(1-s)

class SimpleNeuralNetwork():

    def __init__(self, inputlayers, outputlayers, hiddenlayers=10,
                 activation_fn = sigmoid, activationprime_fn = sigmoid_prime):

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

    def train(self, X, expected_outputs, N=1, prune_rate = 0.0001):
        for _ in range(N):
            try:
                p_error = sum(self.output_error)
            except AttributeError:
                p_error = np.zeros(self.outputlayers)
            output = self.forward_prop(X)
            self.backward_prop(X, output, expected_outputs)

            c_error = sum(self.output_error)

            ientropy = sum(abs(p_error - c_error))
            if(ientropy < prune_rate):
                print('No new info gained; pruning at {}'.format(_))
                break

    

   
    
n = SimpleNeuralNetwork(6,3,hiddenlayers=10)

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

y0 = np.array([1,0,0])
y1 = np.array([1,0,0])
y2 = np.array([1,0,0])
y3 = np.array([1,0,0])
y4 = np.array([0,1,0])
y5 = np.array([0,1,0])
y6 = np.array([0,1,0])
y7 = np.array([0,1,0])
y8 = np.array([0,0,1])
y9 = np.array([0,0,1])
ya = np.array([0,0,1])
yb = np.array([0,0,1])

Y0 = np.array([y0,y1,y2,y3,y4,y5,y6,y7,y8,y9,ya,yb])

n.train(X0,Y0,N=1000)
for i, x in enumerate(X0):
    print(x, n.forward_prop(x).argmax(), Y0[i])





