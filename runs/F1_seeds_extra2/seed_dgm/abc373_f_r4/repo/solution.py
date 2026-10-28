import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    W = int(data[1])
    groups = {}
    for i in range(n):
        w = int(data[2 + 2 * i])
        v = int(data[3 + 2 * i])
        groups.setdefault(w, []).append(v)

    # Marginal gain of k-th item of a type with value v is v - (2k-1), decreasing in k.
    # For each weight class keep only the top W//w gains (merged over all types).
    items = []  # (weight, gain)
    for w, vs in groups.items():
        K = W // w
        heap = []
        for v in vs:
            if v - 1 > 0:
                heap.append((-(v - 1), v, 1))
        heapq.heapify(heap)
        cnt = 0
        while heap and cnt < K:
            negg, v, k = heapq.heappop(heap)
            items.append((w, -negg))
            cnt += 1
            nk = k + 1
            ng = v - (2 * nk - 1)
            if ng > 0:
                heapq.heappush(heap, (-ng, v, nk))

    # 0/1 knapsack over "at most" capacity; dp[c] = best value with weight <= c
    dp = [0] * (W + 1)
    for w, g in items:
        if w > W:
            continue
        dp[w:] = list(map(max, dp[w:], map(g.__add__, dp)))
    print(dp[W])


main()
