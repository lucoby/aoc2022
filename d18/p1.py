from util import lines

if __name__ == '__main__':
    all_p = set()
    for l in lines("in1.txt"):
        p = eval(l)
        all_p.add(p)

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

    print(6 * len(all_p) - total_adj)
