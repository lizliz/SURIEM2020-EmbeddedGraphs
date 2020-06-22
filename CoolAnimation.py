#Levent Batakci
#6/18/2020
#
#This file makes a cool graphic.
import networkx as nx
import DataReader as dr
import Merge as m
import Visualization as v
import Compare as c
import math
import moviepy.editor as mpy
import lib.Tools as t
import glob
from DataCalculations import average_distance

#Make the graphs
pth = "./data/kitty1.graphml"
data = dr.read_graphml(pth)
G1 = t.main_component(data[0])
pos1 = data[1]
m.calc_values_height_reorient(G1, pos1)
M1 = m.merge_tree(G1)

pth = "./data/kitty2.graphml"
data = dr.read_graphml(pth)
G2 = t.main_component(data[0])
pos2 = data[1]
m.calc_values_height_reorient(G2, pos2)
M2 = m.merge_tree(G2)

frames=720

# pth = "./images/cool"
# for i in range(0, frames):
#     print(i)
#     p1 = pos1.copy()
#     p2 = pos2.copy()
#     G1c = G1.copy()
#     G2c = G2.copy()

#     m.calc_values_height_reorient(G1c, p1, math.pi*(1/2 + 2*i/(frames)))
#     M1 = m.merge_tree(G1c, normalize=True)
    
#     m.calc_values_height_reorient(G2c, p2, math.pi*(1/2 + 2*i/(frames)))
#     M2 = m.merge_tree(G2c, normalize=True)
    
#     data = c.morozov_distance(M1, M2, radius=0.001, valid=True, get_map=True)
#     mapping = data[1]
#     distance = data[0]
#     v.draw_mapping(M1, p1, M2, p2, mapping, distance, savepath="./images/coolmap", index=i)

# gif_name = 'cat-map'
# fps = 24
# file_list = glob.glob('./images/coolmap/*.png') # Get all the pngs in the current directory
# list.sort(file_list, key=lambda x: int(x.split('_')[1].split('.png')[0])) # Sort the images by #, this may need to be tweaked for your use case
# clip = mpy.ImageSequenceClip(file_list, fps=fps)
# clip.write_gif('{}.gif'.format(gif_name), fps=fps)

# data = c.morozov_distance(M1, M2, radius=0.001, valid=True, get_map=True)
# mapping = data[1]
# distance = data[0]
# v.draw_mapping(M1, pos1, M2, pos2, mapping, distance)

# v.cool_GIF(G1, pos1, G2, pos2, frames=4, fps = 1)

# p1 = pos1.copy()
# p2 = pos2.copy()
# G1c = G1.copy()
# G2c = G2.copy()

# m.calc_values_height_reorient(G1c, p1, math.pi*(1/2 + 2*87/(frames)))
# M1 = m.merge_tree(G1c, normalize=True)

# m.calc_values_height_reorient(G2c, p2, math.pi*(1/2 + 2*87/(frames)))
# M2 = m.merge_tree(G2c, normalize=True)

# data = c.morozov_distance(M1, M2, radius=0.001, valid=True, get_map=True)
# mapping = data[1]
# distance = data[0]
# v.draw_mapping(M1, p1, M2, p2, mapping, distance)

print(average_distance(M1, pos1, M2, pos2, frames = 1440))



