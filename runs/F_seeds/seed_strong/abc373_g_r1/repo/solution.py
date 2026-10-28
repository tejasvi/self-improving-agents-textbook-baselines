import sys
from functools import cmp_to_key


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    vals = list(map(int, data[1:1 + 4 * n]))
    # points: (x, y, type, index); type 0 = P, 1 = Q
    pts = []
    for i in range(n):
        pts.append((vals[2 * i], vals[2 * i + 1], 0, i))
    base = 2 * n
    for i in range(n):
        pts.append((vals[base + 2 * i], vals[base + 2 * i + 1], 1, i))

    match = [0] * n  # match[p_index] = q_index

    stack = [pts]
    while stack:
        cur = stack.pop()
        if not cur:
            continue
        # lowest point (min y, then min x)
        best = 0
        for k in range(1, len(cur)):
            if (cur[k][1], cur[k][0]) < (cur[best][1], cur[best][0]):
                best = k
        p = cur[best]
        px, py, pt, pi = p
        others = [cur[k] for k in range(len(cur)) if k != best]

        def cmp(a, b):
            cr = (a[0] - px) * (b[1] - py) - (a[1] - py) * (b[0] - px)
            return -1 if cr > 0 else (1 if cr < 0 else 0)

        others.sort(key=cmp_to_key(cmp))
        c = 0
        found = -1
        for k, q in enumerate(others):
            if q[2] != pt:
                if c == 0:
                    found = k
                    break
                c -= 1
            else:
                c += 1
        # found must exist by the balance argument
        q = others[found]
        if pt == 0:
            match[pi] = q[3]
        else:
            match[q[3]] = pi
        stack.append(others[:found])
        stack.append(others[found + 1:])

    print(" ".join(str(match[i] + 1) for i in range(n)))


main()
