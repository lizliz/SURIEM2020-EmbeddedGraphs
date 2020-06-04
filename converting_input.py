# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 15:56:55 2020

@author: artis
"""
import networkx as nx
import matplotlib.pyplot as plt

#The edge data we wish to extract
edgenames=[]
firstvertex=[]
secondvertex=[]

#Get it
edge_path = './data/athens_small_edges_osm.txt'
with open(edge_path) as edge:
    for x in edge.read().split('\n'):
        counter=1
        for y in x.split(','):
            if (counter==1):
                edgenames.append(y)
                counter+=1
            elif(counter==2):
                firstvertex.append(y)
                counter+=1
            elif(counter==3):
                secondvertex.append(y)
                counter+=1
edge.close()

G = nx.Graph()
edges = []
for i in range(len(firstvertex)):
    edges.append((firstvertex[i],secondvertex[i]))
G.add_edges_from(edges)


#The vertex data we wish to extract
vertexnames=[]
coordinate1=[]
coordinate2=[]

#Get it
edge_path = './data/athens_small_vertices_osm.txt'
with open(edge_path) as vertex:
    for x in vertex.read().split('\n'):
        counter=1
        for y in x.split(','):
            if (counter==1):
                vertexnames.append(y)
                counter+=1
            elif(counter==2):
                coordinate1.append(y)
                counter+=1
            elif(counter==3):
                coordinate2.append(y)
                counter+=1
vertex.close()

G.add_nodes_from(vertexnames)

pos_dict = {}
for i in range(len(vertexnames)):
    pos_dict[vertexnames[i]] = (coordinate1[i], coordinate2[i])

nx.draw(G,pos_dict)
plt.show()
