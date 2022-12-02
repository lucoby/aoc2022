from util import lines

if __name__ == '__main__':
    score = 0
    out_map = {"X": 0, "Y": 3, "Z": 6}
    loss_map = {"A": "C", "B": "A", "C": "B"}
    win_map = {"A": "B", "B": "C", "C": "A"}
    score_map = {"A": 1, "B": 2, "C": 3}

    for l in lines("in1.txt"):
        elf, out = l.strip().split(" ")
        score += out_map[out]
        if out == "X":
            score += score_map[loss_map[elf]]
        elif out == "Y":
            score += score_map[elf]
        else:
            score += score_map[win_map[elf]]

    print(score)
