from dimacs import loadDirectedWeightedGraph
from make_tests import generate_tests
import sys
from collections import deque

INF = 1e12

class Vertex():
    def __init__(self):
        self.neigh = {}
        self.visited = False
        self.parent = None

def generate_graph(n, edges):
    G = [Vertex() for _ in range(n)]

    for u, v, c in edges:
        G[u-1].neigh[v-1] = c
        G[v-1].neigh[u-1] = 0
    
    return G

def max_flow(G, s, t):
    flow = 0
    open_path_found = True
    
    while open_path_found:
        for v in G:
            v.visited = False
            v.parent = None
        
        Q = deque()
        Q.appendleft((s, None, INF))

        while len(Q) != 0:
            u, parent, min_cap = Q.pop()
            # print(u, parent, min_cap)
            if not G[u].visited:
                G[u].parent = parent
                G[u].visited = True

                if u == t:
                    break

                for v, c in G[u].neigh.items():
                    if c > 0 and not G[v].visited:
                        Q.appendleft((v, u, min(c, min_cap)))
        
        if u != t:
            open_path_found = False
        else:
            flow += min_cap
            while u != s:
                p = G[u].parent
                G[u].neigh[p] += min_cap
                G[p].neigh[u] -= min_cap

                u = p
    
    return flow

    
if __name__ == '__main__':
    sys.setrecursionlimit(10000)        # set size of maximum depth of Python interpreter stack
    tests = generate_tests('./graphs/flow')
    for test in tests:
        V, E = loadDirectedWeightedGraph('graphs/flow/' + test)

        G = generate_graph(V, E)
        print(test + ' : ' + str(max_flow(G, 0, len(G)-1)))