import sys
from bisect import bisect_left, bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx+1]); sx = int(data[idx+2]); sy = int(data[idx+3])
    idx += 4
    X = [0]*n; Y = [0]*n
    for i in range(n):
        X[i] = int(data[idx]); Y[i] = int(data[idx+1]); idx += 2
    OFF = 1 << 31
    SH = 1 << 32
    LIM = 2 * 10**9
    def enc(a, b):
        # a, b already in range; shift to nonnegative
        return (a + OFF) * SH + (b + OFF)
    # row order: sort by (y,x)
    row_order = sorted(range(n), key=lambda i: (Y[i], X[i]))
    col_order = sorted(range(n), key=lambda i: (X[i], Y[i]))
    rowpos = [0]*n; colpos = [0]*n
    rowkeys = [0]*n; colkeys = [0]*n
    for p, h in enumerate(row_order):
        rowpos[h] = p
        rowkeys[p] = enc(Y[h], X[h])
    for p, h in enumerate(col_order):
        colpos[h] = p
        colkeys[p] = enc(X[h], Y[h])
    rpar = list(range(n+1))
    cpar = list(range(n+1))
    visited = [False]*n

    def find(par, x):
        root = x
        while par[root] != root:
            root = par[root]
        while par[x] != root:
            par[x], x = root, par[x]
        return root

    cx, cy = sx, sy
    count = 0
    for _ in range(m):
        d = data[idx]; c = int(data[idx+1]); idx += 2
        if d == b'U' or d == b'D':
            if d == b'U':
                ny = cy + c
            else:
                ny = cy - c
            lo = min(cy, ny); hi = max(cy, ny)
            lo = max(lo, -LIM); hi = min(hi, LIM)
            if lo <= hi:
                # column cx, y in [lo,hi]
                cxc = cx
                if -LIM <= cxc <= LIM:
                    kl = bisect_left(colkeys, enc(cxc, lo))
                    kr = bisect_right(colkeys, enc(cxc, hi))
                    i = find(cpar, kl)
                    while i < kr:
                        h = col_order[i]
                        visited[h] = True
                        count += 1
                        rp = rowpos[h]
                        rpar[rp] = rp + 1
                        cpar[i] = i + 1
                        i = find(cpar, i + 1)
            cy = ny
        else:
            if d == b'R':
                nx = cx + c
            else:
                nx = cx - c
            lo = min(cx, nx); hi = max(cx, nx)
            lo = max(lo, -LIM); hi = min(hi, LIM)
            if lo <= hi and -LIM <= cy <= LIM:
                kl = bisect_left(rowkeys, enc(cy, lo))
                kr = bisect_right(rowkeys, enc(cy, hi))
                i = find(rpar, kl)
                while i < kr:
                    h = row_order[i]
                    visited[h] = True
                    count += 1
                    cp = colpos[h]
                    cpar[cp] = cp + 1
                    rpar[i] = i + 1
                    i = find(rpar, i + 1)
            cx = nx
    print(cx, cy, count)

main()
