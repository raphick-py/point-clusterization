#!/usr/bin/bash
import matplotlib.pyplot as plt
import numpy as np
import mod
import seaborn as sns
import pandas as pd


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


if __name__ == "__main__":
    ax = plt.subplots()
    stations = mod.stationsd()
    X = mod.creation_sys_cords(0.1)
    matrix = create_matrix(stations)
    matrix = pd.DataFrame(matrix, index=(X[::-1]), columns=X)
    ax = sns.heatmap(matrix)
    xrang = np.arange(0, 100, 0.1)
    k = -1
    b = 100
    graph1 = plt.plot(xrang, k*xrang + b, 'k', color='blue')
    plt.show()
    scatter1 = plt.scatter(stations['1']['x_cords'],
                           stations['1']['y_cords'])
    scatter2 = plt.scatter(stations['2']['x_cords'],
                           stations['2']['y_cords'])
    scatter3 = plt.scatter(stations['3']['x_cords'],
                           stations['3']['y_cords'])
