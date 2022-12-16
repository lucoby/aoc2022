import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FFMpegWriter, PillowWriter
from matplotlib.colors import ListedColormap

from util import lines


def init():
    pass


def update():
    pass

if __name__ == '__main__':
    all_max_x = 0
    all_max_y = 0
    paths = []
    for l in lines("in1.txt"):
        path = l.split(" -> ")
        path = [(int(c.split(",")[0]), int(c.split(",")[1])) for c in path]
        all_max_x = max(max([c[0] for c in path]), all_max_x)
        all_max_y = max(max([c[1] for c in path]), all_max_y)
        paths.append(path)

    arr = np.zeros((all_max_y + 3, all_max_x + 200))
    for p in paths:
        for i in range(1, len(p)):
            p0 = p[i - 1]
            p1 = p[i]

            min_y = min(p0[1], p1[1])
            max_y = max(p0[1], p1[1])
            min_x = min(p0[0], p1[0])
            max_x = max(p0[0], p1[0])

            arr[min_y:max_y + 1, min_x:max_x + 1] = 1

    arr[-1, :] = 1


    cmap = ListedColormap(["black", "brown"])
    fig, ax = plt.subplots()
    cmap.set_bad("white")
    moviewriter = FFMpegWriter()
    with moviewriter.saving(fig, "foo.mp4", dpi=100):
        all_sand = 0
        while True:
            sand = (0, 500)
            moved = True
            while moved:
                moved = False
                if sand[0] + 1 >= arr.shape[0]:
                    abyss = True
                    break
                elif not arr[sand[0] + 1, sand[1]]:
                    moved = True
                    sand = (sand[0] + 1, sand[1])
                elif not arr[sand[0] + 1, sand[1] - 1]:
                    moved = True
                    sand = (sand[0] + 1, sand[1] - 1)
                elif not arr[sand[0] + 1, sand[1] + 1]:
                    moved = True
                    sand = (sand[0] + 1, sand[1] + 1)

            arr[sand[0], sand[1]] = 2
            all_sand += 1
            if all_sand % 50 == 0:
                # anim_arr = np.copy(arr[:, 490:511])
                anim_arr = np.copy(arr[:, 319:682])
                anim_arr[anim_arr == 0] = np.nan
                ax.matshow(anim_arr, cmap=cmap)
                moviewriter.grab_frame()
                if all_sand % 5000 == 0:
                    print(all_sand)
            if sand == (0, 500):
                break



    moviewriter.finish()
    print(all_sand)

    _, c = arr.shape
    min_x = -1
    max_x = -1
    for i in range(c):
        if arr[:, i].sum() != 1 and min_x == -1:
            min_x = i
        elif arr[:, i].sum() != 1:
            max_x = i
