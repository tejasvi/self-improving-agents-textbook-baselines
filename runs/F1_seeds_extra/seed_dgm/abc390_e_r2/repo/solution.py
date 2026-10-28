import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    X = int(data[1])
    items = [[] for _ in range(4)]
    idx = 2
    for _ in range(n):
        v = int(data[idx]); a = int(data[idx + 1]); c = int(data[idx + 2])
        idx += 3
        items[v].append((a, c))

    dps = {}
    for v in (1, 2, 3):
        dp = [0] * (X + 1)
        for a, c in items[v]:
            if c > X:
                continue
            # 0/1 knapsack step: new[k] = max(dp[k], dp[k-c] + a), using old dp
            shifted = [x + a for x in dp[:X + 1 - c]]
            dp[c:] = list(map(max, dp[c:], shifted))
        dps[v] = dp  # nondecreasing in calorie budget

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

    lo, hi = 0, min(dps[1][X], dps[2][X], dps[3][X])
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)


main()
