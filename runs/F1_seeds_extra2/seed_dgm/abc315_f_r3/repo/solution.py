import sys
import math


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    xs = [int(data[1 + 2 * i]) for i in range(n)]
    ys = [int(data[2 + 2 * i]) for i in range(n)]
    # Penalty 2^(C-1) exceeds any possible total distance (~1.5e8) once C > ~29,
    # so at most K skipped checkpoints need to be considered.
    K = 30
    INF = float("inf")
    # dp[j][c]: min distance reaching checkpoint j (0-indexed) having skipped c checkpoints
    dp = [[INF] * (K + 1) for _ in range(n)]
    dp[0][0] = 0.0
    for j in range(1, n):
        row = dp[j]
        xj, yj = xs[j], ys[j]
        for i in range(max(0, j - K - 1), j):
            k = j - i - 1  # number of skipped checkpoints between i and j
            d = math.hypot(xj - xs[i], yj - ys[i])
            src = dp[i]
            for c in range(K + 1 - k):
                v = src[c] + d
                if v < row[c + k]:
                    row[c + k] = v
    best = INF
    for c in range(K + 1):
        v = dp[n - 1][c]
        if v == INF:
            continue
        pen = 0.0 if c == 0 else float(2 ** (c - 1))
        best = min(best, v + pen)
    print("%.20f" % best)


if __name__ == "__main__":
    main()
