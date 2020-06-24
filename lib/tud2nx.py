# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 15:43:00 2020

@author: Candace Todd
"""
import networkx as nx
import pdb
# p: path to FOLDER containing all the data
# ds: name of data set i.e. "Letter-high"
# see https://chrsmrrs.github.io/datasets/docs/format/
def tud2nx(p, ds):
    pGen = p + "/" + ds
    pEdges = pGen + "_A.txt"
    pGraphLabels = pGen + "_graph_labels.txt"
    pGraphIDs = pGen + "_graph_indicator.txt"
    #pNodeLabels = pGen + "_node_labels.txt"
    pNodeAtts = pGen + "_node_attributes.txt"
    
    graphDict = {} # Dictionary of graphs, keys are graph labels (NOT graph IDs)
    allGraphs = {} # Key = graphID, value = label, object, node list tuple
    allNodes = {} # Key = nodeID, value = graph label, graph object tuple
    
    ### Getting Graph IDs
    graphIDs = open(pGraphIDs, "r")
    graphIDsContents = graphIDs.read()
    graphsIDsList = graphIDsContents.split("\n")# List of all the graph IDs, line number corresponds to a node id #
    graphIDs.close() # Close file
    
    ### Getting Graph Labels
    graphLabels = open(pGraphLabels, "r")
    graphLabelsContents = graphLabels.read()
    graphLabelsList = graphLabelsContents.split("\n") # List of all graph labels, line number = a graph id
    graphLabels.close()
    
    ### Getting all edges
    graphEdges = open(pEdges, "r")
    graphEdgesContents = graphEdges.read()
    graphEdgesList = graphEdgesContents.split("\n") # Each line is an edge
    graphEdges.close()
        
    ### Getting node attributes
    nodeAtts = open(pNodeAtts, "r")
    nodeAttsContents = nodeAtts.read()
    nodeAttsList = nodeAttsContents.split("\n") # List of all node atts, line number = the node id
    nodeAtts.close()
    
    n = 0
    while n < len(nodeAttsList):
        if nodeAttsList[n] == "":
            print("Nothing node!!!!")
            break
        
        nodeID = n + 1 # since indexing starts at 0 in python
        x = nodeAttsList[n].split(",")[0]
        y = nodeAttsList[n].split(",")[1][1:] # trim white space
        x, y = float(x), float(y)
        
        # To figure out which graph this node belongs to, look in the graph indicator list
        graphID = graphsIDsList[n] # Get the graph id at the same index as the node
        graphID = int(graphID)
        graphLabel = graphLabelsList[graphID-1] # Get the graph label, subtract 1 from id since indexing starts at 0
        
        # Get its graph; create it if it doesn't exist yet
        if graphID not in allGraphs:
            nodesGraph = nx.Graph()
            allGraphs[graphID] = (graphLabel,nodesGraph,[nodeID])
        else:
            #breakpoint()
            nodesGraph = allGraphs[graphID][1]
            allGraphs[graphID][2].append(nodeID)
        
        #breakpoint()
        # Add to Node dictionary
        allNodes[nodeID] = (graphLabel,nodesGraph)
        
        # Add the node to the graph with its attributes
        nodesGraph.add_node(int(nodeID))
        nodesGraph.nodes[int(nodeID)]["x"] = x
        nodesGraph.nodes[int(nodeID)]["y"] = y

        # Create a spot for graphs of this label if it doesn't already exist        
        if graphLabel not in graphDict:
            graphDict[graphLabel] = []

        # Add this graph to the list of graphs with this label if it isn't there
        if nodesGraph not in graphDict[graphLabel]:
            graphDict[graphLabel].append(nodesGraph)
        n += 1
        
    e = 0
    while e < len(graphEdgesList):
        node1 = graphEdgesList[e].split(",")[0]
        #breakpoint()
        if node1 == "":
            print("Empty edge!!")
            break
        node1 = int(node1)
        node2 = int(graphEdgesList[e].split(",")[1][1:])
            
        # Acess the graph that this edge belongs to
        edgesGraph = allNodes[node1][1]
        edgesGraph.add_edge(node1,node2)
        
        # Each edge is listed twice so we can increment by 2
        e += 2

    print("I'm about to return a list of dictionaries in the following format:")
    print("[keys are graph labels and values are lists of graph objects,")
    print("keys are graph IDs and values are (graph label, graph object, node list) tuple,")
    print("keys are node IDs and values are (graph label, graph object) tuple]")
    
    return [graphDict, allGraphs, allNodes]
            
p = "C:/Users/Candace/Box/Research/REUs/SURIEM/Munch - Embedded Graphs/SURIEM2020-EmbeddedGraphs/data/Letter-high"
ds = "Letter-high"
z = tud2nx(p,ds)        
        
    
    