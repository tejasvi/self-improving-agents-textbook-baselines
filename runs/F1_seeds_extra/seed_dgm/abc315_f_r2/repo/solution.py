import sys
import math


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    xs = [int(data[1 + 2 * i]) for i in range(n)]
    ys = [int(data[2 + 2 * i]) for i in range(n)]

    # Skipping C >= 16 costs >= 2^15 = 32768, more than any direct route
    # (max ~ 1.42e4), so C <= 20 is safe.
    K = 20
    INF = float("inf")
    dp = [[INF] * (K + 1) for _ in range(n)]
    dp[0][0] = 0.0
    for i in range(n):
        row = dp[i]
        if min(row) == INF:
            continue
        xi, yi = xs[i], ys[i]
        for s in range(K + 1):
            j = i + s + 1
            if j >= n:
                break
            d = math.hypot(xs[j] - xi, ys[j] - yi)
            tj = dp[j]
            for c in range(K + 1 - s):
                v = row[c]
                if v == INF:
                    continue
                nv = v + d
                if nv < tj[c + s]:
                    tj[c + s] = nv

    best = INF
    for c in range(K + 1):
        v = dp[n - 1][c]
        if v == INF:
            continue
        pen = 0.0 if c == 0 else float(2 ** (c - 1))
        best = min(best, v + pen)
    print("%.20f" % best)


main()
