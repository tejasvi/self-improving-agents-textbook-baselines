import sys
from bisect import bisect_left


def knapsack(items, X):
    # f[c] = max total vitamin amount using calories at most c
    try:
        import numpy as np
        f = np.zeros(X + 1, dtype=np.int64)
        for a, c in items:
            if c > X:
                continue
            cand = f[:X + 1 - c] + a
            np.maximum(f[c:], cand, out=f[c:])
        return f.tolist()
    except ImportError:
        f = [0] * (X + 1)
        for a, c in items:
            if c > X:
                continue
            # new f[j] = max(f[j], f[j-c] + a) for j >= c; compute from old values
            shifted = [v + a for v in f[:X + 1 - c]]
            f[c:] = [x if x >= y else y for x, y in zip(f[c:], shifted)]
        return f


def main():
    data = sys.stdin.read().split()
    n, X = int(data[0]), int(data[1])
    groups = [[], [], []]
    idx = 2
    for _ in range(n):
        v = int(data[idx]); a = int(data[idx + 1]); c = int(data[idx + 2])
        idx += 3
        groups[v - 1].append((a, c))
    fs = [knapsack(g, X) for g in groups]
    totals = [sum(a for a, _ in g) for g in groups]

    def feasible(M):
        if M == 0:
            return True
        total = 0
        for f in fs:
            # first calorie budget c with f[c] >= M
            if f[X] < M:
                return False
            c = bisect_left(f, M)
            total += c
            if total > X:
                return False
        return total <= X

    lo, hi = 0, min(totals)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)


main()
