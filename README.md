# ChainEnumeration
Maximal Chain Enumeration in Bipartite Graphs

The input is a CI matrix in cv form. The rows correspond to the male individuals and the columns to the females. A value 0 in the cell [i,j] indicates that there is no incompatibility in the cross between male i and female j. 

The program constructs the Bipartite Graph, G,  corresponding to the matrix in input. It produces a pdf file containing as first page the orginal bipartite graph G, and in each page a maximal chain of G. A chain graph will correspond to 1 pair of Toxin\Antitoxin. 

To learn more about the combinatorial properties of chain graphs we refer to
http://www.graphclasses.org/classes/gc_442.html

