import sys
import math

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    xs = [int(data[1 + 2 * i]) for i in range(n)]
    ys = [int(data[2 + 2 * i]) for i in range(n)]
    # Skipping 30 checkpoints costs 2^29 > max possible path length (~1.5e8),
    # so the number of skipped checkpoints never needs to exceed this bound.
    K = 30
    INF = float('inf')
    # dp[j][c]: min distance reaching checkpoint j having skipped exactly c checkpoints
    dp = [[INF] * (K + 1) for _ in range(n)]
    dp[0][0] = 0.0
    for j in range(1, n):
        row = dp[j]
        xj, yj = xs[j], ys[j]
        for g in range(0, K + 1):
            i = j - g - 1
            if i < 0:
                break
            d = math.hypot(xs[i] - xj, ys[i] - yj)
            src = dp[i]
            cand = [v + d for v in src[:K + 1 - g]]
            row[g:] = list(map(min, row[g:], cand))
    best = INF
    for c in range(K + 1):
        v = dp[n - 1][c]
        if v == INF:
            continue
        pen = 0.0 if c == 0 else float(2 ** (c - 1))
        best = min(best, v + pen)
    print("%.20f" % best)

main()
