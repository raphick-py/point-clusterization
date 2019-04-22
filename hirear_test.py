#!/usr/bin/python
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
import testem

#X = np.array([[5,3],
#                  [10,15],
#                  [15,12],
#                  [24,10],
#                  [30,30],
#                  [85,70],
#                  [71,80],
#                  [60,78],
#                  [70,55],
#                  [80,91],])
X,Y = testem.create_dataset()
linked = linkage(X, 'single')

#labelList = range(1, 11)

plt.figure(figsize=(10, 7))
dendrogram(linked,
                       truncate_mode='lastp',
                       p=12,
                       orientation='top',
                      # labels=labelList,
                      #  labels=labelList,
                       distance_sort='descending',
                       show_leaf_counts=True,
                       show_contracted=True)
plt.show()
