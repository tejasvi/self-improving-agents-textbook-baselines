import sys
import math


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    pts = [(int(data[1 + 2 * i]), int(data[2 + 2 * i])) for i in range(n)]

    # Upper bound on the answer: visit every checkpoint.
    ub = 0.0
    for i in range(n - 1):
        ub += math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
    # Skipping C checkpoints costs 2^(C-1); any C with 2^(C-1) > ub is useless.
    K = 1
    while (1 << K) - 1 <= ub or (1 << (K - 1)) <= ub:
        K += 1
    K = min(K, n - 2) if n > 2 else 0

    INF = float("inf")
    dp = [[INF] * (K + 1) for _ in range(n)]
    dp[0][0] = 0.0
    for i in range(n):
        row = dp[i]
        if min(row) == INF:
            continue
        xi, yi = pts[i]
        for s in range(0, K + 1):
            j = i + s + 1
            if j >= n:
                break
            xj, yj = pts[j]
            d = math.hypot(xj - xi, yj - yi)
            tgt = dp[j]
            for c in range(0, K + 1 - s):
                v = row[c]
                if v == INF:
                    continue
                v += d
                if v < tgt[c + s]:
                    tgt[c + s] = v

    best = INF
    for c in range(K + 1):
        v = dp[n - 1][c]
        if v == INF:
            continue
        pen = 0.0 if c == 0 else float(2 ** (c - 1))
        best = min(best, v + pen)
    print("%.20f" % best)


main()
