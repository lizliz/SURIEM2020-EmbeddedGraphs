#Levent Batakci 
#6/16/20
#
#Let's test merge because somehow it still doesn't work
#
# ;(
from Merge import calc_values_height_reorient, merge_tree, reduced, is_merge_tree
import Visualization as v
import Compare as c
import math
import networkx as nx
import Merge as m

edges1 = [(1, 8),
 (1, 10),
 (15, 8),
 (15, 12),
 (15, 13),
 (8, 4),
 (4, 14),
 (4, 3),
 (4, 6),
 (10, 7),
 (10, 9),
 (7, 5),
 (3, 11),
 (11, 2)]

pos1 ={1: (-10379, -6247),
 2: (-11698, -6509),
 3: (-9262, -2347),
 4: (-1698, 1533),
 5: (-2763, 770),
 6: (-7184, -3480),
 7: (-10577, 3513),
 8: (-7800, 2775),
 9: (-6990, 77),
 10: (-2861, -3624),
 11: (-7261, -1644),
 12: (-8876, -2526),
 13: (-9508, 524),
 14: (-11918, -6530),
 15: (-6457, -3505)}


G1 = nx.Graph()
G1.add_edges_from(edges1)
calc_values_height_reorient(G1, pos1)
M1 = merge_tree(G1)
is_merge_tree(M1)

edges2 =[(1, 3),
 (1, 9),
 (1, 12),
 (15, 3),
 (15, 4),
 (15, 10),
 (3, 5),
 (3, 2),
 (5, 13),
 (5, 8),
 (13, 14),
 (8, 11),
 (4, 6),
 (14, 7)]

pos2 = {1: (-2254, 574),
 2: (-1813, 572),
 3: (-2021, 735),
 4: (-2462, 348),
 5: (-1464, 1244),
 6: (-1892, 0),
 7: (-1344, 515),
 8: (-2324, 1126),
 9: (-1254, -214),
 10: (-2111, 1082),
 11: (-1840, 545),
 12: (-2660, 1247),
 13: (-1473, 619),
 14: (-2568, 619),
 15: (-2513, 1206)}


G2 = nx.Graph()
G2.add_edges_from(edges2)
calc_values_height_reorient(G2, pos2)
M2 = merge_tree(G2)
is_merge_tree(M2)

v.compare(M1, pos1, M2, pos2)
