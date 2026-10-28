import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    x = int(data[1])
    groups = [[], [], [], []]
    idx = 2
    for _ in range(n):
        v = int(data[idx])
        a = int(data[idx + 1])
        c = int(data[idx + 2])
        idx += 3
        groups[v].append((a, c))

    INF = float("inf")
    g = [None, None, None, None]
    for v in (1, 2, 3):
        dp = [0] * (x + 1)  # dp[c] = max vitamin with calories <= c
        for a, c in groups[v]:
            if c > x:
                continue
            # 0/1 knapsack update, right-to-left semantics via slices
            shifted = dp[: x + 1 - c]
            new_part = [
                y + a if y + a > z else z
                for z, y in zip(dp[c:], shifted)
            ]
            dp[c:] = new_part
        g[v] = dp

    total = sum(a for v in (1, 2, 3) for a, _ in groups[v])

    def need(v, t):
        if t == 0:
            return 0
        arr = g[v]
        if arr[-1] < t:
            return INF
        return bisect_left(arr, t)

    def feasible(t):
        s = need(1, t) + need(2, t) + need(3, t)
        return s <= x

    lo, hi = 0, total  # lo always feasible
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)


main()
