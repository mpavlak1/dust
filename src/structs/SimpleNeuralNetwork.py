# /dust/src/structs/SimpleNeuralNetwork.py

# Built-ins
import os
import pickle
import zipfile

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
                 learning_rate = 0.01,
                 trainX = None, trainY = None, epochs=1000):
        
        self.inputlayers = inputlayers
        self.outputlayers = outputlayers
        self.hiddenlayers = hiddenlayers

        self.activation_fn = activation_fn
        self.activationprime_fn = activationprime_fn
        self.learning_rate = learning_rate

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
            self.weights[i] += self.learning_rate * a[i].T.dot(deltas[i])

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

def save(model, path):

    os.makedirs(path, exist_ok=True)
    for file in os.listdir(path):
        try:
            os.remove(os.path.join(path, file))
        except Exception as e:
            print(e)
            continue
    
    def _savenp(arrs, type_):
        for i, arr in enumerate(arrs):
            outfile = os.path.join(path,'{}_{}.pickle'.format(type_,i))
            with open(outfile, 'wb') as f: np.save(f, arr)

    _savenp(model.activations, 'activation')
    _savenp(model.weights,     'weight')
    _savenp(model.deltas,      'delta')
    _savenp(model.errors,      'error')

    main_copy = nLayerNeuralNetwork(model.inputlayers, model.outputlayers,
                                    hiddenlayers = model.hiddenlayers,
                                    activation_fn = model.activation_fn,
                                    activationprime_fn = model.activationprime_fn,
                                    learning_rate = model.learning_rate)
    main_copy.weights = []
    with open(os.path.join(path,'main.pickle'), 'wb') as f:
        pickle.dump(main_copy, f)

    z = zipfile.ZipFile('{}.model'.format(path),mode='w')
    for file in os.listdir(path):
        z.write(os.path.join(path,file), arcname=os.path.basename(file))
    z.close()

    for file in os.listdir(path):
        try:
            os.remove(os.path.join(path, file))
        except Exception as e: print(e)
    os.rmdir(path)
    
    
def load(path):

    with zipfile.ZipFile(path) as z:
        path = path.replace('.model','')
        z.extractall(path)
    
    files = tuple(map(lambda x: os.path.join(path, x), os.listdir(path)))

    def _loadnp(files, list_):
        files = sorted(files, key=lambda x: \
                       int(os.path.basename(x).split('_')[1].replace('.pickle','')))
        for file in files:
            with open(file, 'rb') as f:
                list_.append(np.load(f))
    
    with open(os.path.join(path,'main.pickle'), 'rb') as f:
        main = pickle.load(f)

    main.activations = []
    main.weights = []
    main.deltas = []
    main.errors = []

    _loadnp(filter(lambda x: 'activation_' in x, files), main.activations)
    _loadnp(filter(lambda x: 'weight_'     in x, files), main.weights)
    _loadnp(filter(lambda x: 'deltas_'     in x, files), main.deltas)
    _loadnp(filter(lambda x: 'errors_'     in x, files), main.errors)

    for file in os.listdir(path):
        try:
            os.remove(os.path.join(path, file))
        except Exception as e: print(e)
    try: os.rmdir(path)
    except Exception as e: print(e)
    
    return main        
