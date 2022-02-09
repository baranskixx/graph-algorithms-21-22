from dimacs import loadWeightedGraph
from graph import Graph
from make_tests import generate_tests
from lex_bfs import lex_bfs

def greedy_coloring(G):
    lex_bfs_order = lex_bfs(G)

    color = [0]*(G.n + 1)

    for u in lex_bfs_order:
        neigh = G.V[u].out

        used = {color[v] for v in neigh}
        c = min({i for i in range(1, G.n + 1)} - used)
        color[u] = c
    
    return max(color)


TESTS_DIRECTORY = "./graphs/coloring"

if __name__ == '__main__':
    tests = generate_tests(TESTS_DIRECTORY)

    for test in tests:
        size, L = loadWeightedGraph(TESTS_DIRECTORY + "/" + test)
        G = Graph(size, L)
        
        with open(TESTS_DIRECTORY + "/" + test) as f:
            answer = f.readline().split()[-1]
        
        answer = int(answer)
        given_answer = greedy_coloring(G)

        if answer == given_answer:
            print("Test " + test + " passed! answer: " + str(answer))
        else:
            print("Test " + test + " with wrong answer! answer: " + str(answer) + " answer given: " + str(given_answer))