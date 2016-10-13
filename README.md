# MGTrans
easy to use, safe to embed codes that transfer Matrix or Graph between different formats (such as MatrixMarket, METIS, ...) for c/c++, python and matlab language users.  
for Matrix file format transformation, please go to ./Matrix*/  
for Graph file format transformation, please go to ./Graph*/


####WE HAD TO (often)
transfrom our matrix/graph files to different formats to meet the requirment of variant Matrix Software, Libaray and Package (i.e. Matlab, Metis, PETSc, SNAP, LAPACK, MKL,...). We need a easy to use, safe to enbeded codes.


####Supported file format
* <a href="http://math.nist.gov/MatrixMarket/formats.html">Matrix Market</a>    mm
* <a href="http://people.sc.fsu.edu/~jburkardt/data/metis_graph/metis_graph.html">METIS</a>    metis


####To be supported file format
* matlab ascii
* matlab binary
* edge list
* PETSc binary


####Matrix v.s. Graph
The term graph within this project refers to "finite simple graph", know as "directed/undirected, no weight, no self loops, no muliple edges graph".
Even though all finite simple graph can directly be represent by a adjacency matrix (There are other ways, such as Laplacian Matrix). There are differences between the matrix and the graph. So we divide the transformationsinto two parts.
* Matrix
* Graph
for different users.

####USAGE:
check readme of sub-directory.


