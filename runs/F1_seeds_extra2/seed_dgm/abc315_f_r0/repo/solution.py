import sys
import math


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    xs = [int(data[1 + 2 * i]) for i in range(n)]
    ys = [int(data[2 + 2 * i]) for i in range(n)]

    # Upper bound: visiting every checkpoint in order.
    full = 0.0
    for i in range(n - 1):
        full += math.hypot(xs[i + 1] - xs[i], ys[i + 1] - ys[i])
    # Skipping C >= K+1 checkpoints costs 2^K at least; useless once 2^K > full.
    K = 0
    while (1 << K) <= full and K < n - 2:
        K += 1
    K = min(K + 1, n - 2) if n > 2 else 0
    # K is the max number of skipped checkpoints considered.
    INF = float("inf")
    # dp[i][c]: min distance to be at checkpoint i having skipped c checkpoints.
    dp = [[INF] * (K + 1) for _ in range(n)]
    dp[0][0] = 0.0
    for i in range(1, n):
        row = dp[i]
        xi, yi = xs[i], ys[i]
        for k in range(0, K + 1):
            j = i - k - 1
            if j < 0:
                break
            src = dp[j]
            d = math.hypot(xi - xs[j], yi - ys[j])
            for c in range(k, K + 1):
                v = src[c - k] + d
                if v < row[c]:
                    row[c] = v
    best = INF
    for c in range(K + 1):
        if dp[n - 1][c] == INF:
            continue
        pen = 0.0 if c == 0 else float(2 ** (c - 1))
        best = min(best, dp[n - 1][c] + pen)
    print("%.20f" % best)


main()
