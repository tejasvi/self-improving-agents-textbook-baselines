import sys
from functools import cmp_to_key


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    vals = list(map(int, data[1:1 + 4 * n]))
    # points: (x, y, color, index); color 0 = P, 1 = Q
    pts = []
    for i in range(n):
        pts.append((vals[2 * i], vals[2 * i + 1], 0, i))
    base = 2 * n
    for j in range(n):
        pts.append((vals[base + 2 * j], vals[base + 2 * j + 1], 1, j))

    R = [0] * n
    stack = [pts]
    while stack:
        S = stack.pop()
        if not S:
            continue
        # pivot: lowest y, then lowest x
        pi = min(range(len(S)), key=lambda k: (S[k][1], S[k][0]))
        p = S[pi]
        others = [S[k] for k in range(len(S)) if k != pi]
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
        v = 0
        match_idx = -1
        for k, q in enumerate(others):
            if v == 0 and q[2] != p[2]:
                match_idx = k
                break
            v += 1 if q[2] == 0 else -1
        q = others[match_idx]
        if p[2] == 0:
            R[p[3]] = q[3] + 1
        else:
            R[q[3]] = p[3] + 1
        left = others[:match_idx]
        right = others[match_idx + 1:]
        stack.append(left)
        stack.append(right)

    print(" ".join(map(str, R)))


main()
