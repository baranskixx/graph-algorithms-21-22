from dimacs import loadWeightedGraph
from graph import Graph
from make_tests import generate_tests
from lex_bfs import checkLexBFS, lex_bfs

TESTS_DIRECTORY = "./graphs/chordal"

def peo(G):
    lex_bfs_sequence = lex_bfs(G)

    parent = [None]*(G.n+1)
    prev = [set() for _ in range(G.n+1)]

    for u in lex_bfs_sequence:
        for v in G.V[u].out:
            parent[v] = u
            prev[v].add(u)
        
        if parent[u] != None:
            if prev[u] - {parent[u]} != prev[parent[u]]:
                return False
    
    return True


if __name__ == '__main__':
    tests = generate_tests(TESTS_DIRECTORY)

    for test in tests:
        size, L = loadWeightedGraph(TESTS_DIRECTORY + "/" + test)
        G = Graph(size, L)
        
        with open(TESTS_DIRECTORY + "/" + test) as f:
            answer = f.readline()[-1]
        
        if answer == '1':
            answer = True
        else:
            answer = False
        
        if answer == peo(G):
            print("Test " + test +  " passed!")
        else:
            print("Problem in " + test +  "!")