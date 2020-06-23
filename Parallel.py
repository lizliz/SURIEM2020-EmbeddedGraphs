#Levent Batakci
#6/23/20
#
#Let's speed things up! and test
from DataCalculations import distance_data_thread, distance_data
import DataReader as dr
import lib.Tools as t
import Merge as m
import threading
import concurrent.futures
import time

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

# num = 10

# def calc(x):
#     print(x*x)
#     return(x*x)


# start = time.time()
# for i in range(num):
#     calc(i)
# print("Time regular: ", time.time() - start)

# start = time.time()
# with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
#      executor.map(calc, range(num))       
# print("Time threaded: ", time.time() - start) 


data = distance_data(G1, pos1, G2, pos2, frames = 100)
#print(data)
data=[]
distance_data_thread(G1, pos1, G2, pos2, data, frames = 100)
        
        

