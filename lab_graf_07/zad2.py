from typing import Text
import networkx as nx
from make_tests import generate_tests
from dimacs import loadDirectedWeightedGraph, readSolution

TEST_DIR = './graphs/flow/'

if __name__ == '__main__':
    tests = generate_tests(TEST_DIR)

    for test in tests:
        V, E = loadDirectedWeightedGraph(TEST_DIR + test)

        G = nx.DiGraph()
        G.add_nodes_from([i for i in range(1, V+1)])

        for (u, v, c) in E:
            G.add_edge(u, v)
            G[u][v]['capacity'] = c
        
        solution = int(readSolution(TEST_DIR + test))
        ans = nx.algorithms.maximum_flow(G, 1, V)[0]

        if ans == solution:
            print("Test " + test + " zaliczony!")
        else:
            print("Test " + test + " niezaliczony!")
            print(solution, ans)

