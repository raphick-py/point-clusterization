#!/usr/bin/python
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from scipy.stats import multivariate_normal
import pandas as pd
import seaborn as sns
from drawing import create_matrix
from mod import stationsd
from mod import creation_sys_cords
from sklearn.mixture import GaussianMixture
from drawing import find_local_max
from drawing import transform_to_matrix
from sklearn.cluster import KMeans
from sklearn import metrics
#from scipy.spatial.distance import cdist
#from scipy.cluster.hierarchy import dendrogram, linkage
#from scipy.cluster.hierarchy import fcluster
from minisom import MiniSom
#import seaborn as sns
#import pandas as pd

style.use('fivethirtyeight')


def create_dataset():
    stations = stationsd()
    X = creation_sys_cords(0.1)
    matrix = create_matrix(stations)
    initmatrix = matrix  # for drawing matrix to draw heatmap
    m = find_local_max(matrix)
    matrix = transform_to_matrix(m)
    modifmatrix = matrix  # matrix after threshold
    m = np.rot90(matrix, k=1, axes=(1, 0))
    m = find_local_max(m)
    matrix = transform_to_matrix(m)
# matrix = np.rot90(matrix, k=1, axes=(1,0))
    s = int(matrix.sum())
    X = np.zeros((s, 2))
    Y = np.zeros(s)
    s = 0
    for i in range(len(matrix)):
        for k in range(len(matrix[i])):
            for m in range(int(matrix[i][k])):
                X[s] = i, k
                s += 1
    return X, Y, initmatrix, modifmatrix

X, Y, initmat, modifmatr = create_dataset()
som = MiniSom(10, 10, 2, sigma=2, learning_rate=0.5,
              neighborhood_function='triangle', random_seed=10)
som.pca_weights_init(X)
som.train_batch(X, 40000)
plt.figure(figsize=(8, 8))
plt.scatter(X[:, 0], X[:, 1])
#visit_order = np.argsort([som.winner(p)[1] for p in X])
#plt.plot(X[visit_order][:,0], X[visit_order][:,1])
plt.show()
#plt.figure(figsize=(8, 8))
print(som.distance_map())
#plt.pcolor(som.distance_map().T, cmap='bone_r')
X = np.arange(0,10)
matrixd = pd.DataFrame(som.distance_map(), index=(X), columns=X)
ax = sns.heatmap(matrixd)
plt.show()
