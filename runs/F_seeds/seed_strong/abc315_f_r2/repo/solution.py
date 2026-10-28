import sys
import math

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    xs = [float(data[1 + 2 * i]) for i in range(n)]
    ys = [float(data[2 + 2 * i]) for i in range(n)]
    # Total skipped C satisfies 2^(C-1) <= upper bound (~1.42e8), so C <= 28.
    K = 30
    INF = float('inf')
    dp = [None] * n
    dp[0] = [0.0] + [INF] * K
    for i in range(1, n):
        new = [INF] * (K + 1)
        xi = xs[i]; yi = ys[i]
        for d in range(0, min(K, i - 1) + 1):
            j = i - d - 1
            vec = dp[j]
            D = math.hypot(xs[j] - xi, ys[j] - yi)
            cand = [v + D for v in vec[:K + 1 - d]]
            if d:
                cand = [INF] * d + cand
            new = list(map(min, new, cand))
        dp[i] = new
    best = INF
    for c, v in enumerate(dp[n - 1]):
        if v == INF:
            continue
        pen = 0.0 if c == 0 else float(2 ** (c - 1))
        best = min(best, v + pen)
    print("%.20f" % best)

main()
