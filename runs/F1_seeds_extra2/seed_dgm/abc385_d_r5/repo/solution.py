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

    LIM = 10**9
    SH = 1 << 31

    def key_rc(a, b):
        # a: primary coord (+LIM offset), b: secondary coord (+LIM offset)
        return a * SH + b

    # Row order: sort by (y, x)
    row_order = sorted(range(n), key=lambda i: (Y[i], X[i]))
    row_keys = [key_rc(Y[i] + LIM, X[i] + LIM) for i in row_order]
    rpos = [0] * n
    for j, i in enumerate(row_order):
        rpos[i] = j
    # Column order: sort by (x, y)
    col_order = sorted(range(n), key=lambda i: (X[i], Y[i]))
    col_keys = [key_rc(X[i] + LIM, Y[i] + LIM) for i in col_order]
    cpos = [0] * n
    for j, i in enumerate(col_order):
        cpos[i] = j

    rpar = list(range(n + 1))
    cpar = list(range(n + 1))

    def find(par, x):
        root = x
        while par[root] != root:
            root = par[root]
        while par[x] != root:
            par[x], x = root, par[x]
        return root

    count = 0
    cx, cy = sx, sy
    for _ in range(m):
        d = data[p].decode(); c = int(data[p + 1]); p += 2
        if d == 'L' or d == 'R':
            if d == 'L':
                nx, ny = cx - c, cy
            else:
                nx, ny = cx + c, cy
            y = cy
            if -LIM <= y <= LIM:
                lo = max(min(cx, nx), -LIM)
                hi = min(max(cx, nx), LIM)
                if lo <= hi:
                    base = (y + LIM) * SH
                    a = bisect_left(row_keys, base + lo + LIM)
                    b = bisect_right(row_keys, base + hi + LIM)
                    j = find(rpar, a)
                    while j < b:
                        i = row_order[j]
                        count += 1
                        rpar[rpos[i]] = rpos[i] + 1
                        cpar[cpos[i]] = cpos[i] + 1
                        j = find(rpar, j + 1)
            cx, cy = nx, ny
        else:
            if d == 'U':
                nx, ny = cx, cy + c
            else:
                nx, ny = cx, cy - c
            x = cx
            if -LIM <= x <= LIM:
                lo = max(min(cy, ny), -LIM)
                hi = min(max(cy, ny), LIM)
                if lo <= hi:
                    base = (x + LIM) * SH
                    a = bisect_left(col_keys, base + lo + LIM)
                    b = bisect_right(col_keys, base + hi + LIM)
                    j = find(cpar, a)
                    while j < b:
                        i = col_order[j]
                        count += 1
                        rpar[rpos[i]] = rpos[i] + 1
                        cpar[cpos[i]] = cpos[i] + 1
                        j = find(cpar, j + 1)
            cx, cy = nx, ny
    print(cx, cy, count)


main()
