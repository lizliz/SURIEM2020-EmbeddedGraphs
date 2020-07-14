#Levent Batakci
#6/8/2020
#
#This file contains many basic helper and misc. methods.
import networkx as nx
import numpy as np
import random
import math
import matplotlib.pyplot as plt

###
#TREE PROPERTIES
####

#Gets a list including n and all of its descendants, recursively
def descendants(G, n):
    neighbors = G[n]
    
    d = [n]
    for nei in neighbors:
        #Check for child
        if(f_(G.nodes[nei]) < f_(G.nodes[n])):
            list_append(d, descendants(G, nei))
    
    return d

#Returns true/false depending on if the input node is a leaf
def is_leaf(T, node, p):
    #Note: p==node indicates that p is the root of some tree
    if(p != node and len(T[node]) == 1):
        return True
    return False

#True if the node is a leaf, based on function values 
def is_leaf_f(T, n):
    c = list(T[n])
    f = f_(T.nodes[n])
    for i in range(0, len(c)):
        if(f_(T.nodes[c[i]]) < f):
            return False
    return True

#Returns a list (names) of a graph's leaves
def get_leaves(M) :
    n = list(M.nodes)
    
    #Find all of the leaves by checking every node
    leaves = []
    for i in range(0, len(n)):
        if(is_leaf_f(M, n[i])):
            leaves.append(n[i])
    
    return leaves


#Returns a list of a graph's nodes (dictionary objects)
#Also adds the nodes' names to the dictionary for easy access
def listify_nodes(G):
    n = list(G.nodes)
    n_list = []
    for i in range(0, len(n)):
        G.nodes[n[i]]['name'] = n[i]
        n_list.append(G.nodes[n[i]])
    return n_list

#Recursively find the parent
def find_p(n_, G):
    n = G.nodes[n_]
    
    parent = n['p']
    if(n['p'] != n_):
        return find_p(parent, G)
    return n_

#Recursively find the child
def find_c(n_, G):
    n = G.nodes[n_]
    child = n['c']
    if(n['c'] != n_):
        return find_c(child, G)
    return n_

#Returns the function value of a node (dictionary)
def f_(node):
    return node['value']

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


###
#END OF TREE PROPERTIES
###


###
#GEOMETRIC METHODS
###

#Computes the height relative to (0,0) by computing the scalar projection
#direction should be a unit vector!!!
def height(pos, angle):
    return pos[0]*math.cos(angle)+pos[1]* math.sin(angle)

#Essentially rotates the graph by performing vector projection
def reorient(pos, angle):

    norm = angle - math.pi / 2
    
    #testing
    #print("direction: " + str(d) + "  Norm: " + str(norm))

    #Calculate the new positions by computing the vector projection
    for p in pos:
        xNew = height(pos[p], norm)
        yNew = height(pos[p], angle)
        pos[p] = (xNew,yNew)


def get_bounds(pos):
    count = len(list(pos))
    
    xArr = np.empty(count)
    yArr = np.empty(count)
    
    i=0
    for key in pos:
        coords = pos[key]
        
        xArr[i]=coords[0]
        yArr[i]=coords[1]
        i+=1
    
    xMax = np.amax(xArr)
    xMin = np.amin(xArr)
    
    yMax = np.amax(yArr)
    yMin = np.amin(yArr)
    
    return [[xMin, xMax], [yMin, yMax]]

def get_bounds_and_radius(pos):
    bounds = get_bounds(pos)
    
    xRange =  bounds[0][1]-bounds[0][0]
    
    yRange = bounds[1][1]-bounds[1][0]
    
    radius = max(xRange, yRange) * 1.15
    return [radius, bounds]

def get_centroid(G, pos):
    #This is going to determine the final weightings to divide by
    xlength = 0
    ylength = 0
    
    nodes = list(G)
    
    
    xTotal = 0
    yTotal = 0
    for n in nodes:
        neighbors = list(G[n])
        
        x1 = pos[n][0]
        y1 = pos[n][1]
        for nei in neighbors:
            x2 = pos[nei][0]
            y2 = pos[nei][1]
            
            dx = abs(x2-x1)
            dy = abs(y2-y1)
            
            xTotal += dx*(x1+x2)/2
            yTotal += dy*(y1+y2)/2
            
            xlength += dx
            ylength += dy
        
        xAvg = xTotal / (xlength)
        yAvg = yTotal / (ylength)
        
        return [xAvg, yAvg]
    
def shift_centroid(G, pos):
    centr = get_centroid(G, pos)
    
    for p in pos:
        pos[p] = (pos[p][0] - centr[0], pos[p][1] - centr[1])
        
    return pos

def get_center(pos):
    x = [pos[p][0] for p in pos]
    y = [pos[p][1] for p in pos]
    
    xAvg = (max(x) + min(x)) / 2
    yAvg = (max(y) + min(y)) / 2
    
    return [xAvg, yAvg]

def shift_center(pos):
    centr = get_center(pos)
    
    for p in pos:
        pos[p] = (pos[p][0] - centr[0], pos[p][1] - centr[1])
        
    return pos

def get_rad(pos):
    x = [pos[p][0] for p in pos]
    y = [pos[p][1] for p in pos]
    
    r = max(abs(min(x)), abs(max(x)), abs(min(y)), abs(max(y))) * 1.1
    
    return r

###
#END OF GEOMETRY
###


###
#RANDOM GENERATION
###

#Makes a random tree, doesn't assign positions
def random_tree(n):
    T = nx.Graph() #This is the tree
    
    T.add_nodes_from([1,n]) #Add n nodes to the tree

    #This list stores the nodes that have yet to be added to the tree.
    #To be clear, these are the nodes with no connection to the tree.    
    choices = list(range(2,n+1)) 
    
    #This list stores the nodes that have been added to the tree. By default,
    #the tree 'contains' just node 1
    nodes = [1]
    
    #There are no edges yet.
    edge_count = 0
    
    while edge_count < n-1:
        #Choose a random node n1 in the tree
        i1=random.randint(0,len(nodes)-1)
        n1 = nodes[i1]
        
        #Choose a ranom node n2 NOT in the tree
        i2=random.randint(0,len(choices)-1)
        n2 = choices[i2]
        
        #Add n2 to the tree be connecting it to n1
        T.add_edge(n1,n2)
        edge_count = edge_count + 1 #Account for the new edge
        
        #Move n2 to the right list
        choices.remove(n2)
        nodes.append(n2)
        
    return T #return the tree

def random_positions(n):
    pos = {}
    
    center = [random.randint(-10000,10000),random.randint(-10000,10000)]
    spread = random.randint(1,10000)
    
    for i in range(1, n+1):
        pos[i] = (center[0] + random.randint(-1*spread,spread),center[1] + random.randint(-1*spread,spread))
        
    return pos

def random_tree_and_pos(n):
    T = random_tree(n)
    pos = random_positions(n)
    return [T,pos]

#Returns a random subgraph with n nodes
def random_component(G, n, draw=False, pos=None, color='g'):
    nodes = list(G)
    if(n >= len(nodes)):
        print("There aren't even that many nodes to choose!!")
        return None
    
    #Randomly choose a root
    index = random.randint(0, len(nodes)-1)
    root = nodes[index]
    
    included_nodes = [root]
    
    #Perform a BFS to add nodes until there are n nodes
    count = 1
    to_add = list(G[root])
    while(len(to_add) != 0 and count < n):
        cur_node = to_add[0]
        
        #Include the current node
        included_nodes.append(cur_node)
        count += 1
        
        #Remove it from the list and add its 'children'
        to_add.remove(cur_node)
        neighbors = G[cur_node]
        for nei in neighbors:
            if(nei not in included_nodes and nei not in to_add):
                to_add.append(nei)
                
    g = G.subgraph(included_nodes).copy()
    
    if(draw):
        fig = plt.subplots(1,1,figsize=(20,10))
        ax = plt.subplot(111, frameon=False)
        ax.title.set_text("Subgraph with " + str(n) + " nodes")
        nx.draw(G, pos, node_size=0)
        nx.draw_networkx_edges(g, pos, edge_color=color, width=3)     
    return g

###
#END OF RANDOM GENERATION
###


###
#DRAWING TOOLS
###

#Gets the average x position of a node's children
def get_x_pos(T, n, p, pos):
    avg = 0
    c = list(T[n])
    count = 0
    for i in range(0, len(c)):
        if(c[i] != p):
            avg = avg + pos[c[i]][0]
            count = count + 1
    return avg / count
        
#Shifts a node and all its descendants 
def shift(T, n, pos, p, amount):
    pos[n] = (pos[n][0]+amount,pos[n][1])
    c = list(T[n])
    for i in range(0,len(c)):
        if(c[i] != p):
            shift(T, c[i], pos, n, amount)

#Gets the average x position of a node's children, based on a function
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
        
#Shifts a node and all its descendants, based on a function
def shift_f(T, n, pos, amount):
    pos[n] = (pos[n][0]+amount,pos[n][1])
    c = list(T[n])
    f = f_(T.nodes[n])
    for i in range(0,len(c)):
        if(f_(T.nodes[c[i]]) < f):
            shift(T, c[i], pos, amount)
###
#END OF DRAWING TOOLS
###


###
#MISC. METHODS
###
    
def relabel(G, tag):
    nodes = list(G.nodes)
    
    new_names = {}    
    
    for n in nodes:
        new_names[n] = tag + str(n)
        G.nodes[n]['p'] = tag + str(G.nodes[n]['p'])
    
    nx.relabel.relabel_nodes(G, new_names, copy=False)
    
def relabel_dict(D, tag):
    new_D = {}
    
    for d in D:
        new_D[tag + d] = D[d]
        
    return new_D


def is_ghost(a):
    return (isinstance(a, str) and len(a) >= 5 and a[0:5] == "GHOST")

def get_ID(m, val):
    if(m[0] == '*'):
        return m + val
    else:
        return val + m

def get_connections(mapping, ID, c):
    layer = mapping[ID]
    
    #Handle the root branch
    branch = layer['root-branch']
    min1 = branch[1]
    min2 = branch[3]
    c[min1] = min2 #Update the dictionary
    saddle1 = branch[0]
    saddle2 = branch[2]
    c[saddle1] = saddle2 #Update the dictionary
    
   
    #Handle all the matchings
    matching = layer['matching']
    if(matching == 'EMPTY'):
        return c
    
    for m in matching:
        #Deleted Vertex
        val = matching[m]
        if(val == "GHOST " + str(m)):
            c[m] = "DELETED"  
        elif(not is_ghost(val) and not is_ghost(m) and m != "DELETED"):
            new_ID = get_ID(m, val)
            get_connections(mapping, new_ID, c)
            

#Returns a dictionary of minima matchings
def parse_mapping(mapping):
    c={}
    
    ID = mapping['top']
        
    get_connections(mapping, ID, c)
    
    return c
    
#Adds all the elements in L2 to the end of L1, preserving order
def list_append(L1, L2):
    for i in range(0,len(L2)):
        L1.append(L2[i])

#Performs a BFS search and returns the nodes, parent, and level dictionaries
def BFS(G, r):
    #Level Dictionary.
    #Maps each node to a level. The root is level 0, 
    #and every other node has level < 0. Also, the level
    #of a node is its distance (negated) to the root
    level = {r: 0}
    
    #Parent Dictionary.
    #Maps each node to its parent. The root's parent is itself
    parent = {r:r}
    
    #Children Dictionary.
    #Maps each node to a number denoting the number of children it has.
    children = {}
    
    #List of nodes in order of a BFS
    nodes = []  
    nodes.append(r)
    
    #Create the BFS-tree
    index = 0
    while index < len(nodes):
        #Set the current node to the 'head' of the list
        curr_node = nodes[index]
        
        #Children on the current node. This will actually contain the parent too.
        children = list(G[curr_node])
        
        
        #Add the children, set their levels, and set their parent
        for i in range(0, len(children)):
            if(children[i] not in level): #Ignore the parent 
                level[children[i]] = level[curr_node] - 1
                nodes.append(children[i])
                parent[children[i]] = curr_node
        
        #Move to the next node 
        index = index + 1
    
    #Retrurn the relevant dictionaries and the root    
    return [nodes, parent, level, r]

# Returns the largest connected component of a graph as a networkx object
def main_component(G, pos_dict = None, report = True, draw = False):
    largest_cc = max(nx.connected_components(G), key=len)
    mainComponent = G.subgraph(largest_cc).copy()
    
    if draw == True: # Draw largest component
        if pos_dict == None: # Drawing requires position dictionary
            print("I'll return the main component, but I need position dictionary to draw!")
        else:
            nx.draw(mainComponent, pos = pos_dict, with_labels = False, node_size = 0)
    
    if report == True: # Tell user what percent of the nodes were preserved
        print("Largest component has ", (len(list(mainComponent.nodes))/len(list(G.nodes)))*100, "% of the nodes")

    return mainComponent

#Gets the positions from node attributes
def get_pos(G):
    #nodes = list(G)
    
    pos={}        
    for n in list(G.nodes.data()):
        node = n[0]
        x = n[1]['x']
        y = n[1]['y']
        
        pos[node] = (x,y)
        
    return pos

#renames a dictionary key
def rename_key(myDict, oldKey, newKey):
    myDict[newKey] = myDict.pop(oldKey)
    print("\n\tOld Key: ", oldKey)
    print("\n\tNew Key: ", newKey)

###
#END OF MISC.
###
