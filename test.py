# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 11:43:36 2020

@author: Levent
"""
import Visualization as v
import DataReader as dr
import math
import Merge as m
import Compare as c
import time
import networkx as nx
import lib.Tools as t


vert = "./data/athens_small_vertices_osm.txt"
edge = "./data/athens_small_edges_osm.txt"

graph = dr.read_txt(edge, vert)
G1 = graph[0] #nx graph
pos1 = graph[1] #position dic

largest_cc = max(nx.connected_components(G1), key=len)
G1 = G1.subgraph(largest_cc)

m.calc_values_height_reorient(G1, pos1)
M1 = m.merge_tree(G1)

vert = "./data/chicago_vertices_osm.txt"
edge = "./data/chicago_edges_osm.txt"

graph = dr.read_txt(edge, vert)
G2 = graph[0] #nx graph
pos2 = graph[1] #position dic

largest_cc = max(nx.connected_components(G2), key=len)
G2 = G2.subgraph(largest_cc)

m.calc_values_height_reorient(G2, pos2)
M2 = m.merge_tree(G2)

g = t.random_component(G2, 200, draw=True, pos=pos2)
g = t.random_component(G2, 200, draw=True, pos=pos2, color='mediumvioletred')
g = t.random_component(G2, 200, draw=True, pos=pos2, color='blue')