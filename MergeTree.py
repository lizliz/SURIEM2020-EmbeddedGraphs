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


#####TREE DRAWING!!!########

#True if the node is a leaf
def is_leaf(T, node, p):
    if(p != node and len(T[node]) == 1):
        return True
    return False

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

#Basic tree draw with no intersecting edges. 
#However, nodes will not be centered over their children
def tree_draw_basic(T, r):  
    #Set up the relevant BFS dictionaries
    bfs = BFS(T, r)
    nodes = bfs[0]
    level = bfs[2]
    
    #Position dictionary.
    #Maps each node to a coordinate pair (x,y)
    pos_dict = {}   
    
    #Start from the last nodes in the BFS-tree
    ind = len(nodes)-1
    
    #Count is used to space the nodes
    count = 0
    
    #Keep track of the current level
    last_level = level[nodes[ind]]
    
    #'Place' the nodes at each level with even spacing, then adjust the level accordingly
    for i in range(ind,-1,-1):
        #Current node
        n = nodes[i]
        
        #Level finished
        if(last_level != level[n]):
            #Reset the spacing count and update the level
            count=0
            last_level = level[n]
        
        #Space evenly
        pos_dict[n] = (-1*count,level[n])
        count = count + 1
        
    #Produce the drawing of the tree
    nx.draw(T, pos_dict, with_labels=True,node_color="blue")
    
    return pos_dict #This is really just for testing purposes

#Makes a random tree
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
#####################################################################


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

#Recursively find the child
def find_c(n_, G):
    n = G.nodes[n_]
    child = n['c_rep']
    if(n['c_rep'] != n_):
        return find_c(child, G)
    return n_

#Recursively find the parent
def find_p(n_, G):
    n = G.nodes[n_]
    parent = n['p_rep']
    if(n['p_rep'] != n_):
        return find_p(parent, G)
    return n_
    

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
            #Does this work? idk !!!!!!
            rel_cr = find_c(children[i], G)
            
            #Not already connected to child
            if(rel_cr != cr):
                #Add to the list of children to merge
                to_add.append(rel_cr)
                
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
        M.nodes[n_]['p']=p # Update the parent (THIS IS KIND OF REDUNDANT) 
        name = 'R. ' + str(n_)
    #Merge
    elif(c_count>1):
        edges = []
        
        #Check if there's already a node on this level that is representative of
        #one of the components to add
        first_on_lvl = True
        for i in range(0, len(to_add)):
            rep_ = find_p(to_add[i], G) #The "representative parent of the child" before addition
            if(f_(G.nodes[rep_]) == f): #Found node on level
                first_on_lvl = False
                p=rep_ #There won't be a new merged node - we found one to connect to

        #Only create a new node if it'd be the first one on the level
        if(first_on_lvl):
            M.add_node(n_,value=f, p_rep=n_) #Add new vertex to merge tree
            name = 'R. ' + str(n_)
        #The node is representative of multiple from the original graph
        else:
            name += ',' + str(n_)
            
        #Calculate the edges
        for i in range(0, len(to_add)):
            rep_ = find_p(to_add[i], G) #The "representative parent of the child" before addition
            edges.append( (p, rep_) ) #Add the edge
             
            #Set the most direct parent of the connected representative
            M.nodes[rep_]['p'] = p
            

            G.nodes[rep_]['p_rep'] = p #Update the rep. parent
            G.nodes[to_add[i]]['c_rep']=cr #Update the rep child of the node from the list
        
        #Add the edges
        M.add_edges_from(edges)
        M.nodes[p]['p'] = p #A node is its own parent until otherwise
        
    G.nodes[p]['c_rep']=cr #Update child rep of the node we connected to 
    n['c_rep']=cr #Update the child rep of the added node and parent node. This must always be done
    n['p_rep']=p #Update the parent rep of the newly added node
    
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
    
####################################################
    
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
    
def draw_pretty_f_(T):
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
    nx.draw(T, pos_dict, ax, with_labels=False,node_color="white", node_size=0)
    
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

def draw_w_pos_(G, pos):
    ax = plt.subplot(131)
    ax.title.set_text("Input Graph")
    nx.draw(G, pos, ax, with_labels=False,node_color="white",node_size=0)
     
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
#draw_w_pos(G,pos_dict)

#Calculate height values

#Make the mergre tree
#M = merge_tree(G)

#Interleaving
#IL = IL_test(M)

##DRAWING MERGE
#draw_pretty_f(M)


G = nx.Graph()

#The vertex data we wish to extract
vertexnames=[]
coordinate1=[]
coordinate2=[]

#Get it
vert_path = './data/athens_small_vertices_osm.txt'
with open(vert_path) as vertex:
    for x in vertex.read().split('\n'):
        counter=1
        for y in x.split(','):
            if (counter==1):
                vertexnames.append(float(y))
                counter+=1
            elif(counter==2):
                coordinate1.append(float(y))
                counter+=1
            elif(counter==3):
                coordinate2.append(float(y))
                counter+=1
vertex.close()

G.add_nodes_from(vertexnames)


#The edge data we wish to extract
edgenames=[]
firstvertex=[]
secondvertex=[]

#Get it
edge_path = './data/athens_small_edges_osm.txt'
with open(edge_path) as edge:
    for x in edge.read().split('\n'):
        counter=1
        for y in x.split(','):
            if (counter==1):
                edgenames.append(y)
                counter+=1
            elif(counter==2):
                firstvertex.append(float(y))
                counter+=1
            elif(counter==3):
                secondvertex.append(float(y))
                counter+=1
edge.close()

edges = []
for i in range(len(firstvertex)):
    edges.append((firstvertex[i],secondvertex[i]))
G.add_edges_from(edges)

pos_dict = {}
for i in range(len(vertexnames)):
    pos_dict[vertexnames[i]] = [coordinate1[i], coordinate2[i]]
    
angle = math.pi / 2
calc_values_height_reorient(G, pos_dict, angle)
    
draw_w_pos_(G,pos_dict)

M = merge_tree(G)
print(nx.is_forest(M))

draw_pretty_f_(M)
    
#RandomSample = random.sample(list(G.nodes), 2600)
#G.remove_nodes_from(RandomSample)


plt.show()
#testing distance
#print(compare_trees(IL[0],IL[0]))

####################