#Draw things, maybe
#Levent Batakci, 5/29/2020
#My sincerest apologies to anyone who tries to read the code that follows
import networkx as nx
import random

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
def BFS(G):
    #Find the root
    node_list = list(G.nodes)
    r = -1
    if 'root' in node_list: #root is defined
        r = 'root'
    elif len(node_list) != 0: #root is not defined, taken as first node
        r = 1
    else: #Empty tree.
        return
    
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
            if(children[i] != parent[curr_node]): #Ignore the parent 
                level[children[i]] = level[curr_node] - 1
                nodes.append(children[i])
                parent[children[i]] = curr_node
        
        #Move to the next node 
        index = index + 1
    
    #Retrurn the relevant dictionaries and the root    
    return [nodes, parent, level, r]

#Basic tree draw with no intersecting edges. 
#However, nodes will not be centered over their children
def tree_draw_basic(T):  
    #Set up the relevant BFS dictionaries
    bfs = BFS(T)
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
    

#the test
rt = random_tree(20)
pos = tree_draw_basic(rt)