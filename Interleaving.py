#Levent Batakci
#Union-Find data structure basics and testing notebook
#6/1/2020
import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import math
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from MergeTree import *
from Drawing import *


############INTERLEAVING MATRICES###################
#Adds all the elements in L2 to the end of L1, preserving order
def get_leaves(M) :
    n = list(M.nodes)
    
    #Find all of the leaves by checking every node
    leaves = []
    for i in range(0, len(n)):
        if(is_leaf_f(M, n[i])):
            leaves.append(n[i])
    
    return leaves

def list_append(L1, L2):
    for i in range(0,len(L2)):
        L1.append(L2[i])

#Computes and sets the lines of ancestry, given a merge tree and a node
def ancestry_line(M, n,ancestry_dict):
    node = M.nodes[n]
    
    #The ancestry line has already been computed
    if(n in ancestry_dict):
        return 
    
    line = []
    
    #If we aren't at the root...
    if(node['p'] != n):
        p = node['p']
        line.append(p) #Add the parent!
        
        ancestry_line(M, p, ancestry_dict) #Get the rest of the line recursively
        list_append(line,ancestry_dict[p])
    #Why did I use recursion here? Well, this guarantees that we will never do any
    #calculation twice. Consequently, we only need to call ancestry_line on all the leaves.
    
    ancestry_dict[n] = line

#Computes the ancestry dictionary, given a merge tree
#Returns a dictionary
def ancestry(M):
    ancestry_dict= {}
    
    leaves = get_leaves(M)
    for i in range(0,len(leaves)):
        ancestry_line(M, leaves[i], ancestry_dict)
    
    return ancestry_dict

#Calculates the interleaving distance between two nodes
#Also sets the proper entries in the distances matrix
def calc_set_distance(anc, i1, i2, M, distances):
    n = list(M.nodes)
    
    #Distance has already been calculated
    if(distances[i1][i2] != -1):
        return distances[i1][i2]
    
    #The two nodes corresponding to the given indices.
    #We want f(n1) <= f(n2)
    n1 = n[i1]
    node1 = M.nodes[n1]
    n2 = n[i2]
    node2 = M.nodes[n2]
    
    #Make sure node 1 doesn't have the greater function value
    if(f_(node1) > f_(node2)):
        n1, n2 = n2, n1
        node1, node2 = node1, node2
    
    #The ancestry lines of n1 and n2, respectively
    a1 = anc[n1]
    a2 = anc[n2]
    
    #Distance of a node to itself is its function value
    #(not 0)
    if(n1 == n2):
        f = f_(node1)
        distances[i1][i2] = f
        distances[i2][i1] = f
        return f
        
    #Node 2 is an ancestor of node 1
    #Note: node 1 will never be an ancestor of node 2 bc
    #      we ensured that f(n1) <= f(n2)
    if(n2 in a1):
        f = f_(node2)
        distances[i1][i2] = f
        distances[i2][i1] = f
        return f
    
    #We need to find the common ancestor
    for i in range(0, len(a2)):
        if(a2[i] in a1):
            f = f_(M.nodes[a2[i]])
            distances[i1][i2] = f
            distances[i2][i1] = f
            return f
        

#Returns the interleaving distances matrix with labeling as well.
def interleaving_distances(M):
    n = get_leaves(M) #Only leaves matter
    
    ancestry_dict = ancestry(M)
    
    #Set up the square matrix of interleaving distances
    distances = []
    for i in range(0, len(n)):
        distances.append([])
        for j in range(0, len(n)):
            distances[i].append(-1) #Meaningless number, just for initialization
            
    for i in range(0, len(n)):
        for j in range(i, len(n)):
            calc_set_distance(ancestry_dict,i,j,M,distances)
    
    return (np.matrix(distances), n)   
    


##TESTING METHODS##
def draw_w_pos(G, pos):
    ax = plt.subplot(131)
    ax.title.set_text("Input Graph")
    nx.draw(G, pos, ax, with_labels=True,node_color="blue",node_size=700)
     
def IL_test(M):
    IL = interleaving_distances(M)
    print("Labels:" + str(IL[1]))
    print(IL[0])
    return IL
###################

#####TESTING#######
G = nx.Graph()
nodes = list( [1,2,3,4,5,6,7,8,9,11] )
edges = [(1,4),(2,4),(5,4),(6,4),(6,7),(3,5),(7,5),(8,2),(8,11),(9,11),(9,7),(7,8)]
G.add_nodes_from(nodes)
G.add_edges_from(edges)

pos_dict= {
        1: (1,0) ,
        2: (3,0) ,
        3: (0,1) ,
        4: (2,1) ,
        5: (2,2) ,
        6: (3,2) ,
        7: (3,3) ,
        8: (4,1.5) ,
        9: (6,1) ,
        11: (5,0) ,
        }
angle = math.pi / 2
calc_values_height_reorient(G, pos_dict, angle)

#f_vals = {}
#f_vals[1 ]= {'value': 3}
#f_vals[2 ]= {'value': 2}
#f_vals[3 ]= {'value': 1}
#f_vals[4 ]= {'value': 2}
#f_vals[5 ]= {'value': 1}
#f_vals[6 ]= {'value': 1}
#f_vals[7 ]= {'value': 2}
#f_vals[8 ]= {'value': 2.5}
#f_vals[9 ]= {'value': 3}
#f_vals[10]= {'value': 4}
#nx.set_node_attributes(G,f_vals)

fig = plt.subplots(1,3,figsize=(15,5))

add_arrow()

#Draw G
draw_w_pos(G,pos_dict)

#Calculate height values

#Make the mergre tree
M = merge_tree(G)

#Interleaving
IL = IL_test(M)

##DRAWING MERGE
draw_pretty_f(M)

plt.show()
#testing distance
#print(compare_trees(IL[0],IL[0]))

####################