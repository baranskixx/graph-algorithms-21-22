from typing import Text
import networkx as nx
from make_tests import generate_tests
from dimacs import loadCNFFormula, readSolution

TEST_DIR = './graphs/sat/'

if __name__ == '__main__':
    tests = generate_tests(TEST_DIR)
    for test in tests:
        V, F = loadCNFFormula(TEST_DIR + test)
        G = nx.DiGraph()
        
        for x, y in F:
            G.add_edge(-x, y)
            G.add_edge(-y, x)

        ssc = nx.algorithms.components.strongly_connected_components(G)

        solution = bool(int((readSolution(TEST_DIR + test)[-1])))
        ans = True

        for s in ssc:
            if not ans:
                break
            for e in s:
                if -e in s:
                    ans = False
                    break
        
        print(ans, solution)