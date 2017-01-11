# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 20:04:50 2016

@author: makhloufi, lacroix
"""

from graph import Graph
from edge import Edge
from node import Node
from read_stsp import *
import sys

# optimal distances
opt_dist = {'bayg29': 1610, 'bays29': 2020, 'brazil58': 25395,
             'brg180': 1950, 'dantzig42': 699, 'fri26': 937, 'gr17': 2085,
             'gr21': 2707, 'gr24': 1272, 'gr48': 5046, 'gr120': 6942,
             'hk48': 11461, 'pa561': 2763, 'swiss42': 1273}
st_algo_list = ["kruskal", "prim"]


def construct_graph(file):
    """
    This function constructs a graph defined in an stsp instance file
    and bypasses the problem of 0-length nodes set returned
    by the read_node function for some stsp instances
    """

    finstance = file

    with open(finstance, "r") as fd:

        header = read_header(fd)
        dim = header['DIMENSION']
        name = header['NAME']
        G = Graph(name=name)

        nodes = read_nodes(header, fd)
        if nodes:
            for n in range(len(nodes)):
                G.add_node(Node(data=nodes[n]))
        else:
            for n in range(dim):
                G.add_node(Node())

        edges = read_edges(header, fd)
        for e in edges:
            G.add_edge(Edge(startnode=G.nodes[int(e[0])],
                            endnode=G.nodes[int(e[1])], cost=e[2]))

    return G


def plot_cycle(best_cycle, st_algo, cle):
    print("Best cycle found for Instance " + best_cycle.graph_name + " : ")
    print("Spanning Tree Algorithm : " + st_algo)
    print("Root : ")
    print(root_plot)
    print("Weight : " + str(best_cycle.get_graph_weight()))
    print("Optimal Hamilton cycle W : " + str(opt_dist[best_cycle.graph_name]))
    print("Gap : +" + str(best_cycle.get_graph_weight()-opt_dist[cle]) + "\n")
    best_cycle.plot_graph()

#Code de test pour le TP3
# Construct and print example Graph
# G = construct_graph(sys.argv[1])
# construct G minimal weight spanning tree, plot it and print its weight
# G_spanning_tree = G.kruskal()
# G_spanning_tree = G.prim(G.nodes[0])
# print("MST weight of graph is " + str(G_spanning_tree.get_graph_weight()))
# G.plot_graph()
# G_spanning_tree.plot_graph()

# Code de test pour le TP4
# result file
rf = open('resultfile', 'w')

# the structure of the file  we use | as a a delimiter
s = "INSTANCE_NAME|ROOT_CORDINATES|PRIM_SOL|GAP_Prim |KRUSKAL_SOL|GAP_KRUSKAL|OPTIMAL_SOL\n"
rf.write(s)

# We can give one or all the tsp files in arguments
for i in range(1, len(sys.argv)):
    graph = construct_graph(sys.argv[i])
    cle = graph.graph_name.strip()
    root_plot = None
    best_gap = 1000000
    best_cycle = None
    best_st_algo = None

    for root in graph.nodes:
        s = graph.graph_name + "|" + repr(root)
        for st_algo in st_algo_list:
            cycle = graph.rsl(root, st_algo)
            gap = cycle.get_graph_weight() - opt_dist[cle]
            if gap < best_gap:
                best_cycle = cycle
                root_plot = root
                best_cycle.graph_name = graph.graph_name
                best_gap = gap
                best_st_algo = st_algo
            s += "|" + str(cycle.get_graph_weight())+"|"+str(gap)
        s += "|" + str(opt_dist[cle])+"\n"
        rf.write(s)

    plot_cycle(best_cycle, best_st_algo, cle)
