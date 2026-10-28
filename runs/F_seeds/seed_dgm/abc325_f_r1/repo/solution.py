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
    # dp[j]: min number of type-2 sensors needed, having used exactly j type-1 sensors
    dp = [INF] * (K1 + 1)
    dp[0] = 0
    for d in D:
        amax = min(K1, -(-d // L1))
        bs = []
        for a in range(amax + 1):
            rem = d - a * L1
            bs.append(0 if rem <= 0 else -(-rem // L2))
        new = [INF] * (K1 + 1)
        for a in range(amax + 1):
            b = bs[a]
            seg = new[a:]
            src = dp[:K1 + 1 - a]
            new[a:] = [x if x <= y + b else y + b for x, y in zip(seg, src)]
        dp = [min(x, INF) for x in new]

    best = -1
    for j in range(K1 + 1):
        if dp[j] <= K2:
            cost = C1 * j + C2 * dp[j]
            if best < 0 or cost < best:
                best = cost
    print(best)


main()
