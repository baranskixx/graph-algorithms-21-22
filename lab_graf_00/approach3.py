# dijkstra algorithm approach

from dimacs import *
from make_tests import generate_tests
from queue import PriorityQueue
import sys

INF = 1e9

class Vertex():
    def __init__(self):
        self.neighbours = []
        self.d = None

def generate_graph(E, V):
    costs = []
    G = [Vertex() for _ in range(V)]

    for x, y, c in E:
        G[x-1].neighbours.append([y-1, c])
        G[y-1].neighbours.append([x-1, c])

        if c not in costs:
            costs.append(c)
    
    return G, costs

def dijkstra_modified(G, start, end):
    Q = PriorityQueue()
    Q.put((INF, start))

    while G[end].d is None and not Q.empty():
        c, v = Q.get()
        if G[v].d == None:
            G[v].d = abs(c)
            for u, c in G[v].neighbours:
                Q.put((max((-1)*G[v].d, (-1)*abs(c)), u))

    return G[end].d

if __name__ == '__main__':
    tests = generate_tests('./graphs')

    for test in tests:
        print(test, end=' : ')
        V, E = loadWeightedGraph('graphs/' + test)

        G, costs = generate_graph(E, V)
        costs.sort()

        print('Minimal cost of edge on path is ' + str(dijkstra_modified(G, 0, 1)))
