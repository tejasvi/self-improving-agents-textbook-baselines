import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    n, W = int(data[0]), int(data[1])
    # Type i's k-th item has marginal value v_i - (2k-1) (decreasing in k).
    # For a fixed weight w, only the top W // w marginals can be used.
    by_w = {}
    for i in range(n):
        w = int(data[2 + 2 * i])
        v = int(data[3 + 2 * i])
        by_w.setdefault(w, []).append(v)
    items = []  # (weight, value) 0/1 knapsack items
    for w, vs in by_w.items():
        cap = W // w
        heap = [(-(v - 1), v, 1) for v in vs]
        heapq.heapify(heap)
        for _ in range(cap):
            if not heap:
                break
            negval, v, k = heapq.heappop(heap)
            val = -negval
            if val <= 0:
                break
            items.append((w, val))
            nk = k + 1
            nval = v - (2 * nk - 1)
            if nval > 0:
                heapq.heappush(heap, (-nval, v, nk))

    # Packed DP: field j (F bits) holds dp[j] = best value with weight <= j.
    # All values < 2^46, so a guard bit at position F-1 per field is safe.
    F = 48
    G = 1 << (F - 1)
    L = W + 1
    ONES = 0
    for j in range(L):
        ONES |= 1 << (F * j)
    H = ONES * G
    FULL = (1 << (F * L)) - 1
    CAP = FULL  # truncation mask for fields 0..W
    dp = 0  # all zeros
    for w, val in items:
        if w > W:
            continue
        sh = F * w
        # fields j >= w get dp[j-w] + val; fields j < w get 0 (never beats dp)
        cand = ((dp << sh) & CAP) + val * ((ONES << sh) & CAP)
        # per field: guard bit survives iff cand >= dp
        diff = (cand | H) - dp
        g = (diff & H) >> (F - 1)          # 1 in fields where cand >= dp
        m = (g << (F - 1)) - g             # lower F-1 bits set in those fields
        dp = dp ^ ((dp ^ cand) & m)
    # extract field W
    res = (dp >> (F * W)) & ((1 << F) - 1)
    print(res)


main()
