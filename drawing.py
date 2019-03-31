#!/usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
import mod
import seaborn as sns
import pandas as pd
from math import sqrt
from scipy.signal import find_peaks

# Module which create heatmap of airplane, without clusters algorithm

# creates matrix of pilings from coordinates of station
def create_matrix(stations):
    dot_dict = mod.for_draw(stations)
    X = mod.creation_sys_cords(0.01)
    matrix = np.zeros((100, 100))
    for stack in dot_dict.values():
        for Y in stack.values():
            p = 0
            x = 0
            y = 0
            for i in Y:
                y1 = int(i / 0.1)
                x1 = int(X[p] / 0.1)
                p += 1
                if x1 < 100 and y1 < 100 and x1 >= 0 and y1 >= 0:
                    if y1 != y and x1 != x:
                        y = y1
                        x = x1
                        matrix[-y][x] += 1
    return matrix


# search local maximum in matrix of pilings return string[a, {dict}]
# a-number, a = row*10+string, in dict-value
def find_local_max(matrix):
    threshold = matrix.max() / sqrt(5)
    local_max = find_peaks(np.ravel(matrix), height=threshold)
    return local_max


def transform_to_matrix(local_max):
    matrix = np.zeros((100, 100))
    addr = local_max[0]
    value = local_max[1]['peak_heights']
    for i in range(len(addr)):
        x = addr[i] % 100
        y = addr[i] // 100
        matrix[y][x] = value[i]
    return matrix

if __name__ == "__main__":
    ax = plt.subplots()
    stations = mod.stationsd()
    X = mod.creation_sys_cords(0.1)
    matrix = create_matrix(stations)
    matrixd = pd.DataFrame(matrix, index=(X[::-1]), columns=X)
    ax = sns.heatmap(matrixd)
    xrang = np.arange(0, 100, 0.1)
    k = -1
    b = 100
    graph1 = plt.plot(xrang, k*xrang + b, 'k', color='blue')
    plt.savefig('heat1.png')
    print('a')
    ax = plt.subplots()
    m = find_local_max(matrix)
    matrix1 = transform_to_matrix(m)
    matrix1 = pd.DataFrame(matrix1, index=(X[::-1]), columns=X)
    ax = sns.heatmap(matrix1)
    plt.savefig('heat2.png')
    scatter1 = plt.scatter(stations['1']['x_cords'],
                           stations['1']['y_cords'])
    scatter2 = plt.scatter(stations['2']['x_cords'],
                           stations['2']['y_cords'])
    scatter3 = plt.scatter(stations['3']['x_cords'],
                           stations['3']['y_cords'])
