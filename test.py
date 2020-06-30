# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 11:43:36 2020

@author: Levent
"""
#import Visualization as v
import DataReader as dr
import math
import Merge as m
import Compare as c
import time
import networkx as nx
import lib.Tools as t
import matplotlib.pyplot as plt

# vert = "./data/athens_small_vertices_osm.txt"
# edge = "./data/athens_small_edges_osm.txt"

# graph = dr.read_txt(edge, vert)
# G1 = graph[0] #nx graph
# pos1 = graph[1] #position dic

# largest_cc = max(nx.connected_components(G1), key=len)
# G1 = G1.subgraph(largest_cc)

# m.calc_values_height_reorient(G1, pos1)
# M1 = m.merge_tree(G1)

# vert = "./data/chicago_vertices_osm.txt"
# edge = "./data/chicago_edges_osm.txt"

# graph = dr.read_txt(edge, vert)
# G2 = graph[0] #nx graph
# pos2 = graph[1] #position dic

# largest_cc = max(nx.connected_components(G2), key=len)
# G2 = G2.subgraph(largest_cc)

# m.calc_values_height_reorient(G2, pos2)
# M2 = m.merge_tree(G2)

# g = t.random_component(G2, 200, draw=True, pos=pos2)
# g = t.random_component(G2, 200, draw=True, pos=pos2, color='mediumvioletred')
# g = t.random_component(G2, 200, draw=True, pos=pos2, color='blue')

################## Code for picking out outlier letters ######################
key = {"0":"K","1":"N","2":"L","3":"Z","4":"T","5":"X","6":"F","7":"V","8":"Y","9":"W","10":"H","11":"A","12":"I","13":"E","14":"M"}
letters = {"K":"0","N":"1","L":"2","Z":"3","T":"4","X":"5","F":"6","V":"7","Y":"8","W":"9","H":"10","A":"11","I":"12","E":"13","M":"14"}
p = "data/Letter-low"
ds = "Letter-low"
z = dr.read_tud(p,ds,False)

outliers = [] # Make sure you comment this out if you stop and try to pick up again
              # otherwise you'll lose your progress
              
num = letters["K"] # Change the "K" to be the letter you want, then run
letter = key[num]

# Shouldn't need to touch this
for i in range(150):
    g = z[0][num][i]
    g = t.main_component(G = g, report = False)
    nx.draw(g, t.get_pos(g))
    plt.title(str(i))
    plt.show()
    print("\nType 'exit' at any time to stop.")
    answer = input("Outlier? Press enter for no. \nType anything else (except for 'exit') for yes. ")
    if answer == "exit":
        print("\nYou stopped at", letter + str(i))
        print("\nMake sure you don't lose the outliers you've picked so far.")
        break
    elif answer != "":
        one = letter + str(i)
        outliers.append(one)