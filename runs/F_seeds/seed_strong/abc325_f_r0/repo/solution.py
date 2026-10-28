import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    D = [int(data[idx + i]) for i in range(N)]
    idx += N
    L1, C1, K1 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3
    L2, C2, K2 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3

    INF = K2 + 1          # any value > K2 means infeasible
    W = 12                # lane width in bits
    B = W - 1             # value bits per lane (values < 2^B = 2048 > 2*INF)
    VMASK = (1 << B) - 1
    n_lanes = K1 + 1

    ONES = 0
    for i in range(n_lanes):
        ONES |= 1 << (i * W)
    LANES = ONES * ((1 << W) - 1)
    H = ONES << B  # guard bit of each lane

    def lanemin(P, Q):
        # lanewise min of packed P and Q (values < 2^B)
        d = (P | H) - Q
        m = (d >> B) & ONES          # bit set in lane iff p >= q
        full = m * VMASK             # all value bits of lane where p >= q
        return (Q & full) | (P & (LANES ^ full))

    # dp lane x = min type-2 count using exactly x type-1 sensors
    dp = 0
    for i in range(1, n_lanes):
        dp |= INF << (i * W)

    CLAMP = (INF + 1) * ONES
    for d in D:
        amax = min(K1, (d + L1 - 1) // L1)
        new = 0
        lowinf = 0  # lanes < a set to INF
        for a in range(0, amax + 1):
            if a > 0:
                lowinf |= INF << ((a - 1) * W)
                shifted = ((dp << (a * W)) & LANES) | lowinf
            else:
                shifted = dp
            rem = d - a * L1
            need = 0 if rem <= 0 else (rem + L2 - 1) // L2
            if need > INF:
                need = INF
            cand = shifted + need * ONES
            new = cand if a == 0 else lanemin(new, cand)
        # clamp values > INF back to INF
        t = ((new | H) - CLAMP) & H
        g = (t >> B) & ONES
        new = (new & ~(g * VMASK) & LANES) | (g * INF)
        dp = new

    ans = -1
    for x in range(n_lanes):
        v = (dp >> (x * W)) & VMASK
        if v <= K2:
            cost = x * C1 + v * C2
            if ans < 0 or cost < ans:
                ans = cost
    print(ans)


main()
