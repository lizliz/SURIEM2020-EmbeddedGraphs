#Levent Batakci
#6/8/2020
#This program compiles and organizes all our data-reading capabilities
import lib.txt2nx as txt
import lib.graphml2nx as graphml
import lib.osm2nx as osm


#txt reading
def read_txt(edge_path, vertex_path):
    return txt.make_graph(edge_path, vertex_path)

def read_txt_n(name):
    return txt.make(name)
##

#graphml reading
def read_graphml(path, draw = False):
    return graphml.read_graphml(path, draw)
##

#osm reading
def read_osm(path, draw = False):
    return osm.read_graphml(path, draw)
##