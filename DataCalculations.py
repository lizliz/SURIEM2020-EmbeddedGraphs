# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 19:15:49 2020

@author: Leven
"""
from Merge import merge_tree, calc_values_height_reorient
import Compare
import math

def distance_data(G1, pos1, G2, pos2, frames=720, rotate_both=True, accuracy=0.0001):
    data=[]
    for i in range(0, frames+1):
        print(i)
        p1 = pos1.copy()
        p2 = pos2.copy()
        G1c = G1.copy()
        G2c = G2.copy()
    
        if(rotate_both):
            calc_values_height_reorient(G1c, p1, math.pi*(1/2 + i/( 360 * frames/720 )))
        else:
            calc_values_height_reorient(G1c, p1)
        M1 = merge_tree(G1c, normalize=True)
        
        calc_values_height_reorient(G2c, p2, math.pi*(1/2 + i/( 360 * frames/720 )))
        M2 = merge_tree(G2c, normalize=True)
        
        dist = Compare.morozov_distance(M1, M2, accuracy)
        data.append( (i, dist) )
        
    return data
        
def average_distance(G1, pos1, G2, pos2, frames=360, rotate_both=True, accuracy=0.005):
    data = distance_data(G1, pos1, G2, pos2, frames=frames, rotate_both=rotate_both, accuracy=accuracy)
    
    heights = [x[1] for x in data]
    
    return sum(heights)/frames
