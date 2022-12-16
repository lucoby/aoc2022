from dataclasses import dataclass

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

if __name__ == '__main__':
    y = 2000000
    excl = set()
    s_b_on_y = set()
    for l in lines("in1.txt"):
        s, b = l.strip()[10:].split(": closest beacon is at ")
        s = Pos.parse(s)
        b = Pos.parse(b)

        if s.y == y:
            s_b_on_y.add(s.x)

        if b.y == y:
            s_b_on_y.add(b.x)

        d = s.dist(b)
        excl_s = s.excl_y(y, d)
        excl |= excl_s

    excl = excl - s_b_on_y
    print(len(excl))
