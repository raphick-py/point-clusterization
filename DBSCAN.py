#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
from drawing import create_matrix
from mod import stationsd
from mod import creation_sys_cords
from drawing import find_local_max
from drawing import transform_to_matrix
from sklearn.manifold import TSNE
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from EmHiElbow import kmean, em, heatmap


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
kmean(X, 3)
em(X, Y, 3)
heatmap(initmat, modifmatr)
plt.figure(figsize=(10, 8))
clustering = DBSCAN(eps=7, min_samples=15).fit(X)
unique, counts = np.unique(clustering.labels_, return_counts=True)
dictor = dict(zip(unique, counts))
print('####################')
print(dictor)
colordict = {0: 'red',
             1: 'green',
             2: 'blue',
             3: 'brown',
             4: 'orange',
             5: 'pink',
             6: 'gray',
             7: 'navy',
             8: 'violet',
             9: 'yellow',
             10: 'indigo',
             11: 'aqua',
             12: 'hotpink',
             13: 'goldenrod',
             14: 'maroon',
             15: 'aquamarine',
             16: 'lawngreen',
             17: 'purple',
             18: 'mahenta',
             19: 'palegreen',
             20: 'chocolate',
             21: 'coral',
             22: 'rosybrown',
             23: 'darkhaki',
             24: 'mediumseagreen'}
for i in range(0, X.shape[0]):
    for key in dictor:
        if key == -1:
            c3 = plt.scatter(X[i, 0], X[i, 1], c='black', marker='*')
        else:
            if clustering.labels_[i] == key and dictor[key] >= 10:
                c1 = plt.scatter(X[i, 0], X[i, 1], c=colordict[key])
            elif clustering.labels_[i] == key and dictor[key] <= 10:
                c2 = plt.scatter(X[i, 0], X[i, 1], c='black', marker='*')
plt.title('DBSCAN нашел кластера и шум')
plt.savefig('result/dbscan.png')
#plt.show()
