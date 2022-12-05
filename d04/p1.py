from util import lines

def split_part(e):
    p1, p2 = e.split("-")
    return int(p1), int(p2)

if __name__ == '__main__':
    overlap = 0
    for l in lines("in1.txt"):
        e1, e2 = l.strip().split(",")
        e1p1, e1p2 = split_part(e1)
        e2p1, e2p2 = split_part(e2)
        if e1p1 <= e2p1 and e1p2 >= e2p2 or e2p1 <= e1p1 and e2p2 >= e1p2:
            overlap += 1

    print(overlap)
