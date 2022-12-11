def update_crt(cycle, x):
    h_pos = cycle % 40
    if abs(h_pos - x) <= 1:
        return "#"
    else:
        return "."


if __name__ == '__main__':
    l = open("in1.txt").readlines()

    ins_cnt = 0
    cycle = 0
    x = 1

    crt = ["." for i in range(242)]

    while cycle < 240:
        ins = l[ins_cnt].strip()
        if ins == "noop":
            cycle += 1
            crt[cycle] = update_crt(cycle, x)
        else:
            cycle += 1
            crt[cycle] = update_crt(cycle, x)
            cycle += 1
            x += int(ins.strip().split(" ")[1])
            crt[cycle] = update_crt(cycle, x)

        ins_cnt += 1
    for i in range(6):
        print("".join(crt[i * 40:i * 40 + 40]))
