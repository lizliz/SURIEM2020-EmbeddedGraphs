# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 23:47:49 2020

@author: Candace Todd
"""
# I thought I'd write a separate script for this because idk it seemed like a good idea at the time

import subprocess as sp # I don't think this is customary but I'm doing it
import platform as p
import networkx as nx
#from sm2nx import read_sm
from contextlib import contextmanager
#import pdb
import os

# Will come back and clean up later

# Haven't really tested anything but models2xml,
# but they're all connected so it should all work
# the only thing i expect us to use from here is
# ppm2nx, which skeletonizes a binary .ppm image file (convert to .ppm: https://convertio.co/)


# A sad error message in case sad things happen
sorry = "Aborting: {}.\nTry executing the ShapeMatcher commands directly from your terminal.\nFor guidance, see http://www.cs.toronto.edu/~dmac/ShapeMatcher/tutorial.html \nOr see the helpful commands listed in SURIEM2020-EmbeddedGraphs\images\ShapeMatcher\commands.txt"

# We have to do some finagling with directories because ShapeMatcher is a command line program
# Got this little chunk from https://stackoverflow.com/questions/431684/how-do-i-change-the-working-directory-in-python/24176022#24176022
@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

# command line short cut
def cmd(command):
    return sp.run(command, shell = True, capture_output = True, text = True)

######################################################################################
###### Note to self: come back and fix the shape mathcer directory thing maybe #######
######################################################################################

### CONVERT BINARY IMAGES TO NX
# DBname: whatever you want the name of your database and xml file to be
# ppmDir: Directory where the .ppm files you want to use are located
#         NOT including the files themselves
# ppmList: list of the .ppm files you want to convert
#          If none, converts all .ppm in the directory
# SMD: directory to ShapeMatcher application
def read_ppm(DBname, ppmDir, ppmList = None, SMD = None ):
    if SMD == None:
        SMD = "../images/ShapeMatcher"
    with cd(SMD):
        createDB = "sm -doExtSimp 0 -c " + DBname + ".db " + ppmDir
        toXML = "sm -toXML "+ DBname + ".xml " + DBname + ".db"
        #cmd(toXML)
        if ppmList == None:
            print("Creating Database...")
            cmd(createDB)
            print("Converting to XML...")
            cmd(toXML)
            print("Conversion complete.") 
            print("Your", DBname, "database and XML file should be in ", SMD)
        elif type(ppmList) is list:
            print("Creating Database...")
            for ppm in ppmList:
                createDB += "/" + ppm
                if ppm.find('.ppm') < 0:
                    createDB += ".ppm"
            cmd(createDB)
            print("Converting to XML...")
            cmd(toXML)
            print("Conversion complete.") 
            print("Your", DBname, "database and XML file should be in ", SMD)
        else:
            s = sorry.format("Invalid ppmList.")
            print(s)
            return None
    
    print("Converting to NetworkX...")
    # The XML files should have ended up in SMD
    path = SMD + "/" + DBname + ".xml"   
    a = read_sm(path)
    print("Conversion Complete.")    
    return a

# Converting the model data from ShapeMatcher into giant XML files
# ppmFolder: name of the folder all your ppm files are in
#            will also be the name of the database file and xml file that get created
# SMD: Directory of ShapeMatcher Folder (with the ShapeMatcher program)
#      If you haven't moved things around in the repo too much, the default path should work
def models2xml(ppmFolder, SMD = None):
    if SMD == None:
        SMD = '../images/ShapeMatcher'
    print("Converting", ppmFolder, "...")
    
    with cd(SMD): # Directory finagling begins  
        
        directory = 'models/' + ppmFolder
        
        with cd(directory):# finagling x 2
            OS = p.system()
            if OS == 'Windows':
                contents = cmd('dir')
            elif OS in ['Darwin','Linux']:
                contents = cmd('ls')
            else:
                s = sorry.format("Unknown Operating System")
                print(s)
                return None
        
        if contents.returncode != 0:
            s = sorry.format("Couldn't read the directory.")
            print(s)
            return None
        
        # There is a built in ShapeMatcher commands that reads everything in a folder
        # But I found it to be buggy at times
        string = str(contents)
        string = string[string.find(ppmFolder)+1:]
        fileList = string.split(".ppm")
        fileList = fileList[:-1]
        for i in range(len(fileList)):
            file = fileList[i]
            file = file[file.find(ppmFolder):]
            file += ".ppm"
            fileList[i] = file

        # Now we have a list of all the files in the folder
        # So we can make a database consisting of all of these files
        
        # Start building the sm command for creating a database file
        createDB = 'sm -doExtSimp 0 -c ' + ppmFolder + '.db'# + ' models/' + ppmFolder
        
        # Now add each of the files
        for file in fileList:
            createDB = createDB + ' models/' + ppmFolder + '/' + file
        
        # Make a database of the graphs
        cmd(createDB)
        # Convert database to XML file
        toXML = "sm -toXML "+ ppmFolder + ".xml " + ppmFolder + ".db"
        cmd(toXML)
        
    print("Conversion complete.") 
    print("Your", ppmFolder, "database and XML file should be in ", SMD)
    print("You can now use read_sm() from sm2nx.py to convert the XML file into a networkx graph")
    
    return None

def read_sm(path):
    file = open(path, "r")
    contents = file.read()
    graphList = contents.split('<DAG class="ShockGraph" ')
    #breakpoint()
    g = 1
    graphDict = {}
    while g < len(graphList):
        G = nx.Graph()
        pos = {}
        graph = graphList[g]
        nodeCountStart = 11
        nodeCountEnd = 11 + graph[11:].find('"')
        nodeCount = int(graph[nodeCountStart:nodeCountEnd])
        if nodeCount < 1:
            g+=1
            continue
        objectNameStart = 12 + graph.find("<objectName>")
        objectNameEnd = objectNameStart + graph[objectNameStart:].find("</object")
        objectName = graph[objectNameStart:objectNameEnd]
        if objectName not in graphDict:
            graphDict[objectName] = []
        
        #start finding the nodes
        wayList = graph.split("<node ")
        w = 1
        #initialize the node if it doesnt exits!
        # if theres more than one, make a way
        while w < len(wayList):
            way = wayList[w]
            pointCount = 12 + way.find('<pointCount>')
            if int(way[pointCount]) < 1:
                w += 1
                continue
            pointList = way.split("<point ")
            p = 1
            firstPoint = None
            lastPoint = None
            while p < len(pointList):
                point = pointList[p]
                
                xStart = 1 + point.find('"')
                xEnd = point.find("ycoord") - 2
                x = point[xStart:xEnd]
                
                yStart = xEnd + 10
                yEnd = point.find("radius") - 2
                y = point[yStart:yEnd]
                
                pointName = x + ",-" + y
                if pointName not in list(G.nodes):
                    if p == 1 or p == (len(pointList)-1):
                        G.add_node(pointName)
                        x, y = float(x), float(y)*-1
                        G.nodes[pointName]['x'] = x
                        G.nodes[pointName]['y'] = y
                        pos[pointName] = (x,y)
                    
                if p ==1:
                    temp = pointName
                    firstPoint = temp
                #if p > 1:
                    #G.add_edge(lastPoint, pointName)
                #if p != len(pointList)-1:
                    #lastPoint = pointName
                    
                p += 1
                
            G.add_edge(firstPoint, pointName)
            w += 1
        
        
        graphDict[objectName].append( (G,pos) )
        
        g += 1
    keys = list(graphDict.keys())
    print("\nGraph Categories: ", keys)
    print("I am returning a dictionary of graph categories.")
    print("Each value in the dictionary is a LIST of (Graph, Position Dictionary) tuples.")
    return graphDict


######################## Actual Conversions ###################################
# Got the list of model names from:
# with cd('../images/ShapeMatcher/models'):
#     models = sp.run('dir', shell = True, capture_output = True, text = True)
#     models = str(models)
#     z = sp.run('dir', shell = True, capture_output = True)
#     print(z.stdout.decode())
    

#All the models that came with ShapeMatcher
# models = ["ALIEN",
# "BAT",
# "BULL",
# "camel",
# "DINO",
# "dog",
# "Dolphin",
# "duck",
# "eagle",
# "ESPRESSO",
# "guitar",
# "HORSE",
# "KANGAROO",
# "KNIFECLV",
# "LADYBUG",
# "LAMP",
# "m_chld",
# "pawn",
# "pig",
# "seahorse",
# "umbrella"]

# for model in models:
#     models2xml(ppmFolder = model)
#     print("\n")
# print("Done converting all models to XML")

###########################################################trash
#subprocess.check_output(['ls', '-l'])  # All that is technically needed...
# print(subprocess.check_output(['ls', '-l']))

# p1 = sp.run('dir', shell = True, capture_output = True)
# print(p1.stdout.decode()) # pretty print

# #or 

# https://www.youtube.com/watch?v=2Fp1N6dof0Y
# p2 = sp.run('dir', shell = True, capture_output = True, text = True)
# #text, but NOT pretty print


# 
# smdir = 'C:/ShapeMatcher6.0.1beta'#ShapeMather6.0.1beta directory
# cd = 'cd ' + smdir
# sp.run(cd, shell = True)
# files = [
#     "dino1.ppm",
#     "DINO0007.ppm",
#     "DINO0008.ppm",
#     "DINO0009.ppm"
#     ]
# db = "sm -doExtSimp 0 -c"
# dbname = "dino"
# db += " " + dbname + ".db"
# # "dino1.ppm DINO0007.ppm DINO0008.ppm DINO0009.ppm"
# for ppm in files:
#     db += " " + ppm

# z = sp.run(db, shell = True)

# match = "sm -m 1 " + dbname + ".db" 
# y = sp.run(match, shell = True)
# y.returncode
# xmlname = "dinos"
# toxml = "sm -toXML "+ xmlname + " " + dbname + ".db"
# #sm -toXML -from dino.db
# ##### wrong lol toXML = "sm " + dbname + ".db" + " -toXML"
# z = sp.run(toxml, shell = True)
# z.returncode
# w = read_sm("from.txt")


# # -toXML [val]      Saves the graphs from '-from ID' to '-to ID' in XML format
