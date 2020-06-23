# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 15:43:00 2020

@author: Candace
"""
# path to the FOLDER holding all parts of the data set
#p = "C:/Users/Candace/Box/Research/REUs/SURIEM/Munch - Embedded Graphs/SURIEM2020-EmbeddedGraphs/data/Letter-high"
#ds = "Letter-high"
import networkx as nx
# p: path to FOLDER containing all the data
# ds: name of data set i.e. "Letter-high"
# see https://chrsmrrs.github.io/datasets/docs/format/
def tud2nx(p, ds):
    pGen = p + "/" + ds
    pEdges = pGen + "_A.txt"
    pGraphs = pGen + "_graph_labels.txt"
    pNodeLabels = pGem + "_graph_indicator.txt"
    
    graphDict = {}
    
    graphs = open(pGraphs, "r")
    graphLine = graphs.readline()
    while graphLine != "":
        newGraph = nx.Graph()
        graphLabel = graphLine.rstrip("\n")
        
        if graphLabel not in graphDict:
            graphDict[graphLabel] = []
        
        graphDict[graphLabel].append(newGraph)
        
    
    