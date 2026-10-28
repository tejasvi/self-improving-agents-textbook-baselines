import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n, x = int(data[0]), int(data[1])
    groups = [[], [], [], []]
    idx = 2
    for _ in range(n):
        v = int(data[idx]); a = int(data[idx + 1]); c = int(data[idx + 2])
        idx += 3
        groups[v].append((a, c))

    # dp[c] = max vitamin amount obtainable with calories <= c (monotone non-decreasing)
    dps = []
    for v in (1, 2, 3):
        dp = [0] * (x + 1)
        for a, c in groups[v]:
            if c > x:
                continue
            shifted = [t + a for t in dp[: x + 1 - c]]
            dp[c:] = list(map(max, dp[c:], shifted))
        dps.append(dp)

    def feasible(t):
        total = 0
        for dp in dps:
            if dp[x] < t:
                return False
            # minimal calories c with dp[c] >= t (dp is non-decreasing)
            total += bisect_left(dp, t)
            if total > x:
                return False
        return total <= x

    lo, hi = 0, sum(a for g in groups for a, _ in g)
    # find max t with feasible(t); feasible(0) is always True
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)


main()
