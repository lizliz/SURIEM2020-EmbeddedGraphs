# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 22:12:46 2020

@author: Candace Todd
"""

# Will comment more later if needed
import networkx as nx

# This function will take a .graphml file and convert it into a networkx graph
# The entire file path, including the file name itself and the file extension,
# must be a string
# By default the function will also draw the graph you give it

def graphml(filePath, draw = True):
    
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
        
        # Find name of node
        nodeIDStartindex = nodeList[i].find("id") + 4
        nodeIDEndindex = nodeList[i].find("mainText") - 2
        #nodeIDEndindex -= 2
        #nodeIDStartindex += 4 
        nodeID = nodeList[i][nodeIDStartindex:nodeIDEndindex]
        
        # Find x and y position
        xPosStartIndex = nodeList[i].find("positionX") + 11
        #xPosStartIndex += 11
        yPosStartIndex = nodeList[i].find("positionY")
        xPosEndIndex = yPosStartIndex - 2
        yPosStartIndex += 11
        yPosEndIndex = nodeIDStartindex - 7
        xPos = float(nodeList[i][xPosStartIndex:xPosEndIndex])
        yPos = float(nodeList[i][yPosStartIndex:yPosEndIndex])
        
        fixed_positions[nodeID] = (xPos,yPos)
        
        i += 1
    
    file.close()
    
    G = nx.readwrite.graphml.read_graphml(path = filePath)  
    
    for node in list(G.nodes):
        G.nodes[node]['x'] = fixed_positions[node][0]
        G.nodes[node]['y'] = fixed_positions[node][1]
    
    if draw == True:
        fixed_nodes = fixed_positions.keys()
        pos = nx.spring_layout(G,pos=fixed_positions, fixed = fixed_nodes)
        nx.draw_networkx(G,pos)
        #fixed_positions = {1:(0,0),2:(1,2),3:(2,0),4:(1,1)}#dict with two of the positions set
    
    return G
    