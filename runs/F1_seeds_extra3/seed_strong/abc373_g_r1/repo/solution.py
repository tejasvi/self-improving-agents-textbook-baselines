import sys
from functools import cmp_to_key


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    pts = []
    idx = 1
    for i in range(n):
        x, y = int(data[idx]), int(data[idx + 1])
        idx += 2
        pts.append((x, y, 1, i))  # type 1 = P
    for i in range(n):
        x, y = int(data[idx]), int(data[idx + 1])
        idx += 2
        pts.append((x, y, -1, i))  # type -1 = Q
    res = [0] * n

    def solve(group):
        if not group:
            return
        # lowest point (min y, then min x)
        best = 0
        for j in range(1, len(group)):
            a = group[j]
            b = group[best]
            if (a[1], a[0]) < (b[1], b[0]):
                best = j
        p = group[best]
        others = group[:best] + group[best + 1:]
        px, py = p[0], p[1]

        def cmp(a, b):
            ax, ay = a[0] - px, a[1] - py
            bx, by = b[0] - px, b[1] - py
            c = ax * by - ay * bx
            return -1 if c > 0 else (1 if c < 0 else 0)

        others.sort(key=cmp_to_key(cmp))
        t = p[2]
        T = 0
        for i, q in enumerate(others):
            # T is prefix balance times t, before processing q
            if q[2] == -t and T == 0:
                # match p with q
                if t == 1:
                    res[p[3]] = q[3]
                else:
                    res[q[3]] = p[3]
                solve(others[:i])
                solve(others[i + 1:])
                return
            T += t * q[2]
        raise RuntimeError("no split found")

    solve(pts)
    print(" ".join(str(v + 1) for v in res))


main()
