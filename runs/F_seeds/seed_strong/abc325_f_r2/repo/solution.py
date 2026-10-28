import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    D = [int(v) for v in data[1:1 + n]]
    L1, C1, K1 = map(int, data[1 + n:4 + n])
    L2, C2, K2 = map(int, data[4 + n:7 + n])

    # dp[j] = min number of type-2 sensors when at most j type-1 sensors are used.
    # Stored SWAR-packed: field j occupies bits [12j, 12j+12); values < 2048 with
    # bit 11 used as guard for comparisons.
    F = K1 + 1
    W = 12
    ONES = 0
    for j in range(F):
        ONES |= 1 << (W * j)
    H = ONES << 11           # guard bit of each field
    FULL = (1 << (W * F)) - 1
    LOWV = 2047 * ONES       # all fields = 2047 (value fits 11 bits)
    INF = K2 + 1
    INFV = INF * ONES
    CAPM = (K2 + 1) * ONES   # threshold for capping

    def minvec(a, b):
        t = ((a | H) - b) & H
        M = (t >> 11) * 2047
        return (b & M) | (a & (FULL ^ M))

    dp = 0  # all zeros
    for d in D:
        xmax = min(K1, -(-d // L1))
        cand = []
        last = None
        for x in range(xmax + 1):
            rem = d - x * L1
            need = 0 if rem <= 0 else -(-rem // L2)
            if need > K2:
                continue
            if need != last:
                cand.append((x, need))
                last = need
        new = INFV
        for x, need in cand:
            # shift dp by x fields, drop overflow beyond F fields
            mask_keep = (1 << (W * (F - x))) - 1
            shifted = ((dp & mask_keep) << (W * x)) + need * ONES
            if x:
                shifted |= LOWV & ((1 << (W * x)) - 1)
            new = minvec(new, shifted)
        # cap values > K2 to INF
        t = ((new | H) - CAPM) & H
        M = (t >> 11) * 2047
        new = (new & (FULL ^ M)) | (INFV & M)
        dp = new

    best = None
    for j in range(F):
        v = (dp >> (W * j)) & 2047
        if v <= K2:
            cost = C1 * j + C2 * v
            if best is None or cost < best:
                best = cost
    print(-1 if best is None else best)


main()
