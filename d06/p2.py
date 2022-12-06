if __name__ == '__main__':
    with open("in1.txt") as f:
        l = f.read().strip()
        for i in range(len(l) - 14):
            if len(set(l[i:i+14])) == 14:
                print(i + 14)
                break
