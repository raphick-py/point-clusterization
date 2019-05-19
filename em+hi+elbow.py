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
from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster.hierarchy import fcluster
import seaborn as sns
import pandas as pd


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


def em(X, Y, k):
    x, y = np.meshgrid(np.sort(X[:, 0]), np.sort(X[:, 1]))
    XY = np.array([x.flatten(), y.flatten()]).T
    GMM = GaussianMixture(n_components=int(k)).fit(X)  # Instantiate and fit the model
    print('Converged:', GMM.converged_)  # Check if the model has converged
    means = GMM.means_
    #print(means)
    covariances = GMM.covariances_
# Predict
    Y = np.array([[0.5], [0.5]])
    prediction = GMM.predict_proba(Y.T)
    print(prediction)
# Plot
    fig = plt.figure(figsize=(10, 10))
    ax0 = fig.add_subplot(111)
    ax0.scatter(X[:, 0], X[:, 1])
    #ax0.scatter(Y[0,:],Y[1,:],c='orange',zorder=10,s=100)
    for m, c in zip(means, covariances):
        multi_normal = multivariate_normal(mean=m, cov=c)
        ax0.contour(np.sort(X[:, 0]), np.sort(X[:, 1]), multi_normal.pdf(XY).reshape(len(X), len(X)), colors='black', alpha=0.3)
        ax0.scatter(m[0], m[1], c='grey', zorder=10, s=100)

    plt.savefig('result/em.png')


def kmean(X, k):
    Z = linkage(X, 'ward')
    clusters = fcluster(Z, k, criterion='maxclust')
    if int(k) == 4:
        for i in range(len(clusters)):
            if clusters[i] == 2:
                clusters[i] += 5
    print(clusters)
    plt.figure(figsize=(10, 8))
    plt.scatter(X[:, 0], X[:, 1], c=clusters, cmap='prism')  # plot points with cluster dependent colors
    plt.savefig('result/kmean.png')


def elbow(X):
    distortions = []
    K = range(1, 10)
    for k in K:
        kmeanModel = KMeans(n_clusters=k).fit(X)
        kmeanModel.fit(X)
        distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])

# Plot the elbow
    plt.plot(K, distortions, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Искажение')
    plt.title('The Elbow Method показывает оптимельное k')
    plt.savefig('result/elbow.png')
    plt.show()


def dendrogramma(X):
    linked = linkage(X, 'single')
    plt.figure(figsize=(10, 7))
    dendrogram(linked,
               truncate_mode='lastp',
               p=12,
               orientation='top',
               distance_sort='descending',
               show_leaf_counts=True,
               show_contracted=True)
    plt.savefig('result/dendrogram')
    plt.show()


def heatmap(inmatrix, modmatrix):
    x = plt.subplots()
    X = creation_sys_cords(0.1)
    matrixd = pd.DataFrame(inmatrix, index=(X[::-1]), columns=X)
    ax = sns.heatmap(matrixd)
    xrang = np.arange(0, 100, 0.1)
    k = -1
    b = 100
    graph1 = plt.plot(xrang, k*xrang + b, 'k', color='blue')
    plt.savefig('result/heat1.png')
    print('a')
    ax = plt.subplots()
    matrix1 = pd.DataFrame(modmatrix, index=(X[::-1]), columns=X)
    ax = sns.heatmap(matrix1)
    plt.savefig('result/heat2.png')


X, Y, initmat, modifmatr = create_dataset()
elbow(X)
dendrogramma(X)
k = input()
kmean(X, k)
em(X, Y, k)
heatmap(initmat, modifmatr)
