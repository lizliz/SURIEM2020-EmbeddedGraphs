# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 22:12:46 2020

@author: Candace Todd
"""

# Will comment more later if needed
import networkx as nx

# This function will take a .graphml file and convert it into a networkx graph
# This will NOT produce a directed graph and will NOT give any edges a weight
# It won't break if you feed it a weighted directed graph, but the graph you
# get out won't be weighted or directed

# The entire file path, including the file name itself and the file extension,
# must be a string
# By default the function will also draw the graph you give it

def read_graphml(filePath, draw = True, nodeSize = 0, labels = False):
    
    # Open the file and read in its contents as one long string
    file = open(filePath, "r")
    contents = file.read()
    
    # Split the contents into a list so that each element in the list
    # gives us info about one node
    # From looking at the files, I know graphML files start a new node
    # with the string "<node
    nodeList = contents.split("<node ")
    
    # Go through the list of nodes and make a dictionary of each node's position
    fixed_positions = {}
    i = 1
    while i < len(nodeList):
        # the .find() method will find the string I give it and return the index
        # of the first character of the string I gave it, so to access the info I
        # need I have to add to the index it gives me.
        # For example, I know in graphML files it says "id='4'" for node 4's id
        # If I say string.find("id") it will return the index of the character
        # 'i', so to get from the 'i' to the actual number we need to increase the index
        # Same sort of thing for the x and y positions
        # This will all make a lot more sense if you open a GraphML file in notepad or something and look at the layout
        
        # Find name of node
        nodeIDStartindex = nodeList[i].find("id") + 4
        nodeIDEndindex = nodeList[i].find("mainText") - 2
        nodeID = nodeList[i][nodeIDStartindex:nodeIDEndindex]
        
        # Find x and y position
        xPosStartIndex = nodeList[i].find("positionX") + 11
        yPosStartIndex = nodeList[i].find("positionY")
        xPosEndIndex = yPosStartIndex - 2
        yPosStartIndex += 11
        yPosEndIndex = nodeIDStartindex - 6
        xPos = float(nodeList[i][xPosStartIndex:xPosEndIndex]) # Convert strings
        yPos = float(nodeList[i][yPosStartIndex:yPosEndIndex]) # To numbers
        
        # Add positions to dictionary
        # I multiplied the vertical position by -1 because the graphs 
        # kept appearing upside down and I didn't know why
        fixed_positions[nodeID] = (xPos, yPos*(-1)) 
        
        i += 1 # move on th next node in the list
    
    file.close() # close the file
    
    # Use networkx's inbuilt method to build the graph
    G = nx.readwrite.graphml.read_graphml(path = filePath)  
    
    # Networkx doesn't get positions from GraphML files so we use our position dictionary
    for node in list(G.nodes):
        G.nodes[node]['x'] = fixed_positions[node][0]
        G.nodes[node]['y'] = fixed_positions[node][1]
    
    # Draw it if desired
    if draw == True:
        fixed_nodes = fixed_positions.keys()
        pos = nx.spring_layout(G,pos=fixed_positions, fixed = fixed_nodes)
        nx.draw_networkx(G,pos, node_size = nodeSize, with_labels = labels)
    
    # Returns the graph object and position dictionary
    return [G,fixed_positions]
    