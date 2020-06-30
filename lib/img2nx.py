#Levent Batakci
#6/23/2020
#
#img to nx !
import cv2
import random
import networkx as nx
from lib.trace_skeleton import traceSkeleton, thinning
import numpy as np


def read_img(pth, draw = True, nodeSize = 0, labels = False):
    im0 = cv2.imread(pth)

    im = (im0[:,:,0]>128).astype(np.uint8)
    
    # for i in range(im.shape[0]):
    #   for j in range(im.shape[1]):
    #     print(im[i,j],end="")
    #   print("")
    # print(np.sum(im),im.shape[0]*im.shape[1])
    im = thinning(im);
    
    cv2.imshow('',im*255);cv2.waitKey(0)
    
    rects = []
    polys = traceSkeleton(im,0,0,im.shape[1],im.shape[0],10,999,rects)
    
    for l in polys:
      c = (200*random.random(),200*random.random(),200*random.random())
      for i in range(0,len(l)-1):
        cv2.line(im0,(l[i][0],l[i][1]),(l[i+1][0],l[i+1][1]),c)
    
    cv2.imshow('',im0);cv2.waitKey(0)

    G = nx.Graph()
    positions = {}
    
    for walk in polys:
        for j in range(len(walk)-1):
            v=walk[j]
            u=walk[j+1]
            
            x = v[0] #x coord
            y = -1*v[1] #y coord
            ID1 = str(x) + "," + str(y) #ID the first vertex
            positions[ID1] = (x,y)
            
            x = u[0] #x coord
            y = -1*u[1] #y coord
            ID2 = str(x) + "," + str(y) #ID the second vertex
            positions[ID2] = (x,y) 
            
            G.add_edge(ID1, ID2)
        
        
    if(draw):
        nx.draw(G, positions, node_size=nodeSize, with_labels=labels)
        
    return [G, positions]