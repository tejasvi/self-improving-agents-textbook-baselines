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

    # dp[v][c] = max total of vitamin v using calories <= c (0/1 knapsack)
    dps = [None, None, None, None]
    for v in (1, 2, 3):
        dp = [0] * (X + 1)
        for a, c in items[v]:
            if c > X:
                continue
            shifted = [y + a for y in dp[:X + 1 - c]]
            dp[c:] = map(max, dp[c:], shifted)
        dps[v] = dp


    def feasible(T):
        total = 0
        for v in (1, 2, 3):
            if T == 0:
                continue
            dp = dps[v]
            if dp[X] < T:
                return False
            total += bisect_left(dp, T)
            if total > X:
                return False
        return total <= X

    lo, hi = 0, sum(a for v in (1, 2, 3) for a, _ in items[v]) + 1
    # hi is infeasible (exceeds any achievable total for some vitamin)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid
    print(lo)


main()
