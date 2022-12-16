from dataclasses import dataclass

import numpy as np

from util import lines


@dataclass
class Pos:
    x: int
    y: int

    @staticmethod
    def parse(text):
        x, y = text[2:].split(", y=")
        return Pos(x=int(x), y=int(y))

    def dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def excl_y(self, y, distance):
        y_dist = abs(self.y - y)
        x_dist = max(distance - y_dist, -1)
        if x_dist == -1:
            return set()
        return set(range(self.x - x_dist, self.x + x_dist + 1))

    def outside_p(self, d):
        for i in range(d + 1):
            x_dist = d - i
            yield Pos(x=self.x - x_dist, y=self.y - i)
            yield Pos(x=self.x + x_dist, y=self.y - i)
            yield Pos(x=self.x - x_dist, y=self.y + i)
            yield Pos(x=self.x + x_dist, y=self.y + i)

    def __hash__(self):
        return hash((self.x, self.y))


def search(s_dist, dim):
    for s, d in s_dist.items():
        for p in s.outside_p(d + 1):
            if not (0 < p.x < dim and 0 < p.y < dim):
                continue
            outside = True
            for other_s, other_d in s_dist.items():
                if p.dist(other_s) <= other_d:
                    outside = False
                    break
            if outside:
                print(p)
                print(p.x * 4000000 + p.y)
                return


if __name__ == "__main__":
    s_dist = {}

    dim = 20
    dim = 4000000
    for l in lines("in1.txt"):
        s, b = l.strip()[10:].split(": closest beacon is at ")
        s = Pos.parse(s)
        b = Pos.parse(b)

        d = s.dist(b)

        s_dist[s] = d

    search(s_dist, dim)
