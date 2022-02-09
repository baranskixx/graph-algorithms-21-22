from testy import *


def lcg(seed):
    a = 1103515245
    a = 69069
    c = 12345
    m = 2 ** 31
    while True:
        yield seed ^ (seed >> 16)
        seed = (a * seed + c) % m

generator = lcg(314159265)
myrand = lambda a, b: a + next(generator) % (b - 1)


def make_clique_args(n):
    V = n
    edges = []
    for i in range(1, V+1):
        for j in range(i+1, V+1):
                edges.append((i, j))
    return [n, edges]


def make_grid_args(n, m):
    V = n * m
    edges = []

    def idx(i, j): return (i - 1) * m + j
    def inside(c): return 1 <= c[0] <= n and 1 <= c[1] <= m
    def nb(i, j): return filter(inside, [(i+1,j), (i,j+1)])

    for i in range(1, n+1):
        for j in range(1, m+1):
            a = idx(i, j)
            for p, q in nb(i, j):
                b = idx(p, q)
                edges.append((a, b))
    return [V, edges]


def make_random_graph_args(V, conn):
    def flip(): return myrand(0, 1000) / 1000.0 < conn

    edges = []
    for i in range(1, V+1):
        for j in range(i+1, V+1):
            if flip():
                edges.append((i, j))

    return [V, edges]


problems = [
    {"arg": [6, [(1,2), (1,3), (2,3), (2,4), (3,5), (4,5), (4,6), (5,6)]],
    "hint": True,
    },
    {"arg": [5, [(1,2), (1,3), (2,4), (3,4), (2,5), (3,5)]],
    "hint": False,
    },
    {"arg": [7, [(1,2), (1,3), (2,4), (3,4), (4,5), (4,6), (5,7), (6,7)]],
    "hint": False,
    },
    {"arg": [10, [
        (1,3), (3,5), (5,2), (2,4), (4,1),
        (6,7), (7,8), (8,9), (9,10), (10,6),
        (1,6), (2,7), (3,8), (4,9), (5,10),
    ]],
    "hint": True,
    },
    {"arg": [6, [
        (1,5), (3,6), (2,6), (4,5),
        (1,6), (4,6), (2,5), (3,5),
    ]],
    "hint": False,
    },
    {"arg": [11, [
        (1,2), (2,3), (3,4), (4,1),
        (5,6), (5,7), (6,8), (7,8), (8,9), (8,10), (9,11), (10,11),
        (1,5), (11,3), (6,2), (9,2), (7,4), (10,4),
    ]],
    "hint": False,
    },
    {"arg": make_grid_args(25, 10),
    "hint": True,
    },
    {"arg": make_random_graph_args(50, 0.2),
    "hint": True,
    },
    {"arg": make_random_graph_args(50, 0.1),
    "hint": False,
    },
    {"arg": make_clique_args(18),
    "hint": True,
    },
]


def as_graph(V, edges):
    vs = {i: set() for i in range(1, V+1)}
    for a, b in edges:
        vs[a].add(b)
        vs[b].add(a)
    return vs


def cycle_edges(vs):
    edges = [(i, j) for i, j in zip(vs, vs[1:])]
    edges.append((vs[-1], vs[0]))
    return edges


def is_valid(V, edges, sol):
    total = set()
    for vs in sol:
        vs = set(vs)
        if len(vs) < 3:
            return False
        before = len(total)
        total |= vs
        after = len(total)
        if after < before + len(vs):
            return False

    if total != set(range(1, V+1)):
        return False

    G = as_graph(V, edges)
    for group in sol:
        for a, b in cycle_edges(group):
            if b not in G[a]:
                return False

    return True


def printarg(V, edges):
    print("Rozmiar: {}".format(V))
    print("Ilość ścieżek: {}".format(len(edges)))
    print("Ścieżki: {}".format(limit(edges, 120)))

def printhint(hint):
    print("Wynik: {}".format(hint))

def printsol(sol):
    print("Uzyskany wynik: {}".format(sol))

def check(V, edges, hint, sol):
    if hint and is_valid(V, edges, sol) or not hint and not sol:
        print("Test zaliczony")
        return True
    else:
        print("NIEZALICZONY!")
        return False

def runtests(f):
    internal_runtests(printarg, printhint, printsol, check, problems, f)
