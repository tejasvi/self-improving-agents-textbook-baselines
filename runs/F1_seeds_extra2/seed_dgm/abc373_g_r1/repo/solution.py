import sys
from functools import cmp_to_key


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    pts = []
    vals = list(map(int, data[1:]))
    for i in range(2 * n):
        pts.append((vals[2 * i], vals[2 * i + 1]))
    # type 0: P (index i), type 1: Q (index n + j)
    typ = [0] * n + [1] * n
    R = [0] * n

    stack = [list(range(2 * n))]
    while stack:
        items = stack.pop()
        if len(items) <= 1:
            continue
        # lowest (then leftmost) point
        p = min(items, key=lambda k: (pts[k][1], pts[k][0]))
        px, py = pts[p]
        others = [k for k in items if k != p]

        def cmp(a, b):
            ax, ay = pts[a][0] - px, pts[a][1] - py
            bx, by = pts[b][0] - px, pts[b][1] - py
            c = ax * by - ay * bx
            return -1 if c > 0 else (1 if c < 0 else 0)

        others.sort(key=cmp_to_key(cmp))
        tp = typ[p]
        bal = 0
        found = -1
        for idx, k in enumerate(others):
            if typ[k] != tp:
                if bal == 0:
                    found = idx
                    break
                bal -= 1
            else:
                bal += 1
        # found must exist by the balance argument
        q = others[found]
        if tp == 0:
            R[p] = q - n + 1
        else:
            R[q] = p - n + 1
        left = others[:found]
        right = others[found + 1:]
        stack.append(left)
        stack.append(right)

    print(" ".join(map(str, R)))


main()
