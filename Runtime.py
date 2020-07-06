# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 21:12:53 2020

@author: Levent
"""
import time
import Merge as m
import lib.Tools as t
import DataCalculations as d
import matplotlib.pyplot as plt
import numpy as np

min_= 5
max_ = 100
comparetimes = []
mergetimes = []
size = []
for i in range(min_, max_ + 1):
    print(i)
    
    g = t.random_tree_and_pos(i)
    G1 = g[0]
    pos1 = g[1]
    
    start_time = time.time()
    m.calc_values_height_reorient(G1, pos1)
    M1 = m.merge_tree(G1)
    M2 = M1.copy()
    t_ = time.time() - start_time
    print("merge time: " + str(t_))
    mergetimes.append(t_)
    
    leaves = len(t.get_leaves(M1))
    size.append(leaves)
    
    start_time = time.time()
    dif = d.average_distance(G1, pos1, G1.copy(), pos1, frames=45)
    t_ = time.time()-start_time
    print("compare time: " + str(t_))
    comparetimes.append(t_)
    
x = np.array(range(25))
y = x ** 2 / 4

# Create the plot
plt.scatter(x,y)
    
plt.scatter(size, comparetimes)

plt.show()