We had to (often) transform our matrix/graph files to variants formats to meet the research purposes or softwares/libraries/packages (i.e. <a href="https://en.wikipedia.org/wiki/MATLAB">Matlab</a>, <a href="http://glaros.dtc.umn.edu/gkhome/metis/metis/overview">METIS</a>, <a href="http://www.netlib.org/lapack/">LAPACK</a>, <a href="https://software.intel.com/en-us/intel-mkl">MKL</a>, <a href="https://www.mcs.anl.gov/petsc/">PETSc</a>, <a href="https://snap.stanford.edu/">SNAP</a>,<a href="https://networkit.iti.kit.edu/">NetworKit</a> ...) requirements. We need some easy to use, safe to embed codes.

#### MGTrans
MGTrans provides easy to use, safe to embed codes that transfer Matrix or Graph between different formats for *c/c++*, *python* and *matlab* language users.  
* for Matrix file format transformation, please go to ./Matrix*/ 
* for Graph file format transformation, please go to ./Graph*/


#### Supported file format
* mm ------- <a href="http://math.nist.gov/MatrixMarket/formats.html">Matrix Market</a>  
* metis ---- <a href="http://people.sc.fsu.edu/~jburkardt/data/metis_graph/metis_graph.html">METIS</a> 


#### To be supported file format
* matlab ASCII
* matlab binary
* edge list
* PETSc binary

#### Matrix v.s. Graph
The term **graph** within this project refers to the **"finite simple graph"**, know as "directed or undirected, no weight, no self loops, no multiple edges graph".  

Even though all finite simple graph can directly be represent by a adjacency matrix (There are other ways, such as Laplacian Matrix). There are differences between the matrix and the graph. So we divide the transformationsinto two parts.
  * Matrix
  * Graph

for different users.


#### Miscellaneous 
METIS format only support undirected graphs. <a href="http://glaros.dtc.umn.edu/gkhome/metis/metis/faq">How can I partition directed graphs?</a>




#### USAGE:
check the readme of each sub-directory.


