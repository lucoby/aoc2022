from parsy import string, regex, forward_declaration, seq

from util import lines

if __name__ == '__main__':
    all_l = [l.strip() for l in list(lines("ex1.txt")) if l.strip()]
    print(all_l)

    s = string("[")
    e = string("]")
    num = regex(r"[0-9]+").map(int)
    sep = string(",")
    lis = forward_declaration()
    items = (sep.optional() >> (num | lis)).many()
    lis.become(s >> items << e)
    for l in all_l:
        print(lis.parse(l))
