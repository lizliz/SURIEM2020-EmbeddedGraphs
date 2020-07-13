#Levent Batakci
#6/8/2020
#This program compiles and organizes all our data-reading capabilities
import lib.txt2nx as txt
import lib.graphml2nx as graphml
import lib.osm2nx as osm
import lib.json2nx as json
import lib.img2nx as img
import lib.tud2nx as tud
import lib.sm2nx as sm
import lib.ShapeMatcher as ppm
from lib.Tools import main_component


#txt reading
def read_txt(edge_path, vertex_path, main=True):
    g = txt.make_graph(edge_path, vertex_path)
    if(main):
        g[0] = main_component(g[0])
    return g

def read_txt_n(name):
    return txt.make(name)
##

#graphml reading
def read_graphml(path, draw = False, nodeSize = 0, labels = False, main=True):
    g = graphml.read_graphml(path, draw, nodeSize, labels)
    if(main):
        g[0] = main_component(g[0])
    return g
##

#osm reading
def read_osm(path, draw = False, nodeSize = 0, labels = False, main=True):
    g = osm.read_osm(path, draw, nodeSize, labels)
    if(main):
        g[0] = main_component(g[0])
    return g
##

#json
def read_json(path, draw = False, nodeSize = 0, labels = False, main=True):
    g = json.read_json(path, draw, nodeSize, labels)
    if(main):
        g[0] = main_component(g[0])
    return g
##

#img
def read_img(path, draw = False, node_size = 0, labels = False, main=True):
    g = img.read_img(path, draw=draw, nodeSize=node_size, labels=labels)
    if(main):
        g[0] = main_component(g[0])
    return g
##

# large groups of graphs from the TUD data set
def read_tud(path, name, reminder = True):
    g = tud.read_tud(path, name, reminder = reminder)
    return g

# large groups of graphs from the ShapeMaker databases, convert from XML to nx
def read_sm(path):
    g = sm.read_sm(path)
    return g

# large groups of graphs from the ShapeMaker databases, convert directly from binary ppm to nx
def read_ppm(DBname, ppmDir, ppmList = None, SMD = "images/ShapeMatcher"):
    g = ppm.read_ppm(DBname, ppmDir, ppmList, SMD)
    return g
