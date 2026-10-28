import sys
import math


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    xs = [int(data[1 + 2 * i]) for i in range(n)]
    ys = [int(data[2 + 2 * i]) for i in range(n)]
    # Any solution skipping C checkpoints costs >= 2^(C-1), while skipping
    # nothing costs at most ~1.42e8 < 2^28, so C <= 28 always suffices.
    K = 30
    INF = float("inf")
    dp = [[INF] * (K + 1) for _ in range(n)]
    dp[0][0] = 0.0
    for i in range(1, n):
        xi, yi = xs[i], ys[i]
        row = dp[i]
        for k in range(1, min(i, K + 1) + 1):
            j = i - k  # checkpoints j+1..i-1 skipped (k-1 of them)
            cost = math.hypot(xi - xs[j], yi - ys[j])
            m = K + 2 - k  # number of valid skip counts from j
            src = dp[j][:m]
            off = k - 1
            seg = row[off:off + m]
            row[off:off + m] = [a if a < b + cost else b + cost
                                for a, b in zip(seg, src)]
    best = INF
    for c in range(K + 1):
        v = dp[n - 1][c]
        if v == INF:
            continue
        pen = 0.0 if c == 0 else 2.0 ** (c - 1)
        best = min(best, v + pen)
    print("%.20f" % best)


main()
