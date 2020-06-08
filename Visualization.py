#Levent Batakci
#6/8/2020
#
#This file is a compilation of all methods important to visualizing graphs.
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from Merge import merge_tree, calc_values_height_reorient, calc_values_height
from lib.Tools import get_bounds_and_radius
import os
import math

def add_arrow(ax):
    ax.axis('off')
    arrow = mpimg.imread('./images/arrow.png')
    imagebox = OffsetImage(arrow,zoom=0.25)
    ab = AnnotationBbox(imagebox, (0.5, 0.5), frameon=False)
    ax.add_artist(ab)
        
#Basic drawing of a tree given position, title, and axes
def draw(G, pos, title, ax, labels=False, n_size=0):
    ax.title.set_text(title)
    nx.draw(G, pos, ax, with_labels=labels,node_color="blue",node_size=n_size)
    
def draw_basic(G, pos, n_size=0):
    nx.draw(G, pos, with_labels=False, node_color="blue",node_size=n_size)
      
def input_output(G, pos, savepath=""):
    fig = plt.subplots(1,3,figsize=(15,5))
    
    #Show the input
    ax = plt.subplot(131, frameon=False)
    draw(G, pos, "Input Graph", ax)
    
    #Add the COOL arrow
    ax = plt.subplot(132, frameon=False)
    add_arrow(ax)
    
    #Show the output
    calc_values_height(G, pos, math.pi / 2)
    M = merge_tree(G)
    ax = plt.subplot(133, frameon=False)
    draw(M, pos, "Resulting Merge Tree", ax)
    
    #Save the image if specified
    if(savepath != ""):
        plt.savefig(savepath)
    
    plt.show()
    plt.close()
        
def input_output_square(G, pos, r, savepath=""):
    fig = plt.subplots(1,3,figsize=(15,5))
    
    #Figure out the bounds
    geom = get_bounds_and_radius(pos)
    b = geom[1]
    xAvg = (b[0][1]+b[0][0])/2
    yAvg = (b[1][1]+b[1][0])/2
    
    
    #Show the input
    ax = plt.subplot(131, frameon=False)
    ax.set_xlim(xAvg - r/2, xAvg + r/2)
    ax.set_ylim(yAvg - r/2, yAvg + r/2)
    draw(G, pos, "Input Graph", ax)
    
    #Add the COOL arrow
    ax = plt.subplot(132, frameon=False)
    add_arrow(ax)
    
    #Show the output
    calc_values_height(G, pos, math.pi / 2)
    M = merge_tree(G)
    ax = plt.subplot(133, frameon=False)
    ax.set_xlim(xAvg - r/2, xAvg + r/2)
    ax.set_ylim(yAvg - r/2, yAvg + r/2)
    draw(M, pos, "Resulting Merge Tree", ax)
    
    #Save the image if specified
    if(savepath != ""):
        plt.savefig(savepath)
    
    plt.show()
    plt.close()
    
def animate(G, pos, frames, savepath=""):
    pos_copy = pos.copy()
    
    #Make the directory to save the frames
    directory = os.getcwd() + savepath
    if(savepath != ""):
        if( not os.path.isdir(directory) ):
            os.makedirs(directory)
    
    geom = get_bounds_and_radius(pos)
    r = geom[0]
            
    for i in range(0, frames):
        
        pth=""
        if(savepath != ""):
            pth = "." + savepath + str("/frame-" + str(i+1))
              
        calc_values_height_reorient(G, pos_copy, math.pi/2 + 2*math.pi/frames)
        
        input_output_square(G, pos_copy, r, pth)

            
        
    