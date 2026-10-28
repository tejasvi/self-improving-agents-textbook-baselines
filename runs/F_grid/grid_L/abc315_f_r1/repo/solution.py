import sys
import math


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    xs = [int(data[1 + 2 * i]) for i in range(n)]
    ys = [int(data[2 + 2 * i]) for i in range(n)]
    # Path length <= ~1.5e8 < 2^28, so skipping more than 29 checkpoints
    # (penalty >= 2^29) is never beneficial.
    K = 30
    INF = float("inf")
    dp = [[INF] * (K + 1) for _ in range(n)]
    dp[0][0] = 0.0
    for j in range(1, n):
        row = dp[j]
        xj, yj = xs[j], ys[j]
        for d in range(0, K + 1):
            i = j - d - 1
            if i < 0:
                break
            dist = math.hypot(xs[i] - xj, ys[i] - yj)
            src = dp[i]
            for c in range(d, K + 1):
                v = src[c - d] + dist
                if v < row[c]:
                    row[c] = v
    best = INF
    for c in range(K + 1):
        v = dp[n - 1][c]
        if v == INF:
            continue
        pen = 0.0 if c == 0 else 2.0 ** (c - 1)
        best = min(best, v + pen)
    print("%.20f" % best)


main()
