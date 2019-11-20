# /dust/src/structs/metrics

# Package
import __init__

# Additional Packages
import pandas as pd
import matplotlib.pyplot as plt

def accuracy(model, X, Y):
    correct_count = 0
    for i,x in enumerate(X):
        if(model.forward_prop(x).argmax() == Y[i].argmax()):
            correct_count+=1
    return correct_count/len(X)

def confusion_matrix(model, X, Y):

    Yp = [model.forward_prop(x).argmax() for x in X]
    Ya = list(map(lambda x: x.argmax(), Y))
    
    yp = pd.Series(Yp, name='Predicted')
    ya = pd.Series(Ya , name='Actual')

    cmatrix = pd.crosstab(ya,yp)#, rownames=['Actual'], colnames=['Predicted'], margins=True)

    return cmatrix

def plot_performance(conf_matrix, cmap=plt.cm.gray_r):
    plt.matshow(conf_matrix, cmap=cmap)
    plt.colorbar()
    tick_marks = np.arange(len(conf_matrix.columns))
    plt.xticks(tick_marks, conf_matrix.columns, rotation=45)
    plt.yticks(tick_marks, conf_matrix.index)
    plt.ylabel(conf_matrix.index.name)
    plt.xlabel(conf_matrix.columns.name)
    plt.show()
