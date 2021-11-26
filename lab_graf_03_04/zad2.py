import sys
from make_tests import generate_tests
from dimacs import loadDirectedWeightedGraph
from queue import PriorityQueue
from copy import deepcopy

INF = 1e15

class Graph:
    def __init__(self, V, E) -> None:                  
        self.ver = [Node() for _ in range(V)]                # lista zawierająca wierzchołki (Node)
        self.non_empty_ver = 0
        self.V = V

        for u, v, c in E:
            self.add_edge_both_ways(u-1, v-1, c)
                                   

    def add_edge_both_ways(self, u, v, c = 0):               # dodaj miedzy wierzcholkami 
        self.ver[u].addEdge(v, c)                            # u i v krawedzie skierowane 
        self.ver[v].addEdge(u, c)                            # o wadze c

    def merge_verticles(self, u, v):                         # scal wierzcholki u i v ; 
        for a in range(len(self.ver)):                       # krawedzie wychodzace z 
            if a != u and a != v:                            # wierzcholka u przenies do v
                c = self.ver[a].delEdge(u)                   # oraz usun krawedz miedzy u i v
                if c != 0:
                    self.add_edge_both_ways(v, a, c)
        
        self.ver[u].delAllEdges()
        self.ver[v].delEdge(u)
        self.ver[v].consume(u)
        if u == self.non_empty_ver:
            self.non_empty_ver = v
        self.V -= 1

    def get_edge_weight_beetwen(self, u, v):
        return self.ver[u].getEdgeWeight(v)
    
    def draw(self):
        print('Graf posiada ' + str(len(self.ver)) + ' wierzcholkow.')
        if len(self.ver) > 30:
            print('Za duzy graf.')
        else:
            for i in range(len(self.ver)):
                for j in range(len(self.ver)):
                    print(self.ver[i].getEdgeWeight(j), end = ' ')
                print()
    
    def isEmptyVer(self, v):
        return len(self.ver[v].edges) == 0


class Node:
    def __init__(self):
        self.edges = {}    # słownik  mapujący wierzchołki do których są krawędzie na ich wagi
        self.consumed = [] # lista zawierająca wszystkie wierzchołki, które zostały scalone z tym wierzchołkiem

    def addEdge( self, to, weight):
        self.edges[to] = self.edges.get(to,0) + weight  # dodaj krawędź do zadanego wierzchołka
                                                        # o zadanej wadze; a jeśli taka krawędź
                                                        # istnieje, to dodaj do niej wagę
    def delEdge( self, to ):
        return self.edges.pop(to, 0)                    # usuń krawędź do zadanego wierzchołka
    
    def getEdgeWeight(self, to):
        return self.edges.get(to, 0)

    def delAllEdges(self):
        self.edges = {}

    def consume(self, v):
        self.consumed.append(v)



def minimumCutPhase(G : Graph, a = -1):
    if a == -1:
        a = G.non_empty_ver

    Visited = [False]*len(G.ver)
    F = {}
    Q = PriorityQueue()
    Visited[a] = True
    cnt_visited = 1
    last = [a, None]

    for i in range(len(G.ver)):
        v = G.ver[i].edges
        F[i] = v.get(a, 0)
        Q.put(((-1)*F[i], i))

    while cnt_visited < G.V:
        _, i = Q.get()

        if not Visited[i]:
            Visited[i] = True
            cnt_visited += 1
            v = G.ver[i].edges
            last = [i, last[0]]

            for u, c in v.items():
                F[u] = F[u] + c
                Q.put(((-1)*F[u], u))

    s = F[last[0]]    
    G.merge_verticles(last[0], last[1])

    return G, F[last[0]]


if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    tests = generate_tests('./graphs')
    for test in tests:
        print('Test: ' + test)

        V, E = loadDirectedWeightedGraph('graphs/' + test)

        G = Graph(V, E)
        G.draw()

        ans = INF

        for i in range(V-1):
            G, tmp = minimumCutPhase(G)
            ans = min(ans, tmp)

        print('Odpowiedz: ' + str(ans))
        print('-------------------------------------------------------------------------')
