import sys
import math


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    xs = [int(data[1 + 2 * i]) for i in range(n)]
    ys = [int(data[2 + 2 * i]) for i in range(n)]

    # Total length is < 1.5e8 < 2^28, so skipping more than ~30 checkpoints is never optimal.
    K = 32
    INF = float("inf")
    dp = [[INF] * (K + 1) for _ in range(n)]
    dp[0][0] = 0.0
    hypot = math.hypot
    for j in range(1, n):
        target = dp[j]
        xj = xs[j]
        yj = ys[j]
        for k in range(0, min(K, j - 1) + 1):
            i = j - 1 - k
            row = dp[i]
            d = hypot(xj - xs[i], yj - ys[i])
            lim = K + 1 - k
            for c in range(lim):
                v = row[c] + d
                if v < target[c + k]:
                    target[c + k] = v
    best = INF
    for c in range(K + 1):
        if dp[n - 1][c] == INF:
            continue
        pen = 0.0 if c == 0 else float(2 ** (c - 1))
        best = min(best, dp[n - 1][c] + pen)
    print("%.20f" % best)


main()
