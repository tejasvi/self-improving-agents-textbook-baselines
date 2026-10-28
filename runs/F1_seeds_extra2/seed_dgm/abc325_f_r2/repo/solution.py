import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    D = [int(data[idx + i]) for i in range(n)]
    idx += n
    L1, C1, K1 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3
    L2, C2, K2 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3

    INF = 10 ** 9  # larger than any feasible type-2 count (<= 100 * 1e5 / 1 = 1e7)
    # dp[j]: min type-2 sensors using exactly j type-1 sensors (over processed sections)
    try:
        import numpy as np
        dp = np.full(K1 + 1, INF, dtype=np.int64)
        dp[0] = 0
        for d in D:
            new = np.full(K1 + 1, INF, dtype=np.int64)
            amax = min(K1, (d + L1 - 1) // L1)
            for a in range(amax + 1):
                rem = d - a * L1
                b = (rem + L2 - 1) // L2 if rem > 0 else 0
                # new[j] = min(new[j], dp[j - a] + b) for j >= a
                cand = dp[: K1 + 1 - a] + b
                np.minimum(new[a:], cand, out=new[a:])
            np.minimum(new, INF, out=new)
            dp = new
        best = None
        for j in range(K1 + 1):
            t = int(dp[j])
            if t <= K2:
                cost = j * C1 + t * C2
                if best is None or cost < best:
                    best = cost
    except ImportError:
        dp = [INF] * (K1 + 1)
        dp[0] = 0
        for d in D:
            new = [INF] * (K1 + 1)
            amax = min(K1, (d + L1 - 1) // L1)
            for a in range(amax + 1):
                rem = d - a * L1
                b = (rem + L2 - 1) // L2 if rem > 0 else 0
                for j in range(a, K1 + 1):
                    v = dp[j - a] + b
                    if v < new[j]:
                        new[j] = v
            dp = [min(v, INF) for v in new]
        best = None
        for j in range(K1 + 1):
            if dp[j] <= K2:
                cost = j * C1 + dp[j] * C2
                if best is None or cost < best:
                    best = cost

    print(-1 if best is None else best)


main()
