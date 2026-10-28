import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    sx = int(data[2]); sy = int(data[3])
    pos = 4
    X = [0] * n
    Y = [0] * n
    for i in range(n):
        X[i] = int(data[pos]); Y[i] = int(data[pos + 1]); pos += 2

    # Row order: sorted by (y, x); column order: sorted by (x, y)
    row_order = sorted(range(n), key=lambda i: (Y[i], X[i]))
    col_order = sorted(range(n), key=lambda i: (X[i], Y[i]))
    row_keys = [(Y[i], X[i]) for i in row_order]
    col_keys = [(X[i], Y[i]) for i in col_order]
    row_pos = [0] * n
    col_pos = [0] * n
    for p, i in enumerate(row_order):
        row_pos[i] = p
    for p, i in enumerate(col_order):
        col_pos[i] = p

    # DSU "next alive" arrays with sentinel at index n
    rpar = list(range(n + 1))
    cpar = list(range(n + 1))

    def find(par, a):
        r = a
        while par[r] != r:
            r = par[r]
        while par[a] != r:
            par[a], a = r, par[a]
        return r

    count = 0
    x, y = sx, sy
    for _ in range(m):
        d = data[pos].decode(); c = int(data[pos + 1]); pos += 2
        if d == 'U' or d == 'D':
            if d == 'U':
                ny = y + c; lo, hi = y, ny
            else:
                ny = y - c; lo, hi = ny, y
            # vertical move along column x, y in [lo, hi]
            l = bisect_left(col_keys, (x, lo))
            r = bisect_right(col_keys, (x, hi))
            i = find(cpar, l)
            while i < r:
                h = col_order[i]
                count += 1
                cpar[i] = i + 1
                rpar[row_pos[h]] = row_pos[h] + 1
                i = find(cpar, i + 1)
            y = ny
        else:
            if d == 'R':
                nx = x + c; lo, hi = x, nx
            else:
                nx = x - c; lo, hi = nx, x
            l = bisect_left(row_keys, (y, lo))
            r = bisect_right(row_keys, (y, hi))
            i = find(rpar, l)
            while i < r:
                h = row_order[i]
                count += 1
                rpar[i] = i + 1
                cpar[col_pos[h]] = col_pos[h] + 1
                i = find(rpar, i + 1)
            x = nx
    print(x, y, count)


main()
