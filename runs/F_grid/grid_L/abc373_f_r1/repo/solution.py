import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    n, W = int(data[0]), int(data[1])
    groups = {}
    for i in range(n):
        w = int(data[2 + 2 * i])
        v = int(data[3 + 2 * i])
        groups.setdefault(w, []).append(v)

    # Marginal values of the k-th copy of a type with value v: v - (2k-1).
    # For each weight class, keep the top W//w marginal values overall
    # (they form a prefix per type automatically since they decrease per type).
    items = []  # (weight, value)
    for w, vs in groups.items():
        cap = W // w
        heap = [(-(v - 1), idx, 1) for idx, v in enumerate(vs) if v - 1 > 0]
        vals = vs
        heapq.heapify(heap)
        taken = 0
        while heap and taken < cap:
            negm, idx, k = heapq.heappop(heap)
            m = -negm
            if m <= 0:
                break
            items.append((w, m))
            taken += 1
            nm = vals[idx] - (2 * k + 1)
            if nm > 0:
                heapq.heappush(heap, (-nm, idx, k + 1))

    # 0/1 knapsack, dp[c] = max happiness with total weight <= c.
    try:
        import numpy as np
        dp = np.zeros(W + 1, dtype=np.int64)
        for w, m in items:
            if w > W:
                continue
            cand = dp[:W + 1 - w] + m
            np.maximum(dp[w:], cand, out=cand)
            dp[w:] = cand
        print(int(dp[W]))
    except ImportError:
        dp = [0] * (W + 1)
        for w, m in items:
            if w > W:
                continue
            head = dp[:w]
            tail = [a if a >= b + m else b + m
                    for a, b in zip(dp[w:], dp[:W + 1 - w])]
            dp = head + tail
        print(dp[W])


main()
