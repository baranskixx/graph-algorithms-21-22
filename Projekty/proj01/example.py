from os import X_OK
from data import runtests
from queue import deque
from copy import copy
INF = 1e20


class Graph:
    def __init__(self, V):
        self.vertexes = [Vertex(i) for i in range(V)]
        self.edges = {}
    
    def add_edge(self, v, u, costs):
        self.vertexes[v].add_edge(u)
        self.edges[(v, u)] = Edge(v, u, costs)
        self.edges[(-u, v)] = NegativeEdge(u, v, costs)
    
    def reset_distance(self):
        for v in self.vertexes:
            v.d = INF
            v.parent = None
    
    def reset(self):
        for v in self.vertexes:
            v.visited = False
            v.parent = None

    def visited(self, v):
        return self.vertexes[v].visited
    
    def set_visited(self, v):
        self.vertexes[v].visited = True

    def set_parent(self, v, parent):
        self.vertexes[v].parent = parent

    def get_neighbours_of(self, v):
        return self.vertexes[v].neigh

    def add_flow_between(self, u, v, flow_val):
        e1 = self.edges.pop((u, v))
        e2 = self.edges.pop((-v, u))

        e1.add_flow(flow_val)
        e2.increase_capacity(flow_val)
        
        self.edges[(u, v)] = e1
        self.edges[(-v, u)] = e2

    def remove_flow_between(self, u, v, flow_val):
        e1 = self.edges.pop((u, v))
        e2 = self.edges.pop((-v, u))

        e1.remove_flow(flow_val)
        e2.decrease_capacity(flow_val)

        self.edges[(u, v)] = e1
        self.edges[(-v, u)] = e2

    def calculate_flow_cost_between(self, v, u):
        edge = self.edges[(v, u)]
        return sum(edge.costs[0:edge.flow])
    
    def calculate_flow_cost(self):
        ans = 0
        for v in range(len(self.vertexes)):
            for u in self.vertexes[v].neigh:
                ans += self.calculate_flow_cost_between(v, u)
        
        return ans

    def find_required_flow(self, req_flow_val, _from, _to):
        while req_flow_val > 0:
            self.reset()

            Q = deque()
            Q.appendleft((_from, None, INF))

            while len(Q) != 0:
                u, p, cap = Q.pop()

                if not self.visited(u):
                    self.set_parent(u, p)
                    self.set_visited(u)

                    if u == _to:
                        break

                    for v in self.get_neighbours_of(u):
                        edge = self.edges[(u, v)]

                        if edge.flow < edge.capacity and not self.visited(v):
                            Q.appendleft((v, u, min(cap, req_flow_val, edge.capacity - edge.flow)))


            if u != _to:
                return False
            
            while u != _from:
                p = self.vertexes[u].parent
                self.add_flow_between(p, u, cap)

                u = p
            
            req_flow_val -= cap
            # print(cap)
        
        return True

    def search_for_negative_cycle(self):
        self.reset_distance()
        self.vertexes[1].d = 0

        for _ in range(len(self.vertexes)):
            u = None
            for (_from, _to), edge in self.edges.items():
                if self.vertexes[abs(_from)].d == INF:
                    continue
                if _from < 0:
                    if edge.capacity > 0 and self.vertexes[_to].d > self.vertexes[abs(_from)].d + edge.current_cost:
                        u = _to
                        self.vertexes[_to].d = self.vertexes[abs(_from)].d + edge.current_cost
                        self.set_parent(_to, _from)
                elif edge.capacity - edge.flow > 0 and self.vertexes[_to].d > self.vertexes[_from].d + edge.current_cost:
                    u = _to
                    self.vertexes[_to].d = self.vertexes[_from].d + edge.current_cost
                    self.set_parent(_to, _from)
        
        if u == None:
            return []

        for _ in range(len(self.vertexes)):
            u = self.vertexes[abs(u)].parent
        
        v = self.vertexes[abs(u)].parent
        l = [u]

        while True:
            l.append(v)
            if abs(v) == abs(u):
                break
            v = self.vertexes[abs(v)].parent
        
        return l

    def find_minimum_cost_flow(self):
        while True:
            v_list = self.search_for_negative_cycle()
            if len(v_list) == 0:
                break
            print(v_list)
            for i in range(1, len(v_list)):
                u = abs(v_list[i-1])
                v = v_list[i]

                if v > 0:
                    self.add_flow_between(v, u, 1)
                else:
                    self.remove_flow_between(u, abs(v), 1)


class Vertex:
    def __init__(self, i):
        self.neigh = []
        self.visited = False
        self.d = INF
        self.parent = None
    
    def add_edge(self, u):
        self.neigh.append(u)
    
class Edge:
    def __init__(self, _from, _to, costs):
        self._from = _from
        self._to = _to
        self.capacity = len(costs)
        self.costs = costs + [INF]
        self.flow = 0
        self.current_cost = self.costs[0]

        for i in range(len(self.costs)-1, 0, -1):
            self.costs[i] -= self.costs[i-1]
    
    def add_flow(self, flow_val = 1):
        if self.capacity < (self.flow + flow_val):
            print('ERROR')
            return False
        
        self.flow += flow_val
        self.current_cost = self.costs[self.flow]
        return True
    
    def remove_flow(self, flow_val = 1):
        if self.flow - flow_val < 0:
            print('ERROR')
            return False

        self.flow -= flow_val
        self.current_cost = self.costs[self.flow]
        return True

class NegativeEdge:
    def __init__(self, _from, _to, costs):
        self._from = _from
        self._to = _to 
        self.costs = [0] + costs
        self.capacity = 0
        self.current_cost = 0

        for i in range(len(self.costs)):
            self.costs[i] *= (-1)
        for i in range(len(self.costs)-1, 0, -1):
            self.costs[i] -= self.costs[i-1]

    def increase_capacity(self, val = 1):
        if val + self.capacity >= len(self.costs):
            print('ERROR')
            return False
        
        self.capacity += val
        self.current_cost = self.costs[self.capacity]
        return True

    def decrease_capacity(self, val = 1):
        if self.capacity - val < 0:
            print('ERROR')
            return False
        
        self.capacity -= val
        self.current_cost = self.costs[self.capacity]
        return True

def my_solve(V, k, edges):
    print("Ilosc wierzcholkow: {}, krawedzi: {}".format(V, len(edges)))
    print("Ilosc oddzialow: {}".format(k))

    G = Graph(V+1)

    for (u, v), losses in edges:
        G.add_edge(u, v, copy(losses))
    
    G.find_required_flow(k, 1, V)
    G.find_minimum_cost_flow()
    return G.calculate_flow_cost()


runtests(my_solve)
