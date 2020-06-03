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
from Interleaving import *


#################DRAWING#######################
#Produces a level planar drawing based on function values
def LP_draw_f(G):
    #Sorted by function value
    nodes = listify_nodes(G)
    nodes.sort(key=f_)
    
    if(len(nodes) == 0):
        return
    
    pos_dict = {}
    
    #Counter variable for spacing
    count = 0
    lvl = 0
    last_f = f_(nodes[0])
    for i in range(0, len(nodes)):
        n=nodes[i]
        
        if(last_f != f_(n)):
            last_f = f_(n)
            lvl+=1
            count = random.randint(0,5)
        
        pos_dict[n['name']] = (count,f_(n))
        count = count + 1

    ax = plt.subplot(121)
    nx.draw(G, pos_dict, ax, with_labels=True,node_color="yellow",node_size=700)

#True if the node is a leaf
def is_leaf_f(T, n):
    c = list(T[n])
    f = f_(T.nodes[n])
    for i in range(0, len(c)):
        if(f_(T.nodes[c[i]]) < f):
            return False
    return True

#Gets the average x position of a node's children
def get_x_pos_f(T, n, pos):
    avg = 0
    c = list(T[n])
    count = 0
    f = f_(T.nodes[n])
    for i in range(0, len(c)):
        if(f_(T.nodes[c[i]]) < f):
            avg = avg + pos[c[i]][0]
            count = count + 1
    return avg / count
        
#Shifts a node and all its descendants 
def shift_f(T, n, pos, amount):
    pos[n] = (pos[n][0]+amount,pos[n][1])
    c = list(T[n])
    f = f_(T.nodes[n])
    for i in range(0,len(c)):
        if(f_(T.nodes[c[i]]) < f):
            shift(T, c[i], pos, amount)
    
def draw_pretty_f(T):
    #Sorted by function value, reversed
    nodes = listify_nodes(T)
    nodes.sort(key=f_)
    
    pos_dict = {}
    
    #Place the nodes without thinking  
    last_f = f_(nodes[0])
    count = 0
    c2 = 0
    for i in range(0, len(nodes)):
        n=nodes[i]
        
        if(last_f != f_(n)):
            last_f = f_(n)
            c2 += 1
            count = c2
            
        pos_dict[n['name']] = (count,f_(n))
        count += 1
    
    #center over children
    for i in range(0, len(nodes)):
        n=nodes[i]
        
        if(not is_leaf_f(T, n['name'])):
            newX = get_x_pos_f(T, n['name'], pos_dict)
            
            #Shift level neighbors! pretty important for real
            shift_ = newX -pos_dict[n['name']][0]
            f=f_(n)
            j=i+1
            while(j < len(nodes) and f_(nodes[j])==f):
                shift_f(T, nodes[j]['name'], pos_dict, shift_)
                j+=1
            j=i-1
            while(j >= 0 and f_(nodes[j])==f):
                shift_f(T, nodes[j]['name'], pos_dict, shift_)
                j-=1
            
            pos_dict[n['name']] = (newX, f_(n))
            
    
    ax = plt.subplot(133)
    ax.title.set_text("Resulting Merge Tree")
    nx.draw(T, pos_dict, ax, with_labels=True,node_color="yellow", node_size=700)
    
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

#Computes the height relative to (0,0) by computing the scalar projection
#direction should be a unit vector!!!
def height(pos, angle):
    return pos[0]*math.cos(angle)+pos[1]* math.sin(angle)

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
        n[i]['value'] = height(pos[n[i]['name']], direction)
        
def calc_values_height_reorient(G, pos, angle):
    reorient(pos, angle)
    
    #Get the list of node objects
    n = listify_nodes(G)
    
    #Set all of the function values by height
    for i in range(0, len(n)):
        n[i]['value'] = height(pos[n[i]['name']], math.pi / 2)
        
    
def reorient(pos, angle):

    norm = angle - math.pi / 2
    
    #testing
    #print("direction: " + str(d) + "  Norm: " + str(norm))

    #Calculate the new positions by computing the vector projection
    for p in pos:
        xNew = height(pos[p], norm)
        yNew = height(pos[p], angle)
        pos[p] = (xNew,yNew)

def add_arrow():
    ax = plt.subplot(132,frameon=False)
    ax.axis('off')
    arrow = mpimg.imread('./images/arrow.png')
    imagebox = OffsetImage(arrow,zoom=0.25)
    ab = AnnotationBbox(imagebox, (0.5, 0.5), frameon=False)
    ax.add_artist(ab)
##############


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