from parsy import string, regex, seq

from util import lines

if __name__ == '__main__':

    stacks = [[] for i in range(9)]
    state = 0
    for l in lines("in1.txt"):
        if state == 0 and l.startswith(" 1"):
            state = 1
        elif state == 0:
            for i, crate in enumerate(range(1, len(l), 4)):
                if l[crate] != " ":
                    stacks[i].append(l[crate])
        elif state == 1:
            state = 2
        else:
            fr = string(" from ")
            to = string(" to ")
            num = regex(r"[0-9]+").map(int)
            crate = regex(r"[0-9]+").map(lambda x: int(x) - 1)
            ins = seq(num << fr, crate << to, crate)
            num, from_crate, to_crate = ins.parse(l.strip()[5:])
            moved = stacks[from_crate][:num]
            moved.reverse()
            stacks[from_crate] = stacks[from_crate][num:]
            stacks[to_crate] = moved + stacks[to_crate]

    print("".join([c[0] for c in stacks if len(c) > 0]))
