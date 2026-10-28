import sys
from functools import cmp_to_key


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    vals = list(map(int, data[1:]))
    pts = []
    for i in range(n):
        pts.append((vals[2 * i], vals[2 * i + 1], 0, i))  # P: type 0
    for i in range(n):
        pts.append((vals[2 * n + 2 * i], vals[2 * n + 2 * i + 1], 1, i))  # Q: type 1
    R = [0] * n

    stack = [pts]
    while stack:
        cur = stack.pop()
        if not cur:
            continue
        # lowest point (min y, then min x) -> all others lie above it
        best = 0
        for k in range(1, len(cur)):
            if (cur[k][1], cur[k][0]) < (cur[best][1], cur[best][0]):
                best = k
        p = cur[best]
        rest = cur[:best] + cur[best + 1:]
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

        rest.sort(key=cmp_to_key(cmp))
        # walk: same type as p -> +1, opposite type -> -1; pick first opposite
        # point reached while the walk is at 0 (balanced prefix).
        s = 0
        idx = -1
        for k, q in enumerate(rest):
            if q[2] != p[2]:
                if s == 0:
                    idx = k
                    break
                s -= 1
            else:
                s += 1
        q = rest[idx]
        if p[2] == 0:
            R[p[3]] = q[3] + 1
        else:
            R[q[3]] = p[3] + 1
        stack.append(rest[:idx])
        stack.append(rest[idx + 1:])

    print(" ".join(map(str, R)))


main()
