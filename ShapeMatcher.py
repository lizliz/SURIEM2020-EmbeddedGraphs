# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 23:47:49 2020

@author: Candace Todd
"""
# This program uses the ShapeMatcher program to convert binary images to graphs
# using ShapeMatcher6.0.1beta

#import sys
import os
#sys.path.append(os.getcwd())
import subprocess as sp
import platform as p
import networkx as nx
import lib.Tools as t
from lib.sm2nx import read_sm
from contextlib import contextmanager


# ShapeMatcher Documentation: http://www.cs.toronto.edu/~dmac/ShapeMatcher/
# Convert to .ppm: https://convertio.co/

# Warning: these methods have not been thoroughly
# and I don't have a lot of experience calling terminal commands from within Python
# so if things start going wrong I suggest using ShapeMatcher directy from the terminal as it's indended
# I hope to add more functions later to make using ShapeMatcher from within Python a bit easier
# because the documentation for ShapeMatcher is not very detailed and outdated

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

# Convert any binary image with a .ppm extension to NetworkX graph
# Names of your .ppm files CANNOT have spaces
# Body of the image should be black, background should be white
# DBname: whatever you want the name of your database and xml file to be (ShapeMatcher puts images in a database file before converting them to graphs)
# ppmDir: Directory where the .ppm files you want to use are located
#         NOT including the files themselves
# ppmList: list of the .ppm files you want to convert
#          If none, converts all .ppm in the directory
#          I reccomend listing the .ppm files because the ShapeMatcher program 
#          doesn't always read in everything in the directory for some reason
# SMD: directory to ShapeMatcher application
def read_ppm(DBname, ppmDir, ppmList = None, SMD = None ):
    if SMD == None:
        SMD = '../images/ShapeMatcher'
    print("Converting", ppmDir, "...")
    
    with cd(SMD): # Directory finagling begins  
        
        with cd(ppmDir):# finagling x 2
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
        string = string[string.find(ppmDir)+1:]
        fileList = string.split(".ppm")
        fileList = fileList[:-1]
        
        # Need to work backwards from the end of the file name
        # This is why file names can't have spaces
        for i in range(len(fileList)):
            file = None
            j = -1
            while j >= (-1*len(fileList[i])):
                if fileList[i][j] == " ":
                    break
                j-=1
            j+=1
            file = fileList[i][j+len(fileList[i]):]
            file += ".ppm"
            fileList[i] = file

        # Now we have a list of all the files in the folder
        # So we can make a database consisting of all of these files
        
        # Start building the sm command for creating a database file
        createDB = 'sm -doExtSimp 0 -c ' + DBname + '.db'
        
        # Now add each of the files
        for file in fileList:
            createDB += " " + ppmDir + '/' + file
        
        # Make a database of the graphs
        cmd(createDB)
        # Convert database to XML file
        toXML = "sm -toXML "+ DBname + ".xml " + DBname + ".db"
        cmd(toXML)
        print("----------")   
        g = read_sm(DBname + ".xml")
        print("\t----------")   
        t.rename_key(g, list(g.keys())[0], DBname)
        
    print("\t----------")    
    print("\nConversion complete. Returning NetworkX graph object.") 
    print("\nYour", DBname, "database and XML file should be in ", SMD)
    
    return g

# Converting the model data from ShapeMatcher into giant XML files
# This isn't rally ever meant to be used again since read_ppm does the same thing
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

######################## Actual Conversions ###################################
# # Got the list of model names from:
# # with cd('../images/ShapeMatcher/models'):
# #     models = sp.run('dir', shell = True, capture_output = True, text = True)
# #     models = str(models)
# #     z = sp.run('dir', shell = True, capture_output = True)
# #     print(z.stdout.decode())
    

# #All the models that came with ShapeMatcher
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