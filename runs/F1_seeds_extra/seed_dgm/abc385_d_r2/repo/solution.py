import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    sx, sy = int(data[2]), int(data[3])
    idx = 4
    xs = [0] * n
    ys = [0] * n
    for i in range(n):
        xs[i] = int(data[idx]); ys[i] = int(data[idx + 1]); idx += 2

    OFF = 10**9
    W = 1 << 31
    LIM = 10**9

    # Column order: sorted by (x, y); row order: sorted by (y, x)
    ordC = sorted(range(n), key=lambda i: (xs[i], ys[i]))
    ordR = sorted(range(n), key=lambda i: (ys[i], xs[i]))
    keysC = [(xs[i] + OFF) * W + (ys[i] + OFF) for i in ordC]
    keysR = [(ys[i] + OFF) * W + (xs[i] + OFF) for i in ordR]
    posC = [0] * n
    posR = [0] * n
    for p, i in enumerate(ordC):
        posC[i] = p
    for p, i in enumerate(ordR):
        posR[i] = p

    # DSU "next alive" arrays with sentinel at index n
    nxtC = list(range(n + 1))
    nxtR = list(range(n + 1))

    def find(nxt, p):
        root = p
        while nxt[root] != root:
            root = nxt[root]
        while nxt[p] != root:
            nxt[p], p = root, nxt[p]
        return root

    count = 0
    x, y = sx, sy
    for _ in range(m):
        d = data[idx].decode(); c = int(data[idx + 1]); idx += 2
        if d == 'U' or d == 'D':
            if d == 'U':
                ny = y + c
            else:
                ny = y - c
            lo, hi = (y, ny) if y <= ny else (ny, y)
            lo = max(lo, -LIM); hi = min(hi, LIM)
            if lo <= hi and -LIM <= x <= LIM:
                kx = (x + OFF) * W
                left = bisect_left(keysC, kx + (lo + OFF))
                right = bisect_right(keysC, kx + (hi + OFF))
                p = find(nxtC, left)
                while p < right:
                    h = ordC[p]
                    count += 1
                    nxtC[p] = p + 1
                    q = posR[h]
                    nxtR[q] = q + 1
                    p = find(nxtC, p + 1)
            y = ny
        else:
            if d == 'R':
                nx = x + c
            else:
                nx = x - c
            lo, hi = (x, nx) if x <= nx else (nx, x)
            lo = max(lo, -LIM); hi = min(hi, LIM)
            if lo <= hi and -LIM <= y <= LIM:
                ky = (y + OFF) * W
                left = bisect_left(keysR, ky + (lo + OFF))
                right = bisect_right(keysR, ky + (hi + OFF))
                p = find(nxtR, left)
                while p < right:
                    h = ordR[p]
                    count += 1
                    nxtR[p] = p + 1
                    q = posC[h]
                    nxtC[q] = q + 1
                    p = find(nxtR, p + 1)
            x = nx
    print(x, y, count)


main()
