from functools import cmp_to_key

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
    all_l = [eval(l) for l in all_l if l.strip()] + [[[2]], [[6]]]
    all_l = sorted(all_l, key=cmp_to_key(compare), reverse=True)
    a = all_l.index([[2]])
    b = all_l.index([[6]])
    print((a + 1) * (b + 1))
