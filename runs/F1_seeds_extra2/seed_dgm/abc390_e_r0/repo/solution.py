import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n, X = int(data[0]), int(data[1])
    groups = [[], [], []]
    idx = 2
    for _ in range(n):
        v = int(data[idx]); a = int(data[idx + 1]); c = int(data[idx + 2])
        idx += 3
        groups[v - 1].append((a, c))

    # dp[v][c] = max amount of vitamin v with total calories <= c (0/1 knapsack)
    dps = []
    for items in groups:
        dp = [0] * (X + 1)
        for a, c in items:
            if c > X:
                continue
            shifted = [x + a for x in dp[:X + 1 - c]]
            dp = dp[:c] + list(map(max, dp[c:], shifted))
        dps.append(dp)

    INF = X + 1

    def min_cost(dp, t):
        if t <= 0:
            return 0
        i = bisect_left(dp, t)
        return i if i <= X else INF

    def feasible(t):
        total = 0
        for dp in dps:
            total += min_cost(dp, t)
            if total > X:
                return False
        return True

    lo, hi = 0, sum(a for items in groups for a, _ in items) + 1
    # invariant: feasible(lo) true, feasible(hi) false
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid
    print(lo)


main()
