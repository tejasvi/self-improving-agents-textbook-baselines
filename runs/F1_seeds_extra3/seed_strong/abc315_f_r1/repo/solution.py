import sys
import math

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    xs = [int(data[1 + 2 * i]) for i in range(n)]
    ys = [int(data[2 + 2 * i]) for i in range(n)]
    # Skipping C >= 29 costs >= 2^28 > max possible path length (~1.5e8),
    # so capping skips at K = 30 is safe.
    K = 30
    INF = float('inf')
    dp = [[INF] * (K + 1) for _ in range(n)]
    dp[0][0] = 0.0
    for i in range(n):
        row = dp[i]
        xi = xs[i]; yi = ys[i]
        for k in range(K + 1):
            j = i + k + 1
            if j >= n:
                break
            d = math.hypot(xs[j] - xi, ys[j] - yi)
            tgt = dp[j]
            # tgt[c + k] = min(tgt[c + k], row[c] + d)
            cand = [x + d for x in row[:K + 1 - k]]
            tgt[k:] = list(map(min, tgt[k:], cand))
    best = INF
    for c in range(K + 1):
        v = dp[n - 1][c]
        if v == INF:
            continue
        pen = 0.0 if c == 0 else float(2 ** (c - 1))
        best = min(best, v + pen)
    print("%.20f" % best)

main()
