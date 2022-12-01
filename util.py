import networkx as nx
import numpy as np


def lines(fp):
    with open(fp) as f:
        for l in f:
            yield l


def linenumbers(fp):
    with open(fp) as f:
        for i, l in enumerate(f):
            yield i, l


def lines_as_ints(fp):
    return [int(l.strip()) for l in open(fp)]


def line_separated_int_list(fp):
    full_list = []
    sublist = []
    with open(fp) as f:
        for l in f:
            try:
                sublist.append(int(l))
            except ValueError:
                full_list.append(sublist)
                sublist = []
        full_list.append(sublist)
    return full_list


def map_as_np(fp, char_map=None, buffer=0, dtype=None):
    if char_map is None:
        char_map = {".": 0, "#": 1}
    return np.pad(np.array([[char_map[c] for c in l.strip()] for l in open(fp)], dtype=dtype), ((buffer,),))


def digitlines_as_np(fp):
    return np.array([[int(c) for c in l.strip()] for l in open(fp)])


def arr_to_2dgraph(a):
    r, c = a.shape
    g = nx.grid_2d_graph(r, c)
    return nx.relabel_nodes(g, {(i, j): (i, j, a[i, j]) for i in range(r) for j in range(c)})


def arr_to_digraph(a):
    r, c = a.shape
    g = nx.DiGraph()
    g.add_weighted_edges_from([((i - 1, j), (i, j), a[i, j]) for i in range(1, r) for j in range(c)])
    g.add_weighted_edges_from([((i, j), (i - 1, j), a[i - 1, j]) for i in range(1, r) for j in range(c)])
    g.add_weighted_edges_from([((i, j - 1), (i, j), a[i, j]) for i in range(r) for j in range(1, c)])
    g.add_weighted_edges_from([((i, j), (i, j - 1), a[i, j - 1]) for i in range(r) for j in range(1, c)])
    return g
