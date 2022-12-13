import networkx as nx
import numpy as np

from util import arr_to_2dgraph


def to_height(h):
    if h == "S":
        return "a"
    if h == "E":
        return "z"
    return h

if __name__ == '__main__':
    a = np.array([[c for c in l.strip()] for l in open("in1.txt")])
    g = arr_to_2dgraph(a).to_directed()
    remove_edges = []
    for e in g.edges:
        u = to_height(e[0][2])
        v = to_height(e[1][2])
        if ord(v) > ord(u) + 1:
            remove_edges.append(e)
    g.remove_edges_from(remove_edges)

    for n in g.nodes:
        if n[2] == "S" or n[2] == "a":
            s = n
        if n[2] == "E":
            e = n

    paths = nx.single_target_shortest_path(g, e)
    min_path = float("inf")
    for s, path in paths.items():
        if s[2] in {"S", "a"}:
            min_path = min(min_path, len(path))
    print(min_path - 1)
