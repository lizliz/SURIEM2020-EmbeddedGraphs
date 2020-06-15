#Levent Batakci
#6/8/2020
#
#Testing file
import networkx as nx
import Visualization as v
import DataReader as dr
from lib.Tools import random_tree_and_pos
from Merge import calc_values_height
import math
import Merge
import Compare
import timeit
import time


n = 15

tests = 1000
for i in range(0, tests):
    TP = random_tree_and_pos(n)
    G1 = TP[0]
    pos1 = TP[1]
    Merge.calc_values_height(G1, pos1, math.pi/2)
    M1 = Merge.merge_tree(G1)
    print("M1 is merge tree: " + str(nx.is_forest(M1) and nx.is_connected(M1)))
    
    TP = random_tree_and_pos(n)
    G2 = TP[0]
    pos2 = TP[1]
    Merge.calc_values_height(G2, pos2, math.pi/2)
    M2 = Merge.merge_tree(G2)
    print("M2 is merge tree: " + str(nx.is_forest(M2) and nx.is_connected(M2)))
    
    TP = random_tree_and_pos(n)
    G3 = TP[0]
    pos3 = TP[1]
    Merge.calc_values_height(G3, pos3, math.pi/2)
    M3 = Merge.merge_tree(G3)
    print("M3 is merge tree: " + str(nx.is_forest(M3) and nx.is_connected(M3)))
    
    v.compare(M1, pos1, M2, pos2)
    
    dxy = Compare.morozov_distance(M1, M2, 0.1)
    dxz = Compare.morozov_distance(M1, M3, 0.1)
    dzy = Compare.morozov_distance(M3, M2, 0.1)
    
    dif = min(dxy + dxz - dzy, dxy + dzy - dxz, dxz + dzy - dxy)
    print(dif)
    
    if(dif < 0):
        "HUZZAH!"
        i=tests+1
        