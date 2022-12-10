from util import lines

def unit_step(h, t):
    if h == t:
        return 0
    return int((h - t) / abs(h - t))


if __name__ == '__main__':
    h = (0, 0)
    t = (0, 0)
    t_visited = {t}
    h_move = {
        "R": (1, 0),
        "L": (-1, 0),
        "U": (0, 1),
        "D": (0, -1),
    }
    for l in lines("in1.txt"):
        dir, step = l.strip().split()
        step = int(step)

        for i in range(step):
            h = (h[0] + h_move[dir][0], h[1] + h_move[dir][1])
            if abs(h[0] - t[0]) <= 1 and abs(h[1] - t[1]) <= 1:
                pass
            else:
                t = (t[0] + unit_step(h[0], t[0]), t[1] + unit_step(h[1], t[1]))
            t_visited.add(t)
    print(len(t_visited))
