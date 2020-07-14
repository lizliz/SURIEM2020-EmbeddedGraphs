# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 18:26:11 2020

@author: Candace Todd
"""
import networkx as nx
# Turns ShapeMatchers XML files into a networkx object that retains the x and y values
# This will NOT produce directed and/or weighted graphs

# The entire file path, including the file name itself and the file extension,
# must be a string

def read_sm(path):
    file = open(path, mode ='r', encoding='utf-8')
    contents = file.read()
    graphList = contents.split('<DAG class="ShockGraph" ')
    
    g = 1
    graphDict = {}
    while g < len(graphList):
        G = nx.Graph()
        pos = {}
        graph = graphList[g]
        nodeCountStart = 11
        nodeCountEnd = 11 + graph[11:].find('"')
        nodeCount = int(graph[nodeCountStart:nodeCountEnd])
        if nodeCount < 1:
            g+=1
            continue
        objectNameStart = 12 + graph.find("<objectName>")
        objectNameEnd = objectNameStart + graph[objectNameStart:].find("</object")
        objectName = graph[objectNameStart:objectNameEnd]
        if objectName not in graphDict:
            graphDict[objectName] = []
        
        #start finding the nodes
        wayList = graph.split("<node ")
        w = 1
        #initialize the node if it doesnt exits!
        # if theres more than one, make a way
        while w < len(wayList):
            way = wayList[w]
            pointCount = 12 + way.find('<pointCount>')
            if int(way[pointCount]) < 1:
                w += 1
                continue
            pointList = way.split("<point ")
            p = 1
            firstPoint = None
            lastPoint = None
            while p < len(pointList):
                point = pointList[p]
                
                xStart = 1 + point.find('"')
                xEnd = point.find("ycoord") - 2
                x = point[xStart:xEnd]
                
                yStart = xEnd + 10
                yEnd = point.find("radius") - 2
                y = point[yStart:yEnd]
                
                pointName = x + ",-" + y
                #if pointName == "153,-143":
                    #breakpoint()
                if pointName not in list(G.nodes):
                    if p == 1 or p == (len(pointList)-1):
                        G.add_node(pointName)
                        x, y = float(x), float(y)*-1
                        G.nodes[pointName]['x'] = x
                        G.nodes[pointName]['y'] = y
                        pos[pointName] = (x,y)
                    
                if p ==1:
                    temp = pointName
                    firstPoint = temp
                #if p > 1:
                #    G.add_edge(lastPoint, pointName)
                if p != len(pointList)-1:
                    lastPoint = pointName
                    
                p += 1
                
            G.add_edge(firstPoint, pointName)
            w += 1
        
        
        graphDict[objectName].append( (G,pos) )
        
        g += 1
    keys = list(graphDict.keys())
    print("\n\tGraph Categories: ", keys)
    print("\tI am returning a dictionary of graph categories.")
    print("\tEach value in the dictionary is a LIST of (Graph, Position Dictionary) tuples.")
    return graphDict