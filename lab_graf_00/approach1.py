# find union approach

from dimacs import *
from make_tests import generate_tests

class Node():
    def __init__(self):
        self.parent = self
        self.min_edge = None


def find(x : Node):
    if x != x.parent:
        x.parent = find(x.parent)
    return x.parent

def union(x, y):
    x = find(x)
    y = find(y)

    if x == y: return 
    x.parent = y

if __name__ == '__main__':
    tests = generate_tests('./graphs')
    for test in tests:
        V, E = loadWeightedGraph('graphs/' + test)

        # print('Number of verticles: ' + str(V))
        # for (x,y,c) in E:
        #     print('Edge between ' + str(x) + ' and ' + str(y) + ' witch cost ' + str(c))

        G = [Node() for _ in range(V)]
        E = sorted(E, key= lambda x: x[2], reverse=True)


        e_cnt = len(E)
        i = -1
        while i < e_cnt and find(G[0]) != find(G[1]):
            i += 1
            x, y, c = E[i]

            union(G[x-1], G[y-1])

        if find(G[0]) == find(G[1]):
            print(test + ' : Minimal cost of edge is ', end = '')
            print(E[i][2])
        else:
            print('Verticles are not connected!')