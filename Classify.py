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
from lib.Tools import random_tree_and_pos
import random
import DataReader as dr
import lib.Tools as t

#Input list should be a list of pairs of graphs & positions
def draw_dendro(input_list, frames=180, labels=None):
    count = len(input_list)
    
    data = np.zeros(shape=(count,count))
    for i in range(count):
        for j in range(i, count):
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
            
    dendrogram(data, labels)
            

def dendrogram(data, labels=None):
    plt.figure(figsize=(10, 7))  
    plt.title("Dendrograms")  
    dend = shc.dendrogram(shc.linkage(data, method='ward'), labels=labels)
    
    
    
if __name__ == '__main__':
    inputs = []
    # for i in range(0, 5):
    #     inputs.append(random_tree_and_pos(random.randint(5,10)))
     
    pth = "./data/kitty2.graphml"  #0
    inp = dr.read_graphml(pth)
    inp[0] = t.main_component(inp[0])
    inputs.append(inp)
    
    pth = "./data/kitty1.graphml"  #1
    inp = dr.read_graphml(pth)
    inp[0] = t.main_component(inp[0])
    inputs.append(inp)
    
    pth = "./data/kitty2.graphml"  #2
    inp = dr.read_graphml(pth)
    inp[0] = t.main_component(inp[0])
    inputs.append(inp)
    
    pth = "./data/brutus.graphml"  #3
    inp = dr.read_graphml(pth)
    inp[0] = t.main_component(inp[0])
    inputs.append(inp)
    
    pth = "./data/sofie.graphml"  #4
    inp = dr.read_graphml(pth)
    inp[0] = t.main_component(inp[0])
    inputs.append(inp)
    
    labels = ['Kitty2 (1)', 'Kitty1', 'Kitty2 (2)', 'Brutus', 'Sofie']
    
    draw_dendro(inputs, frames=10, labels=labels)