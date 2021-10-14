# BFS/DFS + binary search approach

from dimacs import *
from make_tests import generate_tests
import sys

class Vertex():
    def __init__(self):
        self.neighbours = []
        self.visited = False

def generate_graph(E, V):
    costs = []
    G = [Vertex() for _ in range(V)]

    for x, y, c in E:
        G[x-1].neighbours.append([y-1, c])
        G[y-1].neighbours.append([x-1, c])

        if c not in costs:
            costs.append(c)
    
    return G, costs

def DFS_Visit(G, k, x):
    G[x].visited = True

    for y, c in G[x].neighbours:
        if not G[y].visited and c >= k:
            G = DFS_Visit(G, k, y)
    
    return G

def min_edge_cost(G, costs):
    n = len(costs)

    start = 0
    mid = 0
    end = n-1
    last = 0

    while start < end:
        for v in G:
            v.visited = False
        
        mid = start + (end-start)//2 + 1

        G = DFS_Visit(G, costs[mid], 0)

        if G[1].visited:
            start = mid
            last = mid
        else:
            end = mid-1
    return costs[last]

if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    tests = generate_tests('./graphs')
    
    for test in tests:
        print(test, end=' : ')
        V, E = loadWeightedGraph('graphs/' + test)

        G, costs = generate_graph(E, V)
        costs.sort()

        print('Minimal cost of edge on path is ' + str(min_edge_cost(G, costs)))