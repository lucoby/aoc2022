def add_signal(cycle, x, signals):
    if cycle in signals:
        print(f"{x=}")
        print(f"{cycle=}")
        print("")
        return x * cycle
    else:
        return 0


if __name__ == '__main__':
    l = open("in1.txt").readlines()

    signals = set(list(range(20, 221, 40)))
    print(signals)

    ins_cnt = 0
    cycle = 1
    x = 1

    signal = 0

    while cycle < 220:
        ins = l[ins_cnt].strip()
        if ins == "noop":
            cycle += 1
            signal += add_signal(cycle, x, signals)
        else:
            cycle += 1
            signal += add_signal(cycle, x, signals)
            cycle += 1
            x += int(ins.strip().split(" ")[1])
            signal += add_signal(cycle, x, signals)

        ins_cnt += 1
    print(signal)
