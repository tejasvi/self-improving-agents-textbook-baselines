import sys


def solve(N, D, L1, C1, K1, L2, C2, K2):
    INF = 10 ** 15
    try:
        import numpy as np
        use_np = True
    except ImportError:
        use_np = False

    if use_np:
        dp = np.full(K1 + 1, INF, dtype=np.int64)
        dp[0] = 0
        for d in D:
            need = (d + L1 - 1) // L1  # type-1 sensors that cover the section alone
            m = min(need, K1)
            new = np.full(K1 + 1, INF, dtype=np.int64)
            for x in range(m + 1):
                rem = max(0, d - x * L1)
                f = (rem + L2 - 1) // L2
                # new[a] = min(new[a], dp[a - x] + f)
                np.minimum(new[x:], dp[:K1 + 1 - x] + f, out=new[x:])
            dp = np.minimum(new, INF)
        dp = dp.tolist()
    else:
        dp = [INF] * (K1 + 1)
        dp[0] = 0
        for d in D:
            need = (d + L1 - 1) // L1
            m = min(need, K1)
            fs = []
            for x in range(m + 1):
                rem = max(0, d - x * L1)
                fs.append((rem + L2 - 1) // L2)
            new = [INF] * (K1 + 1)
            for x in range(m + 1):
                f = fs[x]
                for a in range(x, K1 + 1):
                    v = dp[a - x] + f
                    if v < new[a]:
                        new[a] = v
            dp = [min(v, INF) for v in new]

    best = -1
    for a in range(K1 + 1):
        b = dp[a]
        if b <= K2:
            cost = a * C1 + b * C2
            if best < 0 or cost < best:
                best = cost
    return best


def main():
    data = sys.stdin.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    D = [int(data[idx + i]) for i in range(N)]
    idx += N
    L1, C1, K1 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3
    L2, C2, K2 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2])
    print(solve(N, D, L1, C1, K1, L2, C2, K2))


if __name__ == "__main__":
    main()
