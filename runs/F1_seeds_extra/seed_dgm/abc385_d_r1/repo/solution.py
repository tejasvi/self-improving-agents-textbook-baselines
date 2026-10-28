import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    sx = int(data[idx]); idx += 1
    sy = int(data[idx]); idx += 1
    xs = [0] * n
    ys = [0] * n
    for i in range(n):
        xs[i] = int(data[idx]); ys[i] = int(data[idx + 1]); idx += 2

    OFF = 10**9
    M2 = 2 * 10**9 + 1

    def enc(a, b):
        return (a + OFF) * M2 + (b + OFF)

    rowkey = [enc(ys[i], xs[i]) for i in range(n)]
    colkey = [enc(xs[i], ys[i]) for i in range(n)]
    orderR = sorted(range(n), key=lambda i: rowkey[i])
    orderC = sorted(range(n), key=lambda i: colkey[i])
    keysR = [rowkey[i] for i in orderR]
    keysC = [colkey[i] for i in orderC]
    posR = [0] * n
    posC = [0] * n
    for p, h in enumerate(orderR):
        posR[h] = p
    for p, h in enumerate(orderC):
        posC[h] = p
    nxtR = list(range(n + 1))
    nxtC = list(range(n + 1))

    def find(nxt, i):
        root = i
        while nxt[root] != root:
            root = nxt[root]
        while nxt[i] != root:
            nxt[i], i = root, nxt[i]
        return root

    count = 0
    x, y = sx, sy
    for _ in range(m):
        d = data[idx]; c = int(data[idx + 1]); idx += 2
        if d == b'U' or d == b'D':
            nx = x
            ny = y + c if d == b'U' else y - c
            # vertical segment on column x, y in [lo, hi]
            lo, hi = min(y, ny), max(y, ny)
            if -OFF <= x <= OFF:
                lo = max(lo, -OFF)
                hi = min(hi, OFF)
                if lo <= hi:
                    l = bisect_left(keysC, enc(x, lo))
                    r = bisect_right(keysC, enc(x, hi))
                    i = find(nxtC, l)
                    while i < r:
                        h = orderC[i]
                        count += 1
                        nxtC[i] = i + 1
                        p = posR[h]
                        nxtR[p] = p + 1
                        i = find(nxtC, i + 1)
            y = ny
        else:
            nx = x + c if d == b'R' else x - c
            ny = y
            lo, hi = min(x, nx), max(x, nx)
            if -OFF <= y <= OFF:
                lo = max(lo, -OFF)
                hi = min(hi, OFF)
                if lo <= hi:
                    l = bisect_left(keysR, enc(y, lo))
                    r = bisect_right(keysR, enc(y, hi))
                    i = find(nxtR, l)
                    while i < r:
                        h = orderR[i]
                        count += 1
                        nxtR[i] = i + 1
                        p = posC[h]
                        nxtC[p] = p + 1
                        i = find(nxtR, i + 1)
            x = nx
    print(x, y, count)


main()
