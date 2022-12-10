from dataclasses import dataclass
from typing import List, Any, Dict

from parsy import string, regex, seq

from util import lines

@dataclass
class Fi:
    name: str
    size: int

@dataclass
class Dir:
    name: str
    parent: str
    subdirs: Dict
    files: Dict
    total_size: int = 0

def add_total_size(parent):
    for d, dir in parent.subdirs.items():
        parent.total_size += add_total_size(dir)

    parent.total_size += sum([f.size for f in parent.files.values()])
    return parent.total_size


def get_total(parent):
    total = parent.total_size if parent.total_size <= 100000 else 0
    for d, dir in parent.subdirs.items():
        total += get_total(dir)
    return total

def find_min_dir(parent, need_to_free, cur_free):
    if parent.total_size < need_to_free:
        return float("inf")
    if parent.total_size < cur_free:
        cur_free = parent.total_size
    for d, dir in parent.subdirs.items():
        poss_free = find_min_dir(dir, need_to_free, cur_free)
        if poss_free < cur_free:
            cur_free = poss_free
    return cur_free

if __name__ == '__main__':
    root_dir = Dir(name="/", parent="/", subdirs={}, files={})
    cur = root_dir

    start_ins = string("$ ")
    cd = string("cd ")
    parent = string("..")
    subdir = regex(r"[a-zA-Z0-9_\.-]+")
    root = string("/")

    cd_ins = seq(start_ins >> cd, parent | subdir | root)

    ls = string("ls")
    ls_ins = seq(start_ins >> ls)

    dir = string("dir ")
    name = regex(r"[a-zA-Z0-9_\.-]+")
    size = regex(r"[0-9]+\s").map(lambda x: int(x.strip()))

    dir_ls = seq(dir, name)
    file_ls = seq(size, name)


    for l in lines("in1.txt"):
        print(l)
        parsed = (cd_ins | ls_ins | dir_ls | file_ls).parse(l.strip())
        print(parsed)
        if parsed[0] == "cd ":
            if parsed[1] == "/":
                cur = root_dir
            elif parsed[1] == "..":
                cur = cur.parent
            else:
                cur = cur.subdirs[parsed[1]]
        elif parsed[0] == "ls":
            pass
        elif parsed[0] == "dir ":
            cur.subdirs[parsed[1]] = Dir(name=parsed[1], parent=cur, subdirs={}, files={})
        else:
            cur.files[parsed[1]] = Fi(name=parsed[1], size=parsed[0])
        print(cur)

    add_total_size(root_dir)
    print(get_total(root_dir))
    print(free_up := 30000000 - (70000000 - root_dir.total_size))
    print(find_min_dir(root_dir, free_up, root_dir.total_size))
