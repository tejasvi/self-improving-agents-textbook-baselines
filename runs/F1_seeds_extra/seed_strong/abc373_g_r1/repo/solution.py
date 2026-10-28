import sys
from functools import cmp_to_key

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    vals = list(map(int, data[1:]))
    pts = []
    for i in range(n):
        pts.append((vals[2*i], vals[2*i+1], 0, i))
    base = 2 * n
    for i in range(n):
        pts.append((vals[base+2*i], vals[base+2*i+1], 1, i))
    ans = [0] * n

    def cmp(a, b, ox, oy):
        ax, ay = a[0] - ox, a[1] - oy
        bx, by = b[0] - ox, b[1] - oy
        c = ax * by - ay * bx
        return -1 if c > 0 else (1 if c < 0 else 0)

    stack = [pts]
    while stack:
        cur = stack.pop()
        if not cur:
            continue
        # find lowest point (min y, then min x)
        mi = 0
        for j in range(1, len(cur)):
            if (cur[j][1], cur[j][0]) < (cur[mi][1], cur[mi][0]):
                mi = j
        o = cur[mi]
        others = cur[:mi] + cur[mi+1:]
        ox, oy = o[0], o[1]
        others.sort(key=cmp_to_key(lambda a, b: cmp(a, b, ox, oy)))
        f = 0
        k = -1
        for j, p in enumerate(others):
            if p[2] != o[2] and f == 0:
                k = j
                break
            f += 1 if p[2] == o[2] else -1
        p = others[k]
        if o[2] == 0:
            ans[o[3]] = p[3]
        else:
            ans[p[3]] = o[3]
        stack.append(others[:k])
        stack.append(others[k+1:])

    print(" ".join(str(x + 1) for x in ans))

main()
