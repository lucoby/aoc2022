from util import lines


def compare(p0, p1):
    if isinstance(p0, list) and isinstance(p1, list):
        for i0, i1 in zip(p0, p1):
            c = compare(i0, i1)
            if c != 0:
                return c
        if len(p0) == len(p1):
            return 0
        elif len(p0) < len(p1):
            return 1
        else:
            return -1

    if isinstance(p0, int) and isinstance(p1, int):
        if p0 == p1:
            return 0
        elif p0 < p1:
            return 1
        else:
            return -1
    if isinstance(p0, list) and isinstance(p1, int):
        return compare(p0, [p1])
    if isinstance(p0, int) and isinstance(p1, list):
        return compare([p0], p1)


if __name__ == '__main__':
    all_l = list(lines("in1.txt"))
    i = 0
    right_order = []
    while True:
        if i >= len(all_l):
            break
        p0 = eval(all_l[i])
        p1 = eval(all_l[i + 1])

        c = compare(p0, p1)
        if c == 1:
            right_order.append(i // 3 + 1)

        i += 3
    print(right_order)
    print(sum(right_order))
