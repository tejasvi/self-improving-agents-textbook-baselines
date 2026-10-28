import sys
import math


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    xs = [int(data[1 + 2 * i]) for i in range(n)]
    ys = [int(data[2 + 2 * i]) for i in range(n)]
    # Skipping C checkpoints costs 2^(C-1), which must stay below the full
    # path length (<= ~1.5e8), so C <= 30 suffices.
    K = 30
    INF = float("inf")
    # dp[i][c]: min distance to reach checkpoint i (0-indexed) having skipped c checkpoints
    dp = [[INF] * (K + 1) for _ in range(n)]
    dp[0][0] = 0.0
    for i in range(1, n):
        row = dp[i]
        xi, yi = xs[i], ys[i]
        for k in range(0, min(K, i - 1) + 1):
            j = i - 1 - k
            d = math.hypot(xs[j] - xi, ys[j] - yi)
            src = dp[j]
            # transition: skip k checkpoints between j and i
            for c in range(K + 1 - k):
                v = src[c] + d
                if v < row[c + k]:
                    row[c + k] = v
    best = INF
    for c in range(K + 1):
        v = dp[n - 1][c]
        if v == INF:
            continue
        pen = 0.0 if c == 0 else 2.0 ** (c - 1)
        best = min(best, v + pen)
    print("%.20f" % best)


main()
