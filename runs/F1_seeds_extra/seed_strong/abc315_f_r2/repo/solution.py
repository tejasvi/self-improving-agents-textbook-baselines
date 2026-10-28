import sys
import math

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    xs = [int(data[1 + 2 * i]) for i in range(n)]
    ys = [int(data[2 + 2 * i]) for i in range(n)]
    # Skipping >= 29 checkpoints costs >= 2^28 > max possible path length (~1.42e8),
    # so the skip count never needs to exceed K = 30.
    K = 30
    INF = float("inf")
    W = K + 1
    dp = [[INF] * W for _ in range(n)]
    dp[0][0] = 0.0
    hypot = math.hypot
    for j in range(1, n):
        dj = dp[j]
        xj, yj = xs[j], ys[j]
        for k in range(min(K, j - 1) + 1):
            i = j - k - 1
            d = hypot(xj - xs[i], yj - ys[i])
            src = dp[i]
            # dj[c + k] = min(dj[c + k], src[c] + d)
            for c in range(W - k):
                v = src[c] + d
                if v < dj[c + k]:
                    dj[c + k] = v
    best = INF
    last = dp[n - 1]
    for c in range(W):
        v = last[c]
        if v == INF:
            continue
        pen = 0.0 if c == 0 else float(2 ** (c - 1))
        if v + pen < best:
            best = v + pen
    print("%.12f" % best)

main()
