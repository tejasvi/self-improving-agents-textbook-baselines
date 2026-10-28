import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1])
    sx = int(data[idx + 2]); sy = int(data[idx + 3])
    idx += 4
    X = [0] * n
    Y = [0] * n
    for i in range(n):
        X[i] = int(data[idx]); Y[i] = int(data[idx + 1])
        idx += 2

    OFF = 10 ** 9
    SH = 31

    # Column structure: sorted by (x, y)
    order_c = sorted(range(n), key=lambda h: (X[h], Y[h]))
    keys_c = [((X[h] + OFF) << SH) | (Y[h] + OFF) for h in order_c]
    pos_c = [0] * n
    for i, h in enumerate(order_c):
        pos_c[h] = i
    par_c = list(range(n + 1))

    # Row structure: sorted by (y, x)
    order_r = sorted(range(n), key=lambda h: (Y[h], X[h]))
    keys_r = [((Y[h] + OFF) << SH) | (X[h] + OFF) for h in order_r]
    pos_r = [0] * n
    for i, h in enumerate(order_r):
        pos_r[h] = i
    par_r = list(range(n + 1))

    def find(p, par):
        while par[p] != p:
            par[p] = par[par[p]]
            p = par[p]
        return p

    count = 0

    def query_col(x, lo, hi):
        nonlocal count
        if x < -OFF or x > OFF:
            return
        lo = max(lo, -OFF); hi = min(hi, OFF)
        if lo > hi:
            return
        base = (x + OFF) << SH
        l = bisect_left(keys_c, base | (lo + OFF))
        r = bisect_right(keys_c, base | (hi + OFF))
        i = find(l, par_c)
        while i < r:
            h = order_c[i]
            count += 1
            par_c[i] = i + 1
            pr = pos_r[h]
            par_r[pr] = pr + 1
            i = find(i + 1, par_c)

    def query_row(y, lo, hi):
        nonlocal count
        if y < -OFF or y > OFF:
            return
        lo = max(lo, -OFF); hi = min(hi, OFF)
        if lo > hi:
            return
        base = (y + OFF) << SH
        l = bisect_left(keys_r, base | (lo + OFF))
        r = bisect_right(keys_r, base | (hi + OFF))
        i = find(l, par_r)
        while i < r:
            h = order_r[i]
            count += 1
            par_r[i] = i + 1
            pc = pos_c[h]
            par_c[pc] = pc + 1
            i = find(i + 1, par_r)

    cx, cy = sx, sy
    p = idx
    for _ in range(m):
        d = data[p]; c = int(data[p + 1]); p += 2
        if d == b'U':
            query_col(cx, cy, cy + c)
            cy += c
        elif d == b'D':
            query_col(cx, cy - c, cy)
            cy -= c
        elif d == b'L':
            query_row(cy, cx - c, cx)
            cx -= c
        else:
            query_row(cy, cx, cx + c)
            cx += c
    print(cx, cy, count)


main()
