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

edges = [(1, 7), (1, 11), (1, 4), (15, 7), (15, 6), (7, 14), (11, 8), (4, 13), (13, 9), (13, 12), (9, 3), (12, 2), (6, 10), (3, 5)]

pos = {1: (3238, -4627),
 2: (-80, -2415),
 3: (-4421, -6009),
 4: (-4146, -5529),
 5: (-7379, -6993),
 6: (4227, -9328),
 7: (2865, -7714),
 8: (1767, -894),
 9: (-650, -6661),
 10: (-6520, -8028),
 11: (-7097, -1767),
 12: (-5917, -3543),
 13: (-2330, -5529),
 14: (1886, -11240),
 15: (2289, -5662)}



G = nx.Graph()

G.add_edges_from(edges)

calc_values_height_reorient(G, pos, math.pi/2)

print(G.nodes)

v.input_output(G, pos)

#M = merge_tree(G)
#print(nx.is_forest(M))
#print(nx.is_connected(M))
#print(reduced(M))

