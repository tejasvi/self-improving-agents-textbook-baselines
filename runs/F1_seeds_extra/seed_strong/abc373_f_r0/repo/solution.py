import sys


def top_values(vs, K):
    """Return the K largest marginal values among copies of items with values vs.

    The k-th copy (k>=1) of an item with value v has marginal value v-2k+1.
    Only the K largest across all types can be used (total count <= K).
    """
    def cnt(T):
        # number of copies with marginal value >= T (T >= 1), capped at K each
        c = 0
        for v in vs:
            t = (v - T + 1) // 2
            if t > 0:
                c += t if t < K else K
        return c

    if cnt(1) <= K:
        vals = []
        for v in vs:
            t = min(K, v // 2)
            vals.extend(range(v - 1, v - 2 * t, -2))
        return vals

    lo, hi = 1, 2 * 10 ** 9 + 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if cnt(mid) >= K:
            lo = mid
        else:
            hi = mid - 1
    T = lo
    vals = []
    for v in vs:
        t = (v - T) // 2  # copies with marginal value > T
        if t > 0:
            t = min(t, K)
            vals.extend(range(v - 1, v - 2 * t, -2))
    vals.extend([T] * (K - len(vals)))
    return vals


def main():
    data = sys.stdin.buffer.read().split()
    n, W = int(data[0]), int(data[1])
    groups = {}
    for i in range(n):
        w = int(data[2 + 2 * i])
        v = int(data[3 + 2 * i])
        if w <= W:
            groups.setdefault(w, []).append(v)

    # Packed DP: lane j (B bits) holds best value with total weight <= j.
    # Values are < 2^42, so 46-bit lanes leave room for the SWAR max trick.
    B = 46
    LANES = W + 1
    ONES = ((1 << (LANES * B)) - 1) // ((1 << B) - 1)
    H = ONES << (B - 1)                  # top bit of every lane
    LOW = ONES * ((1 << (B - 1)) - 1)    # low B-1 bits of every lane
    dp = 0
    for w, vs in groups.items():
        K = W // w
        if K == 0:
            continue
        vals = top_values(vs, K)
        vals.sort(reverse=True)
        keep = (1 << ((LANES - w) * B)) - 1
        shift = w * B
        for val in vals:
            if val <= 0:
                break
            cand = ((dp & keep) + val * ONES) << shift
            # lane-wise max(cand, dp); all lane values are nonnegative and < 2^(B-1)
            t = ((cand | H) - dp) & H
            m = t - (t >> (B - 1))
            dp = (cand & m) | (dp & (LOW ^ m))
    print((dp >> (W * B)) & ((1 << B) - 1))


main()
