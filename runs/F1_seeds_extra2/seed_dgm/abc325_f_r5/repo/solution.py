import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    D = [int(data[idx + i]) for i in range(n)]
    idx += n
    L1, C1, K1 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3
    L2, C2, K2 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2])

    INF = float('inf')
    # dp[a] = min number of type-2 sensors needed using at most a type-1 sensors
    dp = [0] * (K1 + 1)
    for d in D:
        xmax = min(K1, -(-d // L1))
        new = [INF] * (K1 + 1)
        for x in range(xmax + 1):
            rem = d - x * L1
            gx = -(-rem // L2) if rem > 0 else 0
            # new[a] = min(new[a], dp[a - x] + gx) for a >= x
            seg = dp[:K1 + 1 - x]
            new[x:] = list(map(min, new[x:], [v + gx for v in seg]))
        dp = new
        if dp[K1] == INF:
            break

    if dp[K1] > K2:
        print(-1)
        return
    best = None
    for a in range(K1 + 1):
        b = dp[a]
        if b <= K2:
            cost = a * C1 + b * C2
            if best is None or cost < best:
                best = cost
    print(best)


main()
