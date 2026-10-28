import sys
from math import atan2


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    pts = []
    vals = data[1:]
    for i in range(2 * n):
        x = int(vals[2 * i])
        y = int(vals[2 * i + 1])
        pts.append((x, y))
    # type 0 = P (index i), type 1 = Q (index i - n)
    R = [0] * n
    stack = [list(range(2 * n))]
    while stack:
        group = stack.pop()
        if not group:
            continue
        # pivot: lowest y, then lowest x
        pi = min(group, key=lambda k: (pts[k][1], pts[k][0]))
        px, py = pts[pi]
        ptype = 0 if pi < n else 1
        others = [k for k in group if k != pi]
        others.sort(key=lambda k: atan2(pts[k][1] - py, pts[k][0] - px))
        bal = 0
        found = -1
        for idx, k in enumerate(others):
            ktype = 0 if k < n else 1
            if ktype != ptype and bal == 0:
                found = idx
                break
            bal += 1 if ktype == ptype else -1
        # found must exist by the balance argument
        k = others[found]
        if ptype == 0:
            R[pi] = k - n + 1
        else:
            R[k] = pi - n + 1
        stack.append(others[:found])
        stack.append(others[found + 1:])
    print(" ".join(map(str, R)))


main()
