# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 20:18:29 2020

@author: Leven
"""
import networkx as nx
import Merge as m
import DataReader as dr


nodes = [1,2,3,4,5,6,7]
edges = [(1,4),(2,4),(3,6),(4,6),(7,4),(7,5)]

G = nx.Graph()
G.add_edges_from(edges)

pos = {1: (1,0),
       2: (3,0),
       3: (0,1),
       4: (2,2),
       5: (4,1),
       6: (1,3),
       7: (3,3)}

m.calc_values_height_reorient(G, pos)
M = m.merge_tree(G)

vert = "./data/chicago_vertices_osm.txt"
edge = "./data/chicago_edges_osm.txt"

graph = dr.read_txt(edge, vert)
G2 = graph[0] #nx graph
pos2 = graph[1] #position dic

m.calc_values_height_reorient(G2, pos2)
M2 = m.merge_tree(G2)
