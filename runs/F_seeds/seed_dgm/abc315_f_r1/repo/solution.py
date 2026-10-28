import sys
import math


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    xs = [float(data[1 + 2 * i]) for i in range(n)]
    ys = [float(data[2 + 2 * i]) for i in range(n)]
    # Max useful skips: penalty 2^(C-1) must stay below max path length (~1.5e8).
    K = 28
    INF = float("inf")
    f = [[INF] * (K + 1) for _ in range(n)]
    f[0][0] = 0.0
    for i in range(n):
        fi = f[i]
        if min(fi) == INF:
            continue
        for d in range(0, K + 1):
            j = i + d + 1
            if j >= n:
                break
            dist = math.hypot(xs[j] - xs[i], ys[j] - ys[i])
            fj = f[j]
            for c in range(0, K + 1 - d):
                v = fi[c]
                if v == INF:
                    continue
                v += dist
                if v < fj[c + d]:
                    fj[c + d] = v
    best = INF
    for c in range(K + 1):
        v = f[n - 1][c]
        if v == INF:
            continue
        pen = 0.0 if c == 0 else float(2 ** (c - 1))
        best = min(best, v + pen)
    print("%.12f" % best)


main()
