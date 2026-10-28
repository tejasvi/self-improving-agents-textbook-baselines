import sys
import math


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    xs = [int(data[1 + 2 * i]) for i in range(n)]
    ys = [int(data[2 + 2 * i]) for i in range(n)]
    # Skipping C checkpoints costs 2^(C-1); any useful C satisfies
    # 2^(C-1) <= total path length (< 1.5e8), so C <= 28. K = 35 is safe.
    K = 35
    INF = float("inf")
    # dp[i][c]: min distance reaching checkpoint i (0-indexed) having skipped c so far
    dp = [[INF] * (K + 1) for _ in range(n)]
    dp[0][0] = 0.0
    for i in range(n - 1):
        row = dp[i]
        if min(row) == INF:
            continue
        xi, yi = xs[i], ys[i]
        for g in range(K + 1):
            j = i + g + 1
            if j >= n:
                break
            d = math.hypot(xs[j] - xi, ys[j] - yi)
            tgt = dp[j]
            # skipping g checkpoints: c -> c+g
            for c in range(K + 1 - g):
                v = row[c]
                if v == INF:
                    continue
                v += d
                if v < tgt[c + g]:
                    tgt[c + g] = v
    best = INF
    for c, v in enumerate(dp[n - 1]):
        if v == INF:
            continue
        pen = 0.0 if c == 0 else float(2 ** (c - 1))
        if v + pen < best:
            best = v + pen
    print("%.20f" % best)


main()
