#Levent Batakci
#6/10/2020
#
#Testing file for many scripts
import Compare
import networkx as nx

bip = nx.Graph()

def ghostify(list_):
    for i in range(len(list_)):
        list_[i] = "GHOST " + str(list_[i])

nodesA = [1, 2, 3]  `
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

print(Compare.has_perfect_matching(bip, list_A, list_B))