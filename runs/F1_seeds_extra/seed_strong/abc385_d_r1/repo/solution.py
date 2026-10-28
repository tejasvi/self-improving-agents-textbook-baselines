import sys
from bisect import bisect_left, bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    sx = int(data[2]); sy = int(data[3])
    xs = [0] * n; ys = [0] * n
    p = 4
    for i in range(n):
        xs[i] = int(data[p]); ys[i] = int(data[p + 1]); p += 2

    # row structure: sorted by (y, x)
    rord = sorted(range(n), key=lambda i: (ys[i], xs[i]))
    rowX = [xs[i] for i in rord]
    rowHouse = rord
    rpos = [0] * n
    rowRange = {}
    for j, h in enumerate(rord):
        rpos[h] = j
        y = ys[h]
        if y in rowRange:
            rowRange[y][1] = j + 1
        else:
            rowRange[y] = [j, j + 1]

    # column structure: sorted by (x, y)
    cord = sorted(range(n), key=lambda i: (xs[i], ys[i]))
    colY = [ys[i] for i in cord]
    cpos = [0] * n
    colRange = {}
    for j, h in enumerate(cord):
        cpos[h] = j
        x = xs[h]
        if x in colRange:
            colRange[x][1] = j + 1
        else:
            colRange[x] = [j, j + 1]

    rpar = list(range(n + 1))
    cpar = list(range(n + 1))

    def find(par, i):
        root = i
        while par[root] != root:
            root = par[root]
        while par[i] != root:
            nxt = par[i]
            par[i] = root
            i = nxt
        return root

    count = 0
    x, y = sx, sy
    for _ in range(m):
        d = data[p]; c = int(data[p + 1]); p += 2
        if d == b'U' or d == b'D':
            if d == b'U':
                lo = y; hi = y + c; ny = y + c
            else:
                lo = y - c; hi = y; ny = y - c
            rng = colRange.get(x)
            if rng is not None:
                s, e = rng
                L = bisect_left(colY, lo, s, e)
                R = bisect_right(colY, hi, s, e)
                j = find(cpar, L)
                while j < R:
                    h = cord[j]
                    count += 1
                    cpar[j] = j + 1
                    k = rpos[h]
                    rpar[k] = k + 1
                    j = find(cpar, j + 1)
            y = ny
        else:
            if d == b'R':
                lo = x; hi = x + c; nx = x + c
            else:
                lo = x - c; hi = x; nx = x - c
            rng = rowRange.get(y)
            if rng is not None:
                s, e = rng
                L = bisect_left(rowX, lo, s, e)
                R = bisect_right(rowX, hi, s, e)
                j = find(rpar, L)
                while j < R:
                    h = rowHouse[j]
                    count += 1
                    rpar[j] = j + 1
                    k = cpos[h]
                    cpar[k] = k + 1
                    j = find(rpar, j + 1)
            x = nx
    print(x, y, count)

main()
