class Graph:
    def __init__(self, size, L):
        self.V = [None] + [Node(i) for i in range(1, size+1)]
        self.n = size
        self.visited_cnt = 0

        for (u, v, _) in L:
            self.add_edge(u, v)
    
    def add_edge(self, u, v):
        self.V[u].add_edge(v)
        self.V[v].add_edge(u)

    def reset_graph(self):
        self.visited_cnt = 0
        for v in self.V:
            if v is not None:
                v.visited = False
    
    def set_visited(self, u):
        if not self.V[u].visited:
            self.V[u].visited = True
            self.visited_cnt += 1

class Node:
    def __init__(self, id):
        self.idx = id
        self.out = set()
        self.visited = False

    def add_edge(self, _to):
        self.out.add(_to)