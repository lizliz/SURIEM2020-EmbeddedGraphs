#Levent Batakci
#6/23/2020
#
#Dendro
import scipy.cluster.hierarchy as shc
import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt
from DataCalculations import average_distance
from lib.Tools import random_tree_and_pos, get_pos
import random
import DataReader as dr
import lib.Tools as t
import lib.tud2nx as tud

#Input list should be a list of pairs of graphs & positions
def draw_dendro(input_list, frames=180, labels=None, thresh=None):
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
            data[j, i] = val
            
    dendrogram(data, labels=labels, thresh=thresh)
            

def dendrogram(data, labels=None, thresh=None):
    plt.figure(figsize=(10, 7))  
    plt.title("Dendrograms")  
    dend = shc.dendrogram(shc.linkage(data, method='ward'), labels=labels, color_threshold=thresh)
    if(thresh != None):
        plt.axhline(y=thresh, color='r', linestyle='--')
    
if __name__ == '__main__':
    inputs = []
    labels = []
     
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
    
    z = tud.get_z()
    
    num = 5
    
    #Get 5 N's
    for i in range(num):
        G = z[0]["1"][i]
        pos = get_pos(G)
        
        inputs.append( (G, pos) )
        labels.append("N " + str(i))
        
    #Get 5 Z's
    for i in range(num):
        G = z[0]["3"][i]
        pos = get_pos(G)
        
        inputs.append( (G, pos) )
        labels.append("Z " + str(i))
        
    #Get 5 V's
    for i in range(num):
        G = z[0]["7"][i]
        pos = get_pos(G)
        
        inputs.append( (G, pos) )
        labels.append("V " + str(i))
    
    draw_dendro(inputs, frames=40, labels=labels, thresh=0.75)