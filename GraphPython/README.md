Welcome! this is a python program to transfer graph format between 
* mm ------ matrix market
* metis --- metis
* ..[TODO] other formats

more details please send visit us at https://github.com/ProbShin/MGTrans

#### USAGE ####
There are two ways:  
<pre>
GTrans.py &lt;input_graph_name> &lt;output_graph_name>   
GTrans.py &lt;detailed inputgraph information> &lt;detailed outputgraph info>
</pre>

#### Examples ####
<pre>
$python3 GTrans.py foo.mtx bar.graph
$python3 GTrans.py foo.mtx mm bar.graph metis
$python3 GTrans.py --input foo.mtx --intype mm --output bar.graph --outtype metis
$python3 GTrans.py -i foo.mtx -s mm -o bar.graph -t metis
</pre>

#### Help ####
<pre>
$python3 GTrans.py --help
$python3 GTrans.py -h
</pre>
