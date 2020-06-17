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

#Adds a node to the merge tree
#n_=node name, G=graph, M=merge tree
def add_node(n_, G, M):
    #The actual node
    n = G.nodes[n_] 
    f = f_(n) #The node's value
    
    children = list(G[n_]) #Note: This contains the parent as well.
    cr=n_ #tentative child rep
    
    c_count = 0 #Disconnected child count
    to_add = []
    for i in range(0, len(children)):
        relative = G.nodes[children[i]]
        
        #Relative is a child or a neighbor
        if(f_(relative) <= f):
            if('c' in relative):
                rel_cr = find_c(children[i], G)
                
                #Not already connected to child
                if(rel_cr != cr):
                    #Add to the list of children to merge
                    to_add.append(rel_cr)
                    
                    #New representative child!
                    if(f_(G.nodes[rel_cr]) <= f_(G.nodes[cr])):
                        cr=rel_cr
    
    p = n_   
    c_count=len(to_add)
    #Leaf                   
    if(c_count==0):
        M.add_node(n_,value=f) #Add new leaf to merge tree
        M.nodes[n_]['p']=p # Update the parent (THIS IS KIND OF REDUNDANT) 
    #Merge
    elif(c_count>1):
        edges = []
        
        #Check if there's already a node on this level that is representative of
        #one of the components to add
        first_on_lvl = True
        for i in range(0, len(to_add)):
            rep_ = find_p(to_add[i], M) #The "representative parent of the child" before addition
            if(f_(M.nodes[rep_]) == f): #Found node on level
                first_on_lvl = False
                p=rep_ #There won't be a new merged node - we found one to connect to
                        
        #Update findings
        G.nodes[p]['c']=cr #Update child rep of the node we connected to

        #Only create a new node if it'd be the first one on the level
        if(first_on_lvl):
            M.add_node(n_, value=f, p=n_) #Add new vertex to merge tree
        
        #Calculate the edges
        for i in range(0, len(to_add)):
            rep_ = find_p(to_add[i], G) #The "representative parent of the child" before addition
            if(rep_ != p):
                edges.append( (p, rep_) ) #Add the edge
             
            #Set the most direct parent of the connected representative
            M.nodes[rep_]['p'] = p
        
        #Update stuff
        for i in range(0, len(to_add)):
            rep_ = find_p(to_add[i], G)
            G.nodes[rep_]['p']=p
            G.nodes[to_add[i]]['c']=cr #Update the rep child of the node from the list
        
        #Add the edges
        M.add_edges_from(edges)
        
        M.nodes[p]['p'] = p #A node is its own parent until otherwise
        
    #Update findings
    G.nodes[p]['c']=cr #Update child rep of the node we connected to
    G.nodes[p]['p']=p

    n['c']=cr #Update the child rep of the added node and parent node. This must always be done
    n['p']=p #Update the parent rep of the newly added node
    
    return p

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

#Construct the merge tree given a graph G with function values.
#Returns a networkx tree with a position dictionary for drawing
def merge_tree(G):
    #Get the nodes from the networkx graph
    nodes = listify_nodes(G)
    
    #Sort the nodes in order of increasing function value
    nodes.sort(key=f_)
    
    #The legendary Merge Tree
    M = nx.Graph()
    for i in range(0, len(nodes)):
        add_node(nodes[i]['name'], G, M)
    
    reduce(M)
    return M