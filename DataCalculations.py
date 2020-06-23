# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 19:15:49 2020

@author: Leven
"""
from Merge import merge_tree, calc_values_height_reorient
import Compare
import math
import threading
import time
import concurrent.futures
from itertools import repeat
from multiprocessing import cpu_count

def get_data_point(G1, pos1, G2, pos2, angle, index, data, rotate_both=True, accuracy=0.0001):
    #print(index)
    
    p1 = pos1.copy()
    p2 = pos2.copy()
    G1c = G1.copy()
    G2c = G2.copy()

    if(rotate_both):
        calc_values_height_reorient(G1c, p1, angle)
    else:
        calc_values_height_reorient(G1c, p1)
    M1 = merge_tree(G1c, normalize=True)
    
    calc_values_height_reorient(G2c, p2, angle)
    M2 = merge_tree(G2c, normalize=True)
    
    dist = Compare.morozov_distance(M1, M2, accuracy)
    data.append( (index, dist) ) 
    return (index, dist)

def distance_data(G1, pos1, G2, pos2, frames=720, rotate_both=True, accuracy=0.0001):
    data=[]
    for i in range(0, frames+1):
        angle = math.pi*(1/2 + 2*i/frames)
        get_data_point(G1, pos1, G2, pos2, angle, i, data, rotate_both=rotate_both, accuracy=accuracy)
    return data

def distance_data_thread(G1, pos1, G2, pos2, data, frames=360, rotate_both=True, accuracy=0.0001):    
    angles = [math.pi*(1/2 + 2*i/frames) for i in range(0, frames)]
    indices = [i for i in range(0, frames)]
    
    print("Starting thread")
    start = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=cpu_count() - 1) as executor:
        print(cpu_count())
        executor.map(get_data_point, repeat(G1), repeat(pos1), repeat(G2), repeat(pos2), angles, indices, repeat(data), repeat(rotate_both), repeat(accuracy))

    print("Total time: ", time.time()-start)
    return data
        
def average_distance(G1, pos1, G2, pos2, frames=360, rotate_both=True, accuracy=0.005):
    data = distance_data(G1, pos1, G2, pos2, frames=frames, rotate_both=rotate_both, accuracy=accuracy)
    
    heights = [x[1] for x in data]
    
    return sum(heights)/frames
