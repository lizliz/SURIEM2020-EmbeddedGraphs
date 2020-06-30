# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 14:56:12 2020

@author: Leven
"""
import DataReader as dr
import matplotlib.pyplot as plt
import lib.Tools as t
import networkx as nx

pth = "./data/Binary Images/Arctodus.jpg"  #0
inp = dr.read_img(pth)
g=inp[0]
pos = inp[1]
g = t.main_component(g, report = True)
nx.draw(g, pos, node_size=0)
plt.title("arctodus")
plt.show()

pth = "./data/Binary Images/Aspideretoides.jpg"  #0
inp = dr.read_img(pth)
g=inp[0]
pos = inp[1]
g = t.main_component(g, report = True)
nx.draw(g, pos, node_size=0)
plt.title("aspideretoides")
plt.show()

pth = "./data/Binary Images/Basilemys.jpg"  #0
inp = dr.read_img(pth)
g=inp[0]
pos = inp[1]
g = t.main_component(g, report = True)
nx.draw(g, pos, node_size=0)
plt.title("basilemys")
plt.show()
