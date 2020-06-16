#Levent Batakci
#6/10/2020
#
#Testing file for many scripts
import Compare
import Merge
import networkx as nx
import math
import Visualization

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
M1 = Merge.merge_tree(T1)

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

Visualization.input_output(T2, pos2)
Merge.calc_values_height(T2, pos2, math.pi / 2)
M2 = Merge.merge_tree(T2)

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
M3 = Merge.merge_tree(T3)

print(Compare.descendants(M3, 'm5'))
print(Compare.IsEpsSimilar(M1, M2, 1.9999))
print(Compare.IsEpsSimilar(M1, M2, 1.99))

Visualization.compare(M1, pos1, M2, pos2, n_size = 500, labels = True)
Visualization.compare(M3, pos3, M2, pos2, n_size = 500, labels = True)
Visualization.compare(M1, pos1, M3, pos3, n_size = 500, labels = True)
