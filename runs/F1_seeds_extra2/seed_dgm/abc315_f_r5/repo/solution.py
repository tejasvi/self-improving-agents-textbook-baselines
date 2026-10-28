import sys
import math


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    xs = [int(data[1 + 2 * i]) for i in range(n)]
    ys = [int(data[2 + 2 * i]) for i in range(n)]
    # Skipping more than ~30 checkpoints costs >= 2^29 > max possible path length,
    # so the total number of skipped checkpoints is bounded by K.
    K = 30
    INF = float("inf")
    # dp[j][c]: min distance reaching checkpoint j having skipped c checkpoints
    dp = [[INF] * (K + 1) for _ in range(n)]
    dp[0][0] = 0.0
    for j in range(1, n):
        row = dp[j]
        xj, yj = xs[j], ys[j]
        for d in range(0, K + 1):
            i = j - 1 - d  # skipped checkpoints between i and j: d
            if i < 0:
                break
            dx = xs[i] - xj
            dy = ys[i] - yj
            w = math.sqrt(dx * dx + dy * dy)
            src = dp[i]
            for c in range(0, K + 1 - d):
                v = src[c]
                if v == INF:
                    continue
                v += w
                if v < row[c + d]:
                    row[c + d] = v
    best = INF
    for c in range(K + 1):
        v = dp[n - 1][c]
        if v == INF:
            continue
        pen = 0.0 if c == 0 else float(2 ** (c - 1))
        best = min(best, v + pen)
    print("%.20f" % best)


main()
