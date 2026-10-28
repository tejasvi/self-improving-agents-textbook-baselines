import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    n, W = int(data[0]), int(data[1])
    by_w = {}
    for i in range(n):
        w = int(data[2 + 2 * i])
        v = int(data[3 + 2 * i])
        by_w.setdefault(w, []).append(v)

    # Packed DP: field c (64 bits) holds dp[c] = best happiness with weight <= c.
    # All dp values are < 2^43, so 64-bit fields leave room for a guard bit at bit 63.
    B_BITS = 64
    F = (1 << B_BITS) - 1
    NF = W + 1
    ONES = 0
    for c in range(NF):
        ONES |= 1 << (B_BITS * c)
    FULL = (1 << (B_BITS * NF)) - 1
    HB = ONES << 63  # guard bits

    P = 0
    for w, vals in by_w.items():
        m = W // w
        heap = []
        for idx, v in enumerate(vals):
            if v - 1 > 0:
                heap.append((-(v - 1), idx, 1))
        heapq.heapify(heap)
        items = []
        while heap and len(items) < m:
            negval, idx, k = heapq.heappop(heap)
            items.append(-negval)
            nv = vals[idx] - 2 * (k + 1) + 1
            if nv > 0:
                heapq.heappush(heap, (-nv, idx, k + 1))
        if not items:
            continue
        shift = B_BITS * w
        low_mask = (1 << (B_BITS * (NF - w))) - 1   # fields 0..W-w
        high_mask = FULL ^ ((1 << shift) - 1)        # fields w..W
        Pl = P & low_mask
        for val in items:
            # B[c] = dp[c-w] + val for c >= w, 0 otherwise
            B = ((Pl << shift) + val * ONES) & high_mask
            D = ((P | HB) - B) & HB          # guard bit set iff P[c] >= B[c]
            M = ((D >> 63) << B_BITS) - (D >> 63)   # full 64-bit field masks
            P = B ^ ((P ^ B) & M)
            Pl = P & low_mask
    print((P >> (B_BITS * W)) & F)


main()
