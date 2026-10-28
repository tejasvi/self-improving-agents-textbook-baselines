import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    sx = int(data[2]); sy = int(data[3])
    p = 4
    xs = [0] * n
    ys = [0] * n
    for i in range(n):
        xs[i] = int(data[p]); ys[i] = int(data[p + 1]); p += 2

    LIM = 10**9
    OFF = LIM
    SH = 1 << 31

    # row order: sort by (y, x); column order: sort by (x, y)
    row_order = sorted(range(n), key=lambda i: (ys[i], xs[i]))
    col_order = sorted(range(n), key=lambda i: (xs[i], ys[i]))
    rowkeys = [(ys[i] + OFF) * SH + (xs[i] + OFF) for i in row_order]
    colkeys = [(xs[i] + OFF) * SH + (ys[i] + OFF) for i in col_order]
    rowpos = [0] * n
    colpos = [0] * n
    for j, i in enumerate(row_order):
        rowpos[i] = j
    for j, i in enumerate(col_order):
        colpos[i] = j
    # DSU "next alive" arrays with sentinel n
    rowpar = list(range(n + 1))
    colpar = list(range(n + 1))
    visited = [False] * n

    def find(par, x):
        root = x
        while par[root] != root:
            root = par[root]
        while par[x] != root:
            par[x], x = root, par[x]
        return root

    cx, cy = sx, sy
    count = 0
    for k in range(m):
        d = data[p]; c = int(data[p + 1]); p += 2
        if d == b'U' or d == b'D':
            if d == b'U':
                ny = cy + c
                lo, hi = cy, ny
            else:
                ny = cy - c
                lo, hi = ny, cy
            # vertical segment at x=cx, y in [lo,hi]
            if -LIM <= cx <= LIM:
                a = max(lo, -LIM); b = min(hi, LIM)
                if a <= b:
                    base = (cx + OFF) * SH
                    l = bisect_left(colkeys, base + (a + OFF))
                    r = bisect_right(colkeys, base + (b + OFF))
                    j = find(colpar, l)
                    while j < r:
                        h = col_order[j]
                        visited[h] = True
                        count += 1
                        colpar[j] = j + 1
                        rowpar[rowpos[h]] = rowpos[h] + 1
                        j = find(colpar, j + 1)
            cy = ny
        else:
            if d == b'R':
                nx = cx + c
                lo, hi = cx, nx
            else:
                nx = cx - c
                lo, hi = nx, cx
            # horizontal segment at y=cy, x in [lo,hi]
            if -LIM <= cy <= LIM:
                a = max(lo, -LIM); b = min(hi, LIM)
                if a <= b:
                    base = (cy + OFF) * SH
                    l = bisect_left(rowkeys, base + (a + OFF))
                    r = bisect_right(rowkeys, base + (b + OFF))
                    j = find(rowpar, l)
                    while j < r:
                        h = row_order[j]
                        visited[h] = True
                        count += 1
                        rowpar[j] = j + 1
                        colpar[colpos[h]] = colpos[h] + 1
                        j = find(rowpar, j + 1)
            cx = nx
    print(cx, cy, count)


main()
