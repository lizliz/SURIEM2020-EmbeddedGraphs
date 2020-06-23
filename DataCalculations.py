# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 19:15:49 2020

@author: Leven
"""
from Merge import merge_tree, calc_values_height_reorient
import Compare
import math
import random
import statistics
from scipy import stats
import pdb

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

# data: data returned by the distance_data() funtion
# samples: size of the sampling distribution you want. 3,000 is usually pretty good
# alpha: significance level of the confidence interval, complement of confidence level
#interpretation: whether or not you want to print a generic interpretation of the confidence interval
def bootstrap(data, samples = 3000, alpha = 0.05, interpretation = False):
    #breakpoint()
    n = len(data) # size of sample
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
              "Confidence Level": confidence_level,
              "Confidence Interval": [point_estimate-moe, point_estimate+moe]} 
    
    # Prints a generic interpretation of confidence intervals
    if interpretation == True:
        print("We are ", confidence_level*100, "% confident that the interval from ", point_estimate-moe, "to ", point_estimate+moe, "captures the true population mean.")
        print("If we were to construct a large number of these confidence intervals, we would expect about ", confidence_level*100, "% of them to capture the true population mean.")
    
    # returns the report dictionary
    return report
    
    
    
