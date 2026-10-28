import sys
from functools import cmp_to_key


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    vals = list(map(int, data[1:1 + 4 * n]))
    pts = []
    for i in range(n):
        pts.append((vals[2 * i], vals[2 * i + 1], 1, i))
    base = 2 * n
    for i in range(n):
        pts.append((vals[base + 2 * i], vals[base + 2 * i + 1], -1, i))

    R = [0] * n
    stack = [pts]
    while stack:
        cur = stack.pop()
        if not cur:
            continue
        # lowest point (min y, then min x)
        bi = 0
        for i in range(1, len(cur)):
            if (cur[i][1], cur[i][0]) < (cur[bi][1], cur[bi][0]):
                bi = i
        p = cur[bi]
        others = cur[:bi] + cur[bi + 1:]
        px, py = p[0], p[1]

        def cmp(a, b):
            ax, ay = a[0] - px, a[1] - py
            bx, by = b[0] - px, b[1] - py
            c = ax * by - ay * bx
            return -1 if c > 0 else (1 if c < 0 else 0)

        others.sort(key=cmp_to_key(cmp))
        s = p[2]
        # find j with type -s and prefix sum zero
        S = 0
        k = -1
        for j, q in enumerate(others):
            if q[2] == -s and S == 0:
                k = j
                break
            S += q[2]
        q = others[k]
        if p[2] == 1:
            R[p[3]] = q[3] + 1
        else:
            R[q[3]] = p[3] + 1
        stack.append(others[:k])
        stack.append(others[k + 1:])

    print(" ".join(map(str, R)))


main()
