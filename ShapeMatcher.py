# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 23:47:49 2020

@author: Candace Todd
"""
import subprocess as sp # I don't think this is customary but I'm doing it
import networkx as nx
from sm2nx import read_sm

#subprocess.check_output(['ls', '-l'])  # All that is technically needed...
# print(subprocess.check_output(['ls', '-l']))

p1 = sp.run('dir', shell = True, capture_output = True)
print(p1.stdout.decode()) # pretty print

#or 

https://www.youtube.com/watch?v=2Fp1N6dof0Y
p2 = sp.run('dir', shell = True, capture_output = True, text = True)
#text, but NOT pretty print


# I thought I'd write a separate script for this because idk it seemed like a good idea at the time

### FIND OPERATING SYSTEM FIRST!!! maybe make default shell is tru if windows
smdir = 'C:/ShapeMatcher6.0.1beta'#ShapeMather6.0.1beta directory
cd = 'cd ' + smdir
sp.run(cd, shell = True)
files = [
    "dino1.ppm",
    "DINO0007.ppm",
    "DINO0008.ppm",
    "DINO0009.ppm"
    ]
db = "sm -doExtSimp 0 -c"
dbname = "dino"
db += " " + dbname + ".db"
# "dino1.ppm DINO0007.ppm DINO0008.ppm DINO0009.ppm"
for ppm in files:
    db += " " + ppm

z = sp.run(db, shell = True)

match = "sm -m 1 " + dbname + ".db" 
y = sp.run(match, shell = True)
y.returncode
xmlname = "dinos"
toxml = "sm -toXML "+ xmlname + " " + dbname + ".db"
#sm -toXML -from dino.db
##### wrong lol toXML = "sm " + dbname + ".db" + " -toXML"
z = sp.run(toxml, shell = True)
z.returncode
w = read_sm("from.txt")


# -toXML [val]      Saves the graphs from '-from ID' to '-to ID' in XML format
