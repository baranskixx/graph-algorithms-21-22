from dimacs import loadDirectedWeightedGraph
from make_tests import generate_tests
import sys

INF = 1e12

# function returns list of n lists, each with n int elements
# G[x][y] - weight of edge x -> y
def generate_graph(n, edges):
    G = [[0]*n for _ in range(n)]

    for u, v, c in edges:
        G[u-1][v-1] = c
    
    return G
# recursive function that takes 6 arguments
# G - matrix represented graph
# u - current vertex index
# sink - sink vertex index
# V - Visited list with size = len(G), indicates if vertexes were visited before
# path_edges - list that contains all edges travelled by function so far
# min_cap - minimal flow along all edges in path_edges
def find_open_path(G, u, sink, V, path_edges = [], min_cap = INF):
    V[u] = True
    if u != sink:
        for v in range(len(G)):
            if G[u][v] != 0 and not V[v]:
                tmp_found, tmp_edges, tmp_min = find_open_path(G, v, sink, V, path_edges + [(u, v)], min(min_cap, G[u][v]))
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

    while found:
        max_capacity += min_cap
        for u, v in e:
            G[u][v] -= min_cap
            G[v][u] += min_cap
        
        found, e, min_cap = find_open_path(G, s, t, [False]*len(G))
    
    return max_capacity

if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    tests = generate_tests('./graphs/flow')        # set size of maximum depth of Python interpreter stack
    for test in tests:
        V, E = loadDirectedWeightedGraph('graphs/flow/' + test)

        G = generate_graph(V, E)
        print(test + ' : ' + str(maxFlow(G, 0, len(G)-1)))
