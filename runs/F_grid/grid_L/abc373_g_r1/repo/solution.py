import sys
from functools import cmp_to_key


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    vals = list(map(int, data[1:]))
    # point: (x, y, type, index); type 0 = P, 1 = Q
    pts = []
    for i in range(n):
        pts.append((vals[2 * i], vals[2 * i + 1], 0, i))
    base = 2 * n
    for i in range(n):
        pts.append((vals[base + 2 * i], vals[base + 2 * i + 1], 1, i))

    R = [0] * n
    stack = [pts]
    while stack:
        cur = stack.pop()
        if not cur:
            continue
        # pivot: lowest point (min y, then min x)
        best = 0
        for k in range(1, len(cur)):
            if (cur[k][1], cur[k][0]) < (cur[best][1], cur[best][0]):
                best = k
        o = cur[best]
        others = cur[:best] + cur[best + 1:]
        ox, oy = o[0], o[1]

        def cmp(a, b):
            ax, ay = a[0] - ox, a[1] - oy
            bx, by = b[0] - ox, b[1] - oy
            cr = ax * by - ay * bx
            if cr > 0:
                return -1
            if cr < 0:
                return 1
            return 0

        others.sort(key=cmp_to_key(cmp))
        s = o[2]
        cnt = 0
        found = -1
        for k, p in enumerate(others):
            if p[2] != s and cnt == 0:
                found = k
                break
            cnt += 1 if p[2] == s else -1
        # found must exist by counting argument
        p = others[found]
        if o[2] == 0:
            R[o[3]] = p[3]
        else:
            R[p[3]] = o[3]
        stack.append(others[:found])
        stack.append(others[found + 1:])

    print(" ".join(str(r + 1) for r in R))


main()
