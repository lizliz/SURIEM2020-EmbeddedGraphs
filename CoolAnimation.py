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
import lib.CoolData as cd

#Make the graphs
pth = "./data/cool1.graphml"
data = dr.read_graphml(pth)
G1 = data[0]
pos1 = data[1]

pth = "./data/cool2.graphml"
data = dr.read_graphml(pth)
G2 = data[0]
pos2 = data[1]

#Let's get the data (distances at many angles.)


# data=[]
# for i in range(0, 1441):
#     print(i)
#     p1 = pos1.copy()
#     p2 = pos2.copy()
#     G1c = G1.copy()
#     G2c = G2.copy()

#     m.calc_values_height_reorient(G1c, p1)
#     M1 = m.merge_tree(G1c, normalize=True)
    
#     m.calc_values_height_reorient(G2c, p2, math.pi*(1/2 + i/(720)))
#     M2 = m.merge_tree(G2c, normalize=True)
    
#     dist = c.morozov_distance(M1, M2, 0.000001)
#     data.append( (i, dist) )

# #Save the data.    
# pth = "./data/cool_data.txt"
# data_file = open(pth, "w+")
# data_file.write("data = [ \n")
# for d in data:
#     data_file.write("(" + str(d[0]) +  "," + str(d[1]) + "), \n")
# data_file.write("]")
# data_file.close()

# data = cd.data
# pth = "./images/cool/"
# for i in range(0, 1441):
#     print(i)
#     p1 = pos1.copy()
#     p2 = pos2.copy()
#     G1c = G1.copy()
#     G2c = G2.copy()

#     m.calc_values_height_reorient(G1c, p1)
#     M1 = m.merge_tree(G1c, normalize=True)
    
#     m.calc_values_height_reorient(G2c, p2, math.pi*(1/2 + i/(720)))
#     M2 = m.merge_tree(G2c, normalize=True)
    
#     v.cool(M1, p1, M2, p2, G2c, data, i, savepath=pth)

