from dimacs import loadDirectedWeightedGraph
from make_tests import generate_tests
import sys

INF = 1e12

class Vertex():
    def __init__(self):
        self.neigh = {}
        self.visited = False

# function takes 2 arguments
# n - number of vertexes
# edges - list of edges; 
# 3-element tuples (u, v, c), where:
# u, v - indexes of vertex
# c - weight of directed edge u -> v
# function returns list of Vertex objects
def generate_graph(n, edges):
    G = [Vertex() for _ in range(n)]

    for u, v, c in edges:
        G[u-1].neigh[v-1] = c
        G[v-1].neigh[u-1] = 0
    
    return G

# recursive function that takes 6 arguments
# G - list of Vertex() objects
# u - current vertex index
# sink - sink vertex index
# V - Visited list with size = len(G), indicates if Vertex were visited before
# path_edges - list that contains all edges travelled by function so far
# min_cap - minimal flow along all edges in path_edges, starting with extremely big value
# (so there won't be any edge with weight larger than this value)
# function returns 3 values
# if the path was found function is going to return
# found - bool - indicates if exists path from u to sink which every edge weight is > 0
# path_edges - list of edges of path u -> t
# min_cap - min weight of edges in path_edges
def find_open_path(G, u, sink, V, path_edges = [], min_cap = INF):
    V[u] = True                                                                 # set current vertex as visited
    if u != sink:   
        for v, c in G[u].neigh.items():
            if c != 0 and not V[v]:                                             # if edge from u to v exists and its capacity > 0 and v 
                                                                                # was not visited by function yet then visit the v vertex
                tmp_found, tmp_edges, tmp_min = find_open_path(G, v, sink, V,   
                    path_edges + [(u, v)], min(min_cap, G[u].neigh[v]))
                if tmp_found: return True, tmp_edges, tmp_min
        return [False]*3
    else:
        return True, path_edges, min_cap

# function takes 3 arguments
# G - list of Vertex() objects
# s - index of source vertex
# t - index of sink vertex
def maxFlow(G, s, t):
    max_capacity = 0
    found = True
    min_cap = 0
    e = []

    while found:                        # as long as path from s to t with min(C) exists / C - minimal flow along all edges in that path
        max_capacity += min_cap
        for u, v in e:
            G[u].neigh[v] -= min_cap    # send flow along the path
            G[v].neigh[u] += min_cap    # the flow might be "returned" later
        
        found, e, min_cap = find_open_path(G, s, t, [False]*len(G))
    
    return max_capacity

if __name__ == '__main__':
    sys.setrecursionlimit(10000)        # set size of maximum depth of Python interpreter stack
    tests = generate_tests('./graphs/flow')
    for test in tests:
        V, E = loadDirectedWeightedGraph('graphs/flow/' + test)

        G = generate_graph(V, E)
        print(test + ' : ' + str(maxFlow(G, 0, len(G)-1)))
