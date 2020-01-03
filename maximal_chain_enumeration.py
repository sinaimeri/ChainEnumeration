#################################################################################
#           Enumerates all the maximal chains of a given bipartite graph        #
#################################################################################
import sys
import itertools
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.layout import bipartite_layout
import random
import scipy
import matplotlib.backends.backend_pdf
from matplotlib.figure import Figure
from numpy import genfromtxt
import csv


def usage():
    print("USAGE: ")
    print("Please provide the adjacency matrix of the bipartite graph as an csv file. ")
    sys.exit(1)



####################  Find Candidate    #########################################
##given sets U and W, for each maximal neighbourhood Y of W, returns a unique node u, called candidate, for which N_G(u) = Y.
def computeCandidates(G,U,W):

    n=len(U)
    possibleCandidates=[1 for i in range(n)] ## initailly all nodes are possible candidates
    Candidates=[]
    for i in range(n-1):
       # print("vertice:",U[i])
        if (possibleCandidates[i]==1):
            Neighbors_i=set(G.neighbors(U[i]))
            j=i+1
            #maximal is a boolean variable used to get out the cycle when i is not maximal anymore
            maximal=1
            while((j<n)&(maximal)):
                if (possibleCandidates[j]==1):
                    Neighbors_j=set(G.neighbors(U[j]))
                    #f N(i) is equal to N(j) then we choose the vertex of  larger label
                    if (Neighbors_i==Neighbors_j):
                        possibleCandidates[i]=0
                        maximal=0
                    #if N(i) is included in N(j) then i is not maximal
                    elif Neighbors_i.issubset(Neighbors_j):
                        possibleCandidates[i]=0
                        maximal=0
                    #if N(j) is included in N(i) then j is not maximal
                    elif Neighbors_j.issubset(Neighbors_i):
                        possibleCandidates[j]=0
                j=j+1
    #adds all the nodes that can be candidates to the list Candidates
    for i in range(n):
        if (possibleCandidates[i])==1:
            Candidates.append(U[i])
           # print("nodo in questione",U[i])
            
    return Candidates



def eumerate_maximal_chains(G,U,W,C,list_of_chains):
    
    # C is a list of edges
    #the function extracts a single vertex for each maximal neighborhood, in case of twins it extracts the node with the smallest label
    Candidates=computeCandidates(G,U,W)
    
    if not Candidates:
        CG=nx.Graph(C)
        CG.add_nodes_from(V_1+V_2)
        list_of_chains.append(CG)
        return
    
    else:
        for u in Candidates:
            U_1=list(U).copy()
            U_1.remove(u)
            
            Neighbors_u=G.neighbors(u)
            W_1=list(set(W) & set(Neighbors_u))
            
            # F_u contains all the edges in G of the form (u,w) with w in W_1
            F_u=[]
            for w in W_1:
                F_u.append((u,w))
                
            
            C_1=C.copy()
            C_1=C_1+F_u
            
            # recursive call on the subgraph induced by U_1 + W_1
            G_1=G.subgraph(U_1+W_1)
            eumerate_maximal_chains(G_1,U_1,W_1,C_1,list_of_chains)
    return



#################################################################################
#                                          MAIN                                 #
#################################################################################


arguments = sys.argv[1:]

if len(arguments)!=1:
    usage()

# Load the adjacency matrix into a numpy array.
filename = sys.argv[1]
V_1=list()
V_2=list()
Edges=list()

with open(filename) as fp:
    line=csv.reader(fp,delimiter=' ')
    line_count=0
    for line in fp:
        line = line.strip() # remove \n from the last element
        if (line_count==0):
        #read the vertices of the right side
            li=line.split(' ')
            #print("linea",li)
            V_1=li
            print("vertices in V1 are:",V_1)
            line_count=line_count+1
        else: # we are reading the matrix now
            line = line.strip() # remove \n from the last element
            li=line.split(' ')
            V_2.append(li[0]) # the first position of the row is the name of the node
            # add the edges for the node in the row position at line_count
            for i in range(1,len(V_1)+1,1):
                if (int(li[i])==1):
                    Edges.append((V_1[i-1],V_2[line_count-1]))
                
            line_count=line_count+1
    print("vertices in V2 are:",V_2)
    print("edges are are:",Edges)
        

# Create a Graph object (from the networkx library).
G = nx.Graph()
G.add_nodes_from(V_1, bipartite=0)
G.add_nodes_from(V_2, bipartite=1)
G.add_edges_from(Edges)

# Create the list of graphs for plotting
list_of_chains=[G]
# C = set of edges of the current chain subgraph
C=[]
eumerate_maximal_chains(G,V_1,V_2,C,list_of_chains)
#### drawing the graphs
N=len(list_of_chains)
print("number of chains: ",N)
pdf = matplotlib.backends.backend_pdf.PdfPages("output.pdf")
for i in range(N):
    fig=plt.figure()
    fig=nx.draw_networkx(list_of_chains[i],node_size=1,font_size=8,pos = nx.drawing.layout.bipartite_layout(list_of_chains[i],V_1) )
    pdf.savefig( fig )
pdf.close()

