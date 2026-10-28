import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    D = [int(data[idx + i]) for i in range(n)]
    idx += n
    L1, C1, K1 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3
    L2, C2, K2 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3

    INF = 10 ** 9
    # dp[x] = min number of type-2 sensors needed, given exactly x type-1
    # sensors used over the sections processed so far.
    dp = [INF] * (K1 + 1)
    dp[0] = 0
    for d in D:
        amax = min(K1, (d + L1 - 1) // L1)
        new = [INF] * (K1 + 1)
        for a in range(amax + 1):
            rem = d - a * L1
            b = (rem + L2 - 1) // L2 if rem > 0 else 0
            # new[x + a] = min(new[x + a], dp[x] + b)
            new[a:] = [u if u < v + b else v + b
                       for u, v in zip(new[a:], dp)]
        dp = [v if v < INF else INF for v in new]

    best = -1
    for x in range(K1 + 1):
        y = dp[x]
        if y <= K2:
            cost = x * C1 + y * C2
            if best < 0 or cost < best:
                best = cost
    print(best)


main()
