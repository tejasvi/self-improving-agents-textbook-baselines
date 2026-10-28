import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    D = [int(data[idx + i]) for i in range(n)]
    idx += n
    L1, C1, K1 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3
    L2, C2, K2 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2])

    INF = 10 ** 15

    def need2(d, a):
        rem = d - a * L1
        if rem <= 0:
            return 0
        return (rem + L2 - 1) // L2

    try:
        import numpy as np
        dp = np.full(K1 + 1, INF, dtype=np.int64)
        dp[0] = 0
        for d in D:
            amax = min(K1, (d + L1 - 1) // L1)
            new = np.full(K1 + 1, INF, dtype=np.int64)
            for a in range(amax + 1):
                g = need2(d, a)
                # new[x + a] = min(new[x + a], dp[x] + g) for x in 0..K1-a
                cand = dp[: K1 + 1 - a] + g
                np.minimum(new[a:], cand, out=new[a:])
            np.minimum(new, INF, out=new)
            dp = new
        dp_list = [int(v) for v in dp]
    except ImportError:
        dp_list = [INF] * (K1 + 1)
        dp_list[0] = 0
        for d in D:
            amax = min(K1, (d + L1 - 1) // L1)
            gs = [need2(d, a) for a in range(amax + 1)]
            new = [INF] * (K1 + 1)
            for a in range(amax + 1):
                g = gs[a]
                seg = new[a:]
                new[a:] = [
                    x if x <= y + g else y + g
                    for x, y in zip(seg, dp_list[: K1 + 1 - a])
                ]
            dp_list = [min(v, INF) for v in new]

    best = None
    for x in range(K1 + 1):
        y = dp_list[x]
        if y <= K2:
            cost = C1 * x + C2 * y
            if best is None or cost < best:
                best = cost
    print(-1 if best is None else best)


main()
