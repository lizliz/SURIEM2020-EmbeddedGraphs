# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 22:12:46 2020

@author: Candace Todd
"""
import networkx as nx

#### NOTE: I made longitude values x values and latitude y values

# This function will take a .osm file and convert it into a networkx graph object
# This will NOT produce a directed and/or weighted graph

# The entire file path, including the file name itself and the file extension,
# must be a string

# By default the function will also draw the graph you give it

def read_osm(filePath, draw = True, nodeSize = 0, labels = False):
    G = nx.Graph()
    
    # Open the file and read in its contents as one long string
    file = open(filePath, mode = "r", encoding = "utf8")
    contents = file.read()
    
    # Split the contents into a list so that each element in the list
    # gives us info about one node
    # From looking at the files, I know osm files start a new node
    # with the string "<node
    nodeList = contents.split("<node ")
    
    # Go through the list of nodes and make a dictionary of each node's position
    fixed_positions = {}
    i = 1
    while i < len(nodeList):
        # the .find() method will find the string I give it and return the index
        # of the first character of the string I gave it, so to access the info I
        # need I have to add to the index it gives me.
        # For example, I know in osm files it says "id='4'" for node 4's id
        # If I say string.find("id") it will return the index of the character
        # 'i', so to get from the 'i' to the actual number we need to increase the index
        # Same sort of thing for the long and lat positions
        # This will all make a lot more sense if you open an osm file in notepad or something and look at the layout
        
        # Find name of node
        nodeIDStartindex = nodeList[i].find("id") + 4
        nodeIDEndindex = nodeList[i].find("visible") - 2
        nodeID = nodeList[i][nodeIDStartindex:nodeIDEndindex]
        
        # Find long and lat position
        longStartIndex = nodeList[i].find("lon=")
        latStartIndex = nodeList[i].find("lat=") + 5
        latEndIndex = longStartIndex - 2
        longStartIndex += 5
        
        # I noticed that all of the long and lat positions had 7 digits
        # after the decimal, so after finding the index of the decmial I could
        # easily find the rest of the number
        decimal = longStartIndex
        for char in nodeList[i][longStartIndex:]:
            if char == ".":
                break
            decimal += 1
        
        # Finding the end of the long number is different than lat because the long
        # is at the end of the line, and some of the lines end with different characters
        # whereas the lat number always ends right before the long number
        longEndIndex = decimal + 8
        long = float(nodeList[i][longStartIndex:longEndIndex]) # Convert strings
        lat = float(nodeList[i][latStartIndex:latEndIndex]) # To numbers
        
        # Add positions to dictionary
        fixed_positions[nodeID] = (long, lat)
        G.add_node(nodeID)
        
        i += 1 # move on to next node in the list
    
    # Split the contents into a list so that each element in the list
    # gives us info about one "way" which is basically like a line with
    # a bunch of nodes on it. I'm going to say that there are edges
    # bewteen consecutive nodes listed in a way.
    # From looking at the files, I know osm files start a new way
    # with the string "<way"
    wayList = contents.split("<way ")
    
    # We split each way up into a list of the nodes it contains
    w = 1
    while w < len(wayList):
        way = wayList[w]
        wayNodes = way.split("<nd ref=") # This is how nodes are identified in the .osm file
        
        # We're going to make a list of all of the nodes on this way
        # and then get the edges from that list
        n = 1
        nodesList = []
        while n < len(wayNodes):
            nodeString = wayNodes[n][1:]
            #Find and cut of the quotation mark from the node name
            nodeString = nodeString[:nodeString.find("\"")]
            nodesList.append(nodeString)
            n +=1
        
        # Add an edge between each pair of consecutive nodes
        j = 0
        while j < len(nodesList)-2:
            G.add_edge(nodesList[j], nodesList[j+1])
            j += 1
            
        # Now we've added all of the edges on this way, so we can move on
        w += 1
    
    # For some reason the .osm file that you export is sometimes outside of the
    # field of view on the map you're acually looking at, so we're going to delete
    # those nodes. This may need to be altered later because this might just
    # be a problem specific to openstreetmap.org
    minlat = float(contents[contents.find("minlat") + 8:contents.find("minlon")-2])
    minlon = float(contents[contents.find("minlon") + 8:contents.find("maxlat")-2])
    maxlat = float(contents[contents.find("maxlat") + 8:contents.find("maxlon")-2])
    maxlon = float(contents[contents.find("maxlon") + 8:contents.find("/>\n")-1])
    
    file.close() # close the file

    # Give each node their long and lat attributes
    for node in list(G.nodes):
        lon = fixed_positions[node][0]
        lati = fixed_positions[node][1]
        
        # Remove nodes outside of our range of view
        if (lon < minlon) or (lon > maxlon) or (lati < minlat) or (lati > maxlat):
            G.remove_node(node)
            del fixed_positions[node]
        else:
            G.nodes[node]['longitude'] = lon
            G.nodes[node]['latitude'] = lati
    
    # Draw it if desired
    if draw == True:
        fixed_nodes = fixed_positions.keys()
        pos = nx.spring_layout(G,pos=fixed_positions, fixed = fixed_nodes)
        nx.draw_networkx(G,pos, with_labels = labels, node_size = nodeSize)
    
    # Returns the graph object and position dictionary
    return [G, fixed_positions]