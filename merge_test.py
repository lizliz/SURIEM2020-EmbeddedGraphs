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

edges1 = [(1, 15), (8, 6), (5, 15), (2, 15), (9, 6), (15, 6)]

pos1 ={1: (-6792, 4347),
 2: (-7271, 4637),
 3: (-6837, 4730),
 4: (-6930, 4523),
 5: (-6953, 4632),
 6: (-7138, 4812),
 7: (-7085, 4442),
 8: (-6988, 4465),
 9: (-7028, 4706),
 10: (-7181, 4797),
 11: (-6802, 4597),
 12: (-6942, 4695),
 13: (-6886, 4842),
 14: (-6969, 4797),
 15: (-6824, 4751)}


G1 = nx.Graph()
G1.add_edges_from(edges1)
calc_values_height_reorient(G1, pos1, math.pi/2)
M1 = merge_tree(G1)
is_merge_tree(M1)

edges2 =[(7, 5),
 (13, 3),
 (2, 1),
 (14, 1),
 (4, 6),
 (11, 3),
 (10, 3),
 (15, 3),
 (3, 1),
 (1, 5),
 (5, 6)]

pos2 = {1: (-6593, -2911),
 2: (-6699, -4042),
 3: (-5089, -2928),
 4: (-5334, -3156),
 5: (-5356, -2781),
 6: (-5731, -2379),
 7: (-6450, -4219),
 8: (-4966, -4114),
 9: (-6620, -3937),
 10: (-6589, -2971),
 11: (-5004, -3004),
 12: (-5343, -2898),
 13: (-5189, -4127),
 14: (-5679, -3591),
 15: (-6621, -2954)}

G2 = nx.Graph()
G2.add_edges_from(edges2)
calc_values_height_reorient(G2, pos2, math.pi/2)
M2 = merge_tree(G2)
is_merge_tree(M2)

v.compare(M1, pos1, M2, pos2)


#v.input_output(G, pos)

#M = merge_tree(G)
#print(nx.is_forest(M))
#print(nx.is_connected(M))
#print(reduced(M))

