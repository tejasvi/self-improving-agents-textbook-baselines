import sys
from functools import cmp_to_key


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    vals = list(map(int, data[1:]))
    pts = []
    for i in range(n):
        pts.append((vals[2 * i], vals[2 * i + 1], 0, i))  # P points, type 0
    base = 2 * n
    for i in range(n):
        pts.append((vals[base + 2 * i], vals[base + 2 * i + 1], 1, i))  # Q points, type 1

    R = [0] * n

    # Divide and conquer: take the lowest point (min y, then min x) as pivot,
    # sort the rest by polar angle around it, and find the first prefix where
    # the balance of types is zero and the next point is of opposite type.
    # Match pivot with that point and recurse on both sides.
    # Iterative with an explicit stack to avoid deep recursion issues.
    stack = [pts]
    while stack:
        cur = stack.pop()
        if not cur:
            continue
        pivot = min(cur, key=lambda p: (p[1], p[0]))
        px, py, pt, _ = pivot
        others = [p for p in cur if p is not pivot]

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
        bal = 0
        for k, q in enumerate(others):
            if q[2] != pt and bal == 0:
                # match pivot with q
                if pt == 0:
                    R[pivot[3]] = q[3] + 1
                else:
                    R[q[3]] = pivot[3] + 1
                stack.append(others[:k])
                stack.append(others[k + 1:])
                break
            bal += 1 if q[2] == pt else -1

    sys.stdout.write(" ".join(map(str, R)) + "\n")


main()
