import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1])
    sx = int(data[idx + 2]); sy = int(data[idx + 3])
    idx += 4
    xs = [0] * n
    ys = [0] * n
    for i in range(n):
        xs[i] = int(data[idx]); ys[i] = int(data[idx + 1])
        idx += 2

    OFF = 2 * 10**9
    BIG = 5 * 10**9
    LIM_LO = -10**9 - 1
    LIM_HI = 10**9 + 1

    # row order: sorted by (y, x); col order: sorted by (x, y)
    row_order = sorted(range(n), key=lambda i: (ys[i], xs[i]))
    col_order = sorted(range(n), key=lambda i: (xs[i], ys[i]))
    row_keys = [(ys[i] + OFF) * BIG + (xs[i] + OFF) for i in row_order]
    col_keys = [(xs[i] + OFF) * BIG + (ys[i] + OFF) for i in col_order]
    row_pos = [0] * n
    col_pos = [0] * n
    for j, h in enumerate(row_order):
        row_pos[h] = j
    for j, h in enumerate(col_order):
        col_pos[h] = j

    row_par = list(range(n + 1))
    col_par = list(range(n + 1))

    def find(par, i):
        r = i
        while par[r] != r:
            r = par[r]
        while par[i] != r:
            par[i], i = r, par[i]
        return r

    count = 0
    x, y = sx, sy
    for _ in range(m):
        d = data[idx].decode()
        c = int(data[idx + 1])
        idx += 2
        if d == 'U' or d == 'D':
            nx = x
            ny = y + c if d == 'U' else y - c
            lo, hi = (y, ny) if y <= ny else (ny, y)
            # vertical segment on column x, y range [lo,hi]
            if True:
                a = max(lo, LIM_LO); b = min(hi, LIM_HI)
                if a <= b and LIM_LO <= x <= LIM_HI:
                    base = (x + OFF) * BIG
                    l = bisect_left(col_keys, base + (a + OFF))
                    r = bisect_right(col_keys, base + (b + OFF))
                    j = find(col_par, l)
                    while j < r:
                        h = col_order[j]
                        count += 1
                        col_par[j] = j + 1
                        rp = row_pos[h]
                        row_par[rp] = rp + 1
                        j = find(col_par, j + 1)
            y = ny
        else:
            nx = x + c if d == 'R' else x - c
            ny = y
            lo, hi = (x, nx) if x <= nx else (nx, x)
            a = max(lo, LIM_LO); b = min(hi, LIM_HI)
            if a <= b and LIM_LO <= y <= LIM_HI:
                base = (y + OFF) * BIG
                l = bisect_left(row_keys, base + (a + OFF))
                r = bisect_right(row_keys, base + (b + OFF))
                j = find(row_par, l)
                while j < r:
                    h = row_order[j]
                    count += 1
                    row_par[j] = j + 1
                    cp = col_pos[h]
                    col_par[cp] = cp + 1
                    j = find(row_par, j + 1)
            x = nx
    print(x, y, count)


main()
