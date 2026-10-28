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

    # f[v][c] = max vitamin v using calories <= c (nondecreasing in c)
    fs = []
    for v in range(1, 4):
        dp = [0] * (x + 1)
        for a, c in groups[v]:
            if c > x:
                continue
            shifted = [t + a for t in dp[:x + 1 - c]]
            dp[c:] = list(map(max, dp[c:], shifted))
        fs.append(dp)

    INF = float('inf')

    def min_cost(f, m):
        # smallest c with f[c] >= m, or INF
        if m == 0:
            return 0
        if f[x] < m:
            return INF
        return bisect_left(f, m)

    def feasible(m):
        total = 0
        for f in fs:
            c = min_cost(f, m)
            if c == INF:
                return False
            total += c
            if total > x:
                return False
        return total <= x

    lo, hi = 0, min(fs[0][x], fs[1][x], fs[2][x])
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)


main()
