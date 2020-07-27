# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 21:18:16 2020

@author: Candace Todd
"""
# Running this script generates the plots seen in our paper
# And a gif seen in our SUMMR 2020 conference presentation
from lib.sm2nx import read_sm
from lib.tud2nx import read_tud
import lib.Tools as t
import Classify as classify

########################### Comparing Letters####################################

l_inputs = []
l_target = []
l_labels = []

p = "data/Letter-low"
ds = "Letter-low"
z = read_tud(p,ds,False)

frames = 10 
scheme = "jet"
alpha = 0.6 
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
# see data/DataCleaning.py for how we picked outliers
outliers = ['K0', 'K1', 'K2', 'K3', 'K4', 'K5', 'K6', 'K7', 'K8', 'K9', 'K10', 'K11', 'K12', 'K13', 'K14', 'K15', 'K16', 'K17', 'K18', 'K19', 'K20', 'K21', 'K22', 'K23', 'K24', 'K25', 'K26', 'K27', 'K28', 'K29', 'K30', 'K31', 'K32', 'K33', 'K34', 'K35', 'K36', 'K37', 'K38', 'K39', 'K40', 'K41', 'K42', 'K43', 'K44', 'K45', 'K46', 'K47', 'K48', 'K49', 'K50', 'K51', 'K52', 'K53', 'K54', 'K55', 'K56', 'K57', 'K58', 'K59', 'K60', 'K61', 'K62', 'K63', 'K64', 'K65', 'K66', 'K67', 'K68', 'K69', 'K70', 'K71', 'K72', 'K73', 'K74', 'K75', 'K76', 'K77', 'K78', 'K79', 'K80', 'K81', 'K82', 'K83', 'K84', 'K85', 'K86', 'K87', 'K88', 'K89', 'K90', 'K91', 'K92', 'K93', 'K94', 'K95', 'K96', 'K97', 'K98', 'K99', 'K100', 'K101', 'K102', 'K103', 'K104', 'K105', 'K106', 'K107', 'K108', 'K109', 'K110', 'K111', 'K112', 'K113', 'K114', 'K115', 'K116', 'K117', 'K118', 'K119', 'K120', 'K121', 'K122', 'K123', 'K124', 'K125', 'K126', 'K127', 'K128', 'K129', 'K130', 'K131', 'K132', 'K133', 'K134', 'K135', 'K136', 'K137', 'K138', 'K139', 'K140', 'K141', 'K142', 'K143', 'K144', 'K145', 'K146', 'K147', 'K148', 'K149', 'Y3', 'Y4', 'Y9', 'Y10', 'Y17', 'Y24', 'Y29', 'Y30', 'Y32', 'Y33', 'Y34', 'Y35', 'Y46', 'Y49', 'Y50', 'Y51', 'Y52', 'Y53', 'Y62', 'Y64', 'Y65', 'Y66', 'Y84', 'Y96', 'Y101', 'Y102', 'Y107', 'Y108', 'Y114', 'Y122', 'Y126', 'Y130', 'Y137', 'Y141', 'Y144', 'Y145', 'Y42', 'W8', 'W15', 'W20', 'W25', 'W50', 'W55', 'W61', 'W62', 'W72', 'W73', 'W79', 'W86', 'W88', 'W92', 'W93', 'W94', 'W95', 'W109', 'W120', 'W127', 'W145', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12', 'E13', 'E14', 'E15', 'E16', 'E17', 'E18', 'E19', 'E20', 'E21', 'E22', 'E23', 'E24', 'E25', 'E26', 'E27', 'E28', 'E29', 'E30', 'E31', 'E32', 'E33', 'E34', 'E35', 'E36', 'E37', 'E38', 'E39', 'E40', 'E41', 'E42', 'E43', 'E44', 'E45', 'E46', 'E47', 'E48', 'E49', 'E50', 'E51', 'E52', 'E53', 'E54', 'E55', 'E56', 'E57', 'E58', 'E59', 'E60', 'E61', 'E62', 'E63', 'E64', 'E65', 'E66', 'E67', 'E68', 'E69', 'E70', 'E71', 'E72', 'E73', 'E74', 'E75', 'E76', 'E77', 'E78', 'E79', 'E80', 'E81', 'E82', 'E83', 'E84', 'E85', 'E86', 'E87', 'E88', 'E89', 'E90', 'E91', 'E92', 'E93', 'E94', 'E95', 'E96', 'E97', 'E98', 'E99', 'E100', 'E101', 'E102', 'E103', 'E104', 'E105', 'E106', 'E107', 'E108', 'E109', 'E110', 'E111', 'E112', 'E113', 'E114', 'E115', 'E116', 'E117', 'E118', 'E119', 'E120', 'E121', 'E122', 'E123', 'E124', 'E125', 'E126', 'E127', 'E128', 'E129', 'E130', 'E131', 'E132', 'E133', 'E134', 'E135', 'E136', 'E137', 'E138', 'E139', 'E140', 'E141', 'E142', 'E143', 'E144', 'E145', 'E146', 'E147', 'E148', 'E149', 'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28', 'A29', 'A30', 'A31', 'A32', 'A33', 'A34', 'A35', 'A36', 'A37', 'A38', 'A39', 'A40', 'A41', 'A42', 'A43', 'A44', 'A45', 'A46', 'A47', 'A48', 'A49', 'A50', 'A51', 'A52', 'A53', 'A54', 'A55', 'A56', 'A57', 'A58', 'A59', 'A60', 'A61', 'A62', 'A63', 'A64', 'A65', 'A66', 'A67', 'A68', 'A69', 'A70', 'A71', 'A72', 'A73', 'A74', 'A75', 'A76', 'A77', 'A78', 'A79', 'A80', 'A81', 'A82', 'A83', 'A84', 'A85', 'A86', 'A87', 'A88', 'A89', 'A90', 'A91', 'A92', 'A93', 'A94', 'A95', 'A96', 'A97', 'A98', 'A99', 'A100', 'A101', 'A102', 'A103', 'A104', 'A105', 'A106', 'A107', 'A108', 'A109', 'A110', 'A111', 'A112', 'A113', 'A114', 'A115', 'A116', 'A117', 'A118', 'A119', 'A120', 'A121', 'A122', 'A123', 'A124', 'A125', 'A126', 'A127', 'A128', 'A129', 'A130', 'A131', 'A132', 'A133', 'A134', 'A135', 'A136', 'A137', 'A138', 'A139', 'A140', 'A141', 'A142', 'A143', 'A144', 'A145', 'A146', 'A147', 'A148', 'A149', 'H0', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12', 'H13', 'H14', 'H15', 'H16', 'H17', 'H18', 'H19', 'H20', 'H21', 'H22', 'H23', 'H24', 'H25', 'H26', 'H27', 'H28', 'H29', 'H30', 'H31', 'H32', 'H33', 'H34', 'H35', 'H36', 'H37', 'H38', 'H39', 'H40', 'H41', 'H42', 'H43', 'H44', 'H45', 'H46', 'H47', 'H48', 'H49', 'H50', 'H51', 'H52', 'H53', 'H54', 'H55', 'H56', 'H57', 'H58', 'H59', 'H60', 'H61', 'H62', 'H63', 'H64', 'H65', 'H66', 'H67', 'H68', 'H69', 'H70', 'H71', 'H72', 'H73', 'H74', 'H75', 'H76', 'H77', 'H78', 'H79', 'H80', 'H81', 'H82', 'H83', 'H84', 'H85', 'H86', 'H87', 'H88', 'H89', 'H90', 'H91', 'H92', 'H93', 'H94', 'H95', 'H96', 'H97', 'H98', 'H99', 'H100', 'H101', 'H102', 'H103', 'H104', 'H105', 'H106', 'H107', 'H108', 'H109', 'H110', 'H111', 'H112', 'H113', 'H114', 'H115', 'H116', 'H117', 'H118', 'H119', 'H120', 'H121', 'H122', 'H123', 'H124', 'H125', 'H126', 'H127', 'H128', 'H129', 'H130', 'H131', 'H132', 'H133', 'H134', 'H135', 'H136', 'H137', 'H138', 'H139', 'H140', 'H141', 'H142', 'H143', 'H144', 'H145', 'H146', 'H147', 'H148', 'H149', 'X0', 'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'X10', 'X11', 'X12', 'X13', 'X14', 'X15', 'X16', 'X17', 'X18', 'X19', 'X20', 'X21', 'X22', 'X23', 'X24', 'X25', 'X26', 'X27', 'X28', 'X29', 'X30', 'X31', 'X32', 'X33', 'X34', 'X35', 'X36', 'X37', 'X38', 'X39', 'X40', 'X41', 'X42', 'X43', 'X44', 'X45', 'X46', 'X47', 'X48', 'X49', 'X50', 'X51', 'X52', 'X53', 'X54', 'X55', 'X56', 'X57', 'X58', 'X59', 'X60', 'X61', 'X62', 'X63', 'X64', 'X65', 'X66', 'X67', 'X68', 'X69', 'X70', 'X71', 'X72', 'X73', 'X74', 'X75', 'X76', 'X77', 'X78', 'X79', 'X80', 'X81', 'X82', 'X83', 'X84', 'X85', 'X86', 'X87', 'X88', 'X89', 'X90', 'X91', 'X92', 'X93', 'X94', 'X95', 'X96', 'X97', 'X98', 'X99', 'X100', 'X101', 'X102', 'X103', 'X104', 'X105', 'X106', 'X107', 'X108', 'X109', 'X110', 'X111', 'X112', 'X113', 'X114', 'X115', 'X116', 'X117', 'X118', 'X119', 'X120', 'X121', 'X122', 'X123', 'X124', 'X125', 'X126', 'X127', 'X128', 'X129', 'X130', 'X131', 'X132', 'X133', 'X134', 'X135', 'X136', 'X137', 'X138', 'X139', 'X140', 'X141', 'X142', 'X143', 'X144', 'X145', 'X146', 'X147', 'X148', 'X149', 'T0', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12', 'T13', 'T14', 'T15', 'T16', 'T17', 'T18', 'T19', 'T20', 'T21', 'T22', 'T23', 'T24', 'T25', 'T26', 'T27', 'T28', 'T29', 'T30', 'T31', 'T32', 'T33', 'T34', 'T35', 'T36', 'T37', 'T38', 'T39', 'T40', 'T41', 'T42', 'T43', 'T44', 'T45', 'T46', 'T47', 'T48', 'T49', 'T50', 'T51', 'T52', 'T53', 'T54', 'T55', 'T56', 'T57', 'T58', 'T59', 'T60', 'T61', 'T62', 'T63', 'T64', 'T65', 'T66', 'T67', 'T68', 'T69', 'T70', 'T71', 'T72', 'T73', 'T74', 'T75', 'T76', 'T77', 'T78', 'T79', 'T80', 'T81', 'T82', 'T83', 'T84', 'T85', 'T86', 'T87', 'T88', 'T89', 'T90', 'T91', 'T92', 'T93', 'T94', 'T95', 'T96', 'T97', 'T98', 'T99', 'T100', 'T101', 'T102', 'T103', 'T104', 'T105', 'T106', 'T107', 'T108', 'T109', 'T110', 'T111', 'T112', 'T113', 'T114', 'T115', 'T116', 'T117', 'T118', 'T119', 'T120', 'T121', 'T122', 'T123', 'T124', 'T125', 'T126', 'T127', 'T128', 'T129', 'T130', 'T131', 'T132', 'T133', 'T134', 'T135', 'T136', 'T137', 'T138', 'T139', 'T140', 'T141', 'T142', 'T143', 'T144', 'T145', 'T146', 'T147', 'T148', 'T149', 'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15', 'F16', 'F17', 'F18', 'F19', 'F20', 'F21', 'F22', 'F23', 'F24', 'F25', 'F26', 'F27', 'F28', 'F29', 'F30', 'F31', 'F32', 'F33', 'F34', 'F35', 'F36', 'F37', 'F38', 'F39', 'F40', 'F41', 'F42', 'F43', 'F44', 'F45', 'F46', 'F47', 'F48', 'F49', 'F50', 'F51', 'F52', 'F53', 'F54', 'F55', 'F56', 'F57', 'F58', 'F59', 'F60', 'F61', 'F62', 'F63', 'F64', 'F65', 'F66', 'F67', 'F68', 'F69', 'F70', 'F71', 'F72', 'F73', 'F74', 'F75', 'F76', 'F77', 'F78', 'F79', 'F80', 'F81', 'F82', 'F83', 'F84', 'F85', 'F86', 'F87', 'F88', 'F89', 'F90', 'F91', 'F92', 'F93', 'F94', 'F95', 'F96', 'F97', 'F98', 'F99', 'F100', 'F101', 'F102', 'F103', 'F104', 'F105', 'F106', 'F107', 'F108', 'F109', 'F110', 'F111', 'F112', 'F113', 'F114', 'F115', 'F116', 'F117', 'F118', 'F119', 'F120', 'F121', 'F122', 'F123', 'F124', 'F125', 'F126', 'F127', 'F128', 'F129', 'F130', 'F131', 'F132', 'F133', 'F134', 'F135', 'F136', 'F137', 'F138', 'F139', 'F140', 'F141', 'F142', 'F143', 'F144', 'F145', 'F146', 'F147', 'F148', 'F149', 'I7', 'I16', 'I18', 'I20', 'I21', 'I22', 'I24', 'I28', 'I31', 'I35', 'I36', 'I37', 'I41', 'I43', 'I47', 'I48', 'I63', 'I64', 'I65', 'I77', 'I78', 'I102', 'I104', 'I107', 'I115', 'I121', 'I125', 'I132', 'I134', 'I143', 'I146', 'I147', 'I101', 'V1', 'V21', 'V25', 'V26', 'V35', 'V40', 'V44', 'V52', 'V56', 'V57', 'V60', 'V66', 'V68', 'V70', 'V73', 'V75', 'V81', 'V82', 'V87', 'V88', 'V91', 'V92', 'V95', 'V97', 'V100', 'V103', 'V105', 'V113', 'V115', 'V123', 'V130', 'V135', 'V136', 'V137', 'V141', 'V142', 'V144', 'V10', 'L0', 'L2', 'L11', 'L30', 'L37', 'L53', 'L58', 'L71', 'L74', 'L79', 'L81', 'L87', 'L89', 'L91', 'L96', 'L100', 'L101', 'L104', 'L108', 'L109', 'L116', 'L126', 'L127', 'L128', 'L133', 'L35', 'L51', 'L67', 'L80', 'L139', 'Z0', 'Z6', 'Z16', 'Z18', 'Z21', 'Z29', 'Z31', 'Z33', 'Z39', 'Z42', 'Z43', 'Z44', 'Z45', 'Z49', 'Z52', 'Z55', 'Z56', 'Z60', 'Z64', 'Z67', 'Z75', 'Z77', 'Z80', 'Z92', 'Z95', 'Z96', 'Z101', 'Z104', 'Z105', 'Z108', 'Z110', 'Z111', 'Z113', 'Z116', 'Z117', 'Z122', 'Z125', 'Z130', 'Z135', 'Z136', 'Z139', 'Z141', 'Z142', 'Z143', 'Z146', 'Z147', 'Z149', 'Z30', 'Z131', 'M2', 'M3', 'M4', 'M7', 'M9', 'M10', 'M11', 'M13', 'M14', 'M15', 'M17', 'M24', 'M26', 'M29', 'M30', 'M37', 'M38', 'M40', 'M43', 'M53', 'M56', 'M57', 'M60', 'M65', 'M69', 'M72', 'M73', 'M77', 'M78', 'M81', 'M83', 'M95', 'M100', 'M101', 'M109', 'M112', 'M115', 'M119', 'M121', 'M122', 'M125', 'M128', 'M137', 'M139', 'M142', 'M145', 'N1', 'N8', 'N9', 'N12', 'N15', 'N25', 'N27', 'N36', 'N37', 'N41', 'N45', 'N49', 'N50', 'N51', 'N58', 'N59', 'N63', 'N68', 'N71', 'N73', 'N79', 'N83', 'N87', 'N88', 'N91', 'N95', 'N97', 'N107', 'N108', 'N110', 'N116', 'N125', 'N127', 'N128', 'N129', 'N130', 'N132', 'N134', 'N135', 'N142', 'N145']
nList = [n for n in outliers if n.find("N") !=-1]
zList = [z for z in outliers if z.find("Z") !=-1]
mList = [m for m in outliers if m.find("M") !=-1]
vList = [v for v in outliers if v.find("V") !=-1]
wList = [w for w in outliers if w.find("W") !=-1]


num = 10
for letter in letters:
    # Only graph the letters you're interested in
    if letter not in ["N","Z","M","V","W"]:
         continue
    if letter == "N":
        num = 7
        lst = nList
    if letter == "Z":
        num = 8
        lst = zList
    if letter == "M":
        num = 5
        lst = mList
    if letter == "V":
        num = 9
        lst = vList
    if letter == "W":
        num = 9
        lst = wList
    j = 0    
    for i in range(num):
        while letter + str(j) in lst:
            j += 1
        if j > ( 150 - len(lst) )-1:
            break
        G = z[0][letters[letter]][j]
        G = t.main_component(G = G, report = False)
        pos = t.get_pos(G)
        l_inputs.append( (G, pos) )
        l_labels.append(letter + str(j))
        l_target.append(letter)
        j += 1


matrix = classify.get_matrix(l_inputs, frames, True, True, average = "median")
flat = classify.condense(matrix)

# This plot may render with the axes flippeed
points = classify.mds(input_list = l_inputs,
              target_list = l_target,
              frames = frames,
              D = matrix,
              colorize = True,
              scheme = scheme,
              legend = True,
              legend_position = "lower right",
              alpha = alpha,
              TIME = True,
              xRange = (-1.5,1.5), 
              yRange = [-1,1])


data = classify.draw_dendro(input_list = l_inputs,
                            frames=frames,
                            data = flat,
                            labels= l_labels,
                            thresh=0.3)


############### Makes an ABD gif between an N and W ###########################
p = "data/Letter-low"
ds = "Letter-low"
z = read_tud(p,ds,False)

import Visualization as v
G1 = z[0]["1"][0]
pos1 = t.get_pos(G1)
G2 = z[0]["9"][0]
pos2 = t.get_pos(G2)
v.cool_GIF(G1, pos1, G2, pos2, frames=720)

######################## Binary ShapeMatcher Models ###########################
matrices=[None,None,None,None] # For you to reference later

alienDict = read_sm("data/Shape-Matcher-models/ALIEN.xml")
t.rename_key(alienDict, oldKey = "models/ALIEN/ALIEN", newKey = "alien")

camelDict = read_sm("data/Shape-Matcher-models/camel.xml")
t.rename_key(camelDict, oldKey = "models/camel/camel", newKey = "camel")

eagleDict = read_sm("data/Shape-Matcher-models/eagle.xml")
t.rename_key(eagleDict, oldKey = "models/eagle/eagle", newKey = "eagle")

kangaDict = read_sm("data/Shape-Matcher-models/KANGAROO.xml")
t.rename_key(kangaDict, oldKey = "models/KANGAROO/KANGAROO", newKey = "kangaroo")

# see data/DataCleaning.py for how we picked outliers
biasedAliens = ['alien67','alien0', 'alien1', 'alien2', 'alien4', 'alien5', 'alien6', 'alien9', 'alien16', 'alien18', 'alien19', 'alien27', 'alien28', 'alien30', 'alien31', 'alien32', 'alien33', 'alien34', 'alien36', 'alien37', 'alien38', 'alien39', 'alien40', 'alien41', 'alien43', 'alien44', 'alien45', 'alien48', 'alien55', 'alien57', 'alien58', 'alien66', 'alien68', 'alien69', 'alien70', 'alien71', 'alien72', 'alien73', 'alien75', 'alien76', 'alien77', 'alien78', 'alien80', 'alien87', 'alien89', 'alien90', 'alien98', 'alien99', 'alien101', 'alien102', 'alien103', 'alien105', 'alien106']
biasedCamels = ['camel0', 'camel1', 'camel4', 'camel5', 'camel6', 'camel16', 'camel18', 'camel19', 'camel24', 'camel28', 'camel30', 'camel31', 'camel32', 'camel33', 'camel34', 'camel36', 'camel37', 'camel38', 'camel39', 'camel48', 'camel51', 'camel60', 'camel62', 'camel63', 'camel64', 'camel67', 'camel76', 'camel78', 'camel79', 'camel80', 'camel81', 'camel82', 'camel84', 'camel85', 'camel86', 'camel89', 'camel96', 'camel97', 'camel98', 'camel99', 'camel107', 'camel108', 'camel109', 'camel110', 'camel111', 'camel112', 'camel113', 'camel114', 'camel116', 'camel117', 'camel118', 'camel121', 'camel123']
biasedEagles = ['eagle16', 'eagle21', 'eagle22', 'eagle30', 'eagle47', 'eagle53', 'eagle54', 'eagle68', 'eagle88', 'eagle89', 'eagle90', 'eagle92', 'eagle99', 'eagle106', 'eagle107', 'eagle127']
biasedKangas = ['kangaroo117','kangaroo5', 'kangaroo6', 'kangaroo7', 'kangaroo8', 'kangaroo13', 'kangaroo14', 'kangaroo15', 'kangaroo20', 'kangaroo21', 'kangaroo22', 'kangaroo23', 'kangaroo24', 'kangaroo29', 'kangaroo30', 'kangaroo31', 'kangaroo37', 'kangaroo38', 'kangaroo39', 'kangaroo40', 'kangaroo44', 'kangaroo45', 'kangaroo46', 'kangaroo47', 'kangaroo53', 'kangaroo54', 'kangaroo55', 'kangaroo56', 'kangaroo58', 'kangaroo59', 'kangaroo61', 'kangaroo62', 'kangaroo63', 'kangaroo69', 'kangaroo70', 'kangaroo71', 'kangaroo72', 'kangaroo77', 'kangaroo78', 'kangaroo79', 'kangaroo85', 'kangaroo86', 'kangaroo87', 'kangaroo88', 'kangaroo92', 'kangaroo93', 'kangaroo94', 'kangaroo95', 'kangaroo100', 'kangaroo101', 'kangaroo102', 'kangaroo103', 'kangaroo104', 'kangaroo109', 'kangaroo110', 'kangaroo111', 'kangaroo118', 'kangaroo119', 'kangaroo120', 'kangaroo124', 'kangaroo125', 'kangaroo126', 'kangaroo127', 'kangaroo132', 'kangaroo133', 'kangaroo134', 'kangaroo135', 'kangaroo136', 'kangaroo137', 'kangaroo138', 'kangaroo139', 'kangaroo141', 'kangaroo142', 'kangaroo143', 'kangaroo148', 'kangaroo149', 'kangaroo150', 'kangaroo151', 'kangaroo152', 'kangaroo153', 'kangaroo157', 'kangaroo158', 'kangaroo159']

dictList = [(alienDict, "alien", biasedAliens),
            (camelDict, "camel", biasedCamels),
            (eagleDict, "eagle", biasedEagles), 
            (kangaDict, "kangaroo", biasedKangas)]

inputs = []
target = []
labels = []

num = 20 # Number of graphs from each category
alpha = 0.6 #Translucency of the points
scheme = "jet" #Color mapping used for the plots' cluster color scheme
import time
total_time = 0
start = time.time()
for frame in [5, 20, 50, 100]: # number of frames used for average branching distance
    
    for Dict in dictList:
        tuples = Dict[0][Dict[1]] # List of (graph, posdict) tuples
        
        j = 0
        for i in range(num):
            while ( Dict[1] + str(j) ) in Dict[2]:
                j+=1
            if j > len(tuples)-1:
                break
        
            G = tuples[j][0]
            G = t.main_component(G = G, report = False)
            pos = tuples[j][1]
            inputs.append( (G, pos) )
            labels.append(Dict[1] + str(j))
            target.append(Dict[1])
            j += 1
    
    
    matrix = classify.get_matrix(inputs, frame, True, True, average = "median")
    ind = [5, 20, 50, 100].index(frame)    
    matrices[ind] = matrix # For you to reference later
    points = classify.mds(input_list = inputs,
                  target_list = target,
                  frames = frame,
                  D = matrix,
                  colorize = True,
                  scheme = scheme,
                  legend = True,
                  legend_position = "upper left",
                  alpha = alpha,
                  TIME = True)
total_time = (time.time() - start)
