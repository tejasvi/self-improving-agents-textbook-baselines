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

    # Marginal gain of the j-th copy of a type with value v is v+1-2j,
    # which is decreasing in j. For each weight w, only the top W//w
    # positive gains (over all types with that weight) can matter.
    # Each weight class gives items of weight w with these gains, and
    # the answer is a 0/1 knapsack over all selected items.
    B = 45
    SH = 44
    MASK = (1 << B) - 1
    ONES = 0
    for i in range(W + 1):
        ONES |= 1 << (B * i)
    FULL = ONES * MASK
    H = ONES << SH

    dp = 0  # packed: field c holds best value with weight <= c
    for w, vs in groups.items():
        cap = W // w
        if cap == 0:
            continue
        # heap of (-next_gain, v, next_j) with next_j the copy index (1-based)
        heap = [(-(v - 1), v, 1) for v in vs if v - 1 > 0]
        heapq.heapify(heap)
        gains = []
        while heap and len(gains) < cap:
            ng, v, j = heapq.heappop(heap)
            g = -ng
            gains.append(g)
            nj = j + 1
            ng2 = v + 1 - 2 * nj
            if ng2 > 0:
                heapq.heappush(heap, (-ng2, v, nj))
        if not gains:
            continue
        HIBITS = ONES & ~((1 << (B * w)) - 1)
        for g in gains:
            cand = ((dp << (B * w)) & FULL) + g * ONES
            D = ((cand | H) - dp) >> SH
            M = (D & HIBITS) * MASK
            dp = dp ^ ((dp ^ cand) & M)
    print((dp >> (B * W)) & MASK)


main()
