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


def make_grid_args(n, m, k, costs):
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
                edges.append(((a, b), costs))
    return [V, k, edges]


def random_cost_list(cap, step_min, step_max):
    c = 0
    v = 0
    a = 0
    costs = []
    for _ in range(cap):
        a = myrand(step_min, step_max)
        v += a
        c += v
        costs.append(c)
    return costs


def make_layers_args(k, sizes, cap_min, cap_max, step_min, step_max):
    V = sum(sizes) + 2
    layers = [[1]]
    idx = 2
    for n in sizes:
        layers.append(list(range(idx, idx + n)))
        idx += n
    layers.append([V])

    edges = []
    for la, lb in zip(layers, layers[1:]):
        for i in la:
            for j in lb:
                cap = myrand(cap_min, cap_max)
                costs = random_cost_list(cap, step_min, step_max)
                edges.append(((i, j), costs))
    return [V, k, edges]


def make_random_dag_args(V, k, conn, cap_min, cap_max, step_min, step_max):
    def flip(): return myrand(0, 1000) / 1000.0 < conn

    edges = []
    for i in range(1, V+1):
        for j in range(i+1, V+1):
            if flip():
                cap = myrand(cap_min, cap_max)
                costs = random_cost_list(cap, step_min, step_max)
                edges.append(((i, j), costs))

    return [V, k, edges]



problems = [
    {"arg": [4, 4,
        [
            ((1, 2), [1, 4, 10, 17, 800]),
            ((2, 3), [2, 7, 10, 30]),
            ((3, 4), [5, 13, 40, 100, 5000]),
        ]],
    "hint": 147,
    },
    {"arg": [4, 3,
        [
            ((1, 2), [1, 10, 50]),
            ((1, 3), [3, 7, 12]),
            ((2, 4), [1, 2, 3]),
            ((3, 4), [1, 2, 3]),
        ]],
    "hint": 11
    },
    {"arg": [7, 6,
        [
            ((1,2), [2, 5, 9, 20, 40]),
            ((1,3), [1, 3, 6, 11, 30]),
            ((2,3), [2, 6, 11, 25]),
            ((2, 4), [1, 3, 8, 15, 33]),
            ((3, 4), [2, 6, 14, 28, 90]),
            ((2, 5), [4, 9, 18, 28, 89]),
            ((3, 5), [3, 7, 19, 50, 95]),
            ((2, 6), [1, 3, 40, 100]),
            ((3, 6), [5, 12, 30, 80]),
            ((4, 7), [2, 5, 10, 50]),
            ((5, 7), [1, 4, 17, 70, 180]),
            ((6, 7), [3, 7, 12, 18]),
        ]],
    "hint": 44
    },
    {"arg": make_grid_args(7, 7, 9, [1,3,6,11,20,35,80,200,1300]),
    "hint": 176
    },
    {"arg": make_grid_args(20, 20, 10, [1,3,6,11,20,35,80,200,1300]),
    "hint": 472
    },
    {"arg": make_layers_args(5, [3, 5], 4, 6, 1, 3),
    "hint": 25
    },
    {"arg": make_layers_args(8, [8, 12, 10, 10, 6], 5, 10, 2, 7),
    "hint": 141
    },
    {"arg": make_layers_args(25, [12, 16, 20, 14, 10, 8], 7, 12, 2, 8),
    "hint": 679
    },
    {"arg": make_random_dag_args(10, 5, 0.3, 3, 5, 2, 9),
    "hint": 237
    },
    {"arg": make_random_dag_args(150, 20, 0.2, 7, 15, 1, 15),
    "hint": 272
    }
]


def printarg(V, k, edges):
    print("Rozmiar: {}, oddziały: {}".format(V, k))
    print("Ilość ścieżek: {}".format(len(edges)))
    print("Ścieżki: {}".format(limit(edges, 120)))

def printhint(hint):
    print("Wynik: {}".format(hint))

def printsol(sol):
    print("Uzyskany wynik: {}".format(sol))

def check(V, k, edges, hint, sol):
    if hint == sol:
        print("Test zaliczony")
        return True
    else:
        print("NIEZALICZONY!")
        return False

def runtests(f):
    internal_runtests(printarg, printhint, printsol, check, problems, f)
