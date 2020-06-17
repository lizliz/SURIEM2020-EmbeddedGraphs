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

tests = 10000
i=0
errors = "" #String keeping track of the forest errors
forest_lst = [] #list keeping track of the cyclic graphs
poss = [] #list keeping track of the positions in the cyclic graphs
key_lst = [] # list keeping track of the key error graphs
key = "" #string keeping track of the key errors
posk = []

for i in range(0, tests):
    if(i % 25 == 0):
        print(i)
        
    TP = random_tree_and_pos(n)
    G1 = TP[0]
    pos1 = TP[1]
    Merge.calc_values_height(G1, pos1, math.pi/2)
    try:
        M1 = Merge.merge_tree(G1)
    except KeyError:
        print("Key Error When making G1 a merge tree! Most likely from line 171 in Merge.py")
        key_lst.append((G1, "KeyError when making this Graph into Merge"))
        key += "\nKey Error When making G1 a merge tree! Most likely from line 171 in Merge.py"
        posk.append(pos1)
    if(not nx.is_forest(M1)):
        print("M1 is not a forest!!!")
        errors += "\nM1 is not a forest!!!"
        forest_lst.append((G1,M1))
        poss.append(pos1)
    if(not nx.is_connected(M1)):
        print("M1 is not connected!!!")
        errors += "\nM1 is not connected!!!"
        poss.append(pos1)
        forest_lst.append((G1,M1))
    if(not Merge.reduced(M1)):
        print(M1)
        print("M1 is not reduced")
        poss.append(pos1)
        errors += "\nM1 is not reduced!!!"
        forest_lst.append((G1,M1))
        
    TP = random_tree_and_pos(n)
    G2 = TP[0]
    pos2 = TP[1]
    Merge.calc_values_height(G2, pos2, math.pi/2)
    #M2 = Merge.merge_tree(G2)
    try:
        M2 = Merge.merge_tree(G2)
    except KeyError:
        print("Key Error When making G2 a merge tree! Most likely from line 171 in Merge.py")
        key_lst.append((G2, "KeyError when making this Graph into Merge"))
        key += "\nKey Error When making G2 a merge tree! Most likely from line 171 in Merge.py"
        posk.append(pos2)
    if(not nx.is_forest(M2)):
        print("M2 is not a forest!!!")
        errors += "\nM2 is not a forest!!!"
        poss.append(pos2)
        forest_lst.append((G2,M2))
    if(not nx.is_connected(M2)):
        print("M2 is not connected!!!")
        errors += "\nM2 is not connected!!!"
        poss.append(pos2)
        forest_lst.append((G2,M2))
    if(not Merge.reduced(M2)):
        print("M2 is not reduced")
        errors += "\nM2 is not reduced!!!"
        poss.append(pos2)
        forest_lst.append((G2,M2))
    
    TP = random_tree_and_pos(n)
    G3 = TP[0]
    pos3 = TP[1]
    Merge.calc_values_height(G3, pos3, math.pi/2)
    try:
        M3 = Merge.merge_tree(G3)
    except KeyError:
        print("Key Error When making G3 a merge tree! Most likely from line 171 in Merge.py")
        key_lst.append((G3, "KeyError when making this Graph into Merge"))
        key += "\nKey Error When making G3 a merge tree! Most likely from line 171 in Merge.py"
        posk.append(pos3)
    if(not nx.is_forest(M3)):
        print("M3 is not a forest!!!")
        forest_lst.append((G3,M3))
        poss.append(pos3)
        errors += "\nM3 is not a forest!!!"
    if(not nx.is_connected(M3)):
        forest_lst.append((G3,M3))
        poss.append(pos3)
        print("M3 is not connected!!!")
        errors += "\nM3 is not connected!!!"
    if(not Merge.reduced(M3)):
        poss.append(pos3)
        forest_lst.append((G3,M3))
        print("M3 is not reduced")
        errors += "\nM3 is not reduced!!!"
    
    try:
        Compare.morozov_distance(M1, M2, 0.1)
    #except KeyError:
    #    print("")
    except KeyError:
        print("Key Error with M1 and M2!!!!!!")
        key_lst.append((M1, M2))
        v.compare(M1, pos1, M2, pos2, labels=True, n_size=500)
        key += "\nKey Error with M1 and M2!!!!!!"
        
    try:
        Compare.morozov_distance(M1, M3, 0.1)
    #except KeyError:
    #    print("")
    except KeyError:
        print("Key Error with M1 and M3!!!!!!")
        key_lst.append((M1, M3))
        v.compare(M1, pos1, M3, pos3, labels=True, n_size=500)
        key += "\nKey Error with M1 and M3!!!!!!"
        
    try:
        Compare.morozov_distance(M2, M3, 0.1)
    #except KeyError:
    #    print("")
    except KeyError:
        print("Key Error with M2 and M3!!!!!!")
        v.compare(M2, pos2, M3, pos3, labels=True, n_size=500)
        key_lst.append((M2, M3))
        key += "\nKey Error with M2 and M3!!!!!!"
  
    #v.compare(M1, pos1, M2, pos2, labels=True, n_size=500)
    #dxy = Compare.morozov_distance(M1, M2, 0.1)
    #v.compare(M1, pos1, M3, pos3, labels=True, n_size=500)
    #dxz = Compare.morozov_distance(M1, M3, 0.1)
    #v.compare(M3, pos3, M2, pos2, labels=True, n_size=500)
    #dzy = Compare.morozov_distance(M3, M2, 0.1)
    
    #dif = min(dxy + dxz - dzy, dxy + dzy - dxz, dxz + dzy - dxy)
    #print("dif:" + str(dif))
    print('-')
    
    #if(dif < -5):        
        #print("HUZZAH!")
        #print(pos1)
        #print(pos2)
        #print(pos3)
        #break
print("All Errors: ", errors)