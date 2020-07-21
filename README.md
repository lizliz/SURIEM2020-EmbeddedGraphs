# Comparing Embedded Graphs
<!-- title -->
Geospatial data is readily available but often noisy and inaccurate. 
In the field of map reconstruction, there is a need to be able to quantitatively compare maps in order to evaluate specific methods and data sources
for reconstruction. 
We aim to do so by comparing corresponding merge trees of embedded graphs representing road networks.
  
We provide:
- A merge tree construction algorithm
- An implementation of a merge tree comparison comparison algorithm suggested by [Beketavey et al.](https://link.springer.com/chapter/10.1007%2F978-3-319-04099-8_10 "Measuring the Distance Between Merge Trees"), which we call *branching distance*
- A graph comparison algorithm for a new distance function called *average branching distance*
- Methods for visualizing the results of graph comparisons  
  
All implemented in Python 3.7.6.
<!-- Methods for converting different data formats into NetworkX graph objects? -->

<!--## Using this repository
Should you use the source code and/or data from this site, please cite also the following paper? -->

## Dependencies
The programs in this repository require the following Python libraries:

- SciPy  
- NumPy  
- scikit-learn  
- Matplotlib  
- NetworkX
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
To access all functions, download and run Main.py.  
To recreate the plots in the paper associated with this project, run Plots.py     

To use these programs on your own data, first [convert your data into a NetworkX graph object](https://networkx.github.io/documentation/stable/reference/readwrite/index.html) whose nodes all have a least two attributes (typically representing cartesian coordinate positions). Note that many of NetworkX's built in methods for graph conversion do not preserve node attributes. For help on how to assign node attributes, see [NetworkX's tutorial for node attributes](https://networkx.github.io/documentation/networkx-1.10/tutorial/tutorial.html#adding-attributes-to-graphs-nodes-and-edges "NetworkX Tutorial: Adding attributes to graphs, nodes, and edges"). Alternatively, we provide attribute-preserving methods for converting GraphML, GeoJSON, and PPM files, as well as XML files exported from [OpenStreetMap](https://www.openstreetmap.org/export#map=15/37.9966/23.7486 "OpenStreetMap.org"), and XML files created by [ShapeMatcher6.0.1beta](http://www.cs.toronto.edu/~dmac/ShapeMatcher) into NetworkX Graph objects.

- To **prepare a graph for merge tree construction**, see the `calc_values_height_reorient` function in Mere.py
- To **construct a merge tree** of a graph, see the `merge_tree` function in Merge.py.  
- To determine if two merge trees are 
$\epsilon$ $\varepsilon$ $**\epsilon-similar**$
as defined by Beketayevet al., see the `IsEpsSimilar` function in Compare.py.
- To compute the **branching distance** between two merge trees, see the `branching_distance` function in Compare.py  
- To compute the **average branching distance** (ABD) between two graphs, see the `average_distance` function in DataCalculations.py  
- To **construct a distance matrix** of pairwise ABDs, see the `get_matrix` function in Classify.py  
- To visualize the **hierarchical clusters** in a condensed distance matrix of pairwise ABDs, see the `draw_dendro` function in Classify.py  
- To visualize the results of **multi-dimensional scaling** on a distance matrix of pairwise ABS, see the `mds` function in Classify.py  
  
Details on how to use these and other functions, including explanations of parameters and outputs, are included within respective scripts as comments.  
All programs and most of their in-script documentation rely on a basic understand of NetworkX Graph objects. See [NetworkX's tutorial](https://networkx.github.io/documentation/stable/tutorial.html "NetworkX Tutorial").

## Credits
This repository contains work done by the Embedded Graphs group under Dr. Elizabeth Munch and Dr. Erin Chambers during the SURIEM REU in the summer of 2020. 
Members of this group include Levent Batakci, Abigail Branson, Bryan Castillo, and ([Candace Todd](https://www.linkedin.com/in/candace-todd "Candace Todd's LinkedIn Profile"), [Candace Todd](https://github.com/CLTodd "Candace Todd's GitHub Profile"), or [Candace Todd](mailto:clt5441@psu.edu)).
<!-- list our institution? linkedin? -->

The funding for the project associated with this repository was supported by the National Science Foundation (NSF Award No. 1852066), the National Security Agency (NSA Grant No. H98230-20-1-0006), and Michigan State University. 
The work of Erin Chambers was supported in part by NSF grants CCF-1614562, CCF-1907612, and DBI-
1759807. The work of Elizabeth Munch was supported in part by NSF grants CCF-1907591 and DEB-
1904267.

<!-- ShapeMatcher -->
<!-- data sources -->
