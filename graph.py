# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 20:06:37 2016

@author: makhloufi, lacroix
"""
import numpy as np
from edge import Edge
from ensemble_node import EnsembleNode
from queue import Queue, PriorityMinQueue
from node import Node
from stack import Stack


class Graph(object):
    """
    Une classe générique pour représenter un graphe comme un ensemble de
    noeuds et d'aretes.
    """

    def __init__(self, name='Sans nom'):
        self.__graph_name = name
        self.__nodes = []   # Attribut prive.
        self.__edges = []
        self.__adj_matrix = {}  # matrice d'adjacence
        self.__graph_weight = 0

    def add_node(self, node):
        """Ajouter un noeud au graphe et initialisé la matrice d'adjacence"""
        self.__nodes.append(node)
        self.__adj_matrix[node] = {}

    def add_edge(self, edge):
        "Ajout un edge au graphe et remplissage de adj_matrix"
        if (edge.edge_startnode != edge.edge_endnode):
            self.__adj_matrix[edge.edge_startnode][edge.edge_endnode] = edge
            self.__adj_matrix[edge.edge_endnode][edge.edge_startnode] = edge
            self.__edges.append(edge)
            # Update graph_weight attribute
            self.set_graph_weight(self.get_graph_weight() + edge.edge_cost)

    @property
    def graph_name(self):
        "Donne le nom du graphe."
        return self.__graph_name

    @graph_name.setter
    def graph_name(self, name):
        self.__graph_name = name

    @property
    def edges(self):
        "Donne la liste des aretes du graphe."
        return self.__edges

    @property
    def nodes(self):
        "Donne la liste des noeuds du graphe."
        return self.__nodes

    @nodes.setter
    def nodes(self, nodes):
        """"""
        self.__nodes = nodes
        for node in nodes:
            self.__adj_matrix[node] = {}

    @property
    def adj_matrix(self):
        return self.__adj_matrix

    def get_nb_edges(self):
        "Donne le nombre de noeuds du graphe."
        return (len(self.edges))

    def get_nb_nodes(self):
        "Donne le nombre de noeuds du graphe."
        return (len(self.nodes))

    def set_graph_weight(self, weight):
        self.__graph_weight = weight

    def get_graph_weight(self):
        return self.__graph_weight

    def get_edge(self, startnode, endnode):
        edge = self.adj_matrix.get(startnode).get(endnode)
        if edge == None:
            raise ValueError("Edge not found in Adj Matrix")
        else:
            return edge

    def __repr__(self):
        name = self.graph_name
        nb_nodes = self.get_nb_nodes()
        s = 'Graphe %s comprenant %d noeuds' % (name, nb_nodes)
        for node in self.nodes:
            s += '\n  ' + repr(node)
        for edge in self.edges:
            s += '\n  ' + repr(edge) + '\n  '
        s += "Matrice d'adjacence \n"
        s += str(self.adj_matrix)
        return s

    def reset_visited_nodes(self):
        for node in self.nodes:
            node.visited = False

    def plot_graph(self):
        """
        Plot the graph represented by `nodes` and `edges` using Matplotlib.
        Very basic for now.
        """
        import matplotlib.pyplot as plt
        from matplotlib.collections import LineCollection

        fig = plt.figure()
        ax = fig.add_subplot(111)
        x = [int(node.node_data[0]) for node in self.__nodes]  # liste abs
        y = [int(node.node_data[1]) for node in self.__nodes]  # liste ord

        # Plot edges.
        edge_pos = np.asarray([(e.edge_startnode.node_data, e.edge_endnode.node_data
                                ) for e in self.edges])

        edge_collection = LineCollection(edge_pos, linewidth=1.5,
                                         antialiased=True, colors=(.8, .8, .8),
                                         alpha=.75, zorder=0)

        ax.add_collection(edge_collection)
        ax.scatter(x, y, s=35, c='r', antialiased=True, alpha=.75, zorder=1)
        ax.set_xlim(min(x) - 10, max(x) + 10)
        ax.set_ylim(min(y) - 10, max(y) + 10)
        plt.show()
        return

    def kruskal(self):
        """
        Kruskal algo: this function returns a graph composed with
        Node Object that is the minimal weight spanning tree of the graph.
        """

        nb_noeuds = self.get_nb_nodes()
        spanning_tree = Graph(name=self.graph_name + " spanning tree")

        # function used to sort the list of edges
        def getKey(edge):
            return edge.edge_cost

        # construct a list containing EnsembleNode nodes (constructed from the
        # graph nodes) and a list containing edges between these ensemble nodes
        ensemble_nodes = [EnsembleNode(
            name=node.node_name, data=node.node_data,
            father=None, original_node=node) for node in self.nodes]
        ensemble_edges = [Edge(
            name=edge.edge_name, data=edge.edge_data, cost=edge.edge_cost,
            startnode=ensemble_nodes[self.nodes.index(edge.edge_startnode)],
            endnode=ensemble_nodes[self.nodes.index(edge.edge_endnode)]) for edge in self.edges]

        # set spanning_tree nodes list
        spanning_tree.nodes = self.nodes

        # sort list of edges between ensemble nodes
        sorted_edges = sorted(ensemble_edges, key=getKey)

        n_edge_added = 0
        # Explore sorted edges list
        for edge in sorted_edges:
            # stopping condition of the algorithm
            if n_edge_added == nb_noeuds-1:
                break

            # test whether the 2 nodes connected by the edges
            # belong to the same connected ensembles
            if edge.edge_startnode.get_root_and_compress() != edge.edge_endnode.get_root_and_compress():
                startnode = edge.edge_startnode
                endnode = edge.edge_endnode
                spanning_tree.add_edge(self.get_edge(startnode.original_node, endnode.original_node))
                startnode.rank_union(endnode)
                n_edge_added += 1

        return spanning_tree

    def prim(self, root):
        """
        Prim algo: this function returns a graph composed with
        Node objects that is the minimal weight spanning tree
        of the graph computed by Prim algorithm.
        """

        spanning_tree = Graph(name=self.graph_name + " Prim algo ST")
        spanning_tree.nodes = self.nodes

        # Init of algorithm data structures: queue containing EnsembleNode
        # nodes
        nodes_queue = PriorityMinQueue()

        # Fill nodes_queue with EnsembleNode objects and
        # add corresponding entries in ensnode_to_node
        for node in self.nodes[:]:
            ensemble_node = EnsembleNode(name=node.node_name,
                                        data=node.node_data,
                                        min_weight=float('inf'),
                                        original_node=node)
            if node == root:
                ensemble_node.min_weight = 0
            nodes_queue.enqueue(ensemble_node)

        # Dequeuing nodes in nodes_queue until queue is empty
        while not nodes_queue.is_empty():
            ens_n = nodes_queue.dequeue()
            n = ens_n.original_node  # n is the corresponding Node object

            # If ens_n has no father: this is first node to be chosen and there
            # is no edge to add to spanning tree
            if not ens_n.is_root():
                edge_to_add = self.get_edge(n, ens_n.father.original_node)
                spanning_tree.add_edge(edge_to_add)

            # Explore n neighbors
            for u in self.adj_matrix[n].keys():
                # Explore nodes_queue.items until we find corresponding EnsNode
                for t in nodes_queue.items:
                    if (t.original_node == u) &\
                            (self.get_edge(n, u).edge_cost < t.min_weight):

                        # t is now EnsembleNode corresponding to u
                        adj_edge = self.get_edge(n, u)
                        t.father = ens_n
                        t.min_weight = adj_edge.edge_cost
                        break

        return spanning_tree

    def dfs(self, root):
            """
            Depth first search algorithm
            returns a sorted list of Node Object visited
            during Depth First Search
            """

            visited_nodes = []
            pile = Stack()
            pile.push(root)
            neighbor = None

            while not pile.is_empty():
                u = pile.pop()
                if not u.visited:
                    visited_nodes.append(u)
                    u.visited = True
                for neighbor in self.adj_matrix[u].keys():
                    if not neighbor.visited:
                        pile.push(neighbor)

            self.reset_visited_nodes()  # Reset modifs made on graph nodes
            return visited_nodes

    def rsl(self, root, st_algo):

        if st_algo == "prim":
            G_st = self.prim(root)

        elif st_algo == "kruskal":
            G_st = self.kruskal()
        else:
            raise ValueError("Unrecognized Spanning Tree algorithm")

        # Instantiate Graph corresponding Hamiltonian cycle
        st_dfs_nodes = G_st.dfs(root)
        ham_cycle = Graph(self.graph_name + " Hamiltonian Cycle")
        ham_cycle.nodes = self.nodes

        # Add edges between sequential nodes in st_dfs_nodes to ham_cycle
        for i in range(len(st_dfs_nodes)-1):
            edge_to_add = self.get_edge(st_dfs_nodes[i], st_dfs_nodes[i+1])
            ham_cycle.add_edge(edge_to_add)

        # Add last edge to ham_cycle
        last_edge = self.get_edge(st_dfs_nodes[-1], st_dfs_nodes[0])
        ham_cycle.add_edge(last_edge)

        return ham_cycle

if __name__ == '__main__':

    G = Graph(name='Graphe test')
    for k in range(5):
        G.add_node(Node(name='Noeud test %d' % k))
    for k in range(5):
        G.add_edge(Edge(name='Edge test %d' % k, cost=(10-k)))

    print "liste non trié"
    print G.edges[0]
