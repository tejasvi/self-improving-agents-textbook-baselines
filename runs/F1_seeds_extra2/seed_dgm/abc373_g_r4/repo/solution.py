import sys
import math


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    vals = list(map(int, data[1:]))
    pts = []
    for i in range(n):
        # (x, y, type, index): P has type +1, Q has type -1
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
        # Pivot: lowest point (min y, then min x); all others lie in angle [0, pi)
        pi = min(range(len(cur)), key=lambda j: (cur[j][1], cur[j][0]))
        px, py, pt, pidx = cur[pi]
        others = [cur[j] for j in range(len(cur)) if j != pi]
        others.sort(key=lambda q: math.atan2(q[1] - py, q[0] - px))
        # First opposite-type point reached while the prefix sum is zero
        s = 0
        chosen = -1
        for k, q in enumerate(others):
            if q[2] == -pt and s == 0:
                chosen = k
                break
            s += q[2]
        q = others[chosen]
        if pt == 1:
            R[pidx] = q[3] + 1
        else:
            R[q[3]] = pidx + 1
        stack.append(others[:chosen])
        stack.append(others[chosen + 1:])
    print(" ".join(map(str, R)))


main()
