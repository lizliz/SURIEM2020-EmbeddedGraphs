#Levent Batakci
#6/9/2020
#
#This program is concerned witht he comparison of merge trees
import networkx as nx
from lib.Tools import f_, get_leaves, list_append
import math

#MEMOIZATION VARIABLES
D = {}

global tag

#The associated cost of matching a pair of vertices
#from two rooted representations of branchings
def match_cost(mu,su , mv,sv):
    #m represents the minima
    #s represents the saddle
    return max(math.abs(f_(mu)-f_(mv)), math.abs(f_(su)-f_(sv)))

#The associated cost of removing a vertex 
#from a rooted representation of a branching
def remove_cost(u,v):
    return math.abs(f_(u)-f_(v))/2

#Gets all of the child subtrees of a given root branch
def get_child_subtrees(root, minima, T):
    last = minima
    p = T.nodes[minima]['p']
     
    subtrees = []
    while(True):
        neighbors = T[p]
        
        #Add all the subtrees with child saddle p
        for n in neighbors:
            #Check that n is a child and not an ancestor of minima
            if (n != last and f_(n) < f_(p)):
                stree = sub_special(T, n)
                subtrees.append(stree)
        
        #We've traced back to the root
        if(p == root):
            return subtrees
        
        p = T.nodes[p]['p'] #Move to the next ancestor

#Gets a list including n and all of its descendants, recursively
def descendants(G, n):
    global tag
    
    neighbors = G[n]
    
    d = [n]
    for nei in neighbors:
        if(f_(G.nodes[nei]) < f_(G.nodes[n])):
            #Check if already computed
            if((tag + str(n)) not in D):
                D[tag + str(n)] = descendants(G, nei, tag)
            list_append(d, D[tag + str(n)])
           
    return d

#Returns the special subgraph identified by the almost-root
def sub_special(G, n):
    nodes = []
    list_append(nodes, descendants(G, n))
    nodes.append(G.nodes[n]['p'])

    #Induce the subgraph and return it
    return nx.Graph.subgraph(G, nodes)

#Returns true if the two given graphs are matchable for the given epsilon (e) 
def IsEpsSimilar(S, M, e, memo, rootS="NULL", rootM="NULL"):
    global tag

    if(rootS != "NULL"):
        S_ = rootS
    else:
        S_ = list(S.nodes)[0]
    
    if(rootM != "NULL"):
        M_ = rootM
    else:
        M_ = list(M.nodes)[0]
    
    
    #already computed
    if(S_ in memo and M_ in memo[S_]):
        return memo[S_][M_]
    
    
    minima_S = get_leaves(S)
    minima_M = get_leaves(M)
    #Iterate over all possible root branches
    for i in range(len(minima_S)):
        for j in range(len(minima_M)):
            
            #Check that the matching cost isn't too high
            #for the root branch*
            cost = match_cost(minima_S,S.root , minima_M,M.root)
            
            #Can't be matched.
            if(cost > e):
                    if(S_ not in memo):
                                memo[S_] = {}
                    memo[S_][M_] = False
                
            else:
                #Compare all of the subtrees
                #The subtree lists actually contain nx subgraphs
                tag = "TAG FOR S: "
                subtrees_S = get_child_subtrees(S.root, minima_S, S)
                tag = "TAG FOR M: "
                subtrees_M = get_child_subtrees(M.root, minima_M, M)
                
                #Set up the bipartite graph to later check for a cover
                bip = nx.Graph()
                for s in subtrees_S:
                    s1 = list(s.nodes)[0]
                    bip.add_node(s1)
                for m in subtrees_M:
                    m1 = list(m.nodes)[0]
                    bip.add_node(m1)

                #Compute the matchability of all the children
                for s in subtrees_S:
                    s_ = list(s.nodes)[0]
                    for m in subtrees_M:
                        m_ = list(m.nodes)[0]
                        
                        #This pairing hasn't been computed previously
                        if(s_ not in memo or m_ not in memo[s_]):
                            if(s not in memo):
                                memo[s_] = {}
                            memo[s_][m_] = IsEpsSimilar(s, m, e, memo)
                        
                        if(memo[s][m]):
                            bip.add_edge_from(s1,m1)
                            
                #Compute a maximum-cardinality matching!
                cover = nx.algorithms.matching.eppstein_matching(bip)
                #Check if it's a perfect cover
                if(len(cover.edges) == len(subtrees_S)):
                    if(S_ not in memo):
                                memo[S_] = {}
                    memo[S_][M_] = True
                    return True
                
                #Else, check the next child subtree pairing
                
                
    if(S_ not in memo):
        memo[S_] = {}
    memo[S_][M_] = False           
    return False #No matching found such that e_min <= e