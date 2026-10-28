import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    X = int(data[1])
    items = [[], [], [], []]
    idx = 2
    for _ in range(n):
        v = int(data[idx]); a = int(data[idx + 1]); c = int(data[idx + 2])
        idx += 3
        items[v].append((a, c))

    # g[v][c] = max amount of vitamin v using calories <= c (0/1 knapsack)
    gs = [None, None, None, None]
    for v in (1, 2, 3):
        dp = [0] * (X + 1)
        for a, c in items[v]:
            if c > X:
                continue
            shifted = [x + a for x in dp[:X + 1 - c]]
            dp[c:] = [x if x > y else y for x, y in zip(dp[c:], shifted)]
        gs[v] = dp  # nondecreasing in c

    def need(v, T):
        # minimal calories c with g_v[c] >= T, or infinity
        g = gs[v]
        if g[X] < T:
            return None
        return bisect_left(g, T)

    def feasible(T):
        total = 0
        for v in (1, 2, 3):
            if T == 0:
                continue
            c = need(v, T)
            if c is None:
                return False
            total += c
            if total > X:
                return False
        return total <= X

    lo, hi = 0, sum(a for v in (1, 2, 3) for a, _ in items[v])
    # find max T with feasible(T); feasible is monotone decreasing in T
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)


main()
