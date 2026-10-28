import sys
from functools import cmp_to_key


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    vals = list(map(int, data[1:1 + 4 * n]))
    pts = []
    for i in range(n):
        pts.append((vals[2 * i], vals[2 * i + 1], 0, i))  # P point, index i
    base = 2 * n
    for j in range(n):
        pts.append((vals[base + 2 * j], vals[base + 2 * j + 1], 1, j))  # Q point

    R = [0] * n
    stack = [pts]
    while stack:
        group = stack.pop()
        if not group:
            continue
        # lowest point (min y, then min x)
        best = 0
        for k in range(1, len(group)):
            g, b = group[k], group[best]
            if (g[1], g[0]) < (b[1], b[0]):
                best = k
        p = group[best]
        others = group[:best] + group[best + 1:]
        px, py = p[0], p[1]

        def cmp(a, b):
            ax, ay = a[0] - px, a[1] - py
            bx, by = b[0] - px, b[1] - py
            c = ax * by - ay * bx
            return -1 if c > 0 else (1 if c < 0 else 0)

        others.sort(key=cmp_to_key(cmp))
        bal = 0
        match_idx = -1
        for k, q in enumerate(others):
            if q[2] != p[2]:
                if bal == 0:
                    match_idx = k
                    break
                bal -= 1
            else:
                bal += 1
        q = others[match_idx]
        if p[2] == 0:
            R[p[3]] = q[3] + 1
        else:
            R[q[3]] = p[3] + 1
        stack.append(others[:match_idx])
        stack.append(others[match_idx + 1:])
    print(" ".join(map(str, R)))


main()
