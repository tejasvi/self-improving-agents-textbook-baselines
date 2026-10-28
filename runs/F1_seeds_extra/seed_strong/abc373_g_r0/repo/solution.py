import sys
from functools import cmp_to_key


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    vals = list(map(int, data[1:1 + 4 * n]))
    pts = []
    for i in range(n):
        pts.append((vals[2 * i], vals[2 * i + 1], 0, i))
    base = 2 * n
    for i in range(n):
        pts.append((vals[base + 2 * i], vals[base + 2 * i + 1], 1, i))

    res = [0] * n
    # iterative stack of point lists (each balanced: equal P and Q counts)
    stack = [pts]
    while stack:
        cur = stack.pop()
        if not cur:
            continue
        # lowest point (min y, then min x)
        best = 0
        for k in range(1, len(cur)):
            if (cur[k][1], cur[k][0]) < (cur[best][1], cur[best][0]):
                best = k
        p = cur[best]
        others = cur[:best] + cur[best + 1:]
        px, py = p[0], p[1]

        def cmp(a, b):
            ax, ay = a[0] - px, a[1] - py
            bx, by = b[0] - px, b[1] - py
            c = ax * by - ay * bx
            if c > 0:
                return -1
            if c < 0:
                return 1
            return 0

        others.sort(key=cmp_to_key(cmp))
        bal = 0
        for k, q in enumerate(others):
            if q[2] != p[2]:
                if bal == 0:
                    if p[2] == 0:
                        res[p[3]] = q[3]
                    else:
                        res[q[3]] = p[3]
                    stack.append(others[:k])
                    stack.append(others[k + 1:])
                    break
                bal += 1
            else:
                bal -= 1
    print(" ".join(str(r + 1) for r in res))


main()
