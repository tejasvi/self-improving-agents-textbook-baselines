import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    D = [int(data[idx + i]) for i in range(n)]
    idx += n
    L1, C1, K1 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3
    L2, C2, K2 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3

    INF = float('inf')
    try:
        import numpy as np
        BIG = 10 ** 15
        dp = np.full(K1 + 1, BIG, dtype=np.int64)
        dp[0] = 0
        for d in D:
            amax = min(K1, -(-d // L1))
            new = np.full(K1 + 1, BIG, dtype=np.int64)
            for a in range(amax + 1):
                rem = d - a * L1
                need = 0 if rem <= 0 else -(-rem // L2)
                # new[j + a] = min(new[j + a], dp[j] + need)
                cand = dp[:K1 + 1 - a] + need
                np.minimum(new[a:], cand, out=new[a:])
            # cap unreachable/too-large values
            np.minimum(new, BIG, out=new)
            dp = new
        best = None
        for j in range(K1 + 1):
            t = int(dp[j])
            if t <= K2 and t < BIG:
                c = C1 * j + C2 * t
                if best is None or c < best:
                    best = c
    except ImportError:
        BIG = float('inf')
        dp = [INF] * (K1 + 1)
        dp[0] = 0
        for d in D:
            amax = min(K1, -(-d // L1))
            new = [INF] * (K1 + 1)
            needs = []
            for a in range(amax + 1):
                rem = d - a * L1
                needs.append(0 if rem <= 0 else -(-rem // L2))
            for a in range(amax + 1):
                nd = needs[a]
                seg = new[a:]
                new[a:] = list(map(min, seg, [x + nd for x in dp[:K1 + 1 - a]]))
            dp = new
        best = None
        for j in range(K1 + 1):
            t = dp[j]
            if t <= K2:
                c = C1 * j + C2 * t
                if best is None or c < best:
                    best = c
    print(-1 if best is None else best)


main()
