import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    D = [int(data[idx + i]) for i in range(n)]
    idx += n
    L1, C1, K1 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3
    L2, C2, K2 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3

    # DP over number of type-1 sensors j (0..K1); value = min type-2 count.
    # Values are capped at INF = K2+1 (anything > K2 is infeasible).
    # The row is packed into one big integer with W-bit lanes; lane j holds dp[j].
    W = 16
    SH = 15  # guard bit position within a lane
    INF = K2 + 1
    LANES = K1 + 1
    ONES = 0
    for i in range(LANES):
        ONES |= 1 << (W * i)
    MASK = ONES * 0xFFFF
    H = ONES << SH
    INFP = ONES * INF

    # INFLOW[a]: INF in lanes [0, a), 0 elsewhere (applied to shifted candidates)
    INFLOW = [0] * (K1 + 1)
    acc = 0
    for a in range(K1 + 1):
        INFLOW[a] = acc  # lanes [0,a) set
        acc |= INF << (W * a)

    # lane 0 = 0, all other lanes = INF
    dp = INFP - INF

    for d in D:
        new = INFP
        amax = min(K1, (d + L1 - 1) // L1)
        for a in range(amax + 1):
            rem = d - a * L1
            b = 0 if rem <= 0 else (rem + L2 - 1) // L2
            if b > K2:
                continue
            cand = (((dp << (W * a)) & MASK) + ONES * b) + INFLOW[a]
            # lane-wise min(new, cand)
            t = ((new | H) - cand) & H
            m = (t >> SH) * 0xFFFF
            new = (cand & m) | (new & (MASK ^ m))
        dp = new

    best = None
    for j in range(K1 + 1):
        v = (dp >> (W * j)) & 0xFFFF
        if v <= K2:
            cost = C1 * j + C2 * v
            if best is None or cost < best:
                best = cost

    print(-1 if best is None else best)


main()
