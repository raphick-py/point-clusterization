from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
import matplotlib.pyplot as plt
import testem

x1 = np.array([3, 1, 1, 2, 1, 6, 6, 6, 5, 6, 7, 8, 9, 8, 9, 9, 8])
x2 = np.array([5, 4, 5, 6, 5, 8, 6, 7, 6, 7, 1, 2, 1, 2, 3, 2, 3])

#plt.plot()
#plt.xlim([0, 10])
#plt.ylim([0, 10])
#plt.title('Dataset')
#plt.scatter(x1, x2)
#plt.show()

# create new plot and data
#plt.plot()
X, Y = testem.create_dataset()
colors = ['b', 'g', 'r']
markers = ['o', 'v', 's']

# k means determine k
distortions = []
K = range(1,10)
for k in K:
    kmeanModel = KMeans(n_clusters=k).fit(X)
    kmeanModel.fit(X)
    distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])

# Plot the elbow
plt.plot(K, distortions, 'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k')
#plt.show()



from scipy.cluster.hierarchy import fcluster

Z = linkage(X, 'ward')
max_d = 100
clusters = fcluster(Z, 3, criterion='maxclust')
plt.figure(figsize=(10, 8))
plt.scatter(X[:,0], X[:,1], c=clusters, cmap='prism')  # plot points with cluster dependent colors
plt.show()


#last = Z[-10:, 2]
#last_rev = last[::-1]
#idxs = np.arange(1, len(last) + 1)
#plt.plot(idxs, last_rev)
#acceleration = np.diff(last, 2)
#acceleration_rev = acceleration[::-1]
#plt.plot(idxs[:-2] + 1, acceleration_rev)
#plt.show()
#k = acceleration_rev.argmax() + 2  # if idx 0 is the max of this we want 2 clusters
#print ("clusters:", k)

