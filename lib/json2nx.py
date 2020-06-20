# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 15:09:59 2020

@author: Candace Todd
"""
import networkx as nx

# WARNING: Not thouroughly tested, although I'm pretty sure it works
# ANOTHER WARNING: Some of these have been taking a few minutes to run for 
#                  graphs with a lot of nodes
###############################################################################
# Converting Json to Nx

# This is basically what geoJSON files contain: http://djjr-courses.wikidot.com/128:geojson
# This is another good example: https://terraformer-js.github.io/glossary/#:~:text=A%20GeoJSON%20bounding%20box%20is,45.51%2C%20%2D122.64%2C%2045.53%5D
# As far as I can tell, geoJSON files are made up uf different kinds of collections of points;
# Polygons, lines, etc. All of these geometries have coordinates along them, so we 
# split up our contents by groups of coordinates. This way we know where to 
# put our edges (sets of coordinates in one geometry have a line running through them)


# Function takes a .json file in geoJSON format and outputs a networkx graph
# in my experience when testing this function, geoJSON files have a
# .json extension, not .geojson
def read_json(path, draw = True, nodeSize = 0, labels = False): 
    json_file = open(path, mode = "r") # Open the file
    contents = json_file.read() # Read in all the contents of the file as one long string
    contents_list = contents.split("coordinates") # Split up the string by each group of coordinates
    G = nx.Graph() # Initialize an empty graph
    
    i = 1
    point_positions = {} # initialize a position dictionary
    while i < len(contents_list): # loop through each group of coordinates
        coordinates = contents_list[i]
        coord_points = coordinates.split("],[")
        # Coordinates in geoJSON files are listed like lists with 2 elements 
        # (instead of like the tuples we're used to seeing)
        
        x, y, last_point = None, None, None # Reset our tracking variables
        
        for point in coord_points:
            end = point.find("]]]") # ]]] means we reached the end of our line running through the group of coordinates
            beginning = point.find('[[[') # [[[ means we reached the end of our line running through the group of coordinates
            
            # If we're at the end or beginning remove the extra brackets so we can extract the numbers easily
            if end != -1: 
                point = point[:end]
            if beginning != -1:
                point = point[5:]
            
            # Sometimes there are separate groups of coordinates within groups of coordinates
            # If there are still lone brackets at this point then that means we've reached
            # The beginning or the end of a new line running through a group of coordinates
            newLine = point.find("]")
            startLine = point.find("[")
            
            # Remove the extra bracket so we can extract the numbers easily
            if  newLine != -1:
                point = point[:-1]
            if startLine != -1:
                point = point[1:]
                
            comma = point.find(",")
            x = float(point[:comma])
            y = float(point[comma+1:])
            G.add_node(point)# Have to add the coordinate as the point's name since there are no other unique identifiers
            G.nodes[point]["x"] = x # Give each node position attributes
            G.nodes[point]["y"] = y
            point_positions[point] = (x,y) # Add positions to dictionary
                
            # If we aren't at the beginning of a new line,
            # Add an edge between the previous and current point
            if last_point != None:
                G.add_edge(last_point, point)
            
            # If we are at the end, don't set the current point as the next last_point
            if newLine != -1:# or end != -1:
                last_point = None
            else:
                last_point = point
        
        i += 1
    
    json_file.close()      
    
    # Draw graph if desired
    if draw == True:
        graph_points = point_positions.keys()
        pos = nx.spring_layout(G, pos = point_positions, fixed = graph_points)
        nx.draw_networkx(G, pos, node_size = nodeSize, with_labels = labels)
    
    # Return networkx graph object and position dictionary
    return [G, point_positions]         