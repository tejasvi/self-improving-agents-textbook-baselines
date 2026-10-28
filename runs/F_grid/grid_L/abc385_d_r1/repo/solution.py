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

    # Row ordering: sorted by (y, x)
    row_order = sorted(range(n), key=lambda i: (Y[i], X[i]))
    rpos = [0] * n
    row_xs = [0] * n
    row_range = {}  # y -> (start, end)
    for p, i in enumerate(row_order):
        rpos[i] = p
        row_xs[p] = X[i]
        y = Y[i]
        if y in row_range:
            s, _ = row_range[y]
            row_range[y] = (s, p + 1)
        else:
            row_range[y] = (p, p + 1)

    # Column ordering: sorted by (x, y)
    col_order = sorted(range(n), key=lambda i: (X[i], Y[i]))
    cpos = [0] * n
    col_ys = [0] * n
    col_range = {}
    for p, i in enumerate(col_order):
        cpos[i] = p
        col_ys[p] = Y[i]
        x = X[i]
        if x in col_range:
            s, _ = col_range[x]
            col_range[x] = (s, p + 1)
        else:
            col_range[x] = (p, p + 1)

    rpar = list(range(n + 1))
    cpar = list(range(n + 1))

    def find(par, a):
        root = a
        while par[root] != root:
            root = par[root]
        while par[a] != root:
            par[a], a = root, par[a]
        return root

    visited = 0

    def remove(i):
        rp = rpos[i]
        rpar[rp] = rp + 1
        cp = cpos[i]
        cpar[cp] = cp + 1

    def sweep_row(y, lo, hi):
        nonlocal visited
        rr = row_range.get(y)
        if rr is None:
            return
        s, e = rr
        a = bisect_left(row_xs, lo, s, e)
        b = bisect_right(row_xs, hi, s, e)
        if a >= b:
            return
        p = find(rpar, a)
        while p < b:
            i = row_order[p]
            visited += 1
            remove(i)
            p = find(rpar, p + 1)

    def sweep_col(x, lo, hi):
        nonlocal visited
        cr = col_range.get(x)
        if cr is None:
            return
        s, e = cr
        a = bisect_left(col_ys, lo, s, e)
        b = bisect_right(col_ys, hi, s, e)
        if a >= b:
            return
        p = find(cpar, a)
        while p < b:
            i = col_order[p]
            visited += 1
            remove(i)
            p = find(cpar, p + 1)

    cx, cy = sx, sy
    pos = idx
    for _ in range(m):
        d = data[pos].decode()
        c = int(data[pos + 1])
        pos += 2
        if d == 'U':
            sweep_col(cx, cy, cy + c)
            cy += c
        elif d == 'D':
            sweep_col(cx, cy - c, cy)
            cy -= c
        elif d == 'R':
            sweep_row(cy, cx, cx + c)
            cx += c
        else:  # 'L'
            sweep_row(cy, cx - c, cx)
            cx -= c

    print(cx, cy, visited)


main()
