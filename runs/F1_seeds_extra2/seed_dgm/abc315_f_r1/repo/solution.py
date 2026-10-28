import sys
import math


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    xs = [int(data[1 + 2 * i]) for i in range(n)]
    ys = [int(data[2 + 2 * i]) for i in range(n)]
    # Penalty 2^(C-1) exceeds any possible path length (~1.5e8) once C >= 29,
    # so skipping more than K checkpoints is never optimal.
    K = 30
    INF = float("inf")
    # dp[i][c]: min distance reaching checkpoint i (0-indexed) having skipped c so far
    dp = [[INF] * (K + 1) for _ in range(n)]
    dp[0][0] = 0.0
    for i in range(n):
        row = dp[i]
        if min(row) == INF:
            continue
        xi, yi = xs[i], ys[i]
        for k in range(K + 1):
            j = i + k + 1
            if j >= n:
                break
            d = math.hypot(xs[j] - xi, ys[j] - yi)
            target = dp[j]
            # transition: skip k checkpoints, c -> c + k
            for c in range(K + 1 - k):
                v = row[c] + d
                if v < target[c + k]:
                    target[c + k] = v
    best = INF
    for c in range(K + 1):
        v = dp[n - 1][c]
        if v == INF:
            continue
        pen = 0.0 if c == 0 else float(2 ** (c - 1))
        best = min(best, v + pen)
    print("%.20f" % best)


main()
