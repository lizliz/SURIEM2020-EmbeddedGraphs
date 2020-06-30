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
    print("\nType 'Exit' at any time to stop.")
    answer = input("Outlier? Press enter for no. \nType anything else (except for 'Exit') for yes. ")
    if answer == "exit":
        print("\nYou stopped at", letter + str(i))
        print("\nMake sure you don't lose the outliers you've picked so far.")
        break
    elif answer != "":
        one = letter + str(i)
        outliers.append(one)

['F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15', 'F16', 'F17', 'F18', 'F19', 'F20', 'F21', 'F22', 'F23', 'F24', 'F25', 'F26', 'F27', 'F28', 'F29', 'F30', 'F31', 'F32', 'F33', 'F34', 'F35', 'F36', 'F37', 'F38', 'F39', 'F40', 'F41', 'F42', 'F43', 'F44', 'F45', 'F46', 'F47', 'F48', 'F49', 'F50', 'F51', 'F52', 'F53', 'F54', 'F55', 'F56', 'F57', 'F58', 'F59', 'F60', 'F61', 'F62', 'F63', 'F64', 'F65', 'F66', 'F67', 'F68', 'F69', 'F70', 'F71', 'F72', 'F73', 'F74', 'F75', 'F76', 'F77', 'F78', 'F79', 'F80', 'F81', 'F82', 'F83', 'F84', 'F85', 'F86', 'F87', 'F88', 'F89', 'F90', 'F91', 'F92', 'F93', 'F94', 'F95', 'F96', 'F97', 'F98', 'F99', 'F100', 'F101', 'F102', 'F103', 'F104', 'F105', 'F106', 'F107', 'F108', 'F109', 'F110', 'F111', 'F112', 'F113', 'F114', 'F115', 'F116', 'F117', 'F118', 'F119', 'F120', 'F121', 'F122', 'F123', 'F124', 'F125', 'F126', 'F127', 'F128', 'F129', 'F130', 'F131', 'F132', 'F133', 'F134', 'F135', 'F136', 'F137', 'F138', 'F139', 'F140', 'F141', 'F142', 'F143', 'F144', 'F145', 'F146', 'F147', 'F148', 'F149']
    