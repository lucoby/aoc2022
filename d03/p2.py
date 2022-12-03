if __name__ == '__main__':
    priority = 0
    with open("in1.txt") as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
        for i in range(0, len(lines), 3):
            badge = (set(lines[i]) & set(lines[i + 1]) & set(lines[i + 2])).pop()
            if badge.islower():
                score = ord(badge) - ord("a") + 1
            else:
                score = ord(badge) - ord("A") + 27
            print(score)
            priority += score
    print(priority)
