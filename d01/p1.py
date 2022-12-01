from util import line_separated_int_list

if __name__ == '__main__':
    elves = line_separated_int_list("ex1.txt")
    elves = [sum(elf) for elf in elves]
    print(max(elves))
