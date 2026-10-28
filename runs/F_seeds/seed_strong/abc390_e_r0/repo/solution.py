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

    # best[v][c] = max units of vitamin v with total calories <= c (nondecreasing in c)
    bests = []
    for v in (1, 2, 3):
        dp = [0] * (X + 1)
        for a, c in groups[v]:
            if c > X:
                continue
            # dp[k] = max(dp[k], dp[k-c] + a) for k >= c
            shifted = list(map(a.__add__, dp[:X + 1 - c]))
            dp = dp[:c] + list(map(max, dp[c:], shifted))
        bests.append(dp)

    b1, b2, b3 = bests
    total_max = sum(a for v in (1, 2, 3) for a, _ in groups[v])

    def need(b, T):
        # smallest c with b[c] >= T, or None
        if b[X] < T:
            return None
        return bisect_left(b, T)

    def feasible(T):
        if T == 0:
            return True
        s = 0
        for b in (b1, b2, b3):
            m = need(b, T)
            if m is None:
                return False
            s += m
            if s > X:
                return False
        return s <= X

    lo, hi = 0, min(b1[X], b2[X], b3[X])
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)


main()
