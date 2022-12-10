import numpy as np

from util import lines, digitlines_as_np

if __name__ == '__main__':
    arr = digitlines_as_np("in1.txt")
    r, c = arr.shape
    max_scenic = 0

    for i in range(1, r-1):
        for j in range(1, c-1):
            up = 1
            while True:
                if i - up < 0:
                    up -= 1
                    break
                if arr[i - up, j] >= arr[i, j]:
                    break
                up += 1

            down = 1
            while True:
                if i + down >= r:
                    down -= 1
                    break
                if arr[i + down, j] >= arr[i, j]:
                    break
                down += 1

            left = 1
            while True:
                if j - left < 0:
                    left -= 1
                    break
                if arr[i, j - left] >= arr[i, j]:
                    break
                left += 1

            right = 1
            while True:
                if j + right >= c:
                    right -= 1
                    break
                if arr[i, j + right] >= arr[i, j]:
                    break
                right += 1

            scenic = left * right * up *down
            max_scenic = max(scenic, max_scenic)
    print(max_scenic)
