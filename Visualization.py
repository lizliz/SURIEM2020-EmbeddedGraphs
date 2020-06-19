#Levent Batakci
#6/8/2020
#
#This file is a compilation of all methods important to visualizing graphs.
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from Merge import merge_tree, calc_values_height_reorient, calc_values_height, reduced
from lib.Tools import get_bounds_and_radius
import os
import math
import Compare

def add_arrow(ax):
    ax.axis('off')
    arrow = mpimg.imread('./images/arrow.png')
    imagebox = OffsetImage(arrow,zoom=0.25)
    ab = AnnotationBbox(imagebox, (0.5, 0.5), frameon=False)
    ax.add_artist(ab)
        
#Basic drawing of a tree given position, title, and axes
def draw(G, pos, title, ax, labels=False, n_size=0, n_color="blue"):
    ax.title.set_text(title)
    nx.draw(G, pos, ax, with_labels=labels,node_color=n_color,node_size=n_size)
    
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


#Takes two MERGE trees.
def compare(A, pos_A, B, pos_B, n_size=0, labels=False, pth="", valid=False):
    fig = plt.subplots(1,3,figsize=(15,5))
    
    ax = plt.subplot(131, frameon=False)
    draw(A, pos_A, "Graph A", ax, labels=labels, n_size=n_size)
    
    ax = plt.subplot(133, frameon=False)
    draw(B, pos_B, "Graph B", ax, labels=labels, n_size=n_size)
    
    
    d = Compare.morozov_distance(A, B, 0.05, valid=valid)
    ax = plt.subplot(132, frameon=False)
    ax.axis('off')
    ax.title.set_text("DISTANCE = " + str(d))
    
     #Save the image if specified
    if(pth != ""):
        plt.savefig(pth)
        
    plt.show()
    plt.close()
    
def compare_square(A, pos_A, r_A, B, pos_B, r_B, pth=""):
    fig = plt.subplots(1,3,figsize=(15,5))
    
    geom_A = get_bounds_and_radius(pos_A)
    b = geom_A[1]
    xAvg_A = (b[0][1]+b[0][0])/2
    yAvg_A = (b[1][1]+b[1][0])/2
    
    geom_B = get_bounds_and_radius(pos_B)
    b = geom_B[1]
    xAvg_B = (b[0][1]+b[0][0])/2
    yAvg_B = (b[1][1]+b[1][0])/2
    
    ax = plt.subplot(131, frameon=False)
    ax.set_xlim(xAvg_A - r_A/2, xAvg_A + r_A/2)
    ax.set_ylim(yAvg_A - r_A/2, yAvg_A + r_A/2)
    draw(A, pos_A, "Graph A", ax)
    
    ax = plt.subplot(133, frameon=False)
    ax.set_xlim(xAvg_B - r_B/2, xAvg_B + r_B/2)
    ax.set_ylim(yAvg_B - r_B/2, yAvg_B + r_B/2)
    draw(B, pos_B, "Graph B", ax)
    
    
    d = Compare.morozov_distance(A, B, 10)
    ax = plt.subplot(132, frameon=False)
    ax.axis('off')
    ax.title.set_text("DISTANCE = " + str(d))   
    
    #Save the image if specified
    if(pth != ""):
        plt.savefig(pth)
        
    plt.show()
    plt.close()

def compare_many(A, pos_A, B, pos_B, frames, savepath=""):
    pos_A_copy = pos_A.copy()
    pos_B_copy = pos_B.copy()
    
    #Make the directory to save the frames
    directory = os.getcwd() + savepath
    if(savepath != ""):
        if( not os.path.isdir(directory) ):
            os.makedirs(directory)
    
    geom_A = get_bounds_and_radius(pos_A)
    r_A = geom_A[0]
    
    geom_B = get_bounds_and_radius(pos_B)
    r_B = geom_B[0]
            
    for i in range(0, frames):
        
        pth=""
        if(savepath != ""):
            pth = "." + savepath + str("/frame-" + str(i+1))
            
        calc_values_height_reorient(A, pos_A_copy, math.pi/2 + 2*math.pi/frames)
        calc_values_height_reorient(B, pos_B_copy, math.pi/2 + 2*math.pi/frames)
        
        mA = merge_tree(A)
        mB = merge_tree(B)
        
        print("A reduced: " + str(reduced(mA)))
        print("B reduced: " + str(reduced(mB)))
        
        
        compare_square(mA, pos_A_copy, r_A, mB, pos_B_copy, r_B, pth)
        
def cool(M1, p1, M2, p2, G2, data, index, savepath=""):
    fig = plt.subplots(1,4,figsize=(20,5))
        
    ax = plt.subplot(141, frameon=False)
    draw(M1, p1, "Merge A", ax)
    
    angles = [x[0] for x in data]
    distances = [x[1] for x in data]
    
    point = [angles[index], distances[index]]
    ax = plt.subplot(142)
    ax.title.set_text("Distance vs. Angle")
    ax.plot(angles, distances, '-')
    ax.scatter(point[0], point[1], marker='o', c='b', s=40)
    ax.axes.get_xaxis().set_visible(False)
    
    ax = plt.subplot(143, frameon=False)
    draw(M2, p2, "Merge B", ax)
    
    ax = plt.subplot(144, frameon=False)
    draw(G2, p2, "Input B", ax)
    
     #Save the image if specified
    if(savepath != ""):
        pth = savepath + "/frame" + str(index)
        plt.savefig(pth)
        
    plt.close()
    
    
# #Big method for real.
# def draw_mapping(M1,pos1, M2,pos2, mapping):

#     #Parse the mapping
