from os import X_OK
from data import runtests
from queue import deque
import cProfile
import re
INF = 1e20


class Graph:
    def __init__(self, V):
        self.vertexes = [Vertex(i) for i in range(V)]
        self.edges = {}
        self.edges_list = []
        self.neg_edges_list = []
    
    def generate_edges(self, edges):
        for (v, u), losses in edges:
            e = Edge(v, u, losses)
            ne = NegativeEdge(u, v, losses)

            self.vertexes[v].neigh[u] = e
            self.edges[(v, u)] = e
            self.edges[(-u, v)] = ne
            self.edges_list.append(e)
            self.neg_edges_list.append(ne)


    def add_edge(self, v, u, costs):
        self.vertexes[v].add_edge(u)
        e = Edge(v, u, costs)
        ne = NegativeEdge(u, v, costs)
        
        self.edges[(v, u)] = e
        self.edges[(-u, v)] = ne
        self.edges_list.append(e)
        self.neg_edges_list.append(ne)
    
    def reset_distance(self):
        for v in self.vertexes:
            v.d = INF
            v.parent = None
    
    def reset(self):
        for v in self.vertexes:
            v.visited = False
            v.parent = None
    
    def set_visited(self, v):
        self.vertexes[v].visited = True

    def set_parent(self, v, parent):
        self.vertexes[v].parent = parent

    def get_neighbours_of(self, v):
        return self.vertexes[v].neigh

    def add_flow_between(self, u, v, flow_val):
        self.edges[(u, v)].add_flow(flow_val)
        self.edges[(-v, u)].increase_capacity(flow_val)

    def remove_flow_between(self, u, v, flow_val):
        self.edges[(u, v)].remove_flow(flow_val)
        self.edges[(-v, u)].decrease_capacity(flow_val)


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
            for v in self.vertexes:
                v.visited = False

            Q = deque()
            Q.appendleft((_from, None, INF))

            while len(Q) != 0:
                u, p, cap = Q.pop()

                if not self.vertexes[u].visited:
                    self.vertexes[u].parent = p
                    self.vertexes[u].visited = True

                    if u == _to:
                        break

                    for v, edge in self.vertexes[u].neigh.items():
                        if edge.flow < edge.capacity and not self.vertexes[v].visited:
                            Q.appendleft((v, u, min(cap, req_flow_val, edge.capacity - edge.flow)))

            if u != _to:
                return False
            
            while u != _from:
                p = self.vertexes[u].parent
                self.edges[(p, u)].add_flow(cap)
                self.edges[(-u, p)].increase_capacity(cap)
                u = p
            
            req_flow_val -= cap
        
        return True

    def search_for_negative_cycle_v2(self):
        for v in self.vertexes:
            v.d = INF
        self.vertexes[1].d = 0

        for _ in range(len(self.vertexes)-1):
            u = None
            for edge in self.edges_list:
                if self.vertexes[edge._to].d > self.vertexes[edge._from].d + edge.current_cost:
                    u = edge._to
                    self.vertexes[edge._to].d = self.vertexes[edge._from].d + edge.current_cost
                    self.vertexes[edge._to].parent = edge._from
        
            for edge in self.neg_edges_list:
                if edge.capacity and self.vertexes[edge._to].d > self.vertexes[edge._from].d + edge.current_cost:
                    u = edge._to
                    self.vertexes[edge._to].d = self.vertexes[edge._from].d + edge.current_cost
                    self.vertexes[edge._to].parent = -edge._from

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
            v_list = self.search_for_negative_cycle_v2()
            if len(v_list) == 0:
                break
            # print(v_list)
            while True:
                min_cap = INF
                next_flow_cost = 0
                for i in range(1, len(v_list)):
                    u = abs(v_list[i-1])
                    v = v_list[i]

                    if v > 0:
                        self.vertexes[v].neigh[u] = 
                        self.edges[(-u, v)].increase_capacity(1)
                        next_flow_cost += self.edges[(v, u)].current_cost
                        min_cap = min(min_cap, self.edges[(-u, v)].capacity)
                    else:
                        self.edges[(v, u)].decrease_capacity(1)
                        self.edges[(u, -v)].remove_flow(1)
                        next_flow_cost += self.edges[(v, u)].current_cost
                        min_cap = min(min_cap, self.edges[(v, u)].capacity)
                
                if min_cap == 0 or next_flow_cost > 0:
                    break


class Vertex:
    def __init__(self, i):
        self.neigh = {}
        self.visited = False
        self.d = INF
        self.parent = None
    
    
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
        self.flow += flow_val
        self.current_cost = self.costs[self.flow]
    
    def remove_flow(self, flow_val = 1):
        self.flow -= flow_val
        self.current_cost = self.costs[self.flow]

class NegativeEdge:
    def __init__(self, _from, _to, costs):
        self._from = _from
        self._to = _to 
        self.costs = [0] + costs
        self.capacity = 0
        self.current_cost = 0

        for i in range(len(self.costs)-1, 0, -1):
            self.costs[i] *= (-1)
            self.costs[i] += self.costs[i-1]

    def increase_capacity(self, val = 1):
        self.capacity += val
        self.current_cost = self.costs[self.capacity]

    def decrease_capacity(self, val = 1):
        self.capacity -= val
        self.current_cost = self.costs[self.capacity]

def my_solve(V, k, edges):
    print("Ilosc wierzcholkow: {}, krawedzi: {}".format(V, len(edges)))
    print("Ilosc oddzialow: {}".format(k))

    G = Graph(V+1)
    G.generate_edges(edges)
    G.find_required_flow(k, 1, V)
    G.find_minimum_cost_flow()
    return G.calculate_flow_cost()


# runtests(my_solve)

cProfile.run('runtests(my_solve)')
