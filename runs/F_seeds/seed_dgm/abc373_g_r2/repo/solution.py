import sys
from functools import cmp_to_key


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    vals = list(map(int, data[1:1 + 4 * n]))
    pts = []
    for i in range(n):
        pts.append((vals[2 * i], vals[2 * i + 1], 0, i))  # P points, type 0
    base = 2 * n
    for i in range(n):
        pts.append((vals[base + 2 * i], vals[base + 2 * i + 1], 1, i))  # Q points, type 1

    R = [0] * n

    def solve(group):
        # group: list of points with equal counts of type 0 and type 1
        if not group:
            return
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
            cr = ax * by - ay * bx
            if cr > 0:
                return -1
            if cr < 0:
                return 1
            return 0

        others.sort(key=cmp_to_key(cmp))
        t = p[2]
        cnt = 0
        for i, q in enumerate(others):
            if q[2] != t:
                if cnt == 0:
                    # match p with q; split
                    if p[2] == 0:
                        R[p[3]] = q[3]
                    else:
                        R[q[3]] = p[3]
                    solve(others[:i])
                    solve(others[i + 1:])
                    return
                cnt -= 1
            else:
                cnt += 1
        # Should not happen given balanced input

    solve(pts)
    print(" ".join(str(r + 1) for r in R))


main()
