from operator import ne
from re import S
from data import runtests
from collections import deque

# Opis działania algorytmu
# Interesuje nas znalezienie pokrycia grafu cyklami w taki sposób, by każdy wierzchołek należał do dokładnie jednego takiego cyklu

# Tworzę graf dwudzielny, składający się 2*V + 2 wierzchołków
# 2*V wierzchołków to dwa egzemplarze każdego z wierzchołków w grafie testowanym L_1, L_2, ..., L_V oraz R_1, R_2, ..., R_V
# Jeśli wierzchołki a oraz b są połączone krawędzią w grafie testowanym to L_a jest połączone z R_b krawędzią skierowaną a -> b
# oraz L_B z R_a b -> a

# W tak utworzonym grafie poszukuję maksymalnego skojarzenia (z pomocą maksymalnego przepływu, dwa dodatkowe wierzchołki to źródło oraz ujście)
# Każda krawędź ma przepustowość 1, źródło jest połączone z każdym L wierzchołkiem (Source -> L_1, Source -> L_2, ...),
# ujście z każdym R wierzchołkiem (R_1 -> Sink, R_2 -> Sink, ...)

# Graf da się podzielić na nienachodzące na siebie (wierzchołkami) cykle wtw. gdy w tym grafie dwudzielnym istnieje pełne skojarzenie, a takie istnieje wtw
# gdy w naszym grafie dwudzielnym przepływ będzie mieć wartość V
# W przeciwnym wypadku takie pokrycie nie istnieje.

INF = 1e15

class Graph:
    def __init__(self, V, edges):
        self.Nodes = [Vertex() for _ in range(V)]

        for (a, b) in edges:
            self.Nodes[a].add_arc(b, 1)
            self.Nodes[b].add_arc(a, 0)
    
    # find all cycles in graph with length at least k
    def find_all_k_cycles(self, k):
        def rek()


class Graph_Bi:
    def __init__(self, V, edges) -> None:
        self.Nodes = [Vertex() for i in range(2*V + 2)]

        for u in range(V+1, 2*V+1):
            self.Nodes[0].add_arc(u-V, 1)
            self.Nodes[u-V].add_arc(0, 0)
            self.Nodes[u].add_arc(2*V + 1, 1)
            self.Nodes[2*V+1].add_arc(u, 0)
        
        for (a, b) in edges:
            self.Nodes[a].add_arc(V+b, 1)
            self.Nodes[V+b].add_arc(a, 0)
            self.Nodes[b].add_arc(V+a, 1)
            self.Nodes[V+a].add_arc(b, 0)
        
    def reset(self):
        for u in self.Nodes:
            u.visited = False
            u.parent = None

class Vertex:
    def __init__(self):
        self.neighbours = {}
        self.parent = None
        self.visited = False
        self.flow_to = None
        self.flow_from = None

    def add_arc(self, _to, cap):
        self.neighbours[_to] = cap


def max_flow(G : Graph_Bi, s : int, t : int):
    flow = 0
    open_path_found = True

    while open_path_found:
        G.reset()

        Q = deque()
        Q.appendleft((s, None, 1))
        
        while len(Q) != 0:
            u, parent, _ = Q.pop()
            if not G.Nodes[u].visited:
                G.Nodes[u].parent = parent
                G.Nodes[u].visited = True

                if u == t:
                    break

                for v, c in G.Nodes[u].neighbours.items():
                    if c > 0 and not G.Nodes[v].visited:
                        Q.appendleft((v, u, 1))
        
        if u != t:
            open_path_found = False
        else:
            flow += 1
            while u != s:
                p = G.Nodes[u].parent
                G.Nodes[u].neighbours[p] += 1
                G.Nodes[p].neighbours[u] -= 1
                G.Nodes[p].flow_to = u
                u = p
    
    return flow

def my_solve(V, edges):
    G = Graph_Bi(V, edges)
    flow = max_flow(G, 0, 2*V + 1)
    if flow < V:
        return []
    else:
        G = Graph(V, edges)


        ans = []
        return ans



runtests(my_solve)
