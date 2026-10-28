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

    INF = float('inf')
    # dp[j] = minimum number of type-2 sensors needed using exactly j type-1 sensors
    # over the sections processed so far.
    BIG = 10 ** 18
    dp = [BIG] * (K1 + 1)
    dp[0] = 0
    for d in D:
        amax = min(K1, (d + L1 - 1) // L1)
        # cost in type-2 sensors for each count a of type-1 sensors on this section
        f = []
        for a in range(amax + 1):
            rem = d - a * L1
            f.append(0 if rem <= 0 else (rem + L2 - 1) // L2)
        new = [BIG] * (K1 + 1)
        for a in range(amax + 1):
            b = f[a]
            seg = dp[:K1 + 1 - a]
            new[a:] = map(min, new[a:], map(add, seg, repeat(b)))
        # discard states needing more type-2 sensors than available
        dp = [v if v <= K2 else BIG for v in new]

    best = None
    for j in range(K1 + 1):
        if dp[j] <= K2:
            cost = j * C1 + dp[j] * C2
            if best is None or cost < best:
                best = cost
    print(-1 if best is None else best)


main()
