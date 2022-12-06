if __name__ == '__main__':
    with open("in1.txt") as f:
        l = f.read().strip()
        for i in range(len(l) - 4):
            if len(set(l[i:i+4])) == 4:
                print(i + 4)
                break
