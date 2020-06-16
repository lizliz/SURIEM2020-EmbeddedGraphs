#Levent Batakci 
#6/16/20
#
#Let's test merge because somehow it still doesn't work
#
# ;(
from Merge import calc_values_height_reorient, merge_tree, reduced
import Visualization as v
import math
import networkx as nx


nodes = ['1', '2', '3', '4', '5', 'L' , 'R']
edges = [('1','2'),('2','3'),('3','4'),('4','5'), ('L','2'), ('R','4')]
pos = {
'1': (1,0),
'2': (1,1),
'3': (2,1),
'4': (3,1),
'5': (3,0),
'L': (0,1),
'R': (4,1)
}

G = nx.Graph()

G.add_nodes_from(nodes)
G.add_edges_from(edges)

calc_values_height_reorient(G, pos, math.pi/2)

v.input_output(G, pos)

M = merge_tree(G)
print(nx.is_forest(M))
print(nx.is_connected(M))
print(reduced(M))

