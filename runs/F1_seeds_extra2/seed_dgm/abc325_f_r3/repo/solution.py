import sys
from itertools import repeat
from operator import add


def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    D = [int(data[idx + i]) for i in range(n)]
    idx += n
    L1, C1, K1 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3
    L2, C2, K2 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3

    INF = float("inf")
    # dp[j] = min number of type-2 sensors using exactly j type-1 sensors
    dp = [INF] * (K1 + 1)
    dp[0] = 0
    for d in D:
        amax = min(K1, (d + L1 - 1) // L1)
        # b[a] for a in 0..amax
        bs = []
        for a in range(amax + 1):
            rem = d - a * L1
            bs.append(0 if rem <= 0 else (rem + L2 - 1) // L2)
        new = [INF] * (K1 + 1)
        for a in range(amax + 1):
            b = bs[a]
            # new[j + a] = min(new[j + a], dp[j] + b) for j + a <= K1
            L = K1 + 1 - a
            seg = new[a:a + L]
            cand = map(add, dp[:L], repeat(b, L))
            new[a:a + L] = map(min, seg, cand)
        dp = new
        # prune: values above K2 are useless
        dp = [v if v <= K2 else INF for v in dp]

    best = None
    for j in range(K1 + 1):
        t = dp[j]
        if t <= K2:
            cost = j * C1 + int(t) * C2
            if best is None or cost < best:
                best = cost
    print(-1 if best is None else best)


main()
