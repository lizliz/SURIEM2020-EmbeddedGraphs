#Levent Batakci
#Union-Find data structure basics and testing notebook
#6/1/2020
import networkx as nx
import matplotlib as plt
import random


#####TREE DRAWING!!!#####

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
        
#Preforms a BFS search and returns the nodes, parent, and level dictionaries
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
    f = function_value(n) #The node's value
    
    children = list(G[n_]) #Note: This contains the parent as well.
    cr=n_ #tentative child rep
    
    c_count = 0 #Disconnected child count
    to_add = []
    for i in range(0, len(children)):
        relative = G.nodes[children[i]]
        #Relative is a child
        if(f_(relative) < f):
            rel_cr = relative['c_rep']#rep child of the relative
            #Not already connected to child
            if(rel_cr != cr):
                #Add to the list of children to merge
                to_add.append(rel_cr)
                
                #New representative child!
                if(f_(G.nodes[rel_cr]) < f_(G.nodes[cr])):
                    cr=rel_cr        
    
    c_count=len(to_add)
    #Leaf                   
    if(c_count==0):
        M.add_node(n_,value=f) #Add new leaf to merge tree
        M.nodes[n_]['p_rep']=n_ # Update the parent rep
    #Merge
    elif(c_count>1):
        edges = []
        p=n_ #By default, nodes will connect to a new merged node
        
        #Check for nodes on the level
        first_on_lvl = True
        for i in range(0, len(to_add)):
            rep_ = M.nodes[to_add[i]]['p_rep'] #The "representative parent of the child" before addition
            if(f_(G.nodes[rep_]) == f): #Found node on level
                first_on_lvl = False
                p=rep_ #There won't be a new merged node
                i = -1
        
        #Only create a new node if it'd be the first one on the level
        if(first_on_lvl):
            M.add_node(n_,value=f, p_rep=n_) #Add new vertex to merge tree
            
        #Add the edges
        for i in range(0, len(to_add)):
            rep_ = M.nodes[to_add[i]]['p_rep'] #The "representative parent of the child" before addition
            edges.append( (p, rep_) ) #Add the edge
            M.nodes[to_add[i]]['p_rep'] = p #Update the rep. parent of the child
        M.add_edges_from(edges)
     
    #Update the child rep of the added node. This must always be done
    n['c_rep']=cr

    
#Construct the merge tree given a graph G with function values.
#Returns a networkx tree with a position dictionary for drawing
def merge_tree(G):
    #Get the nodes from the networkx graph
    nodes = listify_nodes(G)
    
    #Sort the nodes in order of increasing function value
    nodes.sort(key=f_)
    print(nodes)
    
    #The legendary Merge Tree
    M = nx.Graph()
    for i in range(0, len(nodes)):
        add_node(nodes[i]['name'], G, M)
    
    return M
###################################################################################################


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
    
    nx.draw(G, pos_dict, with_labels=True,node_color="blue")
##############

#####TESTING#######
G = nx.Graph()
G.clear()
G = nx.Graph()

nodes = list( [1,3,5,4,2,7,8] )
edges = [ (1,4),(2,4),(3,5),(4,5),(4,6),(5,7),(6,7),(6,8)]
f_vals = {}
f_vals[3]= {'value': 2}
f_vals[1]= {'value': 1}
f_vals[2]= {'value': 1}
f_vals[7]= {'value': 4}
f_vals[5]= {'value': 3}
f_vals[4]= {'value': 2}
f_vals[6]= {'value': 3}
f_vals[8]= {'value': 2.5}

G.add_nodes_from(nodes)
G.add_edges_from(edges)
nx.set_node_attributes(G,f_vals)

#tree_draw_basic(G,7)

M = merge_tree(G)

LP_draw_f(M)
####################