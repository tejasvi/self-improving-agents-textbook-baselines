import sys
from functools import cmp_to_key


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    pts = []
    pos = 1
    for i in range(n):
        x, y = int(data[pos]), int(data[pos + 1])
        pos += 2
        pts.append((x, y, 0, i))  # type 0: P
    for i in range(n):
        x, y = int(data[pos]), int(data[pos + 1])
        pos += 2
        pts.append((x, y, 1, i))  # type 1: Q

    ans = [0] * n

    # Divide and conquer: pick lowest point, sort others by angle,
    # find a point of opposite type that splits the rest into balanced halves.
    stack = [pts]
    while stack:
        cur = stack.pop()
        if not cur:
            continue
        # pivot: lowest (min y, then min x)
        best = 0
        for k in range(1, len(cur)):
            if (cur[k][1], cur[k][0]) < (cur[best][1], cur[best][0]):
                best = k
        p = cur[best]
        others = cur[:best] + cur[best + 1:]

        def cmp(a, b):
            cr = (a[0] - p[0]) * (b[1] - p[1]) - (a[1] - p[1]) * (b[0] - p[0])
            return -1 if cr > 0 else (1 if cr < 0 else 0)

        others.sort(key=cmp_to_key(cmp))
        bal = 0
        split = -1
        for k, q in enumerate(others):
            if q[2] != p[2]:
                if bal == 0:
                    split = k
                    break
                bal -= 1
            else:
                bal += 1
        # split must exist
        q = others[split]
        if p[2] == 0:
            ans[p[3]] = q[3] + 1
        else:
            ans[q[3]] = p[3] + 1
        stack.append(others[:split])
        stack.append(others[split + 1:])

    print(' '.join(map(str, ans)))


main()
