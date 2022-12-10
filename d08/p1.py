import numpy as np

from util import lines, digitlines_as_np

if __name__ == '__main__':
    arr = digitlines_as_np("in1.txt")
    r, c = arr.shape

    visible = np.zeros((r, c))

    visible[0, :] = 1
    visible[-1, :] = 1
    visible[:, 0] = 1
    visible[:, -1] = 1

    for i in range(1, r-1):
        left = arr[i, 0]
        right = arr[i, -1]
        for j in range(1, c-1):
            curr_l = arr[i, j]
            curr_r = arr[i, -j - 1]
            visible[i, j] = visible[i, j] or curr_l > left
            visible[i, -j - 1] = visible[i, -j-1] or curr_r > right
            left = max(left, curr_l)
            right = max(right, curr_r)

    for j in range(1, c-1):
        top = arr[0, j]
        bottom = arr[-1, j]
        for i in range(1, r-1):
            curr_t = arr[i, j]
            curr_b = arr[-i - 1, j]
            visible[i, j] = visible[i, j] or curr_t > top
            visible[-i -1, j] = visible[-i-1, j ] or curr_b > bottom
            top = max(top, curr_t)
            bottom = max(bottom, curr_b)

    print(visible)
    print(visible.sum())
