"""Main TSP hook."""

from tsp_helper import get_distance
from graph import Graph
from node import Node
from edge import Edge


def get_visit_order(geoPoints):
    """THIS IS THE ONLY FUNCTION THAT YOU NEED TO MODIFY FOR PHASE 5.

    The only argument, *geoPoints*, is a list of points that user has marked.
    Each element of geoPoints is an instance of the GeoPoint class. You need to
    create your graph using these points. You obtain the distance between two
    points by calling the *getDistance* function; for example:

    get_distance(geoPoints[0], geoPoints[1])

    Run your tsp solver and return the locations visit order. The return value,
    *order*, must be a list of indices of points, specifying the visit order.

    In the example implementation below, we visit each point by the order
    in which they were marked (clicked).
    """

    nMarks = len(geoPoints)
    customGraph = Graph(name="Custom graph made with Google Maps points")

    # A\ Construct Graph object based on GeoPoints objects and distances
    for i in range(len(geoPoints)):
        name = str(i) + "th Node"
        node = Node(name=name, data=(geoPoints[i].lat * 10000, geoPoints[i].lng * 10000))
        customGraph.add_node(node)

        # Add edges between this node and previsously contructed Nodes
        nodeB = node
        for j in range(i):
            nodeA = customGraph.nodes[j]
            cost = get_distance(geoPoints[j], geoPoints[i])
            edge = Edge(startnode=nodeA, endnode=nodeB, cost=cost)
            customGraph.add_edge(edge)

    # B\ Run TSP code with all combinations of (root_node, st_algo) to compute
    # best Hamiltonian Cycle found and load result into result file

    rf = open('resultfile', 'ab')
    # s = "BEST_ROOT_CORDINATES.LAT|BEST_ROOT_CORDINATES.LNG|BEST_ST_ALGO|OPTIMAL_SOL\n"
    # rf.write(s)

    st_algo_list = ["kruskal", "prim"]
    best_weight = float('inf')
    best_cycle = None
    best_root = None
    best_st_algo = None
    for root in customGraph.nodes:
        for st_algo in st_algo_list:
            cycle = customGraph.rsl(root, st_algo)
            weight = cycle.get_graph_weight()
            if weight < best_weight:
                best_cycle = cycle
                best_weight = weight
                best_root = root
                best_st_algo = st_algo

    print("Best cycle found length: " + str(best_weight))
    s = str(best_root.node_data[0]/10000) + "|"
    s += str(best_root.node_data[1]/10000) + "|" + best_st_algo + "|"
    s += str(weight) + "\n"
    rf.write(s)
    rf.close()

    # C\ Compute GeoPoint order corresponding to the best Hamilton Cycle found
    dfs_nodes = best_cycle.dfs(best_root)
    order = [customGraph.nodes.index(node) for node in dfs_nodes]
    order = order + [order[0]]

    return order
