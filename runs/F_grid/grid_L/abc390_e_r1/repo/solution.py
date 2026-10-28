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

    # g[v][c] = max units of vitamin v with total calories <= c
    gs = []
    for v in range(1, 4):
        dp = [0] * (X + 1)
        for a, c in groups[v]:
            if c > X:
                continue
            shifted = [x + a for x in dp[:X + 1 - c]]
            dp = dp[:c] + list(map(max, dp[c:], shifted))
        gs.append(dp)

    def feasible(T):
        total = 0
        for g in gs:
            if g[X] < T:
                return False
            h = bisect_left(g, T)
            total += h
            if total > X:
                return False
        return True

    lo, hi = 0, sum(a for v in range(1, 4) for a, _ in groups[v])
    # lo is always feasible (T=0 costs nothing)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)


main()
