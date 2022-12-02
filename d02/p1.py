from util import lines


if __name__ == '__main__':
    score = 0
    draw_map = {"X": "A", "Y": "B", "Z": "C"}
    win_map = {"X": "C", "Y": "A", "Z": "B"}
    score_map = {"X": 1, "Y": 2, "Z": 3}
    for l in lines("ex1.txt"):
        elf, me = l.strip().split(" ")
        score += score_map[me]
        if draw_map[me] == elf:
            score += 3
        elif win_map[me] == elf:
            score += 6

    print(score)
