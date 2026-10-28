import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    x = int(data[1])
    groups = [[], [], [], []]
    idx = 2
    for _ in range(n):
        v = int(data[idx]); a = int(data[idx + 1]); c = int(data[idx + 2])
        idx += 3
        groups[v].append((a, c))

    # g[v][c] = max units of vitamin v using total calories <= c
    gs = []
    for v in (1, 2, 3):
        g = [0] * (x + 1)
        for a, c in groups[v]:
            if c > x:
                continue
            # 0/1 knapsack step: new g[k] = max(g[k], g[k-c] + a) for k >= c
            g = g[:c] + [p if p > q + a else q + a
                         for p, q in zip(g[c:], g)]
        gs.append(g)

    def feasible(t):
        total = 0
        for g in gs:
            if t == 0:
                continue
            i = bisect_left(g, t)
            if i > x:
                return False
            total += i
            if total > x:
                return False
        return total <= x

    lo, hi = 0, sum(a for v in groups for a, _ in v)
    # find max t with feasible(t); feasible is monotone decreasing in t
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)


main()
