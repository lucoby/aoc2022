from util import lines

if __name__ == '__main__':
    priority = 0
    for l in lines("in1.txt"):
        l = l.strip()
        p1 = set(l[:int(len(l)/2)])
        p2 = set(l[int(len(l)/2):])
        dupe = (p1 & p2).pop()
        if dupe.islower():
            score = ord(dupe) - ord("a") + 1
        else:
            score = ord(dupe) - ord("A") + 27
        print(score)
        priority += score
    print(priority)
