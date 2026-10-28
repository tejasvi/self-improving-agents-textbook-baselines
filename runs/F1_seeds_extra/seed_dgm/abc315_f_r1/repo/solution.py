import sys
import math


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    xs = [int(data[1 + 2 * i]) for i in range(n)]
    ys = [int(data[2 + 2 * i]) for i in range(n)]

    # Skipping C checkpoints costs 2^(C-1); total distance <= ~1.5e8 < 2^28,
    # so C never needs to exceed ~30.
    K = 30
    INF = float("inf")
    # dp[i][c]: min distance from checkpoint 0 to checkpoint i (visited),
    # with c checkpoints skipped so far.
    dp = [[INF] * (K + 1) for _ in range(n)]
    dp[0][0] = 0.0
    for i in range(1, n):
        row = dp[i]
        xi, yi = xs[i], ys[i]
        for s in range(0, K + 1):
            j = i - s - 1
            if j < 0:
                break
            d = math.hypot(xs[j] - xi, ys[j] - yi)
            prev = dp[j]
            for c in range(0, K + 1 - s):
                v = prev[c]
                if v == INF:
                    continue
                v += d
                if v < row[c + s]:
                    row[c + s] = v

    best = INF
    for c in range(K + 1):
        v = dp[n - 1][c]
        if v == INF:
            continue
        pen = 0.0 if c == 0 else float(2 ** (c - 1))
        best = min(best, v + pen)
    print("%.20f" % best)


main()
