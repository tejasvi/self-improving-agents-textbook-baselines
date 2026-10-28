import sys
from collections import defaultdict


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    vals = list(map(int, data[1:1 + 6 * n]))
    lo = []
    hi = []
    for i in range(n):
        b = 6 * i
        lo.append((vals[b], vals[b + 1], vals[b + 2]))
        hi.append((vals[b + 3], vals[b + 4], vals[b + 5]))
    ans = [0] * n
    for d in range(3):
        p, q = [k for k in range(3) if k != d]
        plus = defaultdict(list)   # plane c -> cuboids whose hi[d] == c
        minus = defaultdict(list)  # plane c -> cuboids whose lo[d] == c
        for i in range(n):
            plus[hi[i][d]].append(i)
            minus[lo[i][d]].append(i)
        for c, bs in minus.items():
            as_ = plus.get(c)
            if not as_:
                continue
            grid = [-1] * 10000
            for a in as_:
                p1, p2 = lo[a][p], hi[a][p]
                q1, q2 = lo[a][q], hi[a][q]
                w = q2 - q1
                fill = [a] * w
                for x in range(p1, p2):
                    base = x * 100 + q1
                    grid[base:base + w] = fill
            for b in bs:
                p1, p2 = lo[b][p], hi[b][p]
                q1, q2 = lo[b][q], hi[b][q]
                w = q2 - q1
                S = set()
                for x in range(p1, p2):
                    base = x * 100 + q1
                    S.update(grid[base:base + w])
                S.discard(-1)
                if S:
                    ans[b] += len(S)
                    for a in S:
                        ans[a] += 1
    sys.stdout.write("\n".join(map(str, ans)) + "\n")


main()
