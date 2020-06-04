# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 22:12:46 2020

@author: Candace Todd
"""

# Will comment more later if needed
import networkx as nx

#G = nx.readwrite.graphml.read_graphml(path = "http:\vlado.fmf.uni-lj.si\pub\networks\data\sport\football.net" )

def graphml(filePath, draw = True):
    file = open(filePath, "r")
    contents = file.read()
    nodeList = contents.split("<node ")
    
    fixed_positions = {}
    i = 1
    while i < len(nodeList):
        
        # Find name of node
        nodeIDindex = nodeList[i].find("id")
        nodeIDindex += 4
        nodeID = nodeList[i][nodeIDindex]
        
        # Find x and y position
        xPosStartIndex = nodeList[i].find("positionX")
        xPosStartIndex += 11
        yPosStartIndex = nodeList[i].find("positionY")
        xPosEndIndex = yPosStartIndex - 2
        yPosStartIndex += 11
        yPosEndIndex = nodeIDindex - 7
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
    