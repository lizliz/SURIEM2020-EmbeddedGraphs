# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 12:47:54 2020

@author: Levent
"""
import networkx as nx


edges = [(1,2),(2,3),(3,4)]
pos={
     1: (0,0),
     2: (0,1),
     3: (1,1),
     4: (1,0)}

G = nx.Graph()
G.add_edges_from(edges)

nx.draw(G, pos, with_labels=False, node_size=5000)