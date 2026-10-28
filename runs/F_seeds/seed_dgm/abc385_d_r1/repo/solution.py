import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    sx = int(data[2]); sy = int(data[3])
    p = 4
    X = [0] * n
    Y = [0] * n
    for i in range(n):
        X[i] = int(data[p]); Y[i] = int(data[p + 1]); p += 2

    LIM = 10 ** 9
    OFF = LIM
    W = 1 << 32  # > range of shifted coordinates (0..2e9)

    # vertical index: sorted by (x, y); horizontal index: sorted by (y, x)
    vkey = [((X[i] + OFF) * W + (Y[i] + OFF)) for i in range(n)]
    hkey = [((Y[i] + OFF) * W + (X[i] + OFF)) for i in range(n)]
    vorder = sorted(range(n), key=lambda i: vkey[i])
    horder = sorted(range(n), key=lambda i: hkey[i])
    vkeys = [vkey[i] for i in vorder]
    hkeys = [hkey[i] for i in horder]
    vpos = [0] * n
    hpos = [0] * n
    for j, i in enumerate(vorder):
        vpos[i] = j
    for j, i in enumerate(horder):
        hpos[i] = j
    # DSU "next alive" arrays with sentinel at n
    vpar = list(range(n + 1))
    hpar = list(range(n + 1))
    visited = [False] * n
    cnt = 0

    def find(par, j):
        r = j
        while par[r] != r:
            r = par[r]
        while par[j] != r:
            par[j], j = r, par[j]
        return r

    def sweep(keys, order, par, own_pos, other_par, other_pos, lo_key, hi_key):
        # returns count of newly visited houses in [lo_key, hi_key]
        nonlocal cnt
        l = bisect_left(keys, lo_key)
        r = bisect_right(keys, hi_key)
        j = find(par, l)
        c = 0
        while j < r:
            h = order[j]
            visited[h] = True
            c += 1
            par[j] = j + 1
            k = other_pos[h]
            other_par[k] = k + 1
            j = find(par, j + 1)
        return c

    cx, cy = sx, sy
    for _ in range(m):
        d = data[p].decode(); c = int(data[p + 1]); p += 2
        if d == 'U' or d == 'D':
            if d == 'U':
                y1, y2 = cy, cy + c
            else:
                y1, y2 = cy - c, cy
            ny = cy + c if d == 'U' else cy - c
            lo = max(y1, -LIM); hi = min(y2, LIM)
            if lo <= hi and -LIM <= cx <= LIM:
                base = (cx + OFF) * W
                cnt += sweep(vkeys, vorder, vpar, vpos, hpar, hpos,
                             base + (lo + OFF), base + (hi + OFF))
            cy = ny
        else:
            if d == 'R':
                x1, x2 = cx, cx + c
            else:
                x1, x2 = cx - c, cx
            nx = cx + c if d == 'R' else cx - c
            lo = max(x1, -LIM); hi = min(x2, LIM)
            if lo <= hi and -LIM <= cy <= LIM:
                base = (cy + OFF) * W
                cnt += sweep(hkeys, horder, hpar, hpos, vpar, vpos,
                             base + (lo + OFF), base + (hi + OFF))
            cx = nx
    print(cx, cy, cnt)


main()
