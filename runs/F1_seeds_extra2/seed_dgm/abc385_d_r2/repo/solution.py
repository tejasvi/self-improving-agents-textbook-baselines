import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    sx = int(data[2]); sy = int(data[3])
    xs = [0] * n
    ys = [0] * n
    p = 4
    for i in range(n):
        xs[i] = int(data[p]); ys[i] = int(data[p + 1]); p += 2

    K = 4 * 10 ** 9
    LIM = 10 ** 9
    # column index: sorted by (x, y); row index: sorted by (y, x)
    col_order = sorted(range(n), key=lambda i: (xs[i], ys[i]))
    row_order = sorted(range(n), key=lambda i: (ys[i], xs[i]))
    col_keys = [xs[i] * K + ys[i] for i in col_order]
    row_keys = [ys[i] * K + xs[i] for i in row_order]
    col_idx = [0] * n
    row_idx = [0] * n
    for j, i in enumerate(col_order):
        col_idx[i] = j
    for j, i in enumerate(row_order):
        row_idx[i] = j
    col_nxt = list(range(n + 1))
    row_nxt = list(range(n + 1))

    def find(nxt, i):
        r = i
        while nxt[r] != r:
            r = nxt[r]
        while nxt[i] != r:
            nxt[i], i = r, nxt[i]
        return r

    count = 0
    cx, cy = sx, sy
    for _ in range(m):
        d = data[p]; c = int(data[p + 1]); p += 2
        if d == b'U' or d == b'D':
            x = cx
            if d == b'U':
                y0, y1 = cy, cy + c
                cy = y1
            else:
                y0, y1 = cy - c, cy
                cy = y0
            lo = max(y0, -LIM); hi = min(y1, LIM)
            if lo > hi:
                continue
            if not (-LIM <= x <= LIM):
                continue
            base = x * K
            L = bisect_left(col_keys, base + lo)
            R = bisect_right(col_keys, base + hi)
            i = find(col_nxt, L)
            while i < R:
                h = col_order[i]
                count += 1
                col_nxt[i] = i + 1
                rj = row_idx[h]
                row_nxt[rj] = rj + 1
                i = find(col_nxt, i + 1)
        else:
            y = cy
            if d == b'R':
                x0, x1 = cx, cx + c
                cx = x1
            else:
                x0, x1 = cx - c, cx
                cx = x0
            lo = max(x0, -LIM); hi = min(x1, LIM)
            if lo > hi:
                continue
            if not (-LIM <= y <= LIM):
                continue
            base = y * K
            L = bisect_left(row_keys, base + lo)
            R = bisect_right(row_keys, base + hi)
            i = find(row_nxt, L)
            while i < R:
                h = row_order[i]
                count += 1
                row_nxt[i] = i + 1
                cj = col_idx[h]
                col_nxt[cj] = cj + 1
                i = find(row_nxt, i + 1)
    print(cx, cy, count)


main()
