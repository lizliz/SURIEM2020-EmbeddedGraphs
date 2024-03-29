#Levent Batakci
#6/9/2020
#
#This program is concerned with the comparison of merge trees
import networkx as nx
from lib.Tools import f_, get_leaves, list_append, listify_nodes, relabel, descendants
import time

#MEMOIZATION VARIABLES
global D
D={}

global st
st = 0

global mt
mt = 0

global t
t=0

global matching
matching={}

global branching
branching = [{},{}]

#The associated cost of matching a pair of vertices
#from two rooted representations of branchings
def match_cost(U,V, mu,su , mv,sv):
    #m represents the minima
    #s represents the saddle
    cost = max(abs(f_(U.nodes[mu])-f_(V.nodes[mv])), abs(f_(U.nodes[su])-f_(V.nodes[sv])))
    #print("Match cost: " + str(cost))
    return cost

#The associated cost of removing a vertex 
#from a rooted representation of a branching
def remove_cost(A, u,v):
    return abs(f_(A.nodes[u])-f_(A.nodes[v]))/2

#Gets all of the child subtrees of a given root branch
def get_child_subtrees(root, minima, T):
    last = minima
    p = T.nodes[minima]['p']    
    run = 0
    subtrees = []

    while(last != p):
        neighbors = T[p]
        
        #Add all the subtrees with child saddle p
        for n in neighbors:
            
            #Check that n is a child and not an ancestor of minima
            if (n != last and f_(T.nodes[n]) < f_(T.nodes[p])):
                stree = sub_special(T, n)
                subtrees.append(stree)
        
        #We've traced back to the root
        if(p == root):
            return subtrees
        
        last = p #Update the last variable
        p = T.nodes[p]['p'] #Move to the next ancestor
        run += 1
        
    return subtrees

#Gets all of the child subtrees of a given root branch
def get_child_subtrees_(root, minima, T, subtrees):
    last = minima
    p = T.nodes[minima]['p']
    
    st = []
    while(True):        
        neighbors = T[p]
        
        #Add all the subtrees with child saddle p
        for n in neighbors:
            #Check that n is a child and not an ancestor of minima
            if (n != last and f_(T.nodes[n]) < f_(T.nodes[p])):
                st.append(subtrees[n])
        
        #We've traced back to the root
        if(p == root):
            return st
        
        last = p #Update the last variable
        p = T.nodes[p]['p'] #Move to the next ancestor

#Returns the special subgraph identified by the almost-root
#The almost-root is first node in the graph. 
def sub_special(G, n):
    nodes = []
    nodes.append(G.nodes[n]['p'])
    list_append(nodes, descendants(G, n))

    #Induce the subgraph and return it
    g = nx.Graph.subgraph(G, nodes)
    g = g.copy()
    g.graph['root'] = G.nodes[n]['p']
    g.graph['ID'] = n
    
    return g

#Creates a bipartite graph to represent the connections between two
#sets of child subtrees
def create_bip(list_A, list_B):
    bip = nx.Graph()
    
    #Add all the nodes to the two bipartitions
    #Reliant on the fact that the subtrees were generated by IsEpsSimilar
    for a in list_A:
        bip.add_node(a, bipartite=0)       
    for b in list_B:
        bip.add_node(b, bipartite=1)
        
    return bip

#returns a list of ID nodenames
def node_list(subtrees):
    x = []
    for s in subtrees:
        x.append(s.graph['ID'])

    return x

#Compute all the removal costs at and below a root
#Return the resulting cost dictionary
def compute_costs(A, root, costs=None):
    if(costs==None):
        costs = {}
    
    #Base removal cost
    #print("Saddle and Minima in tree: " + str(root in A and A.nodes[root]['p'] in A))
    c = remove_cost(A, root, A.nodes[root]['p'])
    
    #Account for the necessary removal of descendants
    #Use memoization to speed things up
    f = f_(A.nodes[root])
    neighbors = A[root]
    
    max_cost = c
    for nei in neighbors:
        
        #If nei is a child but its cost hasn't been computed...
        if(f_(A.nodes[nei]) < f):
            
            if(nei not in costs):
                costs[nei] = compute_costs(A, nei, costs)[nei]
            
            if(costs[nei] > max_cost):
                max_cost = costs[nei]    
            
    costs[root] = max_cost
    return costs

#Gets a list including n and all of its descendants, recursively
def descendants_(G, n, des):
    
    if n in des:
        return des[n]
    
    #Add the current node
    d = [n]

    #Add all the children and their descendants
    neighbors = G[n]    
    for nei in neighbors:
        #Check for child
        if(f_(G.nodes[nei]) < f_(G.nodes[n])):
            #memoize!
            if(nei not in des):
                des[nei] = descendants_(G, nei, des)
            list_append(d, des[nei])
    
    des[n] = d
    return d

def compute_subtree(G, saddle, subtrees, des):
    #Include the parent
    nodes = [G.nodes[saddle]['p']]
    list_append(nodes, descendants_(G, saddle, des))
    
    #Induce the subgraph and return it
    g = nx.Graph.subgraph(G, nodes)
    g = g.copy()
    g.graph['root'] = G.nodes[saddle]['p']
    g.graph['ID'] = saddle
    subtrees[saddle] = g

def compute_subtrees(G, root, subtrees=None):
    if(subtrees == None):
        subtrees = {}
    
    des = {}
    
    #Nodes adjacent to the root
    nodes = list(G)
    for n in nodes:
        if(n != root):
            compute_subtree(G, n, subtrees, des)
            
    return subtrees

#Add all the dummy vertices (ghosts) to the bipartite graph
def who_you_gonna_call(subtrees_A, subtrees_B, costs_A, costs_B, bip, e):
    dummy_A = []
    
    for a in subtrees_A:
        id_a = a.graph['ID']
        bip.add_node("GHOST " + str(id_a), bipartite=1) #Add to opposite side
        dummy_A.append("GHOST " + str(id_a))
        
        #Could be removed..
        if(costs_A[id_a] <= e):
            bip.add_edge(id_a, "GHOST " + str(id_a))
            
    dummy_B = []
    for b in subtrees_B:
        id_b = b.graph['ID']
        bip.add_node("GHOST " + str(id_b), bipartite=0) #Add to opposite side
        dummy_B.append("GHOST " + str(id_b))
        
        #Could be removed..
        if(costs_B[id_b] <= e):
            bip.add_edge(id_b, "GHOST " + str(id_b))
          
    #Fully connect all of the dummy vertices 
    for a in dummy_A:
        for b in dummy_B:
            bip.add_edge(a,b)
    
    return dummy_A
            

def has_ghost(A, a):
    nodes = list(A.nodes)
    
    return ("GHOST " + str(a)) in nodes

def is_ghost(a):
    return (isinstance(a, str) and len(a) >= 5 and a[0:5] == "GHOST")

def update_matching(a, b):
    global matching
    
    if(is_ghost(a)):
        matching[b] = "DELETED"
    else:
        matching[a] = b
    
def find_root(T):
     nodes = listify_nodes(T)
     max_ = f_(nodes[0])
     max_node = nodes[0]
     
     for n in nodes:
         
         if(f_(n) > max_):
             max_ = f_(n)
             max_node = n
             
     return max_node['name']
        
def update_branching(B, saddle, minima):
    
    if(saddle not in B):
        B[saddle] = []
    
    B[saddle].append(minima)
  
#Computes whether two subtrees a and b are matchable. Calls IsEpsSimilar
#    in the case that the computation hasn't yet been computed.
def compute_matchability(a, b, e, memo, costs, subtrees, mapping):

    #These indices always pull the ID and roots because of how the subtrees are
    #constructed in a previous method. Generally, this will NOT work on subtrees not
    #computed through IsEpsSimilar!!
    root_a = a.graph['root']
    id_a = a.graph['ID']
    root_b= b.graph['root']
    id_b = b.graph['ID']
    
    roots = [root_a, root_b]
    
    #Check if subtree 'a' has an entry corresponding to it in memo
    #Note: because of the input order, we only ever need entries in the
    #      in the order (a,b)
    if(id_a not in memo or id_b not in memo[id_a]): #Result not computed yet
        if(id_a not in memo):
            memo[id_a] = {}
            
        memo[id_a][id_b] = IsEpsSimilar(a, b, e, costs=costs, roots=roots, memo=memo, subtrees=subtrees, mapping=mapping)
    
    #Return the result (True or False)
    return memo[id_a][id_b]    
  
#A and B are two merge trees to compare
#e is the cost maximum
#roots is an array containing the roots of A and B
#The function returns whether or not the two merge trees are matchable within e
def IsEpsSimilar(A, B, e, costs=None, roots=None, memo=None, subtrees=None, mapping=None):
    start = time.time()
   
    if(memo==None):
        memo = {}
        
    if(roots==None):
        roots = [find_root(A), find_root(B)]
        #Find the root - the highest vertex - of each tree
    root_A = roots[0]
    root_B = roots[1]
    
    if(costs == None):
        costs=[{},{}]
    
    if(not bool(costs[0])):
        compute_costs(A, root_A, costs[0])
        compute_costs(B, root_B, costs[1])
        
    if(subtrees == None):
        subtrees = [compute_subtrees(A, root_A), compute_subtrees(B, root_B)]
        
    if('ID' in A.graph and 'ID' in B.graph):
        ID = A.graph['ID'] + B.graph['ID']
    else:
        ID = str(root_A) + str(root_B)
        
    #Mapping is a dictionary that stores two things for each tree-pair
    # 1. The matched root branches (ID'd by 'root-branch')
    # 2. The perfect matching that worked (ID'd by 'matching')
    if(mapping==None):
        mapping = {'top' : ID}
    
    mapping[ID] = {}

    #Compute all costs for later ghost-vertex marking
    costs_A = costs[0]
    costs_B = costs[1]
    
    #Get the minima of the two treees.
    #These are crucial to the construction of branch decompositions
    minima_A = get_leaves(A)
    minima_B = get_leaves(B)
    
    #Next, Iterate over all root-branch posibilities for each graph.
    #At each step, we will check if pairing the two root-branches is feasible.
    #If it is feasible, we will iterate over all child subtree pairings, and
    #    we will recursively check for epsilon similarity. We will construct a
    #    bipartite graph with vertices representing the child subtrees. In the
    #    case that a pairing is matchable, an edge will be drawn between the
    #    corresponding vertices in the bipartite representation
    
    for mA in minima_A:
    
        for mB in minima_B:
                
            #At this point, a root-branch pairing will be specified.
            #Check if the initial cost of matching this pairing is prohibitive.
            #If it isn't check if the rest of the graph is matchable by considering
            #   all of the child subtrees.
        
            if(match_cost(A,B, mA, root_A, mB, root_B) <= e):
                #Set the matched root branch.
                #List with elements, sA,mA, sB,mB
                mapping[ID]['root-branch'] = [root_A, mA, root_B, mB]
                
                #Get a list of all the child subtrees of each root-branch
                global st
                global mt
                start = time.time()
                subtrees_A = get_child_subtrees_(root_A, mA, A, subtrees[0])
                subtrees_B = get_child_subtrees_(root_B, mB, B, subtrees[1])
                st += time.time()-start
                #print("ST: ", st)
                #print("total~ ", mt+st)
                
                #BASE CASE
                if(len(subtrees_A) == 0 and len(subtrees_B) == 0):                    
                    mapping[ID]['matching'] = 'EMPTY'
                    return True
                
                #Create a bipartite graph representating the matchability of
                #    subtree pairings between the two lists above. Also, save
                #    all of the nodes in lists.
                list_A = node_list(subtrees_A)
                list_B = node_list(subtrees_B)
                bip = create_bip(list_A, list_B)
                
                #Iterate over all child-subtree pairing and compute matchability.
                #Use memoization to use the results of previous computations.
                #Also, fill in the bipartite edges where applicable
                for a in subtrees_A:
                    for b in subtrees_B:
                        if(compute_matchability(a, b, e, memo, costs, subtrees, mapping)):
                            bip.add_edge(a.graph['ID'], b.graph['ID'])
                
                #At this point, we should have a bipartite graph that encodes the
                #matchability of each child-subtree pairing at the current level.
                #
                #However, we need to account for the posibility of deletion!
                #To do this, we will iterate over all the current vertices in the 
                #bip. graph and mark ghosts by checking their removal cost.
                who_you_gonna_call(subtrees_A, subtrees_B, costs_A, costs_B, bip, e)
                top_nodes = {n for n, d in bip.nodes(data=True) if d['bipartite']==0}
                
                start = time.time()
                matching = nx.algorithms.bipartite.hopcroft_karp_matching(bip, top_nodes)
                
                if(len(list(matching)) == 2*(len(list_A)+len(list_B))):
                    mt += time.time() - start
                    #print("MT: ", mt)
                    #print("total~ ", mt+st)
                    mapping[ID]['matching'] = matching
                    return True
                mt += time.time() - start
                #print("MT: ", mt)
                #print("total~ ", mt+st)
    
    #No matching was found!
    mapping[ID]['root-branch'] = 'NONE'
    mapping[ID]['matching'] = 'NONE'
    return False

# returns distance between 2 merge trees within a margin of error
# T1, T2: networkx graphs, merge trees returned by Merge.merge_tree()
# accuracy: int or float, distance returned will be withing this radius of accuracy
# valid: Setting this to true will ensure that the last iteration is one where a valid matching is found.
# get_map: boolean, whether you want to return the mapping between trees that yields the returned epsilon value
def branching_distance(T1, T2, accuracy = 0.05, valid=False, get_map=False):
    global st
    global mt
    st = 0
    mt = 0
    start = time.time()
    
    T1 = T1.copy()
    T2 = T2.copy()
    
    relabel(T1, "*")
    relabel(T2, "~")
    
    # Find the larger amplitude between the two trees as our starting epsilon
    vals1 = [i[1]["value"]for i in list(T1.nodes.data())]
    amp1 = abs(max(vals1)-min(vals1)) # amplitude for T1
    vals2 = [j[1]["value"]for j in list(T2.nodes.data())]
    amp2 = abs(max(vals2)-min(vals2)) # amplitude for T2

    maximum = max(amp1,amp2) # Find the biggest of the two amplitudes
    costs = [{},{}]
    roots = [find_root(T1), find_root(T2)]
    subtrees = [compute_subtrees(T1, roots[0]),compute_subtrees(T2, roots[1])]
    ID = str(roots[0]) + str(roots[1])
    mapping = {'top': ID}
    
    epsilon = maximum
    global t
    t=0
    similar = IsEpsSimilar(T1,T2, epsilon, costs=costs, roots=roots, subtrees=subtrees, mapping=mapping)
    delta = epsilon
    
    its = 0
    # Continue the binary search until we get within our desired margin of error for accuracy
    while delta >= accuracy:
        its+=1
        delta=delta/2
        start_ = time.time()
        mt = 0
        st = 0
        t=0
        
        mapping = {'top': ID}
        # Decrease epsilon by half of the size between current epsilon and the lower end of the interval we're convergin on
        if similar == True:
            epsilon = epsilon - delta
            similar = IsEpsSimilar(T1,T2, epsilon,costs=costs, roots=roots, subtrees=subtrees, mapping=mapping)
        else:
        # Increase epsilon by half of the size between current epsilon and the upper end of the interval we're convergin on
            epsilon = epsilon+delta
            similar = IsEpsSimilar(T1,T2, epsilon,costs=costs, roots=roots, subtrees=subtrees, mapping=mapping)
    
    #Actually get a matching lol
    if (valid and not similar):
        mapping = {'top': ID}
        its+=1
        epsilon += delta 
        similar = IsEpsSimilar(T1,T2, epsilon,costs=costs, roots=roots, subtrees=subtrees, mapping=mapping)
        
    if(get_map):
        return [epsilon, mapping]
    
    return epsilon
