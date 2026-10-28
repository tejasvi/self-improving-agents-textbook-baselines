import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    n = int(data[p]); m = int(data[p + 1]); sx = int(data[p + 2]); sy = int(data[p + 3])
    p += 4
    X = [0] * n
    Y = [0] * n
    for i in range(n):
        X[i] = int(data[p]); Y[i] = int(data[p + 1]); p += 2

    # horizontal ordering: sorted by (y, x)
    horder = sorted(range(n), key=lambda i: (Y[i], X[i]))
    hkeys = [(Y[i], X[i]) for i in horder]
    hrank = [0] * n
    for pos, h in enumerate(horder):
        hrank[h] = pos
    # vertical ordering: sorted by (x, y)
    vorder = sorted(range(n), key=lambda i: (X[i], Y[i]))
    vkeys = [(X[i], Y[i]) for i in vorder]
    vrank = [0] * n
    for pos, h in enumerate(vorder):
        vrank[h] = pos

    hpar = list(range(n + 1))
    vpar = list(range(n + 1))

    def find(par, i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i

    count = 0
    cx, cy = sx, sy
    for _ in range(m):
        d = data[p]; c = int(data[p + 1]); p += 2
        if d == b'R' or d == b'L':
            nx = cx + c if d == b'R' else cx - c
            xl, xr = (cx, nx) if cx <= nx else (nx, cx)
            y = cy
            lo = bisect_left(hkeys, (y, xl))
            hi = bisect_right(hkeys, (y, xr))
            i = find(hpar, lo)
            while i < hi:
                h = horder[i]
                # visit h: remove from both structures
                hpar[i] = i + 1
                r = vrank[h]
                vpar[r] = r + 1
                count += 1
                i = find(hpar, i + 1)
            cx = nx
        else:
            ny = cy + c if d == b'U' else cy - c
            yl, yr = (cy, ny) if cy <= ny else (ny, cy)
            x = cx
            lo = bisect_left(vkeys, (x, yl))
            hi = bisect_right(vkeys, (x, yr))
            i = find(vpar, lo)
            while i < hi:
                h = vorder[i]
                vpar[i] = i + 1
                r = hrank[h]
                hpar[r] = r + 1
                count += 1
                i = find(vpar, i + 1)
            cy = ny
    print(cx, cy, count)


main()
