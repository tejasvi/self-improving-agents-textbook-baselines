import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    sx, sy = int(data[2]), int(data[3])
    p = 4
    X = [0] * n
    Y = [0] * n
    for i in range(n):
        X[i] = int(data[p]); Y[i] = int(data[p + 1]); p += 2
    OFF = 10**9
    SH = 1 << 31

    def enc(a, b):
        return (a + OFF) * SH + (b + OFF)

    order_r = sorted(range(n), key=lambda i: (Y[i], X[i]))
    order_c = sorted(range(n), key=lambda i: (X[i], Y[i]))
    keyr = [enc(Y[i], X[i]) for i in order_r]
    keyc = [enc(X[i], Y[i]) for i in order_c]
    posc = [0] * n
    for j, h in enumerate(order_c):
        posc[h] = j
    posr = [0] * n
    for j, h in enumerate(order_r):
        posr[h] = j

    pr = list(range(n + 1))
    pc = list(range(n + 1))
    visited = [False] * n

    def find(par, i):
        root = i
        while par[root] != root:
            root = par[root]
        while par[i] != root:
            par[i], i = root, par[i]
        return root

    cnt = 0
    x, y = sx, sy
    for _ in range(m):
        d = data[p].decode(); c = int(data[p + 1]); p += 2
        if d == 'U' or d == 'D':
            if d == 'U':
                y2 = y + c
            else:
                y2 = y - c
            # vertical segment on column x, y in [lo, hi]
            lo, hi = (y, y2) if y <= y2 else (y2, y)
            if -OFF <= x <= OFF:
                lo_c = max(lo, -OFF); hi_c = min(hi, OFF)
                if lo_c <= hi_c:
                    l = bisect_left(keyc, enc(x, lo_c))
                    r = bisect_right(keyc, enc(x, hi_c))
                    i = find(pc, l)
                    while i < r:
                        h = order_c[i]
                        if not visited[h]:
                            visited[h] = True
                            cnt += 1
                            pr[posr[h]] = posr[h] + 1
                        pc[i] = i + 1
                        i = find(pc, i + 1)
            y = y2
        else:
            if d == 'R':
                x2 = x + c
            else:
                x2 = x - c
            lo, hi = (x, x2) if x <= x2 else (x2, x)
            if -OFF <= y <= OFF:
                lo_c = max(lo, -OFF); hi_c = min(hi, OFF)
                if lo_c <= hi_c:
                    l = bisect_left(keyr, enc(y, lo_c))
                    r = bisect_right(keyr, enc(y, hi_c))
                    i = find(pr, l)
                    while i < r:
                        h = order_r[i]
                        if not visited[h]:
                            visited[h] = True
                            cnt += 1
                            pc[posc[h]] = posc[h] + 1
                        pr[i] = i + 1
                        i = find(pr, i + 1)
            x = x2
    print(x, y, cnt)


main()
