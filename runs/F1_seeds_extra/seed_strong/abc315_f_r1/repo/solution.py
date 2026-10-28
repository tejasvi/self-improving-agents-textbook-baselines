import sys
from math import hypot
from operator import add
from itertools import repeat

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    X = [int(data[1 + 2 * i]) for i in range(n)]
    Y = [int(data[2 + 2 * i]) for i in range(n)]
    # Skipping >= 30 checkpoints costs >= 2^29 > max cost of visiting all points (~1.42e8)
    K = 30
    INF = float('inf')
    dp = [[INF] * (K + 1) for _ in range(n)]
    dp[0][0] = 0.0
    for j in range(1, n):
        dj = dp[j]
        for d in range(1, K + 2):
            i = j - d
            if i < 0:
                break
            s = d - 1  # checkpoints skipped between i and j
            if s > K:
                break
            dist = hypot(X[i] - X[j], Y[i] - Y[j])
            di = dp[i]
            cand = map(add, di[:K + 1 - s], repeat(dist))
            dj[s:] = map(min, dj[s:], cand)
    best = INF
    for c in range(K + 1):
        v = dp[n - 1][c]
        if v == INF:
            continue
        pen = 0.0 if c == 0 else float(2 ** (c - 1))
        best = min(best, v + pen)
    print("%.20f" % best)

main()
