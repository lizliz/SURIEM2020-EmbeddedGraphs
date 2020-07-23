#Levent Batakci
#6/23/2020

# This program uses clustering techniques to display the results of ABD
import scipy.cluster.hierarchy as shc
import scipy.spatial.distance as ssd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import time
from DataCalculations import average_distance
from sklearn.manifold import MDS
#from sympy import Matrix, pprint# old import from confusion matrix days

########################## Universal Parameters ###############################
# input_list: list, (graph, position dictionary) 2-tuples
# labels: list, labels of data in input_list, matched to input_list by index
#         for example ["cat1", "cat2","dog1"...]
# target_list: list, target classifications/groups of the data in input_list, matched by index
#         for example ["cat","cat","dog"...]
# data: numpy array, 1-D condesed distance matrix
# frames: int, number of angles from which you want to calculate Average Branching Distance
# thresh: int or float, distance value threshold for coloring dendrogram clusters, 
# TIME: boolean, whether you want to time some process
# average: string, whether you want to use "mean" or "median" as average
###############################################################################

# Gets the distance data, then draws a dendrogram
# returns 1-D condensed distance matrix as numpy array
def draw_dendro(input_list, frames=180, data = None, labels=None, thresh=None):
    
    if type(data) == type(None):
        data = get_data(input_list, frames)[0]    
    
    dendrogram(data, labels=labels, thresh=thresh)
    plt.show()
    return data

# Draws a dendrogam given the distance data
# data parameter is NOT a 2D distance matrix
# pass a 2D distance matrix through get_data first
def dendrogram(data, labels=None, thresh=None):
    plt.figure(figsize=(10, 7))  
    plt.title("Dendrograms")
    lkg = shc.linkage(data, method='single')
    dend = shc.dendrogram(lkg, leaf_rotation = 90, labels=labels, color_threshold=thresh)
    
    if(thresh != None):
        plt.axhline(y=thresh, color='r', linestyle='--')
        
    return dend
    
# converts 2-D distance matrix to 1-D condensed distance matrix (both numpy arrays)
def condense(two_dimension_distance_matrix):
    return ssd.squareform(two_dimension_distance_matrix)

# p: boolean, whether you want to print the entry of the 2-D distance matrix that is currently being calculated (printed like a tuple)
# Returns a 2-D Distance matrix as numpy array using average branching distance
def get_matrix(input_list, frames = 180, p = True, TIME = False, average = "median"):
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
                val=average_distance(G1, pos1, G2, pos2, frames=frames, average = average)
            
            data[i,j] = val
            data[j,i] = val
    
    if TIME == True:
        print("Time to make distance matrix: " + str(time.time() - start))
    return data

# Returns matrix data in condensed and uncondensed form (both numpy arrays)
# using average branching distance
# Mostly for use within other functions
def get_data(input_list, frames = 180, p = True, TIME = False, average = "median"):
    
    data = get_matrix(input_list, frames = frames, p = p, TIME = TIME, average = average)
    flattened = condense(data)
    
    return [flattened, data]

# D: numpy array, 2-D distance matrix
# Colorize: boolean, whether you want to see the graph color coded according to the target classes in target_list
# scheme: color scheme for color-coded clusters when plotted
#         see color map options: https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
# legend: boolean, whether you want legend to appear on plot
# legend_positions: string, one of ["best",
# 	"upper right",
# 	"upper left",
# 	"lower left",
# 	"lower right",
# 	"right",
# 	"center left",
# 	"center right",
# 	"lower center",
# 	"upper center",
# 	"center"]
# alpha: float (0,1], opacity of points on scatter plot
# xRange, yRange: 2-tuples or lists, range of x and y values you want to show on the plot
# Adapted coloring method from https://stackoverflow.com/questions/8931268/using-colormaps-to-set-color-of-line-in-matplotlib
# Adapted MDS method from https://jakevdp.github.io/PythonDataScienceHandbook/05.10-manifold-learning.html
def mds(input_list, target_list, frames=180, D = None, colorize = True, scheme = "jet", legend = True, legend_position = "upper right", alpha = 0.4, TIME = True, xRange = None, yRange = None):
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
                ax.legend(handles, labels, loc=legend_position)
            
        # #plt.xlim(xmin, xmax)
        # #plt.ylim(ymin, ymax)
        if xRange != None and yRange != None:
            xmin, xmax = xRange[0], xRange[1]
            ymin, ymax = yRange[0], yRange[1]    
            ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
        else:
            plt.axis('equal')
        plt.show()

    return coords
    
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
