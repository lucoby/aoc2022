import numpy as np

from util import lines


def start_fall(chamber):
    empty_rows = (chamber == 0).all(axis=1)
    return np.argwhere(empty_rows)[-1, 0]


def overlap(chamber, shape, r, c):
    shape_r, shape_c = shape.shape
    o = (chamber[r : r + shape_r, c : c + shape_c] * shape).any()
    return o


def drop_rock(chamber, shape, moves, move_i):
    shape_r, shape_c = shape.shape
    r = start_fall(chamber) - 2 - shape_r
    c = 2
    while True:
        move = moves[move_i]
        if move == "<" and c - 1 >= 0 and not overlap(chamber, shape, r, c - 1):
            c -= 1

        elif move == ">" and c + 1 + shape_c <= 7 and not overlap(chamber, shape, r, c + 1):
            c += 1

        move_i = (move_i + 1) % len(moves)

        if r + 1 + shape_r <= chamber.shape[0] and not overlap(chamber, shape, r + 1, c):
            r += 1
        else:
            chamber[r : r + shape_r, c : c + shape_c] = shape + chamber[r : r + shape_r, c : c + shape_c]
            return chamber, move_i


def print_chamber(chamber):
    r = start_fall(chamber)
    for i in range(r, chamber.shape[0]):
        for j in range(chamber.shape[1]):
            if chamber[i, j]:
                print("#", end="")
            else:
                print(".", end="")
        print()


if __name__ == "__main__":
    m = list(list(lines("in1.txt"))[0].strip())

    shapes = [
        np.ones((1, 4)),
        np.ones((3, 3)),
        np.ones((3, 3)),
        np.ones((4, 1)),
        np.ones((2, 2)),
    ]
    shapes[1][0::2, 0::2] = 0
    shapes[2][0:2, 0:2] = 0

    height = 8000
    chamber = np.zeros((height, 7))

    move_i = 0
    for i in range(2022):
        chamber, move_i = drop_rock(chamber, shapes[i % len(shapes)], m, move_i)

    print(height - start_fall(chamber) - 1)
