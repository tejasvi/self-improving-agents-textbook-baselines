import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    D = [int(data[idx + i]) for i in range(n)]
    idx += n
    L1, C1, K1 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3
    L2, C2, K2 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2])

    INF = float("inf")
    # dp[y] = min number of type-1 sensors when exactly y type-2 sensors are used
    dp = [INF] * (K2 + 1)
    dp[0] = 0
    for d in D:
        new = [INF] * (K2 + 1)
        tmax = min(K2, (d + L2 - 1) // L2)
        # need[t] = type-1 sensors required if t type-2 sensors cover this section
        need = []
        for t in range(tmax + 1):
            rem = d - t * L2
            need.append((rem + L1 - 1) // L1 if rem > 0 else 0)
        for t in range(tmax + 1):
            a = need[t]
            for y in range(K2 + 1 - t):
                v = dp[y] + a
                if v < new[y + t]:
                    new[y + t] = v
        dp = new

    best = None
    for y in range(K2 + 1):
        a = dp[y]
        if a != INF and a <= K1:
            cost = a * C1 + y * C2
            if best is None or cost < best:
                best = cost

    print(-1 if best is None else best)


main()
