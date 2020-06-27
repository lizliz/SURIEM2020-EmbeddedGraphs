# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 15:43:00 2020

@author: Candace Todd
"""
import networkx as nx
# p: path to FOLDER containing all the data
# ds: name of data set i.e. "Letter-high"
# see https://chrsmrrs.github.io/datasets/docs/format/

def read_tud(path, name, reminder = True):
    pGen = path + "/" + name + "_"
    pEdges = pGen + "A.txt"
    pGraphLabels = pGen + "graph_labels.txt"
    pGraphIDs = pGen + "graph_indicator.txt"
    pNodeAtts = pGen + "node_attributes.txt"
      
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
    graphLabels.close() # Close file
    
    ### Getting all edges
    graphEdges = open(pEdges, "r")
    graphEdgesContents = graphEdges.read()
    graphEdgesList = graphEdgesContents.split("\n") # List of edges; Each line is an edge
    graphEdges.close() # Close file
        
    ### Getting node attributes
    nodeAtts = open(pNodeAtts, "r")
    nodeAttsContents = nodeAtts.read()
    nodeAttsList = nodeAttsContents.split("\n") # List of all node atts, line number = the node id
    nodeAtts.close() # Close file
    
    n = 0
    while n < len(nodeAttsList):
        if nodeAttsList[n] == "":
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
            nodesGraph = allGraphs[graphID][1]
            allGraphs[graphID][2].append(nodeID)
        
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
        nodeList = graphEdgesList[e].split(",")
        if nodeList[0] == "":
            break
        
        # Strip the white spaces
        for number in range(len(nodeList)):
            nodeList[number] = nodeList[number].strip()
            
        node1 = int(nodeList[0])
        node2 = int(nodeList[1])
            
        # Acess the graph that this edge belongs to
        edgesGraph = allNodes[node1][1]
        edgesGraph.add_edge(node1,node2)
        
        # Each edge is listed twice so we can increment by 2
        e += 2
    if reminder == True:
        print("I'm about to return a list of dictionaries in the following format:")
        print("[keys are graph labels and values are lists of graph objects,")
        print("keys are graph IDs and values are (graph label, graph object, node list) tuple,")
        print("keys are node IDs and values are (graph label, graph object) tuple]")

    return [graphDict, allGraphs, allNodes]
            
# p = "./data/Letter-low"
# ds = "Letter-low"
# z = tud2nx(p,ds)        

# def get_z():
#     return z
        