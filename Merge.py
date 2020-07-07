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
    
def normalize_f(M, center = "median"):
    if center == "median":
        center = median_f(M)
    elif center == "mean":
        center = mean_f(M)
    else:
        print("Invalid center parameter. Valid choices are 'median' and 'mean'. Using median for normalization.")
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
def collapse(G, n1, n2):
    n2_neighbors = G[n2]
    
    for nei in n2_neighbors:
        if(nei != n1):
            G.add_edge(n1, nei)
            
    G.remove_node(n2)
    
def update_neighbors(G, n1, neighbors, n2):
    lvl_neighbors = on_level_neighbors(G, n2)
    
    for nei in lvl_neighbors:
        if(nei not in neighbors and nei != n1):
            neighbors.append(nei)
    
def collapse_neighbors(G, n, processed):
    lvl_neighbors = on_level_neighbors(G, n)
    
    count=0
    while(len(lvl_neighbors) >= 1):
        nei = lvl_neighbors[0]
        
        #add new on-level neighbors (from what we'll collapse)
        update_neighbors(G, n, lvl_neighbors, nei)
        
        #Collapse the first neighbor
        collapse(G, n, nei)
        lvl_neighbors.remove(nei)
        processed[nei] = True #Mark the neighbor as processed
        
        count +=1
        
    #G.nodes[n]['collapsed'] = True
        
    return count

#Collapse all of the on-level nodes in a given graph
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
#NOTE: In our paper, we describe "superior" and "inferior" pointers.
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
        #Check if there is already a connected rep. on the level
        rep = find_on_level(M, roots, f)
        if(rep != None):
            #Add all the edges
            for r in roots:
                p = find_p(r, M) #What we connect to
                if(p != rep): #Add Edge
                    M.add_edge(p, rep)
                M.nodes[p]['p'] = rep #Update the superior
        else: #New node
            M.add_node(n_) #Create a copy of n in M
            M.nodes[n_]['p'] = n_ #Own parent
            M.nodes[n_]['value'] = f #Function value
            
            for r in roots:
                p = find_p(r, M) #What we connect to
                if(p != n_): #Add Edge
                    M.add_edge(p, n_)
                M.nodes[p]['p'] = n_ #Update the superior
        
        #set c as the inferior of n and all other roots
        n['c'] = min_root
        for r in roots:
            G.nodes[r]['c'] = min_root
        
 
#Construct the merge tree given a graph G with function values.
#Returns a networkx tree with a position dictionary for drawing
def merge_tree(G, normalize=True):
    preprocess(G)
    
    #Get the nodes from the networkx graph
    nodes = listify_nodes(G)
    nodes.sort(key=f_)
    
    #The legendary Merge Tree
    M = nx.Graph()
    for i in range(0, len(nodes)):
        add_node(nodes[i]['name'], G, M)
    
    reduce(M)
    if(normalize):
        normalize_f(M)
    return M            
    
# def get_value_set(G):
#     n = list(G)
#     f_vals = [f_(G.nodes[n[i]]) for i in range(0, len(n))]
#     f_vals.sort() #Sort the list
#     f_vals = np.unique(f_vals) #Remove duplicates!
    
#     return f_vals

# #Optimized Gamma method
# #Returns all the relevant gamma end indices
# #These apply to a sorted nodelist of G
# def calc_gamma_indices(G, nodes):
#     end_indices = []
#     val = f_(nodes[0])
#     for i in range(0, len(nodes)):
#         #Set the current node
#         n = nodes[i]
        
#         #Check if a new value has been reached
#         if(val != f_(n)):
#             val = f_(n) #Update val
#             end_indices.append(i) #Append the found end-index
            
#     #Account for the trivial last end-index
#     end_indices.append(len(nodes))
            
#     return end_indices   

# #For drawing purposes.
# def position_rep(S, nodes, a):
#     for n in nodes:
#         if(f_(S.nodes[n]) == a):
#             return n
        
#     #Should always return..
    
       
# #Returns the set of mu corresponding to the proper sublevel set
# def get_gamma(G, labels, index, a):
#     sublevel_set = G.subgraph(labels[:index])
    
#     components = list(nx.connected_components(sublevel_set))
#     gamma = [] #The second list just contains the pos rep
#     pos = {}
#     for c in components:
#         muu = mu(sublevel_set, c)
#         gamma.append(muu)
#         pos[str(muu)] = position_rep(sublevel_set, c, a)
    
    
#     return (gamma, pos)

# #Weak minima
# def is_minima(G, n):
#     f = f_(G.nodes[n])
    
#     neighbors = G[n]
#     for nei in neighbors:
#         if(f_(G.nodes[nei]) < f): #Found a lower neighbor
#             return False
        
#     return True

# #Returns the minima in connected component
# #S is the sublevel set and nodes is the list of nodes in the connected component
# def mu(S, nodes):
#     minima = []
#     for n in nodes:
#         if(is_minima(S, n)):
#             minima.append(n)
            
#     return minima
  
# #Returns True if arr2 is contained in arr1
# def is_subset(arr1, arr2):
#     d = np.setdiff1d(arr2, arr1)
#     print(d)
#     return (len(d) == 0)

# #Returns the difference of a set of sets
# def set_diff(arr1, arr2):
#     diff = []
#     for x in arr1:
#         for y in arr2:
#             d = np.setdiff1d(x, y)
#             if(len(d) != 0):
#                 diff.append(d)
                
#     return diff

# #Adds the nodes from the changes at 'a'
# def add_nodes(G, end_indices, f, i, labels, M, pos):
#     a = f[i]
    
#     gNew = get_gamma(G, labels, end_indices[i], a)
#     newPos = gNew[1]
#     print(newPos)
#     print(pos)
#     gammaNew = np.array(gNew[0])
    
#     gammaOld = []
#     if(i > 0):
#         gammaOld = np.array(get_gamma(G, labels, end_indices[i-1], a)[0])
        
#     new_nodes = set_diff(gammaNew, gammaOld)
#     print(new_nodes)
#     subsets = set_diff(gammaOld, gammaNew)
    
#     new_names = [str(n) for n in new_nodes]
#     #Add the new vertices
#     M.add_nodes_from(new_names)
    
#     #Set the function values
#     for n in new_names:
#         M.nodes[n]['value'] = a
    
#     #Add the edges and positions
#     for i in range(0, len(new_nodes)):
#         v1 = new_nodes[i]
#         pos_rep=newPos[str(v1)]
#         print(pos_rep)
#         pos[str(v1)] = pos[pos_rep] 
        
#         j = 0
#         while(j < len(subsets)):
#             v2 = subsets[j]
            
#             #Check for adjacency
#             if(is_subset(v1, v2)):
#                 M.add_edge( (str(v1), str(v2)))
#                 subsets.remove(v2)
#             else:
#                 j+=1            

# def merge_tree_(G, pos, normalize=True):
#     #Pre-process the tree: Collapse all adjacent nodes on the same level
#     preprocess(G)
    
#     #Get a sorted set of all function values
#     f_vals = get_value_set(G)
    
#     #Calculate the relevant gamma indices
#     nodes = listify_nodes(G)
#     nodes.sort(key=f_)
#     end_indices = calc_gamma_indices(G, nodes)
    
#     #Get the node names
#     names = [n['name'] for n in nodes]
    
#     #Go through f_vals to add all the nodes and edges
#     M = nx.Graph()
#     for i in range(0, len(f_vals)):
#         add_nodes(G, end_indices, f_vals, i, names, M, pos)
        
#     return M
    
    