from dimacs import loadWeightedGraph
from graph import Graph
from make_tests import generate_tests
from lex_bfs import lex_bfs

TESTS_DIRECTORY = "./graphs/maxclique"

def max_clique(G):
    lex_bfs_order = lex_bfs(G)

    prev = [set() for _ in range(G.n+1)]
    locked = [False]*(G.n + 1)

    max_clique_size = 0

    for u in lex_bfs_order:
        locked[u] = True
        for v in G.V[u].out:
            if not locked[v]:
                prev[v].add(u)

            max_clique_size = max(max_clique_size, len(prev[v]) + 1)
    
    return max_clique_size


if __name__ == '__main__':
    tests = generate_tests(TESTS_DIRECTORY)

    for test in tests:
        size, L = loadWeightedGraph(TESTS_DIRECTORY + "/" + test)
        G = Graph(size, L)
        
        with open(TESTS_DIRECTORY + "/" + test) as f:
            answer = f.readline().split()[-1]
        
        print(answer, max_clique(G))