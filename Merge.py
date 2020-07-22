#Levent Batakci
#6/8/2020
#
#This program is designed to compute a merge tree, given a graph.
from lib.Tools import listify_nodes, list_append, f_, find_p, find_c, get_leaves, ancestry, height, reorient
import networkx as nx
import numpy as np
import math


#Sets all the function values based on height
def calc_values_height(G, pos, angle):
    direction = [math.cos(angle), math.sin(angle)]
    
    x = direction[0]
    y = direction[1]
    if(len(direction) > 2 or (x==0 and y==0)):
        print("Faulty input direction!")
        return
    
    #Get the list of node objects
    n = listify_nodes(G)
    
    #Set all of the function values by height
    for i in range(0, len(n)):
        n[i]['value'] = height(pos[n[i]['name']], angle)


# Run this function on a graph before constructing its merge tree
# This will modify the original graph object
# G: Networx Graph whose nodes all have at least 2 attributes 
#      (attributes corresponding to cartesian coordinates)
# pos: position dictionary of all nodes 
#      containing the node names as keys and cartesian coordinate tuples as values
# angle: angle by which you want to rotate the graph before constructing the merge tree
#      `None` taking the original position as given by the coordinates
#      to be the desired orientation
def calc_values_height_reorient(G, pos, angle=None):
    
    #Get the list of node objects
    n = listify_nodes(G)
    
    if(angle!=None):
        reorient(pos, angle)
        
        #Set all of the function values by height
        for i in range(0, len(n)):
            n[i]['value'] = height(pos[n[i]['name']], math.pi / 2)
            
    else:
        for i in range(0, len(n)):
            n[i]['value'] = pos[n[i]['name']][1]

#comparing the maximum distance between the two matricies by subtracting them
#and taking the absolute value of each entry. The largest entry will be the
#distance. Added (6/2/2020)
def compare_trees(x,y):
    distanceMatrix = np.subtract(x,y)
    distances = []
    #print(distanceMatrix)
    for row in range(0,len(distanceMatrix)):
        for entry in range(0,len(distanceMatrix)):
            distances.append(abs(distanceMatrix.item(row,entry)))      
    return max(distances)

#Calculates the interleaving distance between two nodes
#Also sets the proper entries in the distances matrix
def calc_set_distance(anc, i1, i2, M, distances):
    n = list(M.nodes)
    
    #The two nodes corresponding to the given indices.
    n1 = n[i1]
    node1 = M.nodes[n1]
    n2 = n[i2]
    node2 = M.nodes[n2]
    
    #Make sure node 1 doesn't have the greater function value
    if(f_(node1) > f_(node2)):
        n1, n2 = n2, n1
        node1, node2 = node1, node2
    
    #The ancestry lines of n1 and n2, respectively
    a1 = [n1]
    a1.list_append(anc[n1])
    a2 = [n2]
    a2.list_append(anc[n2])
    
    #Find the common ancestor
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

def find_root(T):
     nodes = listify_nodes(T)
     
     max_ = f_(nodes[0])
     max_node = nodes[0]
     for n in nodes:
         if(f_(n) > max_):
             max_ = f_(n)
             max_node = n
             
     return max_node['name']

def regular(M, node, root):
    return node != root and len(M[node]) == 2

def reduce(M):
    nodes = list(M.nodes)
    
    r = find_root(M)
    for n in nodes:
        if(regular(M, n, r)):
            nei1 = list(M[n])[0]
            nei2 = list(M[n])[1]
            M.add_edge(nei1,nei2)
            
            M.nodes[nei1]['p'] = nei2
            
            M.remove_node(n)

def reduced(M):
    r = find_root(M)
    
    nodes = list(M.nodes)
    
    for n in nodes:
        if(len(M[n]) == 2 and n != r):
            return False
    return True

def is_merge_tree(M):
    acyclic = nx.is_forest(M)
    connected = nx.is_connected(M)
    red = reduced(M)
    
    print('---')
    print("M is acyclic: " + str(acyclic))
    print("M is connected: " + str(connected))
    print("M is reduced: " + str(red))
    print('---')
    
    return acyclic and connected and red


def median_f(M):
    nodes = listify_nodes(M)
    nodes.sort(key=f_)
    
    num = len(nodes)
    
    n1 = nodes[math.ceil((num-1)/2)]
    n2 = nodes[math.floor((num-1)/2)]
    med = (f_(n1)+f_(n2))/2
    
    return med

def mean_f(M):
    nodes = listify_nodes(M)
    
    avg = 0
    for n in nodes:
        avg += f_(n)
    return avg / len(nodes)
    
def shift_f(M, center = "median"):
    if center == "median":
        center = median_f(M)
    elif center == "mean":
        center = mean_f(M)
    else:
        print("Invalid center parameter. Valid choices are 'median' and 'mean'. Using median for shifting.")
        center = median_f(M)
        
    nodes = listify_nodes(M)
    for n in nodes:
        n['value'] = n['value'] - center

def on_level_neighbors(G, n):
    f = f_(G.nodes[n])
    
    neighbors = G[n]
    on_lvl = []
    for nei in neighbors:
        if(f_(G.nodes[nei]) == f):
            on_lvl.append(nei)
            
    return on_lvl

#Collapse n2 into n1
def collapse(G, n1, n2, merge=False):
    n2_neighbors = G[n2]
    
    for nei in n2_neighbors:
        if(nei != n1):
            G.add_edge(n1, nei)
            #Update the parent
            if(merge):
                G.nodes[nei]['p'] = n1
                
    G.remove_node(n2)
    
def update_neighbors(G, n1, neighbors, n2):
    lvl_neighbors = on_level_neighbors(G, n2)
    
    for nei in lvl_neighbors:
        if(nei not in neighbors and nei != n1):
            neighbors.append(nei)
    
def collapse_neighbors(G, n, processed, merge=False):
    lvl_neighbors = on_level_neighbors(G, n)
    
    count=0
    while(len(lvl_neighbors) >= 1):
        nei = lvl_neighbors[0]
        
        #add new on-level neighbors (from what we'll collapse)
        update_neighbors(G, n, lvl_neighbors, nei)
        
        #Collapse the first neighbor
        collapse(G, n, nei, merge=merge)
        lvl_neighbors.remove(nei)
        processed[nei] = True #Mark the neighbor as processed
        
        count +=1
        
    #G.nodes[n]['collapsed'] = True
        
    return count

#Collapse all of the on-level neighbors in a given graph
def preprocess(G):
    #Purge all self-loops
    for e in list(G.edges):
        if(e[0] == e[1]):
            G.remove_edge(e[0], e[1])
            
    nodes = list(G)
    
    #Stores whether or not a node has been processed already
    processed = {}
    
    #Initialize all the dictionary
    for n in nodes:
        processed[n] = False
    
    #Process all the nodes
    i=0
    while(i < len(nodes)):
        n = nodes[i]
        if(processed[n] == False):
            c = collapse_neighbors(G, n, processed)
            
            # if(c > 0):
            #     print("Collapsed " + str(n))
            
            #Mark the node as processed
            processed[n] = True
        
        #Show progress! 
        # if(i%100 == 0):
        #     print(i)
        
        i+=1    

#Node on merge tree level connected to roots
def find_on_level(M, roots, f):
    for r in roots:
        p = find_p(r, M)
        
        if(f_(M.nodes[p]) == f):
            return p
    return None

#Adds a node to the merge tree
#n_=node name, G=graph, M=merge tree
#
#NOTE: In our paper, we describe "parent" and "child" pointers.
#      Here, those correspond to node attributes ['p'] and ['c'], respectively.
def add_node(n_, G, M):
    #The actual node
    n = G.nodes[n_] 
    f = f_(n) #The node's value
    
    #Get all the children
    neighbors = G[n_]
    true_children = []
    for nei in neighbors:
        if(f_(G.nodes[nei]) < f): #Is child
            true_children.append(nei)
    
    #No children => leaf
    if(len(true_children) == 0):
        M.add_node(n_) #Create a copy of n in M
        n['c'] = n_ #Own inferior
        M.nodes[n_]['p'] = n_ #Own superior
        M.nodes[n_]['value'] = f #Function value
        return
    
    #Get the roots of the children
    roots = []
    min_root = find_c(true_children[0], G)
    for c in true_children:
        r = find_c(c, G)
        if(r not in roots): #Add the root if it is new
            roots.append(r)
            if(f_(G.nodes[r]) < f_(G.nodes[min_root])): #Update the min root
                min_root = r

    
    #1 child => just update inferior
    if(len(roots) == 1):
        n['c'] = roots[0]
        return
        
    #2 or MORE children => merge
    if(len(roots) >= 2):
        M.add_node(n_) #Create a copy of n in M
        M.nodes[n_]['p'] = n_ #Own parent
        M.nodes[n_]['value'] = f #Function value
        
        for r in roots:
            p = find_p(r, M) #What we connect to
            if(p != n_): #Add Edge
                M.add_edge(p, n_)    
                M.nodes[p]['p'] = n_ #Update the superior
                if(f_(M.nodes[p]) == f):
                    processed = {}
                    collapse_neighbors(M, n_, processed, merge=True)
        
        #set c as the inferior of n and all other roots
        n['c'] = min_root
        for r in roots:
            G.nodes[r]['c'] = min_root
        
 
#Construct the merge tree given a graph G with function values.
#Returns a networkx tree with a position dictionary for drawing
#G: NetworkX Graph
#shift: Boolean, whether you want to shift the function values by the average
def merge_tree(G, shift=True):
    preprocess(G)
    
    #Get the nodes from the networkx graph
    nodes = listify_nodes(G)
    nodes.sort(key=f_)
    
    #The legendary Merge Tree
    M = nx.Graph()
    for i in range(0, len(nodes)):
        add_node(nodes[i]['name'], G, M)
    
    reduce(M)
    if(shift):
        shift_f(M)
        
    return M            
