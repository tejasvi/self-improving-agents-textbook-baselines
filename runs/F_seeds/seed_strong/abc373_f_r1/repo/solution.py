import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    W = int(data[1])
    classes = {}
    for i in range(n):
        w = int(data[2 + 2 * i])
        v = int(data[3 + 2 * i])
        classes.setdefault(w, []).append(v)

    # Packed DP: field x (bits [F*x, F*x+F)) holds best happiness with capacity <= x.
    # Values < 2^43 always (<= 3000 * 1e9 < 2^42), so bit 43 of a field is a guard bit.
    F = 44
    GUARD = 1 << 43
    VMASK = (1 << 43) - 1
    FMASK = (1 << F) - 1
    nf = W + 1
    ONES = 0
    for x in range(nf):
        ONES |= 1 << (F * x)
    ALLF = ONES * FMASK          # every field fully set
    GUARDS = ONES * GUARD

    P = 0  # all zeros: capacity-0 value of 0 for every capacity

    for w, vs in classes.items():
        L = W // w
        if L == 0:
            continue
        # Marginal values of copies: k-th copy adds v - 2k + 1 (decreasing in k).
        heap = [(-(v - 1), i, 0) for i, v in enumerate(vs)]
        heapq.heapify(heap)
        items = []
        while heap and len(items) < L:
            negval, i, j = heapq.heappop(heap)
            val = -negval
            if val <= 0:
                break
            items.append(val)
            nv = vs[i] - (2 * (j + 1) + 1)  # marginal of copy j+2 (0-indexed j+1)
            if nv > 0:
                heapq.heappush(heap, (-nv, i, j + 1))

        if not items:
            continue

        shift = F * w
        low_mask = (1 << (F * (nf - w))) - 1       # fields 0..nf-w-1
        high_ones = ONES & ~((1 << shift) - 1)     # ONES on fields w..nf-1
        for val in items:
            # Candidate B: field x (x>=w) = dp[x-w] + val; fields x<w = 0.
            B = ((P & low_mask) << shift) + high_ones * val
            # D field = A + 2^43 - B: guard bit set iff A >= B (no borrow since values < 2^43)
            D = (P | GUARDS) - B
            M = ((D & GUARDS) >> 43) * FMASK      # full-field mask where A >= B
            P = (P & M) | (B & (ALLF ^ M))

    print((P >> (F * W)) & VMASK)


main()
