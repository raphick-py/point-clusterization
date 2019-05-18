#!/usr/bin/python
from time import localtime, mktime, sleep
import math
import sys
import numpy as np

a = np.array([[1,1,1,1,1,1],[2,2,2,2,1,2],[2,2,2,2,1,1]])

for i in range(len(a)):
    for j in range(len (a[i])):
        if a[i][j] == 1:
            a[i][j]+=5
print(a)
