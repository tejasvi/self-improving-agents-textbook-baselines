import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    X = int(data[1])
    groups = [[], [], []]
    idx = 2
    for _ in range(n):
        v = int(data[idx]); a = int(data[idx + 1]); c = int(data[idx + 2])
        idx += 3
        groups[v - 1].append((c, a))

    # g[v][c] = max units of vitamin v using at most c calories (0/1 knapsack)
    gs = []
    for items in groups:
        dp = [0] * (X + 1)
        for c, a in items:
            if c > X:
                continue
            # new[j] = max(dp[j], dp[j-c] + a) for j >= c
            shifted = [x + a for x in dp[:X + 1 - c]]
            head = dp[:c]
            tail = dp[c:]
            dp = head + [x if x >= y else y for x, y in zip(tail, shifted)]
        gs.append(dp)

    INF = X + 1

    def need(g, m):
        # min calories c with g[c] >= m, or INF
        if m <= 0:
            return 0
        if g[-1] < m:
            return INF
        return bisect_left(g, m)

    lo, hi = 0, min(gs[0][-1], gs[1][-1], gs[2][-1])
    # feasibility is monotone decreasing in m; find max feasible m
    while lo < hi:
        mid = (lo + hi + 1) // 2
        total = need(gs[0], mid) + need(gs[1], mid) + need(gs[2], mid)
        if total <= X:
            lo = mid
        else:
            hi = mid - 1
    print(lo)


main()
