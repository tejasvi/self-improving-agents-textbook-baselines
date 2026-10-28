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

    # horizontal order: by (y, x)
    hs = sorted(range(n), key=lambda i: (Y[i], X[i]))
    hkeys = [(Y[i], X[i]) for i in hs]
    hpos = [0] * n
    for p, i in enumerate(hs):
        hpos[i] = p
    # vertical order: by (x, y)
    vs = sorted(range(n), key=lambda i: (X[i], Y[i]))
    vkeys = [(X[i], Y[i]) for i in vs]
    vpos = [0] * n
    for p, i in enumerate(vs):
        vpos[i] = p

    hnext = list(range(n + 1))
    vnext = list(range(n + 1))

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
        d = data[idx]; c = int(data[idx + 1])
        idx += 2
        if d == b'R' or d == b'L':
            if d == b'R':
                nx = x + c
                lo, hi = x, nx
            else:
                nx = x - c
                lo, hi = nx, x
            # horizontal range on line y, x in [lo, hi]
            l = bisect_left(hkeys, (y, lo))
            r = bisect_right(hkeys, (y, hi))  # exclusive
            p = find(hnext, l)
            while p < r:
                i = hs[p]
                count += 1
                hnext[hpos[i]] = hpos[i] + 1
                vnext[vpos[i]] = vpos[i] + 1
                p = find(hnext, p + 1)
            x = nx
        else:
            if d == b'U':
                ny = y + c
                lo, hi = y, ny
            else:
                ny = y - c
                lo, hi = ny, y
            l = bisect_left(vkeys, (x, lo))
            r = bisect_right(vkeys, (x, hi))
            p = find(vnext, l)
            while p < r:
                i = vs[p]
                count += 1
                hnext[hpos[i]] = hpos[i] + 1
                vnext[vpos[i]] = vpos[i] + 1
                p = find(vnext, p + 1)
            y = ny
    print(x, y, count)


main()
