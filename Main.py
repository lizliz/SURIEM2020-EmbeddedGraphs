#Levent Batakci
#6/8/2020
#
#Testing file
import Visualization as v
import DataReader as dr
import math

vert = "./data/athens_small_vertices_osm.txt"
edge = "./data/athens_small_edges_osm.txt"

graph = dr.read_txt(edge, vert)
G = graph[0] #nx graph
pos = graph[1] #position dic


#v.input_output(G, pos)
#v.input_output_square(G, pos)
v.animate(G, pos, 60, "/animations/test1")