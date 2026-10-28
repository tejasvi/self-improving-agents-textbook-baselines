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

    # Row structure: sorted by (y, x)
    row_order = sorted(range(n), key=lambda i: (ys[i], xs[i]))
    row_keys = [(ys[i], xs[i]) for i in row_order]
    row_pos = [0] * n
    for k, i in enumerate(row_order):
        row_pos[i] = k
    # Column structure: sorted by (x, y)
    col_order = sorted(range(n), key=lambda i: (xs[i], ys[i]))
    col_keys = [(xs[i], ys[i]) for i in col_order]
    col_pos = [0] * n
    for k, i in enumerate(col_order):
        col_pos[i] = k

    rp = list(range(n + 1))  # next-unvisited DSU over row positions
    cp = list(range(n + 1))  # next-unvisited DSU over column positions

    def find(par, a):
        r = a
        while par[r] != r:
            r = par[r]
        while par[a] != r:
            par[a], a = r, par[a]
        return r

    visited = 0
    cx, cy = sx, sy
    for _ in range(m):
        d = data[p].decode(); c = int(data[p + 1]); p += 2
        if d == 'L' or d == 'R':
            if d == 'L':
                lo, hi = cx - c, cx
                nx = cx - c
            else:
                lo, hi = cx, cx + c
                nx = cx + c
            l = bisect_left(row_keys, (cy, lo))
            r = bisect_right(row_keys, (cy, hi))
            q = find(rp, l)
            while q < r:
                i = row_order[q]
                visited += 1
                rp[q] = q + 1
                cq = col_pos[i]
                cp[cq] = cq + 1
                q = find(rp, q + 1)
            cx = nx
        else:
            if d == 'D':
                lo, hi = cy - c, cy
                ny = cy - c
            else:
                lo, hi = cy, cy + c
                ny = cy + c
            l = bisect_left(col_keys, (cx, lo))
            r = bisect_right(col_keys, (cx, hi))
            q = find(cp, l)
            while q < r:
                i = col_order[q]
                visited += 1
                cp[q] = q + 1
                rq = row_pos[i]
                rp[rq] = rq + 1
                q = find(cp, q + 1)
            cy = ny
    print(cx, cy, visited)


main()
