import sys
import heapq
from operator import add
from itertools import repeat


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    W = int(data[1])
    groups = {}
    for i in range(n):
        w = int(data[2 + 2 * i])
        v = int(data[3 + 2 * i])
        groups.setdefault(w, []).append(v)

    NEG = -(1 << 62)
    dp = [0] + [NEG] * W  # dp[x] = best happiness with total weight exactly x (or NEG)
    # Items: for each weight w, the marginal gains of all copies (v - (2k-1)), merged & sorted.
    for w, vs in groups.items():
        K = W // w
        if K == 0:
            continue
        # heap of (-marginal, index-in-vs, k) where k = number of copies already taken from that type
        heap = [(-(v - 1), idx, 1) for idx, v in enumerate(vs)]
        heapq.heapify(heap)
        cands = []
        while heap and len(cands) < K:
            negm, idx, k = heapq.heappop(heap)
            m = -negm
            if m <= 0:
                break
            cands.append(m)
            nk = k + 1
            nm = vs[idx] - (2 * nk - 1)
            heapq.heappush(heap, (-nm, idx, nk))
        # 0/1 knapsack over candidate items of weight w
        for g in cands:
            # new[x] = max(dp[x], dp[x-w] + g)
            dp = dp[:w] + list(map(max, dp[w:], map(add, dp[: W + 1 - w], repeat(g))))
    print(max(dp))


main()
