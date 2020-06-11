#Levent Batakci
#6/10/2020
#
#Testing file for many scripts
import Compare
import Merge
import networkx as nx
import math
import Visualization

bip = nx.Graph()

def ghostify(list_):
    for i in range(len(list_)):
        list_[i] = "GHOST " + str(list_[i])

nodesA = [1, 2, 3]
nodesB = [4, 5, 6]

ghosts = [1,6]
ghostify(ghosts)

edges = [(1,4), (2,5), (3,4), (1,"GHOST 1"), (6,"GHOST 6")]

bip.add_nodes_from(nodesA)
bip.add_nodes_from(nodesB)
bip.add_nodes_from(ghosts)
bip.add_edges_from(edges)

list_A = [2,3]
list_B = [4,5]

#print(Compare.has_perfect_matching(bip, list_A, list_B))


T1 = nx.Graph()
T2 = nx.Graph()

nodes_t1 = ["m1", "m2", "m3", "m4", "m5", "s1", "s2", "s3", "s4"]
edges_t1 = [("m1","s1"),("m2","s1"),("m3","s2"),("m4","s3"),("m5","s3"),("s1","s2"),("s2","s4"),("s3","s4")]
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

T1.add_nodes_from(nodes_t1)
T1.add_edges_from(edges_t1)
#Visualization.input_output(T1, pos1)
Merge.calc_values_height(T1, pos1, math.pi / 2)
M1 = Merge.merge_tree(T1)


nodes_t2 = ["m6", "m7", "m8", "m9", "m10", "s5", "s6", "s7", "s8"]
edges_t2 = [("m6","s5"),("m7","s6"),("m8","s6"),("s6","s5"),("m9","s7"),("s5","s7"),("s7","s8"),("m10","s8")]
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

T2.add_nodes_from(nodes_t2)
T2.add_edges_from(edges_t2)
#Visualization.input_output(T2, pos2)
Merge.calc_values_height(T2, pos2, math.pi / 2)
M2 = Merge.merge_tree(T2)

#print(Compare.descendants(M1, "s1"))

#print(Compare.IsEpsSimilar(M1, M2, 1.9999, ["s4", "s8"]))
#print(Compare.IsEpsSimilar(M1, M2, 1.99, ["s4", "s8"]))
#print(Compare.IsEpsSimilar(M2, M1, 1, ["s8", "s4"]))
Compare.morozov_distance(M1, M1, 0.05)

