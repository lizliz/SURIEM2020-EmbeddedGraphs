#Levent Batakci
#6/19
#
#Testing for monotonicness
import networkx as nx
import Merge as m
import math
import Compare as c
import matplotlib.pyplot as plt
import Visualization as v

edges1 = [(1,2), (2,3)]
pos1 = {1: (-2,1), 2: (0,4), 3: (-1,0)}

G1 = nx.Graph()
G1.add_edges_from(edges1)

edges2 = [(1,2), (2,3)]
pos2 = {1: (-2,7), 2: (0,8), 3: (-1,6)}

G2 = nx.Graph()
G2.add_edges_from(edges2)

v.distance_data(G1, pos1, G2, pos2, frames= 1440, rotate_both=False)