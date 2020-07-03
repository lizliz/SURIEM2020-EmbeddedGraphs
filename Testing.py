#Levent Batakci
#6/10/2020
#
#Testing file for many scripts
import Compare
import Merge
import networkx as nx
import math
import Visualization as v
import lib.Tools as t
import matplotlib.pyplot as plt

T1 = nx.Graph()
T2 = nx.Graph()
T3 = nx.Graph()

nodes_t1 = ['m1', 'm2', 's1', 's2']
edges_t1 = [('m1','m2'),('s1','m2'),('m2','s2')]
pos1 = {
'm1': (1,16),
'm2': (3,18),
's1': (5,10),
's2': (0,11)
}

T1.add_nodes_from(nodes_t1)
T1.add_edges_from(edges_t1)

#Visualization.input_output(T1, pos1)
Merge.calc_values_height(T1, pos1, math.pi / 2)
M1 = Merge.merge_tree(T1, normalize=False)

nodes_t2 = ['m3', 'm4', 's3','s4','sk','sl']
edges_t2 = [('m3','m4'),('s3','m4'),('m4','s4'),('sk','s3'),('sl','s3')]
pos2 = {
'm3': (2,19),
'm4': (-2,20),
's3': (-1,18),
's4': (3,17),
'sk': (4,18),
'sl': (9,16)
}

T2.add_nodes_from(nodes_t2)
T2.add_edges_from(edges_t2)

v.input_output(T2, pos2)
Merge.calc_values_height(T2, pos2, math.pi / 2)
M2 = Merge.merge_tree(T2, normalize=False)

nodes_t3 = ['m5', 'm6', 's5','a','g']
edges_t3 = [('s5','m5'),('m5','m6'),('a','s5'),('g','s5')]
pos3 = {
'm5': (3,1),
'm6': (-2,-1),
's5': (-1,-2),
'a': (1,-3),
'g': (1,-4),
}

T3.add_nodes_from(nodes_t3)
T3.add_edges_from(edges_t3)

#Visualization.input_output(T3, pos3)
Merge.calc_values_height(T3, pos3, math.pi / 2)
M3 = Merge.merge_tree(T3, normalize=False)

#printCompare.descendants(M3, 'm5'))
#print(Compare.IsEpsSimilar(M1, M2, 1.9999))
#print(Compare.IsEpsSimilar(M1, M2, 1.99))

#Visualization.compare(M1, pos1, M2, pos2, n_size = 500, labels = True, valid=True)
#Visualization.compare(M3, pos3, M2, pos2, n_size = 500, labels = True, valid=True)
v.compare(M1, pos1, M3, pos3, n_size = 500, labels = True, valid=True)

mapping = Compare.morozov_distance(M1, M3, valid=True, get_map=True)[1]


nodes1 = ["m1", "m2", "m3", "m4", "m5", "s1", "s2", "s3", "s4"]
edges1 = [("m1","s1"),("m2","s1"),("m3","s2"),("m4","s3"),("m5","s3"),("s1","s2"),("s2","s4"),("s3","s4")]
pos1 = {
        "m1": (-3,3),
        "m2": (-1,3),
        "m3": (0,0),
        "m4": (1,9),
        "m5": (4,7),
        "s1": (-2,6),
        "s2": (0,11),
        "s3": (2,10),
        "s4": (0,13) 
        }

T1 = nx.Graph()
T1.add_nodes_from(nodes1)
T1.add_edges_from(edges1)
#Visualization.input_output(T1, pos1)
Merge.calc_values_height_reorient(T1, pos1)
#t.shift_centroid(M1, pos1)
t.shift_center(pos1)
M1 = Merge.merge_tree(T1, normalize=False)

#Rotate M1
# r = t.get_rad(pos1)
# for i in range(0, 360):
#     Merge.calc_values_height_reorient(T1, pos1, math.pi* (1/2 + 1/90))
#     M1 = Merge.merge_tree(T1, normalize=False)
    
#     fig = plt.subplots(1,3,figsize=(20,10))

#     ax = plt.subplot(121)
#     ax.set_xlim(-1*r, r)
#     ax.set_ylim(-1*r, r)
#     nx.draw(T1, pos1, ax, node_size=50)
    
#     ax = plt.subplot(122)
#     ax.set_xlim(-1*r, r)
#     ax.set_ylim(-1*r, r)
#     nx.draw(M1, pos1, ax, node_size=50)
    
#     plt.show()
#     plt.close()
    

nodes2 = ["m6", "m7", "m8", "m9", "m10", "s5", "s6", "s7", "s8"]
edges2 = [("m6","s5"),("m7","s6"),("m8","s6"),("s6","s5"),("m9","s7"),("s5","s7"),("s7","s8"),("m10","s8")]
pos2 = {
        "m6": (-4,1),
        "m7": (-2,4),
        "m8": (-1,3),
        "m9": (0,0),
        "m10": (3,7),
        "s5": (-2.5,6),
        "s6": (-1.5,5),
        "s7": (0,11),
        "s8": (0,13) 
        }

T2 = nx.Graph()
T2.add_nodes_from(nodes2)
T2.add_edges_from(edges2)
#Visualization.input_output(T2, pos2)
Merge.calc_values_height_reorient(T2, pos2)
M2 = Merge.merge_tree(T2, normalize=False)


