import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    D = [int(data[idx + i]) for i in range(n)]
    idx += n
    L1, C1, K1 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3
    L2, C2, K2 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3

    INF = 10 ** 15
    # dp[k] = min number of type-2 sensors needed using at most k type-1 sensors
    try:
        import numpy as np
        dp = np.zeros(K1 + 1, dtype=np.int64)
        use_np = True
    except ImportError:
        dp = [0] * (K1 + 1)
        use_np = False

    for d in D:
        amax = min(K1, -(-d // L1))  # ceil(d / L1)
        need = []
        for a in range(amax + 1):
            rem = d - a * L1
            need.append(0 if rem <= 0 else -(-rem // L2))
        if use_np:
            new = np.full(K1 + 1, INF, dtype=np.int64)
            for a in range(amax + 1):
                c = need[a]
                # new[k] = min(new[k], dp[k-a] + c) for k >= a
                np.minimum(new[a:], dp[:K1 + 1 - a] + c, out=new[a:])
            dp = new
        else:
            new = [INF] * (K1 + 1)
            for a in range(amax + 1):
                c = need[a]
                seg = new[a:]
                src = dp[:K1 + 1 - a]
                new[a:] = [x if x <= y + c else y + c for x, y in zip(seg, src)]
            dp = new

    best = None
    dp_list = dp.tolist() if use_np else dp
    for k in range(K1 + 1):
        t = dp_list[k]
        if t <= K2:
            cost = k * C1 + t * C2
            if best is None or cost < best:
                best = cost
    print(-1 if best is None else best)


main()
