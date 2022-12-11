from dataclasses import dataclass
from typing import List, Callable

from util import lines


@dataclass
class Monkey:
    items: List
    op: str
    test: int
    test_t: int
    test_f: int
    inspected = 0


def mop(m_op, old):
    return eval(m_op)


def mtest(m_test, item):
    return item % m_test == 0


if __name__ == "__main__":
    monkeys = []
    for l in lines("in1.txt"):
        if l.startswith("  Starting"):
            items = l.strip().split(": ")[1]
            items = [int(i) for i in items.split(", ")]

        elif l.startswith(("  Operation")):
            op = l.strip().split("= ")[1]

        elif l.startswith("  Test"):
            test = int(l.strip().split(" by ")[1])

        elif l.startswith("    If t"):
            test_t = int(l.strip()[-1])

        elif l.startswith("    If f"):
            test_f = int(l.strip()[-1])

        elif not l.strip():
            monkeys.append(Monkey(items=items, op=op, test=test, test_t=test_t, test_f=test_f))

    monkeys.append(Monkey(items=items, op=op, test=test, test_t=test_t, test_f=test_f))

    for i in range(20):
        for monkey in monkeys:
            while True:
                if len(monkey.items) == 0:
                    break
                new_score = mop(monkey.op, monkey.items.pop(0)) // 3
                if mtest(monkey.test, new_score):
                    monkeys[monkey.test_t].items.append(new_score)
                else:
                    monkeys[monkey.test_f].items.append(new_score)
                monkey.inspected += 1
    biz = sorted([monkey.inspected for monkey in monkeys])
    print(biz[-1] * biz[-2])
