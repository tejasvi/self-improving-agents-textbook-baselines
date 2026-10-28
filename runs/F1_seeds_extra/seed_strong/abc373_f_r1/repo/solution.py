import sys
import heapq
from itertools import repeat
from operator import add

def main():
    data = sys.stdin.buffer.read().split()
    n, W = int(data[0]), int(data[1])
    groups = {}
    for i in range(n):
        w = int(data[2 + 2 * i])
        v = int(data[3 + 2 * i])
        groups.setdefault(w, []).append(v)
    dp = [0] * (W + 1)  # dp[c] = best value with total weight <= c
    for w, vals in groups.items():
        K = W // w
        # Copy k (k>=1) of a type with value v has marginal v - (2k-1), decreasing in k.
        # Take the top K marginals across all types via a heap merge.
        if len(vals) == 1:
            v = vals[0]
            g = [0]
            acc = 0
            for k in range(1, K + 1):
                m = v - (2 * k - 1)
                if m <= 0:
                    break
                acc += m
                g.append(acc)
        else:
            heap = [(-(v - 1), v, 1) for v in vals]  # (neg marginal, v, k)
            heapq.heapify(heap)
            g = [0]
            acc = 0
            for _ in range(K):
                negm, v, k = heap[0]
                m = -negm
                if m <= 0:
                    break
                acc += m
                g.append(acc)
                if v - (2 * k + 1) > 0:
                    heapq.heapreplace(heap, (-(v - (2 * k + 1)), v, k + 1))
                else:
                    heapq.heappop(heap)
                    if not heap:
                        break
        T = len(g) - 1
        new = dp[:]
        for t in range(1, T + 1):
            s = t * w
            if s > W:
                break
            gt = g[t]
            new[s:] = list(map(max, new[s:], map(add, dp[:W + 1 - s], repeat(gt))))
        dp = new
    print(dp[W])

main()
