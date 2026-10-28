import sys
from bisect import bisect_left


def main():
    data = sys.stdin.read().split()
    n, X = int(data[0]), int(data[1])
    groups = [[], [], [], []]
    idx = 2
    for _ in range(n):
        v = int(data[idx]); a = int(data[idx + 1]); c = int(data[idx + 2])
        idx += 3
        groups[v].append((a, c))

    # dp[v][c] = max total vitamin v with calories <= c (nondecreasing in c)
    dps = []
    for v in range(1, 4):
        dp = [0] * (X + 1)
        for a, c in groups[v]:
            if c > X:
                continue
            shifted = [x + a for x in dp[:X + 1 - c]]
            dp[c:] = map(max, dp[c:], shifted)
        dps.append(dp)

    INF = float('inf')

    def feasible(M):
        total = 0
        for dp in dps:
            if M == 0:
                continue
            if dp[X] < M:
                return False
            total += bisect_left(dp, M)
            if total > X:
                return False
        return total <= X

    lo, hi = 0, min(dp[X] for dp in dps)  # answer <= min of max achievable
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)


main()
