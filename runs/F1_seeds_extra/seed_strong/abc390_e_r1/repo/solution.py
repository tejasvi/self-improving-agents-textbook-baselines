import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    X = int(data[1])
    groups = [[], [], []]
    idx = 2
    for _ in range(n):
        v = int(data[idx]) - 1
        a = int(data[idx + 1])
        c = int(data[idx + 2])
        idx += 3
        groups[v].append((a, c))

    # dp[c] = max amount of vitamin v obtainable with total calories <= c
    dps = []
    for items in groups:
        dp = [0] * (X + 1)
        for a, c in items:
            if c > X:
                continue
            shifted = [x + a for x in dp[:X + 1 - c]]
            dp[c:] = map(max, dp[c:], shifted)
        dps.append(dp)

    def min_cost(dp, T):
        # smallest c with dp[c] >= T, or None
        if dp[X] < T:
            return None
        return bisect_left(dp, T)

    def feasible(T):
        if T == 0:
            return True
        total = 0
        for dp in dps:
            m = min_cost(dp, T)
            if m is None:
                return False
            total += m
            if total > X:
                return False
        return total <= X

    lo, hi = 0, min(dp[X] for dp in dps)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)


main()
