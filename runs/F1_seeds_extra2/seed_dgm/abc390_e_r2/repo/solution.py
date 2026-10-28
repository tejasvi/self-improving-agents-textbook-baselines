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

    # f[v][c] = max amount of vitamin v with calorie budget <= c
    fs = []
    for v in range(1, 4):
        dp = [0] * (X + 1)
        for a, c in groups[v]:
            if c > X:
                continue
            shifted = [x + a for x in dp[:X + 1 - c]]
            dp[c:] = list(map(max, dp[c:], shifted))
        fs.append(dp)

    INF = X + 1

    def cost(f, m):
        # smallest c with f[c] >= m, or INF
        if m <= 0:
            return 0
        if f[X] < m:
            return INF
        return bisect_left(f, m)

    def feasible(m):
        total = 0
        for f in fs:
            total += cost(f, m)
            if total > X:
                return False
        return total <= X

    lo, hi = 0, sum(a for v in range(1, 4) for a, _ in groups[v]) + 1
    # lo is always feasible (m=0), hi is infeasible
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid
    print(lo)


main()
