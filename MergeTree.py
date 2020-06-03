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
from Interleaving import *
from Drawing import *

###Merge Tree Construction###
###Merge Tree Construction###
#Returns the function value of a node
def f_(node):
    return node['value']

def listify_nodes(G):
    n = list(G.nodes)
    n_list = []
    for i in range(0, len(n)):
        G.nodes[n[i]]['name'] = n[i]
        n_list.append(G.nodes[n[i]])
    return n_list

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
        #Relative is a child
        if(f_(relative) < f):
            #Does this work? idk
            rel_cr = relative['c_rep']
            rel_cr = M.nodes[rel_cr]['p_rep']
            rel_cr = G.nodes[rel_cr]['c_rep']
            
            #Not already connected to child
            if(rel_cr != cr):
                #Add to the list of children to merge
                to_add.append([relative['c_rep'],rel_cr])
                
                #New representative child!
                if(f_(G.nodes[rel_cr]) < f_(G.nodes[cr])):
                    cr=rel_cr        
    
    #Naming is important
    name = ''
    p = n_
    
    c_count=len(to_add)
    #Leaf                   
    if(c_count==0):
        M.add_node(n_,value=f) #Add new leaf to merge tree
        M.nodes[n_]['p_rep']=n_ # Update the parent rep
        M.nodes[n_]['p']=n_ # Update the parent 
        name = 'R. ' + str(n_)
    #Merge
    elif(c_count>1):
        edges = []
        p=n_ #By default, nodes will connect to a new merged node
        
        #Check for nodes on the level
        first_on_lvl = True
        for i in range(0, len(to_add)):
            rep_ = M.nodes[to_add[i][1]]['p_rep'] #The "representative parent of the child" before addition
            if(f_(G.nodes[rep_]) == f): #Found node on level
                first_on_lvl = False
                p=rep_ #There won't be a new merged node
                i = -1
        #Only create a new node if it'd be the first one on the level
        if(first_on_lvl):
            M.add_node(n_,value=f, p_rep=n_) #Add new vertex to merge tree
            name = 'R. ' + str(n_)
        else:
            name += ',' + str(n_)
            
        #Calculate the edges
        for i in range(0, len(to_add)):
            rep_ = M.nodes[to_add[i][1]]['p_rep'] #The "representative parent of the child" before addition
            edges.append( (p, rep_) ) #Add the edge
             
            #Set the most direct parent of the connected representative
            M.nodes[rep_]['p'] = p

            M.nodes[to_add[i][0]]['p_rep'] = p #Update the rep. parent
            M.nodes[to_add[i][1]]['p_rep'] = p #Update the rep. parent
            G.nodes[rep_]['c_rep']=cr #Update the rep child
        
        #Add the edges
        M.add_edges_from(edges)
        
        M.nodes[p]['p'] = p #A node is its own parent until otherwise
    G.nodes[p]['c_rep']=cr #Update child rep of the node we connected to
     
    #Update the child rep of the added node and parent node. This must always be done
    n['c_rep']=cr
    return [name, p]
    
#Construct the merge tree given a graph G with function values.
#Returns a networkx tree with a position dictionary for drawing
def merge_tree(G):
    #Get the nodes from the networkx graph
    nodes = listify_nodes(G)
    
    #Sort the nodes in order of increasing function value
    nodes.sort(key=f_)
    
    #The legendary Merge Tree
    naming = {}
    M = nx.Graph()
    for i in range(0, len(nodes)):
        #Add the node to the merge tree
        name = add_node(nodes[i]['name'], G, M)
        
        #Naming stuff
        #name[1] is the 'reference'
        if(name[1] in naming):
            naming[name[1]] = naming[name[1]] + name[0]
        else:
            naming[name[1]] = name[0]
    
    #Rename the parent pointers to be consistent with the new naming scheme        
    parent_dict = {}
    parent_dict[nodes[i]['name']] = naming[name[1]]
    m_ = listify_nodes(M)
    for m in m_ :
        m['p'] = naming[m['p']]
        
    M = nx.relabel_nodes(M, naming)
    return M
##############################################################


####################################################
    


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