#!/usr/bin/python
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from scipy.stats import multivariate_normal
from drawing import create_matrix
from mod import stationsd
from mod import creation_sys_cords
from sklearn.mixture import GaussianMixture
from drawing import find_local_max
from drawing import transform_to_matrix

style.use('fivethirtyeight')

# This module use em algorithm for data from mod and drawing
# 0. Create dataset
def create_dataset():
    stations = stationsd()
    X = creation_sys_cords(0.1)
    matrix = create_matrix(stations)
    m = find_local_max(matrix)
    matrix = transform_to_matrix(m)
    m = np.rot90(matrix, k=1, axes=(1,0))
    m = find_local_max(m)
    matrix = transform_to_matrix(m)
# matrix = np.rot90(matrix, k=1, axes=(1,0))
    s = int(matrix.sum())
    X = np.zeros((s,2))
    Y = np.zeros(s)
    s = 0
    for i in range(len(matrix)):
        for k in range(len(matrix[i])):
            for m in range(int(matrix[i][k])):
                X[s] = i,k
                s += 1
    return X,Y

if __name__ == "__main__":
    X,Y = create_dataset()
    x,y = np.meshgrid(np.sort(X[:,0]),np.sort(X[:,1]))
    XY = np.array([x.flatten(),y.flatten()]).T
    GMM = GaussianMixture(n_components=3).fit(X) # Instantiate and fit the model
    print('Converged:',GMM.converged_) # Check if the model has converged
    means = GMM.means_
    print(means)
    covariances = GMM.covariances_
# Predict
    Y = np.array([[0.5],[0.5]])
    prediction = GMM.predict_proba(Y.T)
    print(prediction)
# Plot
    fig = plt.figure(figsize=(10,10))
    ax0 = fig.add_subplot(111)
    ax0.scatter(X[:,0],X[:,1], c=prediction)
    #ax0.scatter(Y[0,:],Y[1,:],c='orange',zorder=10,s=100)
    for m,c in zip(means,covariances):
        multi_normal = multivariate_normal(mean=m,cov=c)
        ax0.contour(np.sort(X[:,0]),np.sort(X[:,1]),multi_normal.pdf(XY).reshape(len(X),len(X)),colors='black',alpha=0.3)
        ax0.scatter(m[0],m[1],c='grey',zorder=10,s=100)

    plt.savefig('em.png')
