import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    D = [int(data[idx + i]) for i in range(n)]
    idx += n
    L1, C1, K1 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3
    L2, C2, K2 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3

    # Packed SWAR representation: dp[x] (x = number of type-1 sensors used, at most K1)
    # is stored in a field of W bits. Values are type-2 counts, capped at INF.
    # Field value < 2^(W-1) always, so the top bit of each field is a guard bit.
    W = 13
    H_BIT = 1 << (W - 1)
    INF = 1100  # > K2 (<= 1000); K2 is the feasibility threshold
    F = K1 + 1  # number of fields
    ONES = sum(1 << (W * i) for i in range(F))
    HIGH = ONES * H_BIT
    FULL = (1 << (W * F)) - 1
    INFV = ONES * INF

    def swar_min(a, b):
        # per-field min(a_i, b_i); all fields < H_BIT
        # g_i = 1 iff a_i >= b_i  (computed via guard bit)
        t = ((a | HIGH) - b) & HIGH
        g = t >> (W - 1)              # 1 in field i iff a_i >= b_i
        m = g * ((1 << (W - 1)) - 1)  # full-field mask where a_i >= b_i
        return (b & m) | (a & (FULL ^ m))

    # dp[0] = 0, all other fields INF
    dp = (INFV - INF) & FULL

    for d in D:
        amax = min(K1, -(-d // L1))
        new = INFV
        for a in range(amax + 1):
            rem = d - a * L1
            fa = 0 if rem <= 0 else -(-rem // L2)
            if fa > K2:
                continue
            shifted = ((dp << (a * W)) & FULL) | (INFV & ((1 << (a * W)) - 1))
            cand = shifted + fa * ONES
            new = swar_min(new, cand)
        dp = swar_min(new, INFV)

    best = None
    for x in range(F):
        y = (dp >> (W * x)) & ((1 << W) - 1)
        if y <= K2:
            cost = x * C1 + y * C2
            if best is None or cost < best:
                best = cost
    print(-1 if best is None else best)


main()
