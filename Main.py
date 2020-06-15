#Levent Batakci
#6/8/2020
#
#Testing file
import networkx as nx
import Visualization as v
import DataReader as dr
import math
import Merge
import Compare
import timeit
import time


vert = "./data/athens_small_vertices_osm.txt"
edge = "./data/athens_small_edges_osm.txt"

graph = dr.read_txt(edge, vert)
G1 = graph[0] #nx graph
pos1 = graph[1] #position dic

components = nx.connected_components(G1)
#for c in components:
    #print(len(c))
    
G1.remove_node(363972226.0)
G1.remove_node(1540878773.0)

Merge.calc_values_height(G1, pos1, math.pi/2)
M1 = Merge.merge_tree(G1)

vert = "./data/chicago_vertices_osm.txt"
edge = "./data/chicago_edges_osm.txt"

graph = dr.read_txt(edge, vert)
G2 = graph[0] #nx graph
pos2 = graph[1] #position dic

components = nx.connected_components(G2)
G2 = G2.subgraph(list(components)[0])
    
Merge.calc_values_height(G2, pos2, math.pi/2)
M2 = Merge.merge_tree(G2)

#v.input_output(G, pos)
#v.input_output_square(G, pos)
#v.animate(G, pos, 60, "/animations/test1")

#print(Compare.morozov_distance(M1,M2))

G2 = G1.copy()
pos2 = pos1.copy()
v.compare_many(G1,pos1, G2,pos2, 10)