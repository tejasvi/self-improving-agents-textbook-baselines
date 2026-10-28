import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    sx = int(data[2]); sy = int(data[3])
    X = [0] * n
    Y = [0] * n
    p = 4
    for i in range(n):
        X[i] = int(data[p]); Y[i] = int(data[p + 1]); p += 2

    # Horizontal order: by (y, x); vertical order: by (x, y). Store house ids.
    horder = sorted(range(n), key=lambda i: (Y[i], X[i]))
    vorder = sorted(range(n), key=lambda i: (X[i], Y[i]))
    hkeyY = [Y[i] for i in horder]
    hkeyX = [X[i] for i in horder]
    vkeyX = [X[i] for i in vorder]
    vkeyY = [Y[i] for i in vorder]

    # Skip structures: nxt[j] points to next position not yet "passed" in that direction.
    hnxt = list(range(n + 1))
    vnxt = list(range(n + 1))
    visited = [False] * n
    count = 0

    def find(nxt, i):
        root = i
        while nxt[root] != root:
            root = nxt[root]
        while nxt[i] != root:
            nxt[i], i = root, nxt[i]
        return root

    x, y = sx, sy
    for _ in range(m):
        d = data[p]; c = int(data[p + 1]); p += 2
        if d == b'U' or d == b'D':
            if d == b'U':
                y2 = y + c
            else:
                y2 = y - c
            lo, hi = (y, y2) if y <= y2 else (y2, y)
            # houses on column x with lo <= Y <= hi
            l = bisect_left(vkeyX, x)
            r = bisect_right(vkeyX, x)
            if l < r:
                l = bisect_left(vkeyY, lo, l, r)
                r = bisect_right(vkeyY, hi, l, r)
                j = find(vnxt, l)
                while j < r:
                    h = vorder[j]
                    if not visited[h]:
                        visited[h] = True
                        count += 1
                    vnxt[j] = j + 1
                    j = find(vnxt, j + 1)
            y = y2
        else:
            if d == b'R':
                x2 = x + c
            else:
                x2 = x - c
            lo, hi = (x, x2) if x <= x2 else (x2, x)
            # houses on row y with lo <= X <= hi
            l = bisect_left(hkeyY, y)
            r = bisect_right(hkeyY, y)
            if l < r:
                l = bisect_left(hkeyX, lo, l, r)
                r = bisect_right(hkeyX, hi, l, r)
                j = find(hnxt, l)
                while j < r:
                    h = horder[j]
                    if not visited[h]:
                        visited[h] = True
                        count += 1
                    hnxt[j] = j + 1
                    j = find(hnxt, j + 1)
            x = x2
    print(x, y, count)


main()
