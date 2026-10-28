import sys
from functools import cmp_to_key


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    vals = list(map(int, data[1:]))
    pts = []
    for i in range(n):
        pts.append((vals[2 * i], vals[2 * i + 1], 0, i))
    for i in range(n):
        pts.append((vals[2 * n + 2 * i], vals[2 * n + 2 * i + 1], 1, i))

    R = [0] * n

    # Divide and conquer: the set has equal numbers of P (type 0) and Q (type 1).
    # Pick the lowest point p, sort others by angle around p, and find a
    # point q of the opposite type such that the prefix before it is balanced.
    # Match p with q and recurse on both sides; segments never cross.
    stack = [pts]
    while stack:
        cur = stack.pop()
        if not cur:
            continue
        p = min(cur, key=lambda t: (t[1], t[0]))
        others = [t for t in cur if t is not p]
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
        d = 0
        for i, q in enumerate(others):
            if q[2] != p[2]:
                if d == 0:
                    if p[2] == 0:
                        R[p[3]] = q[3] + 1
                    else:
                        R[q[3]] = p[3] + 1
                    stack.append(others[:i])
                    stack.append(others[i + 1:])
                    break
                d -= 1
            else:
                d += 1

    print(" ".join(map(str, R)))


main()
