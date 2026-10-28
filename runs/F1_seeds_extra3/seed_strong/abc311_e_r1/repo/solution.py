import sys
from itertools import accumulate
from operator import add, sub


def main():
    data = sys.stdin.buffer.read().split()
    H, W, N = int(data[0]), int(data[1]), int(data[2])
    holes = [[] for _ in range(H)]
    p = 3
    for _ in range(N):
        a = int(data[p]) - 1
        b = int(data[p + 1]) - 1
        p += 2
        holes[a].append(b)

    ones = [1] * W
    up = [0] * W          # consecutive unholed cells upward ending at current row
    prev = [0] * W        # dp of previous row
    total = 0
    for i in range(H):
        hs = holes[i]
        # up run
        up = list(map(add, up, ones))
        for b in hs:
            up[b] = 0
        # left run: j - (index of last hole at or before j), using 1-based positions
        mark = [0] * W
        for b in hs:
            mark[b] = b + 1
        last = list(accumulate(mark, max))
        left = list(map(sub, range(1, W + 1), last))
        # diagonal term: prev[j-1] + 1, with prev[-1] = 0
        diag = [1]
        diag.extend(map(add, prev[:-1], ones[1:]))
        cur = list(map(min, diag, up, left))
        total += sum(cur)
        prev = cur
    print(total)


main()
