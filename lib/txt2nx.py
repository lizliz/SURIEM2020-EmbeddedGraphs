#This file reads '.txt' files and creates nx graphs
import networkx as nx

#Sets the edges
def set_edges(G, edge_path):
    #The edge data we wish to extract
    edgenames=[]
    firstvertex=[]
    secondvertex=[]
    
    #Get it
    with open(edge_path) as edge:
        for x in edge.read().split('\n'):
            counter=1
            for y in x.split(','):
                if (counter==1):
                    edgenames.append(float(y))
                    counter+=1
                elif(counter==2):
                    firstvertex.append(float(y))
                    counter+=1
                elif(counter==3):
                    secondvertex.append(float(y))
                    counter+=1
    edge.close()
    
    edges = []
    for i in range(len(firstvertex)):
        edges.append((firstvertex[i],secondvertex[i]))
    G.add_edges_from(edges)

#Sets the vertices and returns the position dictionary 
def set_vertices(G, vertex_path):
    #The vertex data we wish to extract
    vertexnames=[]
    coordinate1=[]
    coordinate2=[]
    
    #Get it
    with open(vertex_path) as vertex:
        for x in vertex.read().split('\n'):
            counter=1
            for y in x.split(','):
                if (counter==1):
                    vertexnames.append(float(y))
                    counter+=1
                elif(counter==2):
                    coordinate1.append(float(y))
                    counter+=1
                elif(counter==3):
                    coordinate2.append(float(y))
                    counter+=1
    vertex.close()
    
    pos_dict = {}
    for i in range(len(vertexnames)):
        pos_dict[vertexnames[i]] = (coordinate1[i], coordinate2[i])

    G.add_nodes_from(vertexnames)
    
    return pos_dict
    
#Makes the graph, given the edges and vertices data paths
def make_graph(edge_path, vertex_path):
    G = nx.Graph()

    set_edges(G, edge_path)
    
    pos_dict = set_vertices(G, vertex_path)
    
    return [G, pos_dict]

#Relies on the data files being named with the proper naming convention
#That is, "[Name]_edges.txt" etc.
def make(name):
    return make_graph("./data/" + name + "_edges.txt", "./data/" + name + "_vertices.txt")
    