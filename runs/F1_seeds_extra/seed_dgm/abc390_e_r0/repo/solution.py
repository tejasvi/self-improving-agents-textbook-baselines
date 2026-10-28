import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    X = int(data[1])
    groups = [[], [], [], []]
    idx = 2
    for _ in range(n):
        v = int(data[idx]); a = int(data[idx + 1]); c = int(data[idx + 2])
        idx += 3
        groups[v].append((a, c))

    # f[v][c] = max amount of vitamin v using at most c calories (nondecreasing in c)
    fs = []
    for v in (1, 2, 3):
        dp = [0] * (X + 1)
        for a, c in groups[v]:
            if c > X:
                continue
            shifted = [x + a for x in dp[:X + 1 - c]]
            dp = dp[:c] + list(map(max, dp[c:], shifted))
        fs.append(dp)

    INF = float('inf')

    def min_cost(f, T):
        if T <= 0:
            return 0
        if f[X] < T:
            return INF
        return bisect_left(f, T)

    def feasible(T):
        total = 0
        for f in fs:
            c = min_cost(f, T)
            if c == INF:
                return False
            total += c
            if total > X:
                return False
        return total <= X

    lo, hi = 0, min(fs[0][X], fs[1][X], fs[2][X])
    # find max T with feasible(T); feasible(0) is always true
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)


main()
