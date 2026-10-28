import sys
import math

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    xs = [int(data[1 + 2 * i]) for i in range(n)]
    ys = [int(data[2 + 2 * i]) for i in range(n)]
    # Answer <= direct path length (< 1.5e8), so penalty 2^(C-1) bounds C <= 28.
    L = 28
    INF = float('inf')
    dp = [None] * n
    dp[0] = [0.0] + [INF] * L
    for i in range(1, n):
        xi, yi = xs[i], ys[i]
        row = [INF] * (L + 1)
        for k in range(max(0, i - 1 - L), i):
            s = i - k - 1  # checkpoints skipped going k -> i
            d = math.hypot(xs[k] - xi, ys[k] - yi)
            src = dp[k]
            # row[c + s] = min(row[c + s], src[c] + d)
            seg = [v + d for v in src[:L + 1 - s]]
            row[s:] = map(min, row[s:], seg)
        dp[i] = row
    best = INF
    for c in range(L + 1):
        v = dp[n - 1][c]
        if v == INF:
            continue
        pen = 0.0 if c == 0 else float(2 ** (c - 1))
        best = min(best, v + pen)
    print("%.20f" % best)

main()
