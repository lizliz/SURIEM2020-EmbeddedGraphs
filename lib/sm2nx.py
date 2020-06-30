# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 18:26:11 2020

@author: Candace Todd
"""
import networkx as nx
# Turns ShapeMatchers XML files into a networkx object that retains the x and y values
# This will NOT produce a directed and/or weighted graph

# The entire file path, including the file name itself and the file extension,
# must be a string

# By default the function will also draw the graph you give it
def read_sm(path, draw = True, nodeSize = 0, labels = False, main=True):
    G = nx.Graph()
    file = open(path, "r")
    contents = file.read()

p = "C:/Users/Candace/Downloads/hand.txt"
read_sm(p,True,10,True,True)

