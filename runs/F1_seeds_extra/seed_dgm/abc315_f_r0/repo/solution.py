import sys
import math


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    xs = [int(v) for v in data[1:1 + 2 * n:2]]
    ys = [int(v) for v in data[2:2 + 2 * n:2]]

    # Upper bound: visit every checkpoint (no penalty).
    L0 = 0.0
    for i in range(n - 1):
        L0 += math.hypot(xs[i + 1] - xs[i], ys[i + 1] - ys[i])

    # Skipping C points costs 2^(C-1); once 2^(C-1) > L0 it is never useful.
    K = 0
    while K < n - 2 and (K == 0 or 2 ** (K - 1) <= L0):
        K += 1
    # K is the max number of skipped checkpoints considered.

    INF = float("inf")
    dp = [None] * n
    dp[0] = [0.0] + [INF] * K
    for i in range(1, n):
        row = [INF] * (K + 1)
        xi, yi = xs[i], ys[i]
        for k in range(0, min(K, i - 1) + 1):
            j = i - 1 - k
            d = math.hypot(xi - xs[j], yi - ys[j])
            prev = dp[j]
            cand = [a + d for a in prev[:K + 1 - k]]
            row[k:] = map(min, row[k:], cand)
        dp[i] = row

    best = INF
    for c, v in enumerate(dp[n - 1]):
        if v == INF:
            continue
        total = v + (2.0 ** (c - 1) if c > 0 else 0.0)
        if total < best:
            best = total
    print("%.20f" % best)


main()
