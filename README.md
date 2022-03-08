
# Comparing Embedded Graphs
<!-- title -->
Geospatial data is readily available but often noisy and inaccurate. 
In the field of map reconstruction, there is a need to be able to quantitatively compare maps in order to evaluate specific methods and data sources
for reconstruction. 
We aim to do so by comparing corresponding merge trees of embedded graphs representing road networks.
  
We provide:
- A merge tree construction algorithm
- An implementation of a merge tree comparison algorithm suggested by [Beketayev et al.](https://link.springer.com/chapter/10.1007%2F978-3-319-04099-8_10 "Measuring the Distance Between Merge Trees"), which we call *branching distance*
- A graph comparison algorithm for a new distance function called *average branching distance*
- Methods for visualizing the results of graph comparisons  
  
and some assisting methods, all implemented in Python 3.7.6.
<!-- Methods for converting different data formats into NetworkX graph objects? -->

## Dependencies
The programs in this repository require the following Python libraries:

- SciPy  
- NumPy  
- scikit-learn  
- Matplotlib  
- NetworkX*
- MoviePy
- threading 
- concurrent.futures
- itertools
- multiprocessing
- os
- glob
- time  
- math  
- time
- random
- statistics

## Usage
To access everything, it is easiest to clone the whole repo and run [Main.py](https://github.com/lizliz/SURIEM2020-EmbeddedGraphs/blob/master/Main.py "Main.py script").   
  
Some sample data and binary images are included in the /data and /images directories respectively, but nothing in either directory is required for any program functionality. 
Both directories contain .txt files listing the sources for their contents.

To use these programs on your own data, first [convert your data into a NetworkX graph object](https://networkx.github.io/documentation/stable/reference/readwrite/index.html) whose nodes all have a least two attributes (typically representing cartesian coordinate positions). Note that many of NetworkX's built in methods for graph conversion do not preserve node attributes. For help on how to assign node attributes, see [NetworkX's tutorial for node attributes](https://networkx.github.io/documentation/networkx-1.10/tutorial/tutorial.html#adding-attributes-to-graphs-nodes-and-edges "NetworkX Tutorial: Adding attributes to graphs, nodes, and edges").  
  
Alternatively, we provide attribute-preserving methods for converting GraphML, GeoJSON, PPM, and XML* files into NetworkX Graph objects. For convenience, these conversion methods are consolidated in [DataReader.py](https://github.com/lizliz/SURIEM2020-EmbeddedGraphs/blob/master/DataReader.py "DataReader.py script"). For detailed documentation on individual functions, see their respective scripts in the /lib directory.
  
- To **prepare a graph for merge tree construction**, see the `calc_values_height_reorient` function in [Merge.py](https://github.com/lizliz/SURIEM2020-EmbeddedGraphs/blob/master/Merge.py "Merge.py script")
- To **construct a merge tree** of a graph, see the `merge_tree` function in [Merge.py](https://github.com/lizliz/SURIEM2020-EmbeddedGraphs/blob/master/Merge.py "Merge.py script").  
- To determine if two merge trees are ![](http://latex.codecogs.com/gif.latex?%5Cvarepsilon) **-similar** as defined by Beketayevet al., see the `IsEpsSimilar` function in [Compare.py](https://github.com/lizliz/SURIEM2020-EmbeddedGraphs/blob/master/Compare.py "Compare.py script").
- To compute the **branching distance** between two merge trees, see the `branching_distance` function in [Compare.py](https://github.com/lizliz/SURIEM2020-EmbeddedGraphs/blob/master/Compare.py "Compare.py script")
- To compute the **average branching distance** (ABD) between two graphs, see the `average_distance` function in [DataCalculations.py](https://github.com/lizliz/SURIEM2020-EmbeddedGraphs/blob/master/DataCalculations.py "DataCalculations.py Script")  
- To **construct a distance matrix** of pairwise ABDs, see the `get_matrix` function in [Classify.py](https://github.com/lizliz/SURIEM2020-EmbeddedGraphs/blob/master/Classify.py  "Classify.py script")    
- To visualize the **hierarchical clusters** in a condensed distance matrix of pairwise ABDs, see the `draw_dendro` function in [Classify.py](https://github.com/lizliz/SURIEM2020-EmbeddedGraphs/blob/master/Classify.py  "Classify.py script")   
- To visualize the results of **multi-dimensional scaling** on a distance matrix of pairwise ABDs, see the `mds` function in [Classify.py](https://github.com/lizliz/SURIEM2020-EmbeddedGraphs/blob/master/Classify.py  "Classify.py script")   
- To recreate the plots in the paper associated with this project, run [Plots.py](https://github.com/lizliz/SURIEM2020-EmbeddedGraphs/blob/master/Plots.py "Plots.py script") (this will take several hours to finish running)
- To create other various visualizations, like some of the plots seen in [our paper](https://github.com/lizliz/SURIEM2020-EmbeddedGraphs/blob/master/Comparing%20Embedded%20Graphs%20Using%20Average%20Branching%20Distance.pdf), see [Visualization.py](https://github.com/lizliz/SURIEM2020-EmbeddedGraphs/blob/master/Visualization.py "Visualization.py scripts")

Details on how to use these and other functions, including explanations of parameters and outputs, are included within respective scripts as comments.  
  
Should you use the source code from this repository, please cite [the following paper](https://github.com/lizliz/SURIEM2020-EmbeddedGraphs/blob/master/Comparing%20Embedded%20Graphs%20Using%20Average%20Branching%20Distance.pdf):  

```
@unpublished{embedded_graphs_suriem2020,
author = "Batakci, Levent
and Branson, Abigail
and Castillo, Bryan
and Chambers, Erin W.
and Munch, Elizabeth
and Todd, Candace",
title = "Comparing Embedded Graphs Using Average Branching Distance",
note = "Unpublished"
}
```

Should you use any of the data in this repository or the ShapeMatcher program, please cite their original sources as listed in /images/Image Sources.txt and /data/Data Sources.txt.

## Credits
This repository contains work done by the Embedded Graphs group under [Dr. Elizabeth Munch](https://www.linkedin.com/in/elizabethmunch/ "Elizabeth Munch's LinkedIn Profile") and [Dr. Erin Chambers](https://www.linkedin.com/in/erin-wolf-chambers-836a37/ "Erin Wolf Chambers' LinkedIn Profile") during the 8-week SURIEM REU hosted by Michigan State in the summer of 2020. 
Members of this group include [Levent Batakci](https://www.linkedin.com/in/levent-batakci-306a31190/ "Levent Batakci's LinkedIn Profile"), [Abigail Branson](https://www.linkedin.com/in/abigail-branson-466128180/ "Abigail Branson's LinkedIn Profile"), [Bryan Castillo](https://www.linkedin.com/in/bryan-castillo-7a12651ab/ "Bryan Castillo's LinkedIn Profile"), and [Candace Todd](https://www.linkedin.com/in/candace-todd "Candace Todd's LinkedIn Profile").
  
The funding for the project associated with this repository was supported by the National Science Foundation (NSF Award No. 1852066), the National Security Agency (NSA Grant No. H98230-20-1-0006), and Michigan State University. 
The work of Erin Chambers was supported in part by NSF grants CCF-1614562, CCF-1907612, and DBI-
1759807. The work of Elizabeth Munch was supported in part by NSF grants CCF-1907591 and DEB-
1904267.
  
---
\*All programs and most of their in-script documentation rely on a basic understand of NetworkX Graph objects. See [NetworkX's tutorial](https://networkx.github.io/documentation/stable/tutorial.html "NetworkX Tutorial").  
\*\* Only supports XML files as exported from [OpenStreetMap.org](https://www.openstreetmap.org/export#map=15/37.9966/23.7486 "OpenStreetMap.org") (`read_osm`) or the [ShapeMatcher6.0.1beta](http://www.cs.toronto.edu/~dmac/ShapeMatcher) program (`read_sm`)
