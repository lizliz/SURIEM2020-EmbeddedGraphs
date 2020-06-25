#Levent Batakci
#6/23/2020
#
#Dendro
import scipy.cluster.hierarchy as shc
import scipy.spatial.distance as ssd
import pandas as pd
import numpy as np
#from sympy import Matrix, pprint# old code from confusion matrix days
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt
from DataCalculations import average_distance
from lib.Tools import random_tree_and_pos, get_pos
import random
import DataReader as dr
import lib.Tools as t
import lib.tud2nx as tud
import Visualization as v

#Input list should be a list of pairs of graphs & positions
def draw_dendro(input_list, frames=180, labels=None, thresh=None):
    # count = len(input_list)
    data = get_data(input_list, frames)    
    # data = np.zeros(shape=(count,count))
    # for i in range(count):
    #     for j in range(i, count):
    #         print("(",i,",",j,")")
    #         if(i==j):
    #             val=0
    #         else:
    #             G1 = input_list[i][0]
    #             pos1 = input_list[i][1]
    #             G2 = input_list[j][0]
    #             pos2 = input_list[j][1]
    #             val=average_distance(G1, pos1, G2, pos2, frames=frames)
            
    #         data[i,j] = val
    #         data[j,i] = val
    
    
    dendrogram(data, labels=labels, thresh=thresh)
    return data
            

def dendrogram(data, labels=None, thresh=None):
    plt.figure(figsize=(10, 7))  
    plt.title("Dendrograms")
    #data = ssd.squareform(data)
    lkg = shc.linkage(data, method='single')
    dend = shc.dendrogram(lkg, labels=labels, color_threshold=thresh)
    if(thresh != None):
        plt.axhline(y=thresh, color='r', linestyle='--')
    
# I made this its own function cause I was gonna use it for the confusion matrix
# Guess we don't need it anymore but I left it
def get_data(input_list, frames = 180):
    count = len(input_list)
    data = np.zeros(shape=(count,count))
    
    for i in range(count):
        
        for j in range(i, count):
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
    
    data = ssd.squareform(data)
    return data


    
    
if __name__ == '__main__':
    inputs = []
    labels = []
    #predicted_classes = []# old code from confusion matrix days
     
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
    
    p = "data/Letter-low"
    ds = "Letter-low"
    z = tud.read_tud(p,ds)
    
    num = 5
    
    #L0 = z[0]["2"][0]
    #pos1 = get_pos(L0)
    #V1 = z[0]["7"][1]
    #pos2 = get_pos(V1)
    
    #v.cool_GIF(L0, pos1, V1, pos2, frames=180, fps=20)
    
    #Get 5 Z's
    for i in range(num):
        G = z[0]["3"][i]
        G = t.main_component(G)
        pos = get_pos(G)
        
        inputs.append( (G, pos) )
        labels.append("Z " + str(i))
        #predicted_classes.append("Z")# old code from confusion matrix days
    
    #Get 5 L's
    for i in range(num):
        G = z[0]["2"][i]
        G = t.main_component(G)
        pos = get_pos(G)
        
        inputs.append( (G, pos) )
        labels.append("L " + str(i))
        #predicted_classes.append("L")# old code from confusion matrix days
    
    #Get 5 N's
    for i in range(num):
        G = z[0]["1"][i]
        G = t.main_component(G)
        pos = get_pos(G)
        
        inputs.append( (G, pos) )
        labels.append("N " + str(i))
        #predicted_classes.append("N")# old code from confusion matrix days

        
    #Get 5 V's
    for i in range(num):
        G = z[0]["7"][i]
        pos = get_pos(G)
        G = t.main_component(G)
        
        inputs.append( (G, pos) )
        labels.append("V " + str(i))
        #predicted_classes.append("V")# old code from confusion matrix days
    
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

    data = draw_dendro(inputs, frames=10, labels=labels, thresh=0.38)
    
    #labels = ['a','b','c','d']
    #data = np.array( [[0,1,10,7],[1,0,8,9],[10,8,0,2],[7,9,2,0]] )
    #data = np.array([1,10,8,7,9,2])
    #dendrogram(data, labels=labels)
    
    
###############################################################################
# Old code from back when we thought we were going to use a confusion matrix
# Didn't wanna throw it away so here it is.
# It's not at all near complete but this is where I stopped so ¯\_(ツ)_/¯

# def confusion(input_list, labels, thresh, predicted_classes):
#     data = get_data(input_list)# Get the data in the format we want
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