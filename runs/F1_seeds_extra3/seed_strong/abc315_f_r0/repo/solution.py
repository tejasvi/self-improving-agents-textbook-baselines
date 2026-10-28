import sys
import math


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    xs = [int(v) for v in data[1:1 + 2 * n:2]]
    ys = [int(v) for v in data[2:2 + 2 * n:2]]

    # Upper bound: no skipping.
    base = 0.0
    for i in range(n - 1):
        base += math.hypot(xs[i + 1] - xs[i], ys[i + 1] - ys[i])
    # Max useful skip count K: 2^(K-1) must not exceed base.
    K = 0
    while K < 60 and 2 ** K <= base:
        K += 1
    # K now such that 2^(K-1) <= base < 2^K ; skipping more than K is useless.
    K = max(K, 1)
    K = min(K, n - 2) if n > 2 else 0

    INF = float("inf")
    dp = [None] * n
    dp[0] = [0.0] + [INF] * K
    for i in range(1, n):
        row = [INF] * (K + 1)
        xi, yi = xs[i], ys[i]
        for m in range(0, min(K, i - 1) + 1):
            j = i - 1 - m
            d = math.hypot(xi - xs[j], yi - ys[j])
            prev = dp[j]
            new = [p + d for p in prev[:K + 1 - m]]
            row[m:] = map(min, row[m:], new)
        dp[i] = row

    best = INF
    for c, v in enumerate(dp[n - 1]):
        if v == INF:
            continue
        pen = 0.0 if c == 0 else 2.0 ** (c - 1)
        if v + pen < best:
            best = v + pen
    print("%.12f" % best)


main()
