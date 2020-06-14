# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 15:09:59 2020

@author: Candace Todd
"""
import networkx as nx

# Will add comments later when I have better internet
# WARNING: Not thouroughly tested
# ANOTHER WARNING: Some of these have been taking a few minutes to run for 
# graphs with a lot of nodes
###############################################################################
# Converting Json to Nx

# This is basically what geoJSON files look like: http://djjr-courses.wikidot.com/128:geojson
# This is another good example: https://terraformer-js.github.io/glossary/#:~:text=A%20GeoJSON%20bounding%20box%20is,45.51%2C%20%2D122.64%2C%2045.53%5D
# As far as I can tell, geoJSON files are made up uf different kinds of collections of points;
# Polygons, lines, etc. But all of these geometries have coordinates, so we 
# split up our contents by strings of coordinates. This way we know where to 
# put our edges (sets of coordinates in one geometry have a line running through them)


# function takes a .json file in geoJSON format and outputs a networkx graph
# in my experience when testing this function, geoJSON files have a
# .json extension, not .geojson
def read_json(path, draw = True):
    json_file = open(path, mode = "r")
    contents = json_file.read()
    contents_list = contents.split("coordinates")
    G = nx.Graph()
    
    i = 1
    point_positions = {}
    while i < len(contents_list):
        coordinates = contents_list[i]
        coord_points = coordinates.split("],[")
        
        x, y, last_point = None, None, None
        
        #breakpoint()
        for point in coord_points:
            end = point.find("]]]")
            beginning = point.find('[[[')
            
            if end != -1:
                point = point[:end]
            if beginning != -1:
                point = point[5:]
            
            
            newLine = point.find("]")
            startLine = point.find("[")
            
            if  newLine != -1:
                point = point[:-1]
            if startLine != -1:
                point = point[1:]
                
            comma = point.find(",")
            x = float(point[:comma])
            y = float(point[comma+1:])
            G.add_node(point)# Have to add the coordinate as the point's name
            G.nodes[point]["x"] = x
            G.nodes[point]["y"] = y
            point_positions[point] = (x,y)
                
            # If we aren't at the beginning
            if last_point != None:
                #last_point = str(lastx) + "," + str(lasty) 
                G.add_edge(last_point, point)
            
            # If we are at the end
            if newLine != -1:# or end != -1:
                last_point = None
            else:
                last_point = point
        
        i += 1
    
    json_file.close()      
    if draw == True:
        options = {"node_size":0,"edge_color" : "black"}
        graph_points = point_positions.keys()
        pos = nx.spring_layout(G, pos = point_positions, fixed = graph_points)
        nx.draw_networkx(G, pos, with_labels = False, **options)
    
    return G         