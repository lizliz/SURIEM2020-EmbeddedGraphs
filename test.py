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

G = nx.Graph()
G.add_nodes_from([1,2,3,4,5])

nodes = list(G.nodes)
print(nodes)
G.remove_node(5)
print(nodes)


vert = "./data/athens_small_vertices_osm.txt"
edge = "./data/athens_small_edges_osm.txt"

graph = dr.read_txt(edge, vert)
G1 = graph[0] #nx graph
pos1 = graph[1] #position dic

comp = list(nx.connected_components(G1))
G1 = G1.subgraph(comp[0])

m.calc_values_height_reorient(G1, pos1)
M1 = m.merge_tree(G1)

vert = "./data/chicago_vertices_osm.txt"
edge = "./data/chicago_edges_osm.txt"

graph = dr.read_txt(edge, vert)
G2 = graph[0] #nx graph
pos2 = graph[1] #position dic

comp = list(nx.connected_components(G2))
G2 = G2.subgraph(comp[0])

m.calc_values_height_reorient(G2, pos2)
M2 = m.merge_tree(G2)

print("Starting Comparison...")
start = time.time()
v.compare(M1, pos1, M2, pos2)
print(time.time()-start)