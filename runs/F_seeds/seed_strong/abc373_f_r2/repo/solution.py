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

    # Each capacity s in 0..W is a bit-field of B bits; values < 2^(B-1).
    # Max total value <= W * 1e9 < 2^42, so B = 43 is safe.
    B = 43
    F = W + 1
    VB = B - 1
    ONESF = sum(1 << (B * s) for s in range(F))
    H = ONESF << VB                       # top bit of each field
    VALMASK1 = (1 << VB) - 1              # value bits of one field
    FIELDS_MASK = (1 << (F * B)) - 1
    VALFULL = ONESF * VALMASK1            # all value bits of all fields

    D = 0  # dp[s] = 0 for all s (weight at most s)

    for w, vs in groups.items():
        K = W // w
        if K == 0:
            continue
        # Top-K merged marginal gains: type with value v gives v-1, v-3, ...
        heap = []
        for v in vs:
            if v - 1 > 0:
                heap.append((-(v - 1), v, 0))  # (neg gain, v, t)
        heapq.heapify(heap)
        gains = []
        while heap and len(gains) < K:
            ng, v, t = heapq.heappop(heap)
            g = -ng
            gains.append(g)
            t += 1
            ng2 = v - 1 - 2 * t
            if ng2 > 0:
                heapq.heappush(heap, (-ng2, v, t))
        if not gains:
            continue
        # Fields s >= w receive the added gain.
        low = (1 << (w * B)) - 1
        ONES_ge = ONESF ^ (ONESF & low)
        shift = w * B
        for g in gains:
            cand = ((D << shift) & FIELDS_MASK) + g * ONES_ge
            # Fieldwise max(cand, D)
            d = (cand | H) - D
            ge = (d & H) >> VB
            mask = ge * VALMASK1
            D = (cand & mask) | (D & ~mask)

    ans = (D >> (W * B)) & VALMASK1
    print(ans)


main()
