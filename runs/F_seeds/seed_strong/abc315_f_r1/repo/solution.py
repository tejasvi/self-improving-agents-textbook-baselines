import sys, math

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    xs = [int(data[1 + 2 * i]) for i in range(n)]
    ys = [int(data[2 + 2 * i]) for i in range(n)]
    K = 30  # optimal answer <= no-skip path <= 1.42e8 < 2^30, so optimal skips C satisfy 2^(C-1) <= 1.42e8, i.e. C <= 28 < 30
    INF = float('inf')
    # g[i][c]: min distance to reach checkpoint i (0-indexed) having skipped exactly c checkpoints
    g = [None] * n
    g[0] = [0.0] + [INF] * K
    for i in range(1, n):
        cur = [INF] * (K + 1)
        xi, yi = xs[i], ys[i]
        for k in range(0, K + 1):
            j = i - k - 1
            if j < 0:
                break
            gj = g[j]
            d = math.hypot(xi - xs[j], yi - ys[j])
            # cur[c] = min(cur[c], gj[c-k] + d) for c in [k, K]
            seg = gj[0:K + 1 - k]
            cur[k:] = map(min, cur[k:], [v + d for v in seg])
        g[i] = cur
    best = INF
    for c in range(K + 1):
        v = g[n - 1][c]
        if v == INF:
            continue
        pen = 0.0 if c == 0 else float(2 ** (c - 1))
        best = min(best, v + pen)
    print("%.20f" % best)

main()
