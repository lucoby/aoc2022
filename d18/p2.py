import networkx as nx

from util import lines

def get_sf(all_p):
    adj = [
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0,),
        (0, -1, 0,),
        (0, 0, 1),
        (0, 0, -1),
    ]

    total_adj = 0
    for p in all_p:
        for a in adj:
            adj_p = tuple(p + a for p, a in zip(p, a))
            if adj_p in all_p:
                total_adj += 1

    return 6 * len(all_p) - total_adj

if __name__ == '__main__':
    all_p = set()
    for l in lines("in1.txt"):
        p = eval(l)
        all_p.add(p)

    all_sf = get_sf(all_p)

    max_d = max((max(p) for p in all_p))

    min_d = min((min(p) for p in all_p))

    G = nx.grid_graph(dim=([range(min_d - 1, max_d + 2)] * 3))

    G.remove_nodes_from(list(all_p))

    for c in nx.connected_components(G):
        if (min_d - 1, min_d - 1, min_d - 1) in c:
            print(get_sf(c) - (max_d - min_d + 3) ** 2 * 6)
            break
