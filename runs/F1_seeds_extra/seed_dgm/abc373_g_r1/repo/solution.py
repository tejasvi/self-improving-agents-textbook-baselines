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

    R = [0] * n
    stack = [pts]
    while stack:
        sub = stack.pop()
        if not sub:
            continue
        # lowest point (min y, then min x)
        best = 0
        for k in range(1, len(sub)):
            if (sub[k][1], sub[k][0]) < (sub[best][1], sub[best][0]):
                best = k
        p = sub[best]
        others = sub[:best] + sub[best + 1:]
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
        found = -1
        for k, q in enumerate(others):
            if q[2] != p[2]:
                if bal == 0:
                    found = k
                    break
                bal -= 1
            else:
                bal += 1
        # found must exist
        q = others[found]
        if p[2] == 0:
            R[p[3]] = q[3] + 1
        else:
            R[q[3]] = p[3] + 1
        stack.append(others[:found])
        stack.append(others[found + 1:])

    sys.stdout.write(" ".join(map(str, R)) + "\n")


main()
