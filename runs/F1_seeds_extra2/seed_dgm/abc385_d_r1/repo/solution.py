import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    n = int(data[pos]); m = int(data[pos + 1])
    sx = int(data[pos + 2]); sy = int(data[pos + 3])
    pos += 4
    X = [0] * n
    Y = [0] * n
    for i in range(n):
        X[i] = int(data[pos]); Y[i] = int(data[pos + 1])
        pos += 2

    # vertical order: sorted by (x, y); horizontal order: sorted by (y, x)
    vord = sorted(range(n), key=lambda i: (X[i], Y[i]))
    hord = sorted(range(n), key=lambda i: (Y[i], X[i]))
    posV = [0] * n
    posH = [0] * n
    for idx, h in enumerate(vord):
        posV[h] = idx
    for idx, h in enumerate(hord):
        posH[h] = idx
    vkeys = [(X[h], Y[h]) for h in vord]
    hkeys = [(Y[h], X[h]) for h in hord]
    # DSU "next alive" arrays of size n+1
    parV = list(range(n + 1))
    parH = list(range(n + 1))

    def find(par, i):
        root = i
        while par[root] != root:
            root = par[root]
        while par[i] != root:
            par[i], i = root, par[i]
        return root

    count = 0
    x, y = sx, sy

    def visit_range(par, order, other_par, other_pos, lo, hi):
        # remove all alive houses in order[lo:hi]; returns number removed
        nonlocal count
        i = find(par, lo)
        while i < hi:
            h = order[i]
            count += 1
            par[i] = i + 1
            other_par[other_pos[h]] = other_pos[h] + 1
            i = find(par, i + 1)

    for _ in range(m):
        d = data[pos]; c = int(data[pos + 1])
        pos += 2
        if d == b'U' or d == b'D':
            if d == b'U':
                ylo, yhi = y, y + c
                ny = y + c
            else:
                ylo, yhi = y - c, y
                ny = y - c
            lo = bisect_left(vkeys, (x, ylo))
            hi = bisect_right(vkeys, (x, yhi))
            if lo < hi:
                visit_range(parV, vord, parH, posH, lo, hi)
            y = ny
        else:
            if d == b'R':
                xlo, xhi = x, x + c
                nx = x + c
            else:
                xlo, xhi = x - c, x
                nx = x - c
            lo = bisect_left(hkeys, (y, xlo))
            hi = bisect_right(hkeys, (y, xhi))
            if lo < hi:
                visit_range(parH, hord, parV, posV, lo, hi)
            x = nx

    print(x, y, count)


main()
