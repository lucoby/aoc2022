from dataclasses import dataclass
from typing import List, Callable

from util import lines


@dataclass
class Monkey:
    items: List
    op: Callable
    test: Callable
    test_t: int
    test_f: int
    inspected = 0


ex1 = [
    Monkey(items=[79, 98], op=lambda x: x * 19, test=lambda x: x % 23 == 0, test_t=2, test_f=3),
    Monkey(items=[54, 65, 75, 74], op=lambda x: x + 6, test=lambda x: x % 19 == 0, test_t=2, test_f=0),
    Monkey(items=[79, 60, 97], op=lambda x: x**2, test=lambda x: x % 13 == 0, test_t=1, test_f=3),
    Monkey(items=[74], op=lambda x: x + 3, test=lambda x: x % 17 == 0, test_t=0, test_f=1),
]

in1 = [
    Monkey(items=[71, 86], op=lambda x: x * 13, test=lambda x: x % 19 == 0, test_t=6, test_f=7),
    Monkey(items=[66, 50, 90, 53, 88, 85], op=lambda x: x + 3, test=lambda x: x % 2 == 0, test_t=5, test_f=4),
    Monkey(items=[97, 54, 89, 62, 84, 80, 63], op=lambda x: x + 6, test=lambda x: x % 13 == 0, test_t=4, test_f=1),
    Monkey(items=[82, 97, 56, 92], op=lambda x: x + 2, test=lambda x: x % 5 == 0, test_t=6, test_f=0),
    Monkey(items=[50, 99, 67, 61, 86], op=lambda x: x**2, test=lambda x: x % 7 == 0, test_t=5, test_f=3),
    Monkey(items=[61, 66, 72, 55, 64, 53, 72, 63], op=lambda x: x + 4, test=lambda x: x % 11 == 0, test_t=3, test_f=0),
    Monkey(items=[59, 79, 63], op=lambda x: x * 7, test=lambda x: x % 17 == 0, test_t=2, test_f=7),
    Monkey(items=[55], op=lambda x: x + 7, test=lambda x: x % 3 == 0, test_t=2, test_f=1),
]


if __name__ == "__main__":
    monkeys = in1
    for i in range(20):
        for monkey in monkeys:
            while True:
                if len(monkey.items) == 0:
                    break
                new_score = monkey.op(monkey.items.pop(0)) // 3
                if monkey.test(new_score):
                    monkeys[monkey.test_t].items.append(new_score)
                else:
                    monkeys[monkey.test_f].items.append(new_score)
                monkey.inspected += 1
    biz = sorted([monkey.inspected for monkey in monkeys])
    print(biz[-1] * biz[-2])
