from dimacs import loadWeightedGraph
from graph import Graph
from make_tests import generate_tests
from lex_bfs import lex_bfs

TESTS_DIRECTORY = "./graphs/vcover"

def vcover(G):
    lex_bfs_order = lex_bfs(G)
    lex_bfs_order.reverse()
    I = set()

    for u in lex_bfs_order:
        neigh = G.V[u].out

        if len(I & neigh) == 0:
            I.add(u)
    
    return len(I)

if __name__ == '__main__':
    tests = generate_tests(TESTS_DIRECTORY)

    for test in tests:
        size, L = loadWeightedGraph(TESTS_DIRECTORY + "/" + test)
        G = Graph(size, L)
        
        with open(TESTS_DIRECTORY + "/" + test) as f:
            answer = f.readline().split()[-1]
        
        answer = int(answer)
        given_answer = vcover(G)

        if answer == given_answer:
            print("Test " + test + " passed! answer: " + str(answer))
        else:
            print("Test " + test + " with wrong answer! answer: " + str(answer) + " answer given: " + str(given_answer))