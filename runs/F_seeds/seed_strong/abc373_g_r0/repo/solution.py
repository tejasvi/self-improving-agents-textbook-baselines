import sys
from functools import cmp_to_key


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    vals = list(map(int, data[1:1 + 4 * n]))
    # point: (x, y, type, index); type 0 = P, 1 = Q
    pts = []
    for i in range(n):
        pts.append((vals[2 * i], vals[2 * i + 1], 0, i))
    off = 2 * n
    for i in range(n):
        pts.append((vals[off + 2 * i], vals[off + 2 * i + 1], 1, i))

    R = [0] * n
    stack = [pts]
    while stack:
        cur = stack.pop()
        if len(cur) == 0:
            continue
        # lowest (then leftmost) point
        best = 0
        for t in range(1, len(cur)):
            a = cur[t]
            b = cur[best]
            if a[1] < b[1] or (a[1] == b[1] and a[0] < b[0]):
                best = t
        L = cur[best]
        others = cur[:best] + cur[best + 1:]
        lx, ly = L[0], L[1]

        def cmp(p, q):
            c = (p[0] - lx) * (q[1] - ly) - (p[1] - ly) * (q[0] - lx)
            return -1 if c > 0 else (1 if c < 0 else 0)

        others.sort(key=cmp_to_key(cmp))
        s = 0
        k = -1
        for t, x in enumerate(others):
            if s == 0 and x[2] != L[2]:
                k = t
                break
            s += 1 if x[2] == L[2] else -1
        # k must exist by balance argument
        x = others[k]
        if L[2] == 0:
            R[L[3]] = x[3]
        else:
            R[x[3]] = L[3]
        stack.append(others[:k])
        stack.append(others[k + 1:])

    print(' '.join(str(r + 1) for r in R))


main()
