import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    X = int(data[1])
    groups = {1: [], 2: [], 3: []}
    idx = 2
    for _ in range(n):
        v = int(data[idx]); a = int(data[idx + 1]); c = int(data[idx + 2])
        idx += 3
        groups[v].append((a, c))

    dps = []
    hi = None
    for v in (1, 2, 3):
        dp = [0] * (X + 1)
        total = 0
        for a, c in groups[v]:
            total += a
            if c > X:
                continue
            # 0/1 knapsack: dp[k] = max(dp[k], dp[k-c] + a), using old values
            shifted = [x + a for x in dp[:X + 1 - c]]
            dp[c:] = list(map(max, dp[c:], shifted))
        dps.append(dp)
        hi = total if hi is None else min(hi, total)

    INF = X + 1

    def feasible(m):
        if m == 0:
            return True
        s = 0
        for dp in dps:
            c = bisect_left(dp, m)  # dp is nondecreasing
            if c > X:
                return False
            s += c
            if s > X:
                return False
        return s <= X

    lo, high = 0, hi  # lo always feasible
    while lo < high:
        mid = (lo + high + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            high = mid - 1
    print(lo)


main()
