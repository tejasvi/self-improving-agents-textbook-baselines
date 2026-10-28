import sys


def solve():
    data = sys.stdin.read().split()
    n, k, x = int(data[0]), int(data[1]), int(data[2])
    T = [0] + sorted(int(v) for v in data[3:3 + n])
    P = [0] * (n + 1)
    for i in range(1, n + 1):
        P[i] = P[i - 1] + T[i]

    # front[j]: Pareto front of (last shipment day, accumulated cost) states
    # after shipping the first j orders (sorted by T).
    # Earlier day is better for the future and lower cost is better, so we
    # keep only states with strictly decreasing cost as the day increases.
    front = [[] for _ in range(n + 1)]
    front[0] = [(-x, 0)]  # virtual shipment so the first one is unconstrained
    for j in range(n):
        cur = front[j]
        if not cur:
            continue
        cur.sort()
        pruned = []
        best = None
        for t, c in cur:
            if best is None or c < best:
                pruned.append((t, c))
                best = c
        front[j] = pruned
        for jp in range(j + 1, min(n, j + k) + 1):
            size = jp - j
            base = T[jp]
            sub = P[jp] - P[j]
            tgt = front[jp]
            for t, c in pruned:
                tp = t + x
                if tp < base:
                    tp = base
                tgt.append((tp, c + size * tp - sub))
    print(min(c for _, c in front[n]))


solve()
