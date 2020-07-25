#Levent Batakci
#6/8/2020
#
#This file is a compilation of all methods important to visualizing graphs.
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from Merge import merge_tree, calc_values_height_reorient, calc_values_height, reduced
from lib.Tools import get_bounds_and_radius, parse_mapping, is_leaf_f, relabel, relabel_dict, descendants, get_bounds
import os
import math
import Compare
import glob
import moviepy.editor as mpy
from DataCalculations import distance_data

#General Note: Most methods have an optional 'savepath' argument. By default, it is None
#              If you wish to save the resultant plots of a method, specify a file path
#              to save to.


#Adds the image of the right-facing arrow (=>) to the specified axis
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

#Draws a graph, given a position diction
def draw_basic(G, pos, n_size=0):
    nx.draw(G, pos, with_labels=False, node_color="blue",node_size=n_size)
    
#Draws a given graph with square resolution.
#The drawing will be centered around the average of the bounds.
#d is the "sidelength" of the square
#(Useful for animations of rotations)
def draw_square(G, pos, title, ax, d, b=None):
    if(b==None):
        b = get_bounds(pos)
    xAvg = (b[0][1]+b[0][0])/2
    yAvg = (b[1][1]+b[1][0])/2
        
    ax.set_xlim(xAvg - d/2, xAvg + d/2)
    ax.set_ylim(yAvg - d/2, yAvg + d/2)
    
    draw(G, pos, title, ax, n_size = 100)
    

#Draws the given graph and corresponding merge tree
#(Merge tree is computed at the standard orientation)
#(There is a pretty arrow in between! (=>) )
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
    
#Draws the given graph and corresponding merge tree with the same square resolution
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

#Creates an animation of G being rotated over 'frames' many angles.
#At each step, the merge tree is also shown.
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
#Plots the merge trees and displays the Branching Distance between them
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

#Same as above, except plots with square resolution
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

#Rotates both graphs simultaneously and compares them at each step
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

#Produces a GIF that shows how the distance changes at various orientations for a pair of input graphs
#The gif will be saved in the main directory as whatever 'gif_name' is 
def cool_GIF(G1, pos1, G2, pos2, frames=720, rotate_both=True, gif_name="cool_gif", fps=30, delete_frames=True):
    data = distance_data(G1, pos1, G2, pos2, frames=frames, rotate_both=rotate_both)
    pth = "./images/frames"
    
    r1 = get_bounds_and_radius(pos1)[0]
    r2 = get_bounds_and_radius(pos2)[0]
    
    #Make sure the gif is 8 seconds long
    fps = frames/8
    
    for i in range(0, frames):
        if frames <=5:
            print("Working on frame", i, "...")
        elif frames <= 100:
            if i % 5 == 0:
                print("Working on frame", i, "...")
        else:
            if i % 25 == 0:
                print("Working on frame", i, "...")
        p1 = pos1.copy()
        p2 = pos2.copy()
        G1c = G1.copy()
        G2c = G2.copy()
    
        calc_values_height_reorient(G1c, p1, math.pi*(1/2 + 2*i/(frames)))
        M1 = merge_tree(G1c, shift=True)
        
        calc_values_height_reorient(G2c, p2, math.pi*(1/2 + 2*i/(frames)))
        M2 = merge_tree(G2c, shift=True)
        
        cool(M1, p1, M2, p2, G2c, data, i, r1, r2, savepath=pth, rotate_both=True, G1=G1c)
        
    file_list = glob.glob('./images/frames/*.png') # Get all the pngs in the current directory
    list.sort(file_list, key=lambda x: int(x.split('_')[1].split('.png')[0])) # Sort the images by #, this may need to be tweaked for your use case
    clip = mpy.ImageSequenceClip(file_list, fps=fps)
    clip.write_gif('{}.gif'.format(gif_name), fps=fps)
    
    #Delete the frames
    if(delete_frames):
        
        filelist = [ f for f in os.listdir("./images/frames")]
        for f in filelist:
            os.remove(os.path.join("./images/frames", f))
            

#Helper method for cool_GIF
#Draws the graphs, merge trees, and distance data plot
def cool(M1, p1, M2, p2, G2, data, index, r1, r2, savepath="", rotate_both=True, G1=None):
    if(rotate_both):
        fig = plt.subplots(2,3,figsize=(15,10))
        
        b1 = get_bounds(p1)
        b2 = get_bounds(p2)
        
        ax = plt.subplot(231, frameon=False)
        draw_square(M1, p1, "Merge A", ax, r1, b=b1)
        
        angles = [x[0] for x in data]
        distances = [x[1] for x in data]
        
        point = [angles[index], distances[index]]
        ax = plt.subplot(232)
        ax.title.set_text("Distance vs. Angle")
        ax.plot(angles, distances, '-')
        ax.scatter(point[0], point[1], marker='o', c='b', s=40)
        ax.axes.get_xaxis().set_visible(False)
        
        ax = plt.subplot(233, frameon=False)
        draw_square(M2, p2, "Merge B", ax, r2, b=b2)
        
        ax = plt.subplot(234, frameon=False)
        draw_square(G1, p1, "Input A", ax, r1, b=b1)
        
        ax = plt.subplot(235, frameon=False)
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        
        ax = plt.subplot(236, frameon=False)
        draw_square(G2, p2, "Input B", ax, r2, b=b2)
    else:
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
        pth = savepath + "/frame_" + str(index)
        plt.savefig(pth)
        
    plt.close()

#Produces a plot of how the distance between a pair of input graphs 
#changes as one or both are rotated
def distance_data_plot(G1, pos1, G2, pos2, frames=720, rotate_both=True, accuracy=0.0001):
    data=distance_data(G1, pos1, G2, pos2, frames=frames, rotate_both=rotate_both, accuracy=accuracy)

    angles = [x[0] for x in data]
    distances = [x[1] for x in data]
    
    fig = plt.subplots(1,1,figsize=(15,15))
    ax = plt.subplot(111, frameon=False)
    ax.title.set_text("Distance vs. Frame")
    ax.plot(angles, distances, '-')
    
    return data
  
#Shifts pos2 next to pos1 without deformation
#Useful for nicely drawing two graphs on the same matplotlib axis
def alter_positions(pos1, pos2, normalize_y):
    bounds1 = get_bounds_and_radius(pos1)[1]
    bounds2 = get_bounds_and_radius(pos2)[1]
    
    right_1 = bounds1[0][1]
    left_2 = bounds2[0][0]
    
    x_shift = 5 + right_1-left_2
    
    y_shift=0    
    if(normalize_y):
        y_avg_1 = sum(bounds1[1])/2
        y_avg_2 = sum(bounds2[1])/2
        
        y_shift = y_avg_1 - y_avg_2
    
    #Shift all the points!
    for p in pos2:
        new_x = pos2[p][0] + x_shift
        new_y = pos2[p][1] + y_shift
        pos2[p] = (new_x, new_y)
        
#Draws a mapping that shows how the leaves of the inputs got mapped to eachother
#as well as which vertices were deleted.
def draw_mapping(M1,pos1, M2,pos2, mapping, distance,savepath="", index=None, normalize_y=True):

    relabel(M1, '*')
    relabel(M2, '~')
    pos1 = relabel_dict(pos1, '*')
    pos2 = relabel_dict(pos2, '~')

    #Parse the mapping
    connections = parse_mapping(mapping)
    
    #Make the connections graph!
    match_graph = nx.Graph()
    del_graph = nx.Graph()
    del_edges = nx.Graph()
    for c in connections:
        val = connections[c]
        if(c[0] == '~' and val != "DELETED"):
            c, val = val, c
        
        #Deleted node
        if(val == 'DELETED'):
            if(c[0] == '*'):
                g = M1
            else:
                g = M2
                
            desc = descendants(g, c)
                
            del_graph.add_nodes_from(desc)
            del_edges.add_edges_from(g.edges(desc))
        #Matched minima
        elif(is_leaf_f(M1, c)):
            match_graph.add_edge(c, val)
        
    
    alter_positions(pos1, pos2, normalize_y)
    #Grand position matrix!
    pos = {**pos1, **pos2}
    
    fig = plt.subplots(1,1,figsize=(20,10))
    ax = plt.subplot(111, frameon=False)
    ax.title.set_text("Distance: " + str(distance))
    nx.draw(M1, pos1, node_color='blue', node_size=500)
    nx.draw(M2, pos2, node_color='blue', node_size=500)   
    nx.draw_networkx_edges(del_edges, pos, edge_color='red', width= 3)
    nx.draw(del_graph, pos, node_color='r', node_size=500)
    nx.draw(match_graph, pos, node_color='green', edge_color='green', node_size=500, width= 5)
    
    if(savepath != ""):
        pth = savepath + "/frame_" + str(index)
        plt.savefig(pth)
    
    plt.show()
    
    plt.close()
    
    
    
    