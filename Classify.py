#Levent Batakci
#6/23/2020
#
#Dendro
import scipy.cluster.hierarchy as shc
import scipy.spatial.distance as ssd
import pandas as pd
import numpy as np
from sklearn.manifold import MDS
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt
from DataCalculations import average_distance
from lib.Tools import random_tree_and_pos, get_pos
import random
import DataReader as dr
import lib.Tools as t
import lib.tud2nx as tud
import matplotlib.colors as colors
import matplotlib.cm as cmx
import timeit
import time
#import Visualization as v
#from sympy import Matrix, pprint# old code from confusion matrix days

# Input list should be a list of pairs of graphs & positions
# data should be a 1-D condesed distance matrix if you use it
# I had to make the default data value 0 instead of None because 
def draw_dendro(input_list, frames=180, data = None, labels=None, thresh=None):
    if type(data) == type(None):
        data = get_data(input_list, frames)[0]    
    dendrogram(data, labels=labels, thresh=thresh)
    return data
            
# data parameter is a 1-D condensed distance matrix or a 2-D array of observation vectors
# data parameter is NOT a 2D distance matrix, pass a 2D distance matrix through get_data first
def dendrogram(data, labels=None, thresh=None):
    plt.figure(figsize=(10, 7))  
    plt.title("Dendrograms")
    lkg = shc.linkage(data, method='single')
    dend = shc.dendrogram(lkg, leaf_rotation = 90, labels=labels, color_threshold=thresh)
    if(thresh != None):
        plt.axhline(y=thresh, color='r', linestyle='--')
    
# converts 2-D distance matrix to 1-D condensed distance matrix
def condense(two_dimension_distance_matrix):
    return ssd.squareform(two_dimension_distance_matrix)

# Returns a 2D Distance matrix
def get_matrix(input_list, frames = 180, p = True, TIME = False):
    start = time.time()
    count = len(input_list)
    data = np.zeros(shape=(count,count))
    
    for i in range(count):
        
        for j in range(i, count):
            if p == True:
                print("(",i,",",j,")")
            
            if(i==j):
                val=0
            else:
                G1 = input_list[i][0]
                pos1 = input_list[i][1]
                G2 = input_list[j][0]
                pos2 = input_list[j][1]
                val=average_distance(G1, pos1, G2, pos2, frames=frames)
            
            data[i,j] = val
            data[j,i] = val
    
    if TIME == True:
        print("Making Distance Matrix: " + str(time.time() - start))
    return data

# I made this its own function so I could use it in mds
def get_data(input_list, frames = 180, p = True, TIME = False):
    
    data = get_matrix(input_list, frames = frames, p = p, TIME = TIME)
    flattened = condense(data)
    
    return [flattened, data]

# input_list: ordered list of graphs
# frames: same as before; number of frames from the rotation
# target_list: ordered list of the TARGET LABELS for the graphs, for example ["cats","cats","dogs"...] (NOT ["cat1", "cat2","dog1"...])
# D: 2D Distance matrix
# Colorize: whether or not you want to see the graph color coded according to the target labels
# scheme: see color map options: https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
# Adapted coloring method from https://stackoverflow.com/questions/8931268/using-colormaps-to-set-color-of-line-in-matplotlib
# Adapted MDS method from https://jakevdp.github.io/PythonDataScienceHandbook/05.10-manifold-learning.html
def mds(input_list, target_list, frames=180, D = None, colorize = True, scheme = "jet", legend = True, alpha = 0.4, TIME = True):
    if type(D) == type(None):
        D = get_data(input_list, frames, p = True, TIME = TIME)[1] # Get a distance matrix from the input list
    model = MDS(n_components=2, dissimilarity='precomputed', random_state=1)
    coords = model.fit_transform(D) # Outputs an array of the coordinates
    
    if colorize == False:
        x = coords[:, 0] # Get the x values
        y = coords[:, 1] # Get the y values
        plt.scatter(x, y) # Plot them
        plt.axis('equal')
    
    else: 
        
        label = {} # Dictionary of target labels
        for i in range(len(target_list)):# Find all the target labels in the data
            lbl = target_list[i]
            
            if lbl not in label:
                label[lbl] = []    
            label[lbl].append(i) # Keep track of the index of each element with this label
        
        clusters = [] #List of (label, Xarray, Yarray) tuples
        for l in label:
            Xs = []# Keep track of the x and y values of elements with this label
            Ys = []
            
            for index in label[l]: # Get the coordinates of elements with this label
                Xs.append(coords[:,0][index]) # Get the x value
                Ys.append(coords[:,1][index]) # Get the y value    
            clusters.append((l, np.array(Xs), np.array(Ys))) 
            
        fig = plt.figure() #initialize figure
        ax = fig.add_subplot(111) # 1x1 grid, 1st subplot
        values = range(len(label))
        jet = cm = plt.get_cmap(scheme) # Use matplotlib's jet color scheme by default
        cNorm  = colors.Normalize(vmin=0, vmax=values[-1])
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
        
        for j in range(len(clusters)):
 
            colorVal = scalarMap.to_rgba(values[j])
            colorText = (str(clusters[j][0]))
            retPoints = plt.scatter(x = clusters[j][1], 
                                   y = clusters[j][2], 
                                   c = [colorVal],# Make 'c' a vector to keep long warning message from printing
                                   label = colorText,
                                   alpha = alpha)
           
            if legend == True:
                handles,labels = ax.get_legend_handles_labels()
                ax.legend(handles, labels, loc='upper right')
        
        plt.axis('equal')
        plt.show()
 
    return coords    

######################### Testing Subgraphs ####################################
if __name__ == '__main__':
    inputs = []
    labels = []
    target = []
     
    p1 = "data/SanJoaquinCounty.json"
    w = dr.read_json(p1,False)[0]
    
    p2 = "data/eureka.json"
    x = dr.read_json(p2,False)[0]
    
    p3 = "data/atlanta.osm"
    y = dr.read_osm(p3,False)[0]
    
    p4 = "data/lancaster.osm"
    u = dr.read_osm(p4,False)[0]
    
    p5 = "data/dc.osm"
    v = dr.read_osm(p5,False)[0]
    
    num = 10 # Number of selections from the graph
    nodes = 300 # Number of nodes you want eat random selection to have
    frames = 90
    scheme = "jet"#"nipy_spectral"#"rainbow"# some good color choices
    alpha = 0.6 #Translucency of the points
    graphs = {
        "SanJoaquin":(w,[]),# Tuple with full graph object and list of all the randomly picked subgraphs
        "Eureka":(x,[]),
        "Atlanta":(y,[]),
        "Lancaster":(u,[]),
        "DC":(v,[])
              }

    for graph in graphs:
        if graph not in ["Eureka", "SanJoaquin"]: # Graphs you want
            continue
        for i in range(num):
            G = t.random_component(graphs[graph][0], nodes) #Get random subgraph
            pos = get_pos(G)
            graphs[graph][1].append(G)
            inputs.append( (G, pos) )
            labels.append(graph + str(i))
            target.append(graph)
            
matrix = get_matrix(inputs, frames, True, True)
flat = condense(matrix)
points = mds(inputs,target,frames,matrix,True,scheme,True,alpha,True)
data = draw_dendro(inputs, data = flat, frames=frames, labels=labels, thresh=0.03)

################################## Testing Letters ###########################
if __name__ == '__main__':
    inputs = []
    labels = []
    target = []
     
    p = "data/Letter-low"
    ds = "Letter-low"
    z = tud.read_tud(p,ds,False)
    num = 20
    frames = 10
    scheme = "rainbow"#"nipy_spectral"#"jet"# some good color choices
    alpha = 0.6 #Translucency of the points
    letters = {"K":"0",# There are 150 graphs of each letter in letter-low
            "N":"1",
            "L":"2",
            "Z":"3",
            "T":"4",
            "X":"5",
            "F":"6",
            "V":"7",
            "Y":"8",
            "W":"9",
            "H":"10",
            "A":"11",
            "I":"12",
            "E":"13",
            "M":"14"}
    # see test.py for how we picked outliers
    outliers = ['K0', 'K1', 'K2', 'K3', 'K4', 'K5', 'K6', 'K7', 'K8', 'K9', 'K10', 'K11', 'K12', 'K13', 'K14', 'K15', 'K16', 'K17', 'K18', 'K19', 'K20', 'K21', 'K22', 'K23', 'K24', 'K25', 'K26', 'K27', 'K28', 'K29', 'K30', 'K31', 'K32', 'K33', 'K34', 'K35', 'K36', 'K37', 'K38', 'K39', 'K40', 'K41', 'K42', 'K43', 'K44', 'K45', 'K46', 'K47', 'K48', 'K49', 'K50', 'K51', 'K52', 'K53', 'K54', 'K55', 'K56', 'K57', 'K58', 'K59', 'K60', 'K61', 'K62', 'K63', 'K64', 'K65', 'K66', 'K67', 'K68', 'K69', 'K70', 'K71', 'K72', 'K73', 'K74', 'K75', 'K76', 'K77', 'K78', 'K79', 'K80', 'K81', 'K82', 'K83', 'K84', 'K85', 'K86', 'K87', 'K88', 'K89', 'K90', 'K91', 'K92', 'K93', 'K94', 'K95', 'K96', 'K97', 'K98', 'K99', 'K100', 'K101', 'K102', 'K103', 'K104', 'K105', 'K106', 'K107', 'K108', 'K109', 'K110', 'K111', 'K112', 'K113', 'K114', 'K115', 'K116', 'K117', 'K118', 'K119', 'K120', 'K121', 'K122', 'K123', 'K124', 'K125', 'K126', 'K127', 'K128', 'K129', 'K130', 'K131', 'K132', 'K133', 'K134', 'K135', 'K136', 'K137', 'K138', 'K139', 'K140', 'K141', 'K142', 'K143', 'K144', 'K145', 'K146', 'K147', 'K148', 'K149', 'Y3', 'Y4', 'Y9', 'Y10', 'Y17', 'Y24', 'Y29', 'Y30', 'Y32', 'Y33', 'Y34', 'Y35', 'Y46', 'Y49', 'Y50', 'Y51', 'Y52', 'Y53', 'Y62', 'Y64', 'Y65', 'Y66', 'Y84', 'Y96', 'Y101', 'Y102', 'Y107', 'Y108', 'Y114', 'Y122', 'Y126', 'Y130', 'Y137', 'Y141', 'Y144', 'Y145', 'Y42', 'W8', 'W15', 'W20', 'W25', 'W50', 'W55', 'W61', 'W62', 'W72', 'W73', 'W79', 'W86', 'W88', 'W92', 'W93', 'W94', 'W95', 'W109', 'W120', 'W127', 'W145', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12', 'E13', 'E14', 'E15', 'E16', 'E17', 'E18', 'E19', 'E20', 'E21', 'E22', 'E23', 'E24', 'E25', 'E26', 'E27', 'E28', 'E29', 'E30', 'E31', 'E32', 'E33', 'E34', 'E35', 'E36', 'E37', 'E38', 'E39', 'E40', 'E41', 'E42', 'E43', 'E44', 'E45', 'E46', 'E47', 'E48', 'E49', 'E50', 'E51', 'E52', 'E53', 'E54', 'E55', 'E56', 'E57', 'E58', 'E59', 'E60', 'E61', 'E62', 'E63', 'E64', 'E65', 'E66', 'E67', 'E68', 'E69', 'E70', 'E71', 'E72', 'E73', 'E74', 'E75', 'E76', 'E77', 'E78', 'E79', 'E80', 'E81', 'E82', 'E83', 'E84', 'E85', 'E86', 'E87', 'E88', 'E89', 'E90', 'E91', 'E92', 'E93', 'E94', 'E95', 'E96', 'E97', 'E98', 'E99', 'E100', 'E101', 'E102', 'E103', 'E104', 'E105', 'E106', 'E107', 'E108', 'E109', 'E110', 'E111', 'E112', 'E113', 'E114', 'E115', 'E116', 'E117', 'E118', 'E119', 'E120', 'E121', 'E122', 'E123', 'E124', 'E125', 'E126', 'E127', 'E128', 'E129', 'E130', 'E131', 'E132', 'E133', 'E134', 'E135', 'E136', 'E137', 'E138', 'E139', 'E140', 'E141', 'E142', 'E143', 'E144', 'E145', 'E146', 'E147', 'E148', 'E149', 'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28', 'A29', 'A30', 'A31', 'A32', 'A33', 'A34', 'A35', 'A36', 'A37', 'A38', 'A39', 'A40', 'A41', 'A42', 'A43', 'A44', 'A45', 'A46', 'A47', 'A48', 'A49', 'A50', 'A51', 'A52', 'A53', 'A54', 'A55', 'A56', 'A57', 'A58', 'A59', 'A60', 'A61', 'A62', 'A63', 'A64', 'A65', 'A66', 'A67', 'A68', 'A69', 'A70', 'A71', 'A72', 'A73', 'A74', 'A75', 'A76', 'A77', 'A78', 'A79', 'A80', 'A81', 'A82', 'A83', 'A84', 'A85', 'A86', 'A87', 'A88', 'A89', 'A90', 'A91', 'A92', 'A93', 'A94', 'A95', 'A96', 'A97', 'A98', 'A99', 'A100', 'A101', 'A102', 'A103', 'A104', 'A105', 'A106', 'A107', 'A108', 'A109', 'A110', 'A111', 'A112', 'A113', 'A114', 'A115', 'A116', 'A117', 'A118', 'A119', 'A120', 'A121', 'A122', 'A123', 'A124', 'A125', 'A126', 'A127', 'A128', 'A129', 'A130', 'A131', 'A132', 'A133', 'A134', 'A135', 'A136', 'A137', 'A138', 'A139', 'A140', 'A141', 'A142', 'A143', 'A144', 'A145', 'A146', 'A147', 'A148', 'A149', 'H0', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12', 'H13', 'H14', 'H15', 'H16', 'H17', 'H18', 'H19', 'H20', 'H21', 'H22', 'H23', 'H24', 'H25', 'H26', 'H27', 'H28', 'H29', 'H30', 'H31', 'H32', 'H33', 'H34', 'H35', 'H36', 'H37', 'H38', 'H39', 'H40', 'H41', 'H42', 'H43', 'H44', 'H45', 'H46', 'H47', 'H48', 'H49', 'H50', 'H51', 'H52', 'H53', 'H54', 'H55', 'H56', 'H57', 'H58', 'H59', 'H60', 'H61', 'H62', 'H63', 'H64', 'H65', 'H66', 'H67', 'H68', 'H69', 'H70', 'H71', 'H72', 'H73', 'H74', 'H75', 'H76', 'H77', 'H78', 'H79', 'H80', 'H81', 'H82', 'H83', 'H84', 'H85', 'H86', 'H87', 'H88', 'H89', 'H90', 'H91', 'H92', 'H93', 'H94', 'H95', 'H96', 'H97', 'H98', 'H99', 'H100', 'H101', 'H102', 'H103', 'H104', 'H105', 'H106', 'H107', 'H108', 'H109', 'H110', 'H111', 'H112', 'H113', 'H114', 'H115', 'H116', 'H117', 'H118', 'H119', 'H120', 'H121', 'H122', 'H123', 'H124', 'H125', 'H126', 'H127', 'H128', 'H129', 'H130', 'H131', 'H132', 'H133', 'H134', 'H135', 'H136', 'H137', 'H138', 'H139', 'H140', 'H141', 'H142', 'H143', 'H144', 'H145', 'H146', 'H147', 'H148', 'H149', 'X0', 'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'X10', 'X11', 'X12', 'X13', 'X14', 'X15', 'X16', 'X17', 'X18', 'X19', 'X20', 'X21', 'X22', 'X23', 'X24', 'X25', 'X26', 'X27', 'X28', 'X29', 'X30', 'X31', 'X32', 'X33', 'X34', 'X35', 'X36', 'X37', 'X38', 'X39', 'X40', 'X41', 'X42', 'X43', 'X44', 'X45', 'X46', 'X47', 'X48', 'X49', 'X50', 'X51', 'X52', 'X53', 'X54', 'X55', 'X56', 'X57', 'X58', 'X59', 'X60', 'X61', 'X62', 'X63', 'X64', 'X65', 'X66', 'X67', 'X68', 'X69', 'X70', 'X71', 'X72', 'X73', 'X74', 'X75', 'X76', 'X77', 'X78', 'X79', 'X80', 'X81', 'X82', 'X83', 'X84', 'X85', 'X86', 'X87', 'X88', 'X89', 'X90', 'X91', 'X92', 'X93', 'X94', 'X95', 'X96', 'X97', 'X98', 'X99', 'X100', 'X101', 'X102', 'X103', 'X104', 'X105', 'X106', 'X107', 'X108', 'X109', 'X110', 'X111', 'X112', 'X113', 'X114', 'X115', 'X116', 'X117', 'X118', 'X119', 'X120', 'X121', 'X122', 'X123', 'X124', 'X125', 'X126', 'X127', 'X128', 'X129', 'X130', 'X131', 'X132', 'X133', 'X134', 'X135', 'X136', 'X137', 'X138', 'X139', 'X140', 'X141', 'X142', 'X143', 'X144', 'X145', 'X146', 'X147', 'X148', 'X149', 'T0', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12', 'T13', 'T14', 'T15', 'T16', 'T17', 'T18', 'T19', 'T20', 'T21', 'T22', 'T23', 'T24', 'T25', 'T26', 'T27', 'T28', 'T29', 'T30', 'T31', 'T32', 'T33', 'T34', 'T35', 'T36', 'T37', 'T38', 'T39', 'T40', 'T41', 'T42', 'T43', 'T44', 'T45', 'T46', 'T47', 'T48', 'T49', 'T50', 'T51', 'T52', 'T53', 'T54', 'T55', 'T56', 'T57', 'T58', 'T59', 'T60', 'T61', 'T62', 'T63', 'T64', 'T65', 'T66', 'T67', 'T68', 'T69', 'T70', 'T71', 'T72', 'T73', 'T74', 'T75', 'T76', 'T77', 'T78', 'T79', 'T80', 'T81', 'T82', 'T83', 'T84', 'T85', 'T86', 'T87', 'T88', 'T89', 'T90', 'T91', 'T92', 'T93', 'T94', 'T95', 'T96', 'T97', 'T98', 'T99', 'T100', 'T101', 'T102', 'T103', 'T104', 'T105', 'T106', 'T107', 'T108', 'T109', 'T110', 'T111', 'T112', 'T113', 'T114', 'T115', 'T116', 'T117', 'T118', 'T119', 'T120', 'T121', 'T122', 'T123', 'T124', 'T125', 'T126', 'T127', 'T128', 'T129', 'T130', 'T131', 'T132', 'T133', 'T134', 'T135', 'T136', 'T137', 'T138', 'T139', 'T140', 'T141', 'T142', 'T143', 'T144', 'T145', 'T146', 'T147', 'T148', 'T149', 'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15', 'F16', 'F17', 'F18', 'F19', 'F20', 'F21', 'F22', 'F23', 'F24', 'F25', 'F26', 'F27', 'F28', 'F29', 'F30', 'F31', 'F32', 'F33', 'F34', 'F35', 'F36', 'F37', 'F38', 'F39', 'F40', 'F41', 'F42', 'F43', 'F44', 'F45', 'F46', 'F47', 'F48', 'F49', 'F50', 'F51', 'F52', 'F53', 'F54', 'F55', 'F56', 'F57', 'F58', 'F59', 'F60', 'F61', 'F62', 'F63', 'F64', 'F65', 'F66', 'F67', 'F68', 'F69', 'F70', 'F71', 'F72', 'F73', 'F74', 'F75', 'F76', 'F77', 'F78', 'F79', 'F80', 'F81', 'F82', 'F83', 'F84', 'F85', 'F86', 'F87', 'F88', 'F89', 'F90', 'F91', 'F92', 'F93', 'F94', 'F95', 'F96', 'F97', 'F98', 'F99', 'F100', 'F101', 'F102', 'F103', 'F104', 'F105', 'F106', 'F107', 'F108', 'F109', 'F110', 'F111', 'F112', 'F113', 'F114', 'F115', 'F116', 'F117', 'F118', 'F119', 'F120', 'F121', 'F122', 'F123', 'F124', 'F125', 'F126', 'F127', 'F128', 'F129', 'F130', 'F131', 'F132', 'F133', 'F134', 'F135', 'F136', 'F137', 'F138', 'F139', 'F140', 'F141', 'F142', 'F143', 'F144', 'F145', 'F146', 'F147', 'F148', 'F149', 'I7', 'I16', 'I18', 'I20', 'I21', 'I22', 'I24', 'I28', 'I31', 'I35', 'I36', 'I37', 'I41', 'I43', 'I47', 'I48', 'I63', 'I64', 'I65', 'I77', 'I78', 'I102', 'I104', 'I107', 'I115', 'I121', 'I125', 'I132', 'I134', 'I143', 'I146', 'I147', 'I101', 'V1', 'V21', 'V25', 'V26', 'V35', 'V40', 'V44', 'V52', 'V56', 'V57', 'V60', 'V66', 'V68', 'V70', 'V73', 'V75', 'V81', 'V82', 'V87', 'V88', 'V91', 'V92', 'V95', 'V97', 'V100', 'V103', 'V105', 'V113', 'V115', 'V123', 'V130', 'V135', 'V136', 'V137', 'V141', 'V142', 'V144', 'V10', 'L0', 'L2', 'L11', 'L30', 'L37', 'L53', 'L58', 'L71', 'L74', 'L79', 'L81', 'L87', 'L89', 'L91', 'L96', 'L100', 'L101', 'L104', 'L108', 'L109', 'L116', 'L126', 'L127', 'L128', 'L133', 'L35', 'L51', 'L67', 'L80', 'L139', 'Z0', 'Z6', 'Z16', 'Z18', 'Z21', 'Z29', 'Z31', 'Z33', 'Z39', 'Z42', 'Z43', 'Z44', 'Z45', 'Z49', 'Z52', 'Z55', 'Z56', 'Z60', 'Z64', 'Z67', 'Z75', 'Z77', 'Z80', 'Z92', 'Z95', 'Z96', 'Z101', 'Z104', 'Z105', 'Z108', 'Z110', 'Z111', 'Z113', 'Z116', 'Z117', 'Z122', 'Z125', 'Z130', 'Z135', 'Z136', 'Z139', 'Z141', 'Z142', 'Z143', 'Z146', 'Z147', 'Z149', 'Z30', 'Z131', 'M2', 'M3', 'M4', 'M7', 'M9', 'M10', 'M11', 'M13', 'M14', 'M15', 'M17', 'M24', 'M26', 'M29', 'M30', 'M37', 'M38', 'M40', 'M43', 'M53', 'M56', 'M57', 'M60', 'M65', 'M69', 'M72', 'M73', 'M77', 'M78', 'M81', 'M83', 'M95', 'M100', 'M101', 'M109', 'M112', 'M115', 'M119', 'M121', 'M122', 'M125', 'M128', 'M137', 'M139', 'M142', 'M145', 'N1', 'N8', 'N9', 'N12', 'N15', 'N25', 'N27', 'N36', 'N37', 'N41', 'N45', 'N49', 'N50', 'N51', 'N58', 'N59', 'N63', 'N68', 'N71', 'N73', 'N79', 'N83', 'N87', 'N88', 'N91', 'N95', 'N97', 'N107', 'N108', 'N110', 'N116', 'N125', 'N127', 'N128', 'N129', 'N130', 'N132', 'N134', 'N135', 'N142', 'N145']

    for letter in letters:
        # Only graph the letters you're interested in
        #if letter not in ["K","M","Z", "L", "W", "V", "E", "M"]:
        #   continue
        for i in range(num):
            if letter + str(i) in outliers:
                continue
            G = z[0][letters[letter]][i]
            G = t.main_component(G = G, report = False)
            pos = get_pos(G)
            inputs.append( (G, pos) )
            labels.append(letter + str(i))
            target.append(letter)
            
matrix = get_matrix(inputs, frames, True, True)
flat = condense(matrix)
points = mds(inputs,target,frames,matrix,True,scheme,True,alpha,True)
data = draw_dendro(inputs, data = flat, frames=frames, labels=labels, thresh=0.38)

 
########################### Comparing Letters####################################

    # #Get 5 Z's
    # for i in range(num):
    #     G = z[0]["3"][i]
    #     G = t.main_component(G)
    #     pos = get_pos(G)
        
    #     inputs.append( (G, pos) )
    #     labels.append("Z " + str(i))
    #     target.append("Z")
    
    # #Get 5 L's
    # for i in range(num):
    #     G = z[0]["2"][i]
    #     G = t.main_component(G)
    #     pos = get_pos(G)
        
    #     inputs.append( (G, pos) )
    #     labels.append("L " + str(i))
    #     target.append("L")
    
    # #Get 5 N's
    # for i in range(num):
    #     G = z[0]["1"][i]
    #     G = t.main_component(G)
    #     pos = get_pos(G)
        
    #     inputs.append( (G, pos) )
    #     labels.append("N " + str(i))
    #     target.append("N")
        
    # #Get 5 V's
    # for i in range(num):
    #     G = z[0]["7"][i]
    #     pos = get_pos(G)
    #     G = t.main_component(G)
        
    #     inputs.append( (G, pos) )
    #     labels.append("V " + str(i))
    #     target.append("V")
   
####################### Comparing Cat Graphs  #####################################

    # pth = "./data/kitty2.graphml"  #0
    # inp = dr.read_graphml(pth)
    # inputs.append(inp)
    
    # pth = "./data/kitty1.graphml"  #1
    # inp = dr.read_graphml(pth)
    # inputs.append(inp)
    
    # pth = "./data/kitty2.graphml"  #2
    # inp = dr.read_graphml(pth)
    # inputs.append(inp)
    
    # pth = "./data/brutus.graphml"  #3
    # inp = dr.read_graphml(pth)
    # inputs.append(inp)
    
    # pth = "./data/sofie.graphml"  #4
    # inp = dr.read_graphml(pth)
    # inputs.append(inp)
    
    # labels = ["kitty2 (1)","kitty1","kitty2 (2)","Brutus","Sofie"]

###################### Comparing Cat and Dog images ###########################  
 
    # pth = "./data/Binary Images/cat2.png"  #0
    # inp = dr.read_img(pth)
    # inputs.append(inp)
    
    # pth = "./data/Binary Images/cat3.png"  #0
    # inp = dr.read_img(pth)
    # inputs.append(inp)
    
    # pth = "./data/Binary Images/dog1.png"  #0
    # inp = dr.read_img(pth)
    # inputs.append(inp)
    
    # pth = "./data/Binary Images/dog2.png"  #0
    # inp = dr.read_img(pth)
    # inputs.append(inp)
    
    # pth = "./data/Binary Images/dog.png"  #0
    # inp = dr.read_img(pth)
    # inputs.append(inp)
    
    # labels = ["cat2","cat3","dog1","dog2","dog3"]

################################ Misc? #######################################
   
    #labels = ['a','b','c','d']
    #data = np.array( [[0,1,10,7],[1,0,8,9],[10,8,0,2],[7,9,2,0]] )
    #data = np.array([1,10,8,7,9,2])
    #dendrogram(data, labels=labels)


    #L0 = z[0]["2"][0]
    #pos1 = get_pos(L0)
    #V1 = z[0]["7"][1]
    #pos2 = get_pos(V1)
    
    #v.cool_GIF(L0, pos1, V1, pos2, frames=180, fps=20)
    
###############################################################################
# Old code from back when we thought we were going to use a confusion matrix
# Didn't wanna throw it away so here it is.
# It's not at all near complete but this is where I stopped so ¯\_(ツ)_/¯

# def confusion(input_list, labels, thresh, predicted_classes):
#     data = get_data(input_list)[0]# Get the data in the format we want
#     lkg = shc.linkage(data, method='single')# Get the linkage
    
#     # Get the list of all the classes that actually appeared in the data
#     # The index in this corresponds to the elements at the same index in input_list
#     actual_classes = list(shc.fcluster(lkg, thresh, criterion='distance'))
    
#     # Columns in the confusion matrix correspond to the predicted labels
#     n = len(predicted_classes)
#     # Rows in the confusion matrix correspond to the actual labels
#     m = len(actual_classes)
#     # start with an empty m by n matrix
#     confusionMatrix = [ [0 for i in range(n)] for j in range(m) ]
#     pkey = {} # Going to use dictionaries to keep track of the indices of labels
#     akey = {}
#     index = 0
#     known = []
#     for p in predicted_classes:
#         pkey[index] = p # Adding the classes to the dictionaries
#         akey[index] = p
#         index += 1
#         known.append(p)
#     for a in actual_classes:
#         if a not in known:
#             known.append(a)
#             akey[index] = a
#             index += 1
    
#     for i in range(len(labels)):
#         p = predicted_classes[i] # Predicted class of a certain graph
#         a = actual_classes[i] # Actual class of a the same graph


# # Scipy will group things together, but we need to figure out what the group labels mean
# def convert_classes(linkage, input_list, predicted_classes, actual_classes):S
#     # We're going to assume that the most prevalent label in an actual class
#     # is the proper label for that class
#     members = {} # Dictionary of lists of class members
#     for c in range(len(actual_classes)):
#         a = actual_classes[c]
#         p = predicted_classes[c]
#         if a not in members:
#             members[a] = []
#         members[a].append(p)