import networkx as nx
from make_tests import generate_tests
from dimacs import loadWeightedGraph, readSolution

TEST_DIR = './graphs/planar/'
if __name__ == '__main__':
    tests = generate_tests(TEST_DIR)

    for test in tests:
        V, E = loadWeightedGraph(TEST_DIR + test)

        G = nx.Graph()
        G.add_nodes_from([i for i in range(1, V+1)])
        for (u, v, _) in E:
            G.add_edge(u, v)
        
        ans = nx.algorithms.check_planarity(G)[0]
        if readSolution(TEST_DIR + test) == '0':
            assert_ans = False
        else:
            assert_ans = True

        if ans == assert_ans:
            print("Test " + test + " zaliczony!")
        else:
            print("Test " + test + " niezaliczony!")