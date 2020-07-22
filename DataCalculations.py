# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 19:15:49 2020

@author: Levent
"""
from Merge import merge_tree, calc_values_height_reorient
import Compare
import math
import threading
import time
import concurrent.futures
from itertools import repeat
from multiprocessing import cpu_count
import random
import statistics
from scipy import stats

########################## Universal Parameters ###############################
# G1, G2: NetworkX Graph objects
# pos1, pos2: dict, position dictionaries for nodes of the respective graphs 
# angle: The angle to calculate the merge tree from when getting data
# index: The index of the angle. Used to create scatterplots.
# data: list(right?), data returned by the distance_data() funtion (better description?)
# rotate_both: boolean, whether you want to rotate G1 in addition to G2
# accuracy: float or int, value returned will be within this radius of accuracy
# frames: int, number of times you want to rotate a tree for average branching distance
###############################################################################


def get_data_point(G1, pos1, G2, pos2, angle, index, data, rotate_both=True, accuracy=0.0001):
    
    p1 = pos1.copy()
    p2 = pos2.copy()
    G1c = G1.copy()
    G2c = G2.copy()

    if(rotate_both):
        calc_values_height_reorient(G1c, p1, angle)
    else:
        calc_values_height_reorient(G1c, p1)
 
    M1 = merge_tree(G1c, shift=True)
    
    calc_values_height_reorient(G2c, p2, angle)
    M2 = merge_tree(G2c, shift=True)
    
    dist = Compare.branching_distance(M1, M2, accuracy)
    data.append( (index, dist) ) 
    return (index, dist)



def distance_data(G1, pos1, G2, pos2, frames=180, rotate_both=True, accuracy=0.0001):
    data=[]
    for i in range(0, frames+1):
        angle = math.pi*(1/2 + 2*i/frames)
        get_data_point(G1, pos1, G2, pos2, angle, i, data, rotate_both=rotate_both, accuracy=accuracy)
    return data

def distance_data_thread(G1, pos1, G2, pos2, data, frames=180, rotate_both=True, accuracy=0.0001):    
    angles = [math.pi*(1/2 + 2*i/frames) for i in range(0, frames)]
    indices = [i for i in range(0, frames)]
    
    print("Starting thread")
    start = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=cpu_count() - 1) as executor:
        print(cpu_count())
        executor.map(get_data_point, repeat(G1), repeat(pos1), repeat(G2), repeat(pos2), angles, indices, repeat(data), repeat(rotate_both), repeat(accuracy))

    print("Total time: ", time.time()-start)
    return data
        
def average_distance(G1, pos1, G2, pos2, frames=180, rotate_both=True, accuracy=0.005, average = "median"):
    data = distance_data(G1, pos1, G2, pos2, frames=frames, rotate_both=rotate_both, accuracy=accuracy)
    
    heights = [x[1] for x in data]
    num=len(heights)
    
    heights.sort()
    n1 = heights[math.ceil((num-1)/2)]
    n2 = heights[math.floor((num-1)/2)]
    med = (n1+n2)/2
    
    if average == "median":
        return med
    elif average == "mean":
        return sum(heights)/frames
    else:
        print("Invalid average parameter. Valid choices are 'median' and 'mean'. Returning median.")
        return med

# samples: int, size of the sampling distribution you want. a few thousand is usually pretty good
# alpha: float (0,1) significance level of the confidence interval, complement of confidence level
# interpretation: boolean, whether or not you want to print a generic interpretation of the confidence interval
def bootstrap(data, samples = 3000, alpha = 0.05, interpretation = False):
    n = len(data) # size of original sample
    originalSample = [data[i][1] for i in range(n)] # list containing only the data points
    point_estimate = statistics.mean(originalSample) # get mean of our sample as the estimate we center our interval around
    bootstrap_distribution = []
    confidence_level = 1-alpha
    
    for j in range(samples):
        current_sample = random.choices(originalSample, k = n) # Sample from the original sample with replacement
        current_mean = statistics.mean(current_sample) # Find mean of this bootstrap sample
        bootstrap_distribution.append(current_mean) # Add bootstrap mean to the distribution of means
    
    # Standard error is the standard deviation of the sampling distribution
    standard_error = statistics.stdev(bootstrap_distribution)
    # using a t distribution, find the multiplier for our confidence interval
    t_multiplier = stats.t.ppf(confidence_level,n)
    #construct margin of error
    moe = t_multiplier*standard_error
    
    # Create a dictionary so you can access the info you want or print it out nicely
    report = {"Estimated Mean":point_estimate,
              "Margin of Error": moe,
              "Confidence Interval": [point_estimate-moe, point_estimate+moe],
              "Standard Deviation": statistics.stdev(originalSample),# Standard Deviation of ORIGINAL SAMPLE
              "Standard Error": standard_error,# Standard deviation of the SAMPLING DISTRIBUTION
              "Confidence Level": confidence_level}
    
    # Prints a generic interpretation of confidence intervals
    if interpretation == True:
        print("We are ", confidence_level*100, "% confident that the interval from ", point_estimate-moe, "to ", point_estimate+moe, "captures the true population mean.")
        print("If we were to construct a large number of these confidence intervals, we would expect about ", confidence_level*100, "% of them to capture the true population mean.")
    
    # returns the report dictionary
    return report
    
    
    
