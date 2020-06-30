#Levent Batakci
#6/23/2020
#
#Dendro
import scipy.cluster.hierarchy as shc
import scipy.spatial.distance as ssd
import pandas as pd
import numpy as np
from sklearn.manifold import MDS
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt
from DataCalculations import average_distance
from lib.Tools import random_tree_and_pos, get_pos
import random
import DataReader as dr
import lib.Tools as t
import lib.tud2nx as tud
import matplotlib.colors as colors
import matplotlib.cm as cmx
import timeit
import time
#import Visualization as v
#from sympy import Matrix, pprint# old code from confusion matrix days

# Input list should be a list of pairs of graphs & positions
# data should be a 1-D condesed distance matrix if you use it
# I had to make the default data value 0 instead of None because 
def draw_dendro(input_list, frames=180, data = None, labels=None, thresh=None):
    if type(data) == type(None):
        data = get_data(input_list, frames)[0]    
    dendrogram(data, labels=labels, thresh=thresh)
    return data
            
# data parameter is a 1-D condensed distance matrix or a 2-D array of observation vectors
# data parameter is NOT a 2D distance matrix, pass a 2D distance matrix through get_data first
def dendrogram(data, labels=None, thresh=None):
    plt.figure(figsize=(10, 7))  
    plt.title("Dendrograms")
    lkg = shc.linkage(data, method='single')
    dend = shc.dendrogram(lkg, leaf_rotation = 90 , labels=labels, color_threshold=thresh)
    if(thresh != None):
        plt.axhline(y=thresh, color='r', linestyle='--')
    
# converts 2-D distance matrix to 1-D condensed distance matrix
def condense(two_dimension_distance_matrix):
    return ssd.squareform(two_dimension_distance_matrix)

# Returns a 2D Distance matrix
def get_matrix(input_list, frames = 180, p = True, TIME = False):
    start = time.time()
    count = len(input_list)
    data = np.zeros(shape=(count,count))
    
    for i in range(count):
        
        for j in range(i, count):
            if p == True:
                print("(",i,",",j,")")
            
            if(i==j):
                val=0
            else:
                G1 = input_list[i][0]
                pos1 = input_list[i][1]
                G2 = input_list[j][0]
                pos2 = input_list[j][1]
                val=average_distance(G1, pos1, G2, pos2, frames=frames)
            
            data[i,j] = val
            data[j,i] = val
    
    if TIME == True:
        print("Making Distance Matrix: " + str(time.time() - start))
    return data

# I made this its own function so I could use it in mds
def get_data(input_list, frames = 180, p = True, TIME = False):
    
    data = get_matrix(input_list, frames = frames, p = p, TIME = TIME)
    flattened = condense(data)
    
    return [flattened, data]

# input_list: ordered list of graphs
# frames: same as before; number of frames from the rotation
# target_list: ordered list of the TARGET LABELS for the graphs, for example ["cats","cats","dogs"...] (NOT ["cat1", "cat2","dog1"...])
# D: 2D Distance matrix
# Colorize: whether or not you want to see the graph color coded according to the target labels
# scheme: see color map options: https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
# Adapted coloring method from https://stackoverflow.com/questions/8931268/using-colormaps-to-set-color-of-line-in-matplotlib
# Adapted MDS method from https://jakevdp.github.io/PythonDataScienceHandbook/05.10-manifold-learning.html
def mds(input_list, target_list, frames=180, D = None, colorize = True, scheme = "jet", legend = True, alpha = 0.4, TIME = True):
    if type(D) == type(None):
        D = get_data(input_list, frames, p = True, TIME = TIME)[1] # Get a distance matrix from the input list
    model = MDS(n_components=2, dissimilarity='precomputed', random_state=1)
    coords = model.fit_transform(D) # Outputs an array of the coordinates
    
    if colorize == False:
        x = coords[:, 0] # Get the x values
        y = coords[:, 1] # Get the y values
        plt.scatter(x, y) # Plot them
        plt.axis('equal')
    
    else: 
        
        label = {} # Dictionary of target labels
        for i in range(len(target_list)):# Find all the target labels in the data
            lbl = target_list[i]
            
            if lbl not in label:
                label[lbl] = []    
            label[lbl].append(i) # Keep track of the index of each element with this label
        
        clusters = [] #List of (label, Xarray, Yarray) tuples
        for l in label:
            Xs = []# Keep track of the x and y values of elements with this label
            Ys = []
            
            for index in label[l]: # Get the coordinates of elements with this label
                Xs.append(coords[:,0][index]) # Get the x value
                Ys.append(coords[:,1][index]) # Get the y value    
            clusters.append((l, np.array(Xs), np.array(Ys))) 
            
        fig = plt.figure() #initialize figure
        ax = fig.add_subplot(111) # 1x1 grid, 1st subplot
        values = range(len(label))
        jet = cm = plt.get_cmap(scheme) # Use matplotlib's jet color scheme by default
        cNorm  = colors.Normalize(vmin=0, vmax=values[-1])
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
        
        for j in range(len(clusters)):
 
            colorVal = scalarMap.to_rgba(values[j])
            colorText = (str(clusters[j][0]))
            retPoints = plt.scatter(x = clusters[j][1], 
                                   y = clusters[j][2], 
                                   c = [colorVal],# Make 'c' a vector to keep long warning message from printing
                                   label = colorText,
                                   alpha = alpha)
           
            if legend == True:
                handles,labels = ax.get_legend_handles_labels()
                ax.legend(handles, labels, loc='upper right')
        
        plt.axis('equal')
        plt.show()
 
    return coords    
################################## Testing Letters ###########################
if __name__ == '__main__':
    inputs = []
    labels = []
    target = []
     
    p = "data/Letter-low"
    ds = "Letter-low"
    z = tud.read_tud(p,ds,False)
    num = 5
    frames = 10
    scheme = "nipy_spectral"#"jet"#"rainbow"# some good color choices
    alpha = 0.6 #Translucency of the points
    letters = { # There are 150 graphs of each letter in letter-low
        	"K":"0",
            "N":"1",
            "L":"2",
            "Z":"3",
            "T":"4",
            "X":"5",
            "F":"6",
            "V":"7",
            "Y":"8",
            "W":"9",
            "H":"10",
            "A":"11",
            "I":"12",
            "E":"13",
            "M":"14"
            }
#"N","M","Z", "L", "W", "V", "E", and "M" get the best results in my opinion
    for letter in letters:
        # Only graph the letters you're interested in
        if letter not in ["N","M","Z", "L", "W", "V", "E", "M"]:
            continue
        for i in range(num):
            G = z[0][letters[letter]][i]
            G = t.main_component(G = G, report = False)
            pos = get_pos(G)
            inputs.append( (G, pos) )
            labels.append(letter + str(i))
            target.append(letter)
            
matrix = get_matrix(inputs, frames, True, True)
flat = condense(matrix)
points = mds(inputs,target,frames,matrix,True,scheme,True,alpha,True)
data = draw_dendro(inputs, data = flat, frames=frames, labels=labels, thresh=0.38)

######################### Testing Subgraphs ####################################
if __name__ == '__main__':
    inputs = []
    labels = []
    target = []
     
    p1 = "data/SanJoaquinCounty.json"
    w = dr.read_json(p1,False)[0]
    
    p2 = "data/eureka.json"
    x = dr.read_json(p2,False)[0]
    
    p3 = "data/atlanta.osm"
    y = dr.read_osm(p,False)[0]
    
    p4 = "data/lancaster.osm"
    u = dr.read_osm(p,False)[0]
    
    p5 = "data/dc.osm"
    v = dr.read_osm(p,False)[0]
    
    num = 5 # Number of selections from the graph
    nodes = 100 # Number of nodes you want eat random selection to have
    frames = 45
    scheme = "jet"#"nipy_spectral"#"rainbow"# some good color choices
    alpha = 0.6 #Translucency of the points
    graphs = {
        "SanJoaquin":(w,[]),# Tuple with full graph object and list of all the randomly picked subgraphs
        "Eureka":(x,[]),
        "Atlanta":(y,[]),
        "Lancaster":(u,[]),
        "DC":(v,[])
              }

    for graph in graphs:
        if graph not in ["Eureka", "SanJoaquin"]: # Graphs you want
            continue
        for i in range(num):
            G = t.random_component(graphs[graph][0], nodes) #Get random subgraph
            pos = get_pos(G)
            graphs[graph][1].append(G)
            inputs.append( (G, pos) )
            labels.append(graph + str(i))
            target.append(graph)
            
matrix = get_matrix(inputs, frames, True, True)
flat = condense(matrix)
points = mds(inputs,target,frames,matrix,True,scheme,True,alpha,True)
data = draw_dendro(inputs, data = flat, frames=frames, labels=labels, thresh=0.38) 
########################### Comparing Letters####################################

    # #Get 5 Z's
    # for i in range(num):
    #     G = z[0]["3"][i]
    #     G = t.main_component(G)
    #     pos = get_pos(G)
        
    #     inputs.append( (G, pos) )
    #     labels.append("Z " + str(i))
    #     target.append("Z")
    
    # #Get 5 L's
    # for i in range(num):
    #     G = z[0]["2"][i]
    #     G = t.main_component(G)
    #     pos = get_pos(G)
        
    #     inputs.append( (G, pos) )
    #     labels.append("L " + str(i))
    #     target.append("L")
    
    # #Get 5 N's
    # for i in range(num):
    #     G = z[0]["1"][i]
    #     G = t.main_component(G)
    #     pos = get_pos(G)
        
    #     inputs.append( (G, pos) )
    #     labels.append("N " + str(i))
    #     target.append("N")
        
    # #Get 5 V's
    # for i in range(num):
    #     G = z[0]["7"][i]
    #     pos = get_pos(G)
    #     G = t.main_component(G)
        
    #     inputs.append( (G, pos) )
    #     labels.append("V " + str(i))
    #     target.append("V")
   
####################### Comparing Cat Graphs  #####################################

    # pth = "./data/kitty2.graphml"  #0
    # inp = dr.read_graphml(pth)
    # inputs.append(inp)
    
    # pth = "./data/kitty1.graphml"  #1
    # inp = dr.read_graphml(pth)
    # inputs.append(inp)
    
    # pth = "./data/kitty2.graphml"  #2
    # inp = dr.read_graphml(pth)
    # inputs.append(inp)
    
    # pth = "./data/brutus.graphml"  #3
    # inp = dr.read_graphml(pth)
    # inputs.append(inp)
    
    # pth = "./data/sofie.graphml"  #4
    # inp = dr.read_graphml(pth)
    # inputs.append(inp)
    
    # labels = ["kitty2 (1)","kitty1","kitty2 (2)","Brutus","Sofie"]

###################### Comparing Cat and Dog images ###########################  
 
    # pth = "./data/Binary Images/cat2.png"  #0
    # inp = dr.read_img(pth)
    # inputs.append(inp)
    
    # pth = "./data/Binary Images/cat3.png"  #0
    # inp = dr.read_img(pth)
    # inputs.append(inp)
    
    # pth = "./data/Binary Images/dog1.png"  #0
    # inp = dr.read_img(pth)
    # inputs.append(inp)
    
    # pth = "./data/Binary Images/dog2.png"  #0
    # inp = dr.read_img(pth)
    # inputs.append(inp)
    
    # pth = "./data/Binary Images/dog.png"  #0
    # inp = dr.read_img(pth)
    # inputs.append(inp)
    
    # labels = ["cat2","cat3","dog1","dog2","dog3"]

################################ Misc? #######################################
   
    #labels = ['a','b','c','d']
    #data = np.array( [[0,1,10,7],[1,0,8,9],[10,8,0,2],[7,9,2,0]] )
    #data = np.array([1,10,8,7,9,2])
    #dendrogram(data, labels=labels)


    #L0 = z[0]["2"][0]
    #pos1 = get_pos(L0)
    #V1 = z[0]["7"][1]
    #pos2 = get_pos(V1)
    
    #v.cool_GIF(L0, pos1, V1, pos2, frames=180, fps=20)
    
###############################################################################
# Old code from back when we thought we were going to use a confusion matrix
# Didn't wanna throw it away so here it is.
# It's not at all near complete but this is where I stopped so ¯\_(ツ)_/¯

# def confusion(input_list, labels, thresh, predicted_classes):
#     data = get_data(input_list)[0]# Get the data in the format we want
#     lkg = shc.linkage(data, method='single')# Get the linkage
    
#     # Get the list of all the classes that actually appeared in the data
#     # The index in this corresponds to the elements at the same index in input_list
#     actual_classes = list(shc.fcluster(lkg, thresh, criterion='distance'))
    
#     # Columns in the confusion matrix correspond to the predicted labels
#     n = len(predicted_classes)
#     # Rows in the confusion matrix correspond to the actual labels
#     m = len(actual_classes)
#     # start with an empty m by n matrix
#     confusionMatrix = [ [0 for i in range(n)] for j in range(m) ]
#     pkey = {} # Going to use dictionaries to keep track of the indices of labels
#     akey = {}
#     index = 0
#     known = []
#     for p in predicted_classes:
#         pkey[index] = p # Adding the classes to the dictionaries
#         akey[index] = p
#         index += 1
#         known.append(p)
#     for a in actual_classes:
#         if a not in known:
#             known.append(a)
#             akey[index] = a
#             index += 1
    
#     for i in range(len(labels)):
#         p = predicted_classes[i] # Predicted class of a certain graph
#         a = actual_classes[i] # Actual class of a the same graph


# # Scipy will group things together, but we need to figure out what the group labels mean
# def convert_classes(linkage, input_list, predicted_classes, actual_classes):S
#     # We're going to assume that the most prevalent label in an actual class
#     # is the proper label for that class
#     members = {} # Dictionary of lists of class members
#     for c in range(len(actual_classes)):
#         a = actual_classes[c]
#         p = predicted_classes[c]
#         if a not in members:
#             members[a] = []
#         members[a].append(p)