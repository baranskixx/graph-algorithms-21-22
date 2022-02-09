from dimacs import loadDirectedWeightedGraph
from graph import Graph

def lex_bfs(G : Graph, s = None):
    if s == None:
        s = 1
    
    G.reset_graph()

    first_set = set(range(1, G.n+1)) - {s}
    sets_list = [first_set, {s}]
    n = G.n
    visited_order = []

    while G.visited_cnt < G.n:
        u = sets_list[-1].pop()
        visited_order.append(u)
        G.set_visited(u)
        neighbours = G.V[u].out

        j = 0
        while j < len(sets_list):
            X = sets_list.pop(j)
            Y = X & neighbours
            K = X - neighbours

            next_move = 0
            if len(Y) != 0:
                sets_list.insert(j, Y)
                next_move += 1
            
            if len(K) != 0:
                sets_list.insert(j, K)
                next_move += 1
            
            j += next_move

    return visited_order

def checkLexBFS(G):
    vs = lex_bfs(G)
    n = G.n + 1
    pi = [None] * n
    for i, v in enumerate(vs):
        pi[v] = i

    for i in range(n-1):
        for j in range(i+1, n-1):
            Ni = G.V[vs[i]].out
            Nj = G.V[vs[j]].out

            verts = [pi[v] for v in Nj - Ni if pi[v] < i]
            if verts:
                viable = [pi[v] for v in Ni - Nj]
                if not viable or min(verts) <= min(viable):
                    return False
    return True


# test - graf z przykładu działania lexBFS
# G = Graph(8)

# G.add_edge(1, 6)
# G.add_edge(6, 3)
# G.add_edge(6, 8)
# G.add_edge(6, 7)
# G.add_edge(3, 8)
# G.add_edge(8, 2)
# G.add_edge(8, 5)
# G.add_edge(8, 4)
# G.add_edge(8, 7)
# G.add_edge(5, 7)
# G.add_edge(4, 7)

